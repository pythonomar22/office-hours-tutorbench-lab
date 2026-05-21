"""Command-line interface for the TutorBench lab."""

from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from tutorbench_lab.constants import (
    DEFAULT_CANDIDATE_MODEL,
    DEFAULT_CRITIC_MODEL,
    DEFAULT_EXAMPLES_JSONL,
    DEFAULT_HF_METADATA_PATH,
    DEFAULT_JUDGE_MODEL,
    DEFAULT_MANIFEST_PATH,
    DEFAULT_RAW_DATASET_DIR,
    DEFAULT_SOLVER_MODEL,
)
from tutorbench_lab.dataset import (
    build_manifest,
    fetch_dataset_metadata,
    iter_examples,
    load_examples_jsonl,
    load_tutorbench,
    save_dataset,
    validate_examples,
    write_examples_jsonl,
    write_manifest,
)
from tutorbench_lab.doctor import check_providers
from tutorbench_lab.io import append_jsonl, read_json, read_model_jsonl, write_json
from tutorbench_lab.judge import judge_run_record
from tutorbench_lab.reports import (
    compare_report_markdown,
    compare_reports,
    score_report_markdown,
)
from tutorbench_lab.schemas import JudgedRunRecord, RunRecord, ScoreReport, Strategy
from tutorbench_lab.scoring import build_score_report
from tutorbench_lab.tutor import (
    dry_run_response,
    record_for_response,
    run_agentic,
    run_baseline,
)

load_dotenv()

app = typer.Typer(no_args_is_help=True, help="TutorBench evaluation lab.")
console = Console()


@app.command()
def doctor(
    ping: bool = typer.Option(
        False,
        "--ping",
        help="Ping provider model-list endpoints. This is cheap and does not generate.",
    )
) -> None:
    """Check which provider keys are configured."""

    checks = check_providers(ping=ping)
    table = Table(title="Provider diagnostics")
    table.add_column("Provider")
    table.add_column("Env")
    table.add_column("Present")
    table.add_column("Ping")
    table.add_column("Status")
    table.add_column("Detail")
    for check in checks:
        status = "-" if check.ok is None else ("ok" if check.ok else "fail")
        table.add_row(
            check.provider,
            check.key_env,
            "yes" if check.present else "no",
            "yes" if check.pinged else "no",
            status if check.status_code is None else f"{status} ({check.status_code})",
            check.detail,
        )
    console.print(table)


@app.command()
def fetch(
    raw_dataset_dir: Path = typer.Option(DEFAULT_RAW_DATASET_DIR),
    manifest_path: Path = typer.Option(DEFAULT_MANIFEST_PATH),
    examples_path: Path = typer.Option(DEFAULT_EXAMPLES_JSONL),
    metadata_path: Path = typer.Option(DEFAULT_HF_METADATA_PATH),
    save_raw: bool = typer.Option(True, "--save-raw/--no-save-raw"),
    strict: bool = typer.Option(True, "--strict/--no-strict"),
    limit: int | None = typer.Option(
        None,
        help="Limit rows for smoke tests. Automatically disables strict distribution checks.",
    ),
    metadata_only: bool = typer.Option(
        False,
        "--metadata-only",
        help="Fetch only cheap Hugging Face repo metadata; do not download parquet.",
    ),
) -> None:
    """Download/validate the pinned TutorBench dataset and write a manifest."""

    if metadata_only:
        metadata = fetch_dataset_metadata()
        write_json(metadata_path, metadata)
        console.print(f"Wrote Hugging Face metadata to [bold]{metadata_path}[/bold]")
        return

    dataset = load_tutorbench(raw_dataset_dir=raw_dataset_dir)
    if save_raw and not raw_dataset_dir.exists():
        save_dataset(dataset, raw_dataset_dir)
    examples = iter_examples(dataset, limit=limit)
    validate_examples(examples, strict=strict and limit is None)
    manifest = build_manifest(examples)
    write_manifest(manifest, manifest_path)
    write_examples_jsonl(examples, examples_path)
    console.print(
        f"Wrote {len(examples)} examples to [bold]{examples_path}[/bold] "
        f"and manifest to [bold]{manifest_path}[/bold]"
    )


@app.command()
def run(
    examples_path: Path = typer.Option(DEFAULT_EXAMPLES_JSONL),
    output_dir: Path = typer.Option(Path("runs")),
    strategy: Strategy = typer.Option(
        Strategy.DRY_RUN,
        help="Use dry_run until you intentionally want to spend model tokens.",
    ),
    model: str = typer.Option(
        os.getenv("TUTORBENCH_CANDIDATE_MODEL", DEFAULT_CANDIDATE_MODEL)
    ),
    solver_model: str = typer.Option(
        os.getenv("TUTORBENCH_SOLVER_MODEL", DEFAULT_SOLVER_MODEL)
    ),
    critic_model: str = typer.Option(
        os.getenv("TUTORBENCH_CRITIC_MODEL", DEFAULT_CRITIC_MODEL)
    ),
    limit: int | None = typer.Option(None),
    max_tokens: int = typer.Option(1200),
) -> None:
    """Generate candidate tutor responses."""

    examples = load_examples_jsonl(examples_path)
    if limit is not None:
        examples = examples[:limit]

    run_id = str(uuid4())
    run_dir = output_dir / run_id
    out_path = run_dir / "responses.jsonl"

    for index, example in enumerate(examples, start=1):
        console.print(f"[{index}/{len(examples)}] {example.task_id} {strategy.value}")
        if strategy == Strategy.DRY_RUN:
            turn = dry_turn_for_example(example)
            response = dry_run_response(example)
        elif strategy == Strategy.BASELINE:
            turn, response = run_baseline(example, model=model, max_tokens=max_tokens)
        else:
            turn, response = run_agentic(
                example,
                composer_model=model,
                solver_model=solver_model,
                critic_model=critic_model,
                max_tokens=max_tokens,
            )
        append_jsonl(
            out_path,
            record_for_response(
                example=example,
                turn=turn,
                response=response,
                run_id=run_id,
            ),
        )

    console.print(f"Wrote responses to [bold]{out_path}[/bold]")


@app.command()
def judge(
    responses_path: Path,
    output_path: Path | None = typer.Option(None),
    judge_model: str = typer.Option(
        os.getenv("TUTORBENCH_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)
    ),
    limit: int | None = typer.Option(None),
    max_tokens: int = typer.Option(2000),
) -> None:
    """Judge candidate responses with sample-specific rubrics."""

    records = list(read_model_jsonl(responses_path, RunRecord))
    if limit is not None:
        records = records[:limit]
    out_path = output_path or responses_path.with_name("judged.jsonl")

    for index, record in enumerate(records, start=1):
        console.print(f"[{index}/{len(records)}] judging {record.example.task_id}")
        judged = judge_run_record(
            record,
            judge_model=judge_model,
            max_tokens=max_tokens,
        )
        append_jsonl(out_path, judged)

    console.print(f"Wrote judgments to [bold]{out_path}[/bold]")


@app.command()
def score(
    judged_path: Path,
    output_path: Path | None = typer.Option(None),
    bootstrap_samples: int = typer.Option(1000),
) -> None:
    """Aggregate judged rows into TutorBench score slices."""

    records = list(read_model_jsonl(judged_path, JudgedRunRecord))
    report = build_score_report(records, bootstrap_samples=bootstrap_samples)
    out_path = output_path or judged_path.with_name("scores.json")
    write_json(out_path, report.model_dump(mode="json"))
    console.print(f"Overall ARRw: [bold]{report.overall.mean_arrw:.2%}[/bold]")
    console.print(f"Wrote score report to [bold]{out_path}[/bold]")


@app.command()
def report(
    score_path: Path,
    output_path: Path | None = typer.Option(None),
) -> None:
    """Render a score JSON as Markdown."""

    score_report = ScoreReport.model_validate(read_json(score_path))
    markdown = score_report_markdown(score_report)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        console.print(f"Wrote Markdown report to [bold]{output_path}[/bold]")
    else:
        console.print(markdown)


@app.command()
def compare(
    left_score_path: Path,
    right_score_path: Path,
    output_path: Path | None = typer.Option(None),
) -> None:
    """Compare two score JSON files."""

    left = ScoreReport.model_validate(read_json(left_score_path))
    right = ScoreReport.model_validate(read_json(right_score_path))
    comparison = compare_reports(left, right)
    markdown = compare_report_markdown(comparison)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        console.print(f"Wrote comparison to [bold]{output_path}[/bold]")
    else:
        console.print(markdown)


def dry_turn_for_example(example):
    from tutorbench_lab.protocol import build_turn_input

    return build_turn_input(example, prompt_version="dry-run-v1")


if __name__ == "__main__":
    app()

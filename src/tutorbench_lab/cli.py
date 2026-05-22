"""Command-line interface for the TutorBench lab."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from uuid import uuid4

import typer
from rich.console import Console
from rich.table import Table

from tutorbench_lab.config import (
    candidate_model_default,
    critic_model_default,
    judge_model_default,
    load_environment,
    max_revision_attempts_default,
    planner_model_default,
    request_timeout_default,
    solver_model_default,
    verifier_model_default,
)
from tutorbench_lab.constants import (
    DEFAULT_EXAMPLES_JSONL,
    DEFAULT_HF_METADATA_PATH,
    DEFAULT_MANIFEST_PATH,
    DEFAULT_RAW_DATASET_DIR,
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
from tutorbench_lab.eval_sets import (
    build_eval_set,
    examples_for_eval_set,
    load_eval_set,
    write_eval_set,
)
from tutorbench_lab.io import append_jsonl, read_json, read_model_jsonl, write_json
from tutorbench_lab.judge import judge_run_record
from tutorbench_lab.parity import build_parity_checks, checks_to_json, parity_level
from tutorbench_lab.reports import (
    compare_report_markdown,
    compare_reports,
    score_report_markdown,
)
from tutorbench_lab.schemas import JudgedRunRecord, RunRecord, ScoreReport, Strategy
from tutorbench_lab.scoring import build_score_report
from tutorbench_lab.selection import StratifyBy, select_examples
from tutorbench_lab.tutor import (
    dry_run_response,
    record_for_response,
    run_agentic,
    run_baseline,
)

app = typer.Typer(no_args_is_help=True, help="TutorBench evaluation lab.")
console = Console()


@app.callback()
def main(
    env_file: Path = typer.Option(
        Path(".env"),
        "--env-file",
        help="Path to the dotenv file to load before running a command.",
    ),
) -> None:
    """Load local environment before any command runs."""

    load_environment(env_file)


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


@app.command("audit-parity")
def audit_parity(
    manifest_path: Path = typer.Option(DEFAULT_MANIFEST_PATH),
    metadata_path: Path = typer.Option(DEFAULT_HF_METADATA_PATH),
    output_path: Path | None = typer.Option(
        None,
        help="Optional JSON path for machine-readable parity checks.",
    ),
    judge_model: str | None = typer.Option(None),
) -> None:
    """Explain whether local scores are comparable to public leaderboard scores."""

    judge_model = judge_model or judge_model_default()
    manifest = read_json(manifest_path)
    metadata = read_json(metadata_path) if metadata_path.exists() else None
    checks = build_parity_checks(
        manifest=manifest,
        metadata=metadata,
        judge_model=judge_model,
    )
    level = parity_level(checks)

    table = Table(title=f"Evaluation parity: {level}")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Expected")
    table.add_column("Observed")
    for check in checks:
        table.add_row(
            check.name,
            check.status.value,
            check.expected,
            check.observed,
        )
    console.print(table)
    console.print(
        "[bold]Interpretation:[/bold] local public-HF runs can guide engineering, "
        "but leaderboard claims require Scale-side evaluation or calibrated "
        "reproduction of published baselines."
    )

    if output_path:
        write_json(
            output_path,
            {
                "level": level,
                "checks": checks_to_json(checks),
            },
        )
        console.print(f"Wrote parity audit to [bold]{output_path}[/bold]")


@app.command("create-eval-set")
def create_eval_set(
    output_path: Path,
    name: str = typer.Option(..., help="Stable eval set name."),
    description: str = typer.Option("", help="Human-readable eval set purpose."),
    examples_path: Path = typer.Option(DEFAULT_EXAMPLES_JSONL),
    limit: int = typer.Option(..., help="Number of rows to include."),
    stratified_per_bucket: int = typer.Option(
        9,
        help="Rows sampled per stratum before applying the final limit.",
    ),
    stratify_by: StratifyBy = typer.Option(StratifyBy.USE_CASE_MODALITY),
    seed: int = typer.Option(20260521, help="Deterministic sampling seed."),
    exclude_eval_set: list[Path] | None = typer.Option(
        None,
        "--exclude-eval-set",
        help="Eval set(s) whose task IDs should be excluded from selection.",
    ),
) -> None:
    """Create a deterministic JSON eval set for fairer iteration."""

    examples = load_examples_jsonl(examples_path)
    excluded: set[str] = set()
    for path in exclude_eval_set or []:
        excluded.update(load_eval_set(path).ids)
    if excluded:
        examples = [example for example in examples if example.task_id not in excluded]

    selected = select_examples(
        examples,
        limit=limit,
        stratified_per_bucket=stratified_per_bucket,
        stratify_by=stratify_by,
        seed=seed,
    )
    eval_set = build_eval_set(
        name=name,
        description=description,
        examples=selected,
        stratify_by=stratify_by,
        selection_policy=[
            f"source_examples={examples_path}",
            f"limit={limit}",
            f"stratified_per_bucket={stratified_per_bucket}",
            f"stratify_by={stratify_by.value}",
            f"seed={seed}",
            f"excluded_task_ids={len(excluded)}",
        ],
    )
    write_eval_set(eval_set, output_path)
    console.print(
        f"Wrote eval set [bold]{name}[/bold] with {len(eval_set.task_ids)} rows "
        f"to [bold]{output_path}[/bold]"
    )


@app.command()
def run(
    examples_path: Path = typer.Option(DEFAULT_EXAMPLES_JSONL),
    output_dir: Path = typer.Option(Path("runs")),
    strategy: Strategy = typer.Option(
        Strategy.DRY_RUN,
        help="Use dry_run until you intentionally want to spend model tokens.",
    ),
    model: str | None = typer.Option(None),
    solver_model: str | None = typer.Option(None),
    planner_model: str | None = typer.Option(None),
    verifier_model: str | None = typer.Option(None),
    critic_model: str | None = typer.Option(None),
    limit: int | None = typer.Option(None),
    task_id: list[str] | None = typer.Option(
        None,
        "--task-id",
        help="Run specific TutorBench task IDs in the order provided.",
    ),
    eval_set: Path | None = typer.Option(
        None,
        help="JSON eval set file containing ordered TutorBench task IDs.",
    ),
    stratified_per_bucket: int | None = typer.Option(
        None,
        help="Sample this many examples per stratification bucket.",
    ),
    stratify_by: StratifyBy = typer.Option(StratifyBy.USE_CASE_MODALITY),
    seed: int = typer.Option(7, help="Deterministic sampling seed."),
    max_tokens: int = typer.Option(1200),
    max_revision_attempts: int | None = typer.Option(
        None,
        help="Maximum critic-triggered revision passes for agentic runs.",
    ),
    request_timeout_s: float | None = typer.Option(
        None,
        "--request-timeout-s",
        help="Per-provider request timeout in seconds.",
    ),
    workers: int = typer.Option(
        1,
        "--workers",
        min=1,
        help=(
            "Number of examples to process concurrently. "
            "Keep at 1 for strict provider-rate safety."
        ),
    ),
    run_id: str | None = typer.Option(
        None,
        "--run-id",
        help="Optional stable run ID. Useful with --resume after interrupted runs.",
    ),
    resume: bool = typer.Option(
        False,
        "--resume",
        help="Skip task IDs already present in this run's responses.jsonl.",
    ),
) -> None:
    """Generate candidate tutor responses."""

    model = model or candidate_model_default()
    solver_model = solver_model or solver_model_default()
    planner_model = planner_model or planner_model_default()
    verifier_model = verifier_model or verifier_model_default()
    critic_model = critic_model or critic_model_default()
    max_revision_attempts = (
        max_revision_attempts
        if max_revision_attempts is not None
        else max_revision_attempts_default()
    )
    request_timeout_s = (
        request_timeout_s
        if request_timeout_s is not None
        else request_timeout_default()
    )
    examples = load_examples_jsonl(examples_path)
    if task_id:
        by_task_id = {example.task_id: example for example in examples}
        missing = [item for item in task_id if item not in by_task_id]
        if missing:
            raise typer.BadParameter(
                f"Unknown task ID(s): {', '.join(missing)}",
                param_hint="--task-id",
            )
        examples = [by_task_id[item] for item in task_id]
        console.print(f"Loaded {len(examples)} requested task ID(s)")
        if limit is not None:
            examples = examples[:limit]
    elif eval_set is not None:
        selected_eval_set = load_eval_set(eval_set)
        examples = examples_for_eval_set(examples, selected_eval_set)
        console.print(
            f"Loaded eval set [bold]{selected_eval_set.name}[/bold] "
            f"with {len(examples)} examples"
        )
        if limit is not None:
            examples = examples[:limit]
    else:
        examples = select_examples(
            examples,
            limit=limit,
            stratified_per_bucket=stratified_per_bucket,
            stratify_by=stratify_by,
            seed=seed,
        )

    run_id = run_id or str(uuid4())
    run_dir = output_dir / run_id
    out_path = run_dir / "responses.jsonl"
    if resume and out_path.exists():
        completed = {
            record.example.task_id for record in read_model_jsonl(out_path, RunRecord)
        }
        examples = [example for example in examples if example.task_id not in completed]
        console.print(
            f"Resuming run [bold]{run_id}[/bold]; "
            f"skipping {len(completed)} completed task ID(s)"
        )

    def generate_record(index: int, example) -> RunRecord:
        console.print(f"[{index}/{len(examples)}] {example.task_id} {strategy.value}")
        if strategy == Strategy.DRY_RUN:
            turn = dry_turn_for_example(example)
            response = dry_run_response(example)
        elif strategy == Strategy.BASELINE:
            turn, response = run_baseline(
                example,
                model=model,
                max_tokens=max_tokens,
                request_timeout_s=request_timeout_s,
            )
        else:
            turn, response = run_agentic(
                example,
                composer_model=model,
                solver_model=solver_model,
                planner_model=planner_model,
                verifier_model=verifier_model,
                critic_model=critic_model,
                max_tokens=max_tokens,
                max_revision_attempts=max_revision_attempts,
                request_timeout_s=request_timeout_s,
                progress_callback=lambda stage: console.print(
                    f"  - [{index}/{len(examples)}] {stage}"
                ),
            )
        return record_for_response(
            example=example,
            turn=turn,
            response=response,
            run_id=run_id,
        )

    if workers == 1:
        for index, example in enumerate(examples, start=1):
            append_jsonl(out_path, generate_record(index, example))
    else:
        console.print(f"Running with [bold]{workers}[/bold] worker threads")
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(generate_record, index, example): index
                for index, example in enumerate(examples, start=1)
            }
            for future in as_completed(futures):
                append_jsonl(out_path, future.result())

    console.print(f"Wrote responses to [bold]{out_path}[/bold]")


@app.command()
def judge(
    responses_path: Path,
    output_path: Path | None = typer.Option(None),
    judge_model: str | None = typer.Option(None),
    limit: int | None = typer.Option(None),
    max_tokens: int = typer.Option(2000),
    request_timeout_s: float | None = typer.Option(
        None,
        "--request-timeout-s",
        help="Per-provider request timeout in seconds.",
    ),
    workers: int = typer.Option(
        1,
        "--workers",
        min=1,
        help=(
            "Number of responses to judge concurrently. "
            "Keep at 1 for strict provider-rate safety."
        ),
    ),
    resume: bool = typer.Option(
        False,
        "--resume",
        help="Skip task IDs already present in the output judgments file.",
    ),
) -> None:
    """Judge candidate responses with sample-specific rubrics."""

    judge_model = judge_model or judge_model_default()
    request_timeout_s = (
        request_timeout_s
        if request_timeout_s is not None
        else request_timeout_default()
    )
    records = list(read_model_jsonl(responses_path, RunRecord))
    if limit is not None:
        records = records[:limit]
    out_path = output_path or responses_path.with_name("judged.jsonl")
    if resume and out_path.exists():
        completed = {
            record.run.example.task_id
            for record in read_model_jsonl(out_path, JudgedRunRecord)
        }
        records = [
            record for record in records if record.example.task_id not in completed
        ]
        console.print(f"Resuming judge; skipping {len(completed)} completed task ID(s)")

    def judge_record(index: int, record: RunRecord) -> JudgedRunRecord:
        console.print(f"[{index}/{len(records)}] judging {record.example.task_id}")
        return judge_run_record(
            record,
            judge_model=judge_model,
            max_tokens=max_tokens,
            request_timeout_s=request_timeout_s,
        )

    if workers == 1:
        for index, record in enumerate(records, start=1):
            append_jsonl(out_path, judge_record(index, record))
    else:
        console.print(f"Judging with [bold]{workers}[/bold] worker threads")
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(judge_record, index, record): index
                for index, record in enumerate(records, start=1)
            }
            for future in as_completed(futures):
                append_jsonl(out_path, future.result())

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

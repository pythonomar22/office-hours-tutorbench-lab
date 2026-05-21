"""Markdown and comparison reports."""

from __future__ import annotations

from tutorbench_lab.constants import LEADERBOARD_TARGET_SCORE
from tutorbench_lab.schemas import CompareReport, ScoreReport


def score_report_markdown(report: ScoreReport) -> str:
    lines = [
        f"# TutorBench Score Report: `{report.run_id}`",
        "",
        f"- Judge model: `{report.judge_model}`",
        f"- Overall ARRw: {_fmt(report.overall)}",
        f"- Target threshold: {LEADERBOARD_TARGET_SCORE:.2%}",
        f"- Negative-weight manual review rows: {report.negative_weight_review_count}",
        "",
        "## By Use Case",
        _table(report.by_use_case),
        "",
        "## By Modality",
        _table(report.by_modality),
        "",
        "## By Subject",
        _table(report.by_subject),
        "",
        "## By Bloom Taxonomy",
        _table(report.by_bloom),
        "",
    ]
    return "\n".join(lines)


def compare_reports(left: ScoreReport, right: ScoreReport) -> CompareReport:
    delta = right.overall.mean_arrw - left.overall.mean_arrw
    if abs(delta) < 1e-9:
        winner = "tie"
    elif delta > 0:
        winner = "right"
    else:
        winner = "left"
    return CompareReport(left=left, right=right, delta_overall=delta, winner=winner)


def compare_report_markdown(report: CompareReport) -> str:
    return "\n".join(
        [
            "# TutorBench Run Comparison",
            "",
            f"- Left: `{report.left.run_id}` {_fmt(report.left.overall)}",
            f"- Right: `{report.right.run_id}` {_fmt(report.right.overall)}",
            f"- Delta, right minus left: {report.delta_overall:+.2%}",
            f"- Winner: `{report.winner}`",
            "",
        ]
    )


def _fmt(score) -> str:
    ci = ""
    if score.ci_low is not None and score.ci_high is not None:
        ci = f" ({score.ci_low:.2%}-{score.ci_high:.2%} CI)"
    return f"{score.mean_arrw:.2%} over {score.count} rows{ci}"


def _table(scores) -> str:
    lines = ["| Slice | Rows | ARRw | CI |", "| --- | ---: | ---: | --- |"]
    for score in scores:
        ci = "-"
        if score.ci_low is not None and score.ci_high is not None:
            ci = f"{score.ci_low:.2%}-{score.ci_high:.2%}"
        lines.append(f"| {score.name} | {score.count} | {score.mean_arrw:.2%} | {ci} |")
    return "\n".join(lines)

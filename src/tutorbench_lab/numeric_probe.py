"""Small deterministic arithmetic checks for visible TutorBench work."""

from __future__ import annotations

import ast
import operator
import re
from collections import OrderedDict

from tutorbench_lab.schemas import TutorTurnInput

_SUPERSCRIPTS = str.maketrans("⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹", "-+0123456789")
_SCI_RE = re.compile(
    r"(?P<base>\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:×|x|\*)\s*10"
    r"(?:\s*\^\s*(?P<caret>[+-]?\d+)|(?P<sup>[⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹]+))",
    re.IGNORECASE,
)
_NUMBER_RE = re.compile(
    r"(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)"
    r"(?:\s*(?:×|x|\*)\s*10(?:\s*\^\s*[+-]?\d+|[⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹]+))?",
    re.IGNORECASE,
)
_BINARY_RE = re.compile(
    rf"(?P<a>{_NUMBER_RE.pattern})"
    r"(?:\s*(?:N|kg|g|m/s²|m/s\^2|m/s|m|s|J|kJ|MJ/mol|mol|L|M|%))*"
    r"\s*(?P<op>[+\-−*/÷])\s*"
    rf"(?P<b>{_NUMBER_RE.pattern})",
    re.IGNORECASE,
)
_UNIT_RE = re.compile(
    r"(?<=\d)\s*(?:MJ/mol|m/s²|m/s\^2|m/s|kg|g|N|J|kJ|mol|L|M|s|m|%)\b",
    re.IGNORECASE,
)
_ALLOWED_EXPR_RE = re.compile(r"^[0-9eE+\-*/().,\s]+$")


def build_numeric_probe(
    turn: TutorTurnInput,
    *texts: str | None,
    max_checks: int = 12,
) -> str | None:
    """Return deterministic arithmetic notes derived only from visible text.

    This intentionally stays conservative. It is not a symbolic solver; it just
    catches common benchmark-killing slips like scientific-notation expansion,
    one-step arithmetic, and simple visible substitution expressions.
    """

    corpus = "\n".join(part for part in [turn.user_prompt, *texts] if part)
    checks: OrderedDict[str, str] = OrderedDict()

    for match in _SCI_RE.finditer(corpus):
        raw = match.group(0)
        value = _eval_number(raw)
        if value is not None:
            checks.setdefault(raw, f"{raw} = {_format_number(value)}")
        if len(checks) >= max_checks:
            break

    for match in _BINARY_RE.finditer(corpus):
        if len(checks) >= max_checks:
            break
        a = _eval_number(match.group("a"))
        b = _eval_number(match.group("b"))
        op = match.group("op")
        value = _apply_binary(a, b, op)
        if value is None:
            continue
        expression = f"{match.group('a')} {op} {match.group('b')}"
        checks.setdefault(expression, f"{expression} = {_format_number(value)}")

    for line in corpus.splitlines():
        if len(checks) >= max_checks:
            break
        if line.count("=") > 2:
            continue
        if not any(op in line for op in ("+", "-", "−", "*", "×", "/", "÷")):
            continue
        expression = _candidate_expression(line)
        if not expression:
            continue
        value = _safe_eval_expression(expression)
        if value is None:
            continue
        pretty_expression = expression.replace("**", "^")
        checks.setdefault(
            pretty_expression,
            f"{pretty_expression} = {_format_number(value)}",
        )

    if not checks:
        return None

    lines = [
        "Local numeric probe (deterministic; derived from visible prompt/OCR only):"
    ]
    lines.extend(f"- {check}" for check in checks.values())
    lines.append(
        "Use these as arithmetic sanity checks; if they conflict with an LLM "
        "audit, explicitly resolve the conflict before composing."
    )
    return "\n".join(lines)


def _eval_number(text: str) -> float | None:
    expression = _replace_scientific(text.replace(",", ""))
    expression = expression.replace("×", "*").replace("−", "-").replace("÷", "/")
    expression = expression.replace("x", "*").replace("X", "*")
    return _safe_eval_expression(expression)


def _replace_scientific(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        base = match.group("base").replace(",", "")
        raw_exp = match.group("caret") or match.group("sup") or "1"
        exp = raw_exp.translate(_SUPERSCRIPTS)
        return f"({base}*10**{exp})"

    return _SCI_RE.sub(repl, text)


def _apply_binary(a: float | None, b: float | None, op: str) -> float | None:
    if a is None or b is None:
        return None
    if op in {"+", "＋"}:
        return a + b
    if op in {"-", "−"}:
        return a - b
    if op in {"*", "×"}:
        return a * b
    if op in {"/", "÷"}:
        if b == 0:
            return None
        return a / b
    return None


def _candidate_expression(line: str) -> str | None:
    line = line.split("=", 1)[-1]
    line = _replace_scientific(line)
    line = _UNIT_RE.sub("", line)
    line = line.replace("×", "*").replace("−", "-").replace("÷", "/")
    line = line.replace("{", "(").replace("}", ")")
    line = line.replace("[", "(").replace("]", ")")
    line = re.sub(r"(?<=\d),(?=\d{3}\b)", "", line)
    line = re.sub(r"[^0-9eE+\-*/().,\s]", " ", line)
    line = re.sub(r"\s+", " ", line).strip()
    if not _ALLOWED_EXPR_RE.match(line):
        return None
    if len(_NUMBER_RE.findall(line)) < 2:
        return None
    return line


def _safe_eval_expression(expression: str) -> float | None:
    expression = expression.strip()
    if not expression or not _ALLOWED_EXPR_RE.match(expression):
        return None
    try:
        tree = ast.parse(expression, mode="eval")
        value = _eval_ast(tree.body)
    except (SyntaxError, ValueError, ZeroDivisionError):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _eval_ast(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
        }
        op = operations.get(type(node.op))
        if op is None:
            raise ValueError("unsupported operator")
        return float(op(_eval_ast(node.left), _eval_ast(node.right)))
    raise ValueError("unsupported expression")


def _format_number(value: float) -> str:
    if value == 0:
        return "0"
    abs_value = abs(value)
    if 1e-3 <= abs_value < 1e6:
        rendered = f"{value:.6f}".rstrip("0").rstrip(".")
    else:
        rendered = f"{value:.6g}"
    return rendered

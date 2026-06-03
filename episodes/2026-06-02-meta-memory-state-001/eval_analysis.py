#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys
from statistics import mean, pstdev
from typing import Any


EPISODE_DIR = pathlib.Path(__file__).resolve().parent
ENV_DIR = EPISODE_DIR / "env"
sys.path.insert(0, str(ENV_DIR))

from meta_memory_state import _selected_ledger_candidate, response_diagnostics  # noqa: E402


def _assistant_contents(completion: Any) -> list[str]:
    if not isinstance(completion, list):
        return []
    contents = []
    for message in completion:
        if isinstance(message, dict) and message.get("role") == "assistant":
            content = message.get("content")
            if isinstance(content, str):
                contents.append(content)
    return contents


def _answer_info(row: dict[str, Any]) -> dict[str, Any]:
    answer = row.get("answer")
    if isinstance(answer, str):
        try:
            parsed = json.loads(answer)
        except Exception:
            parsed = None
        if isinstance(parsed, dict):
            return parsed
    info = row.get("info")
    if isinstance(info, dict) and isinstance(info.get("ground_truths"), list):
        return info
    return {}


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def _selected_payload(text: str) -> dict[str, Any] | None:
    selected = _selected_ledger_candidate(text)
    if selected is None:
        return None
    payload, _ = selected
    return payload


def _compare_payload(payload: dict[str, Any] | None, expected: dict[str, Any]) -> dict[str, float]:
    expected_balances = expected.get("balances")
    if not isinstance(payload, dict) or not isinstance(expected_balances, dict):
        return {
            "turn_exact": 0.0,
            "all_balances_exact": 0.0,
            "total_exact": 0.0,
            "account_exact_rate": 0.0,
        }

    balances = payload.get("balances")
    normalized = {}
    if isinstance(balances, dict):
        for key, value in balances.items():
            if isinstance(key, str):
                coerced = _coerce_int(value)
                if coerced is not None:
                    normalized[key.strip().lower()] = coerced

    account_hits = []
    for account, expected_value in expected_balances.items():
        expected_int = _coerce_int(expected_value)
        if expected_int is None:
            account_hits.append(0.0)
            continue
        actual = normalized.get(str(account).strip().lower())
        account_hits.append(1.0 if actual == expected_int else 0.0)

    account_exact_rate = mean(account_hits) if account_hits else 0.0
    all_balances_exact = 1.0 if account_hits and all(hit == 1.0 for hit in account_hits) else 0.0
    total_actual = _coerce_int(payload.get("total"))
    expected_total_value = expected.get("total")
    if expected_total_value is None:
        expected_total_value = sum(_coerce_int(v) or 0 for v in expected_balances.values())
    total_expected = _coerce_int(expected_total_value)
    total_exact = 1.0 if total_actual == total_expected else 0.0
    turn_exact = 1.0 if all_balances_exact and total_exact else 0.0
    return {
        "turn_exact": turn_exact,
        "all_balances_exact": all_balances_exact,
        "total_exact": total_exact,
        "account_exact_rate": account_exact_rate,
    }


def _stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "std": None, "min": None, "max": None}
    return {
        "mean": mean(values),
        "std": pstdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def summarize_results(path: pathlib.Path) -> dict[str, Any]:
    rows = []
    with path.open() as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))

    rewards = [float(row.get("reward", 0.0) or 0.0) for row in rows]
    output_tokens = [
        float(row.get("token_usage", {}).get("output_tokens", 0.0) or 0.0)
        for row in rows
    ]
    input_tokens = [
        float(row.get("token_usage", {}).get("input_tokens", 0.0) or 0.0)
        for row in rows
    ]
    truncated = [bool(row.get("is_truncated")) for row in rows]
    errors = [row.get("error") is not None for row in rows]

    turn_count = 0
    parseable_turns = 0
    exact_one_tag_turns = 0
    exact_one_candidate_turns = 0
    exact_one_ledger_turns = 0
    multi_candidate_turns = 0
    code_fence_turns = 0
    candidate_counts = []
    tag_counts = []
    output_chars = []
    turn_exact_values = []
    all_balances_exact_values = []
    total_exact_values = []
    account_exact_values = []
    example_solve_all_values = []

    for row in rows:
        contents = _assistant_contents(row.get("completion"))
        output_chars.append(sum(len(content) for content in contents))
        info = _answer_info(row)
        ground_truths = info.get("ground_truths") if isinstance(info, dict) else None
        example_turn_exact = []
        for content in contents:
            turn_count += 1
            diagnostics = response_diagnostics(content)
            candidate_count = int(diagnostics["candidate_count"])
            tag_count = int(diagnostics["tag_count"])
            candidate_counts.append(float(candidate_count))
            tag_counts.append(float(tag_count))
            if diagnostics["parseable"]:
                parseable_turns += 1
            if diagnostics["exact_one_tag"]:
                exact_one_tag_turns += 1
            if diagnostics["exact_one_candidate"]:
                exact_one_candidate_turns += 1
            if diagnostics["exact_one_ledger"]:
                exact_one_ledger_turns += 1
            if diagnostics["multi_candidate"]:
                multi_candidate_turns += 1
            if diagnostics["code_fence"]:
                code_fence_turns += 1
            turn_idx = len(example_turn_exact)
            if isinstance(ground_truths, list) and turn_idx < len(ground_truths):
                comparison = _compare_payload(_selected_payload(content), ground_truths[turn_idx])
                turn_exact_values.append(comparison["turn_exact"])
                all_balances_exact_values.append(comparison["all_balances_exact"])
                total_exact_values.append(comparison["total_exact"])
                account_exact_values.append(comparison["account_exact_rate"])
                example_turn_exact.append(comparison["turn_exact"])
        if example_turn_exact:
            example_solve_all_values.append(1.0 if all(item == 1.0 for item in example_turn_exact) else 0.0)

    def rate(count: int) -> float | None:
        if turn_count == 0:
            return None
        return count / turn_count

    return {
        "num_examples": len(rows),
        "assistant_turns": turn_count,
        "reward": _stats(rewards),
        "truncation_rate": mean([1.0 if item else 0.0 for item in truncated]) if rows else None,
        "error_rate": mean([1.0 if item else 0.0 for item in errors]) if rows else None,
        "avg_input_tokens": mean(input_tokens) if input_tokens else None,
        "avg_output_tokens": mean(output_tokens) if output_tokens else None,
        "mean_output_chars_per_example": mean(output_chars) if output_chars else None,
        "parseable_turn_rate": rate(parseable_turns),
        "exact_one_tag_turn_rate": rate(exact_one_tag_turns),
        "exact_one_candidate_turn_rate": rate(exact_one_candidate_turns),
        "exact_one_ledger_turn_rate": rate(exact_one_ledger_turns),
        "multi_candidate_turn_rate": rate(multi_candidate_turns),
        "code_fence_turn_rate": rate(code_fence_turns),
        "mean_candidates_per_turn": mean(candidate_counts) if candidate_counts else None,
        "mean_tags_per_turn": mean(tag_counts) if tag_counts else None,
        "exact_turn_rate": mean(turn_exact_values) if turn_exact_values else None,
        "all_balances_exact_turn_rate": mean(all_balances_exact_values) if all_balances_exact_values else None,
        "total_exact_turn_rate": mean(total_exact_values) if total_exact_values else None,
        "account_exact_rate": mean(account_exact_values) if account_exact_values else None,
        "solve_all_examples_rate": mean(example_solve_all_values) if example_solve_all_values else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results_jsonl")
    args = parser.parse_args()
    summary = summarize_results(pathlib.Path(args.results_jsonl))
    json.dump(summary, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

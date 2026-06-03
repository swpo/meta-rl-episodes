import csv
import io
import json
import random
import re
import string
from typing import Any


REGIONS = ["north", "south", "east", "west"]
PRODUCTS = ["alpha", "beta", "gamma", "delta"]
CHANNELS = ["online", "retail"]
TASK_FAMILIES = [
    "sum_units_by_region",
    "sum_revenue_by_product",
    "count_rows_filter",
    "max_region_revenue",
    "diff_product_revenue",
    "avg_unit_price_by_channel",
]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def parse_task_families(task_families: str | list[str] | tuple[str, ...] | None) -> list[str]:
    if task_families is None or task_families == "":
        return list(TASK_FAMILIES)
    if isinstance(task_families, str):
        families = [item.strip() for item in task_families.split(",") if item.strip()]
    else:
        families = [str(item).strip() for item in task_families if str(item).strip()]
    unknown = sorted(set(families) - set(TASK_FAMILIES))
    if unknown:
        raise ValueError(f"unknown task families: {', '.join(unknown)}")
    if not families:
        raise ValueError("at least one task family is required")
    return families


def make_rows(rng: random.Random, num_rows: int) -> list[dict[str, Any]]:
    if num_rows < 4:
        raise ValueError("num_rows must be at least 4")

    rows: list[dict[str, Any]] = []
    for row_idx in range(num_rows):
        units = rng.randint(2, 24)
        returns = rng.randint(0, min(5, units // 2))
        net_units = units - returns
        unit_price = rng.choice([5, 8, 10, 12, 15, 20, 25, 30])
        rows.append(
            {
                "row_id": f"R{row_idx + 1:02d}",
                "region": rng.choice(REGIONS),
                "product": rng.choice(PRODUCTS),
                "channel": rng.choice(CHANNELS),
                "units": units,
                "returns": returns,
                "net_units": net_units,
                "unit_price": unit_price,
                "revenue": net_units * unit_price,
            }
        )
    return rows


def table_csv(rows: list[dict[str, Any]]) -> str:
    fieldnames = [
        "row_id",
        "region",
        "product",
        "channel",
        "units",
        "returns",
        "net_units",
        "unit_price",
        "revenue",
    ]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().strip()


def _present_values(rows: list[dict[str, Any]], key: str, fallback: list[str]) -> list[str]:
    values = sorted({str(row[key]) for row in rows})
    return values or list(fallback)


def _sum(rows: list[dict[str, Any]], column: str, **filters: str) -> int:
    total = 0
    for row in rows:
        if all(str(row[key]) == value for key, value in filters.items()):
            total += int(row[column])
    return total


def _question_for_family(
    rows: list[dict[str, Any]], family: str, rng: random.Random
) -> tuple[str, dict[str, Any]]:
    if family == "sum_units_by_region":
        region = rng.choice(_present_values(rows, "region", REGIONS))
        answer = _sum(rows, "net_units", region=region)
        return (
            f"What is the total net_units for rows where region is {region}?",
            {
                "answer": answer,
                "answer_type": "number",
                "task_family": family,
                "target": {"region": region},
            },
        )

    if family == "sum_revenue_by_product":
        product = rng.choice(_present_values(rows, "product", PRODUCTS))
        answer = _sum(rows, "revenue", product=product)
        return (
            f"What is the total revenue for rows where product is {product}?",
            {
                "answer": answer,
                "answer_type": "number",
                "task_family": family,
                "target": {"product": product},
            },
        )

    if family == "count_rows_filter":
        channel = rng.choice(_present_values(rows, "channel", CHANNELS))
        threshold = rng.choice([8, 10, 12, 15, 18])
        answer = sum(
            1
            for row in rows
            if str(row["channel"]) == channel and int(row["net_units"]) >= threshold
        )
        return (
            "How many rows have channel "
            f"{channel} and net_units greater than or equal to {threshold}?",
            {
                "answer": answer,
                "answer_type": "number",
                "task_family": family,
                "target": {"channel": channel, "min_net_units": threshold},
            },
        )

    if family == "max_region_revenue":
        totals = {region: _sum(rows, "revenue", region=region) for region in REGIONS}
        answer = sorted(totals.items(), key=lambda item: (-item[1], item[0]))[0][0]
        return (
            "Which region has the highest total revenue? "
            "If there is a tie, choose the alphabetically first region.",
            {
                "answer": answer,
                "answer_type": "string",
                "task_family": family,
                "target": {"totals": totals},
            },
        )

    if family == "diff_product_revenue":
        products = _present_values(rows, "product", PRODUCTS)
        if len(products) == 1:
            first = products[0]
            second = rng.choice([product for product in PRODUCTS if product != first])
        else:
            first, second = rng.sample(products, 2)
        answer = _sum(rows, "revenue", product=first) - _sum(rows, "revenue", product=second)
        return (
            "What is the difference between total revenue for product "
            f"{first} and total revenue for product {second}? "
            f"Compute {first} minus {second}.",
            {
                "answer": answer,
                "answer_type": "number",
                "task_family": family,
                "target": {"product_a": first, "product_b": second},
            },
        )

    if family == "avg_unit_price_by_channel":
        channel = rng.choice(_present_values(rows, "channel", CHANNELS))
        prices = [int(row["unit_price"]) for row in rows if str(row["channel"]) == channel]
        answer = round(sum(prices) / len(prices), 2) if prices else 0.0
        return (
            "What is the average unit_price for rows where channel is "
            f"{channel}? Round to two decimal places.",
            {
                "answer": answer,
                "answer_type": "number",
                "task_family": family,
                "target": {"channel": channel},
            },
        )

    raise ValueError(f"unknown task family: {family}")


def make_examples(
    *,
    seed: int = 20260603,
    num_examples: int = 128,
    min_rows: int = 8,
    max_rows: int = 12,
    task_families: str | list[str] | tuple[str, ...] | None = None,
) -> list[dict[str, Any]]:
    if min_rows < 4:
        raise ValueError("min_rows must be at least 4")
    if max_rows < min_rows:
        raise ValueError("max_rows must be >= min_rows")

    families = parse_task_families(task_families)
    rng = random.Random(seed)
    examples: list[dict[str, Any]] = []

    for example_idx in range(num_examples):
        num_rows = rng.randint(min_rows, max_rows)
        rows = make_rows(rng, num_rows)
        family = rng.choice(families)
        question, answer_payload = _question_for_family(rows, family, rng)
        placeholder = 0 if answer_payload["answer_type"] == "number" else "name"
        prompt = (
            "Analyze the CSV table and answer the question exactly.\n"
            "Return only one <result>...</result> tag containing JSON with exactly "
            'one key, "answer". Do not use code fences.\n'
            "For numeric answers, return a JSON number. For string answers, use the "
            "lowercase category name exactly as it appears in the table.\n\n"
            "CSV:\n"
            f"{table_csv(rows)}\n\n"
            f"Question: {question}\n\n"
            "Required shape:\n"
            f"<result>{json.dumps({'answer': placeholder}, sort_keys=True)}</result>"
        )
        examples.append(
            {
                "prompt": [{"role": "user", "content": prompt}],
                "answer": json.dumps(answer_payload, sort_keys=True),
                "task": "tabular-arithmetic",
                "info": {
                    "example_idx": example_idx,
                    "rows": rows,
                    "num_rows": num_rows,
                    "question": question,
                    **answer_payload,
                },
            }
        )
    return examples


def _extract_result_blocks(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r"<result>(.*?)</result>", text, flags=re.IGNORECASE | re.DOTALL)


def _json_payloads(candidate: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    payloads = []
    seen = set()
    for match in re.finditer(r"{", candidate):
        try:
            payload, _ = decoder.raw_decode(candidate[match.start() :])
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        marker = json.dumps(payload, sort_keys=True, default=str)
        if marker in seen:
            continue
        seen.add(marker)
        payloads.append(payload)
    return payloads


def _coerce_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip().replace(",", "")
        if re.fullmatch(r"-?\d+(\.\d+)?", stripped):
            return float(stripped)
    return None


def _normalize_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    lowered = value.strip().lower()
    lowered = lowered.translate(str.maketrans("", "", string.punctuation))
    return re.sub(r"\s+", " ", lowered).strip()


def _result_candidates(text: Any) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    base_meta = {
        "has_tag": False,
        "tag_count": 0,
        "candidate_in_tag": False,
        "valid_json": False,
    }
    if not isinstance(text, str) or not text.strip():
        return []

    blocks = _extract_result_blocks(text)
    base_meta["has_tag"] = bool(blocks)
    base_meta["tag_count"] = len(blocks)
    parsed: list[tuple[dict[str, Any], dict[str, Any]]] = []

    for block in blocks:
        for payload in _json_payloads(block):
            meta = dict(base_meta)
            meta["candidate_in_tag"] = True
            meta["valid_json"] = True
            parsed.append((payload, meta))

    for payload in _json_payloads(text):
        marker = json.dumps(payload, sort_keys=True, default=str)
        if any(json.dumps(item[0], sort_keys=True, default=str) == marker for item in parsed):
            continue
        meta = dict(base_meta)
        meta["valid_json"] = True
        parsed.append((payload, meta))

    return parsed


def selected_result_candidate(text: Any) -> tuple[dict[str, Any], dict[str, Any]] | None:
    candidates = _result_candidates(text)
    if not candidates:
        return None

    if isinstance(text, str):
        blocks = _extract_result_blocks(text)
        if len(blocks) == 1:
            payloads = _json_payloads(blocks[0])
            if payloads:
                return (
                    payloads[-1],
                    {
                        "has_tag": True,
                        "tag_count": 1,
                        "candidate_in_tag": True,
                        "valid_json": True,
                    },
                )
    return candidates[-1]


def response_diagnostics(text: Any) -> dict[str, float]:
    candidates = _result_candidates(text)
    blocks = _extract_result_blocks(text) if isinstance(text, str) else []
    candidate_count = len(candidates)
    tag_count = len(blocks)
    output_chars = len(text) if isinstance(text, str) else 0
    return {
        "candidate_count": float(candidate_count),
        "tag_count": float(tag_count),
        "parseable": 1.0 if candidate_count > 0 else 0.0,
        "exact_one_tag": 1.0 if tag_count == 1 else 0.0,
        "exact_one_candidate": 1.0 if candidate_count == 1 else 0.0,
        "exact_one_result": 1.0 if tag_count == 1 and candidate_count == 1 else 0.0,
        "multi_candidate": 1.0 if candidate_count > 1 else 0.0,
        "code_fence": 1.0 if isinstance(text, str) and "```" in text else 0.0,
        "output_chars": float(output_chars),
    }


def _expected_from_answer_or_state(answer_or_state: Any) -> dict[str, Any]:
    if isinstance(answer_or_state, dict) and "answer" in answer_or_state:
        return answer_or_state
    if isinstance(answer_or_state, dict) and isinstance(answer_or_state.get("info"), dict):
        return answer_or_state["info"]
    if isinstance(answer_or_state, str):
        try:
            parsed = json.loads(answer_or_state)
        except Exception:
            return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _answer_score(actual: Any, expected: dict[str, Any]) -> tuple[float, dict[str, float]]:
    expected_value = expected.get("answer")
    answer_type = expected.get("answer_type")
    if answer_type == "number" or isinstance(expected_value, int | float):
        actual_number = _coerce_number(actual)
        expected_number = _coerce_number(expected_value)
        if actual_number is None or expected_number is None:
            return 0.0, {"exact_answer": 0.0, "numeric_abs_error": -1.0}
        error = abs(actual_number - expected_number)
        exact = 1.0 if error <= 1e-6 else 0.0
        scale = max(1.0, abs(expected_number))
        return clamp(1.0 - error / scale), {
            "exact_answer": exact,
            "numeric_abs_error": error,
        }

    actual_text = _normalize_text(actual)
    expected_text = _normalize_text(expected_value)
    if actual_text is None or expected_text is None:
        return 0.0, {"exact_answer": 0.0, "numeric_abs_error": -1.0}
    if actual_text == expected_text:
        return 1.0, {"exact_answer": 1.0, "numeric_abs_error": -1.0}
    if expected_text in actual_text or actual_text in expected_text:
        return 0.5, {"exact_answer": 0.0, "numeric_abs_error": -1.0}
    return 0.0, {"exact_answer": 0.0, "numeric_abs_error": -1.0}


def _response_penalty(text: Any) -> float:
    diagnostics = response_diagnostics(text)
    candidate_count = diagnostics["candidate_count"]
    tag_count = diagnostics["tag_count"]
    output_chars = diagnostics["output_chars"]
    penalty = 1.0
    if candidate_count > 1:
        penalty *= max(0.20, 1.0 / (candidate_count ** 0.5))
    if tag_count > 1:
        penalty *= max(0.60, 1.0 - 0.08 * (tag_count - 1.0))
    if diagnostics["code_fence"]:
        penalty *= 0.90
    if output_chars > 800:
        penalty *= max(0.65, 1.0 - (output_chars - 800.0) / 6000.0)
    return clamp(penalty)


def score_result_response(text: Any, expected: dict[str, Any]) -> float:
    selected = selected_result_candidate(text)
    if selected is None:
        return 0.0
    payload, meta = selected
    answer_key = "answer" if "answer" in payload else "value"
    answer_score, _ = _answer_score(payload.get(answer_key), expected)
    payload_keys = {key.strip().lower() for key in payload if isinstance(key, str)}
    schema_score = clamp(
        1.0
        - (0.55 if "answer" not in payload_keys else 0.0)
        - 0.25 * len(payload_keys - {"answer"})
    )
    format_score = 0.0
    if meta["valid_json"]:
        format_score += 0.08
    if meta["candidate_in_tag"]:
        format_score += 0.05
    if meta["tag_count"] == 1 and meta["candidate_in_tag"]:
        format_score += 0.02
    return clamp(
        (0.75 * answer_score + 0.10 * schema_score + format_score)
        * _response_penalty(text)
    )


def score_completion(completion: Any, answer_or_state: Any) -> float:
    expected = _expected_from_answer_or_state(answer_or_state)
    if not isinstance(completion, list):
        return 0.0
    assistant_contents = [
        _message_content(message)
        for message in completion
        if _message_role(message) == "assistant"
    ]
    if not assistant_contents:
        return 0.0
    return score_result_response(assistant_contents[-1], expected)


def answer_diagnostics(completion: Any, answer_or_state: Any) -> dict[str, float]:
    expected = _expected_from_answer_or_state(answer_or_state)
    if not isinstance(completion, list):
        return {
            "exact_answer": 0.0,
            "numeric_abs_error": -1.0,
            "answer_score": 0.0,
        }
    assistant_contents = [
        _message_content(message)
        for message in completion
        if _message_role(message) == "assistant"
    ]
    if not assistant_contents:
        return {
            "exact_answer": 0.0,
            "numeric_abs_error": -1.0,
            "answer_score": 0.0,
        }
    selected = selected_result_candidate(assistant_contents[-1])
    if selected is None:
        return {
            "exact_answer": 0.0,
            "numeric_abs_error": -1.0,
            "answer_score": 0.0,
        }
    payload, _ = selected
    answer_key = "answer" if "answer" in payload else "value"
    answer_score, diagnostics = _answer_score(payload.get(answer_key), expected)
    diagnostics["answer_score"] = answer_score
    return diagnostics


def completion_diagnostics(completion: Any) -> dict[str, float]:
    if not isinstance(completion, list):
        return {
            "candidate_count": 0.0,
            "tag_count": 0.0,
            "parseable": 0.0,
            "exact_one_result": 0.0,
            "multi_candidate": 0.0,
            "code_fence": 0.0,
            "output_chars": 0.0,
        }
    assistant_contents = [
        _message_content(message)
        for message in completion
        if _message_role(message) == "assistant"
    ]
    if not assistant_contents:
        return {
            "candidate_count": 0.0,
            "tag_count": 0.0,
            "parseable": 0.0,
            "exact_one_result": 0.0,
            "multi_candidate": 0.0,
            "code_fence": 0.0,
            "output_chars": 0.0,
        }
    return response_diagnostics(assistant_contents[-1])


def _message_role(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("role")
    return getattr(message, "role", None)


def _message_content(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("content")
    return getattr(message, "content", None)


def load_environment(
    num_examples: int = 128,
    min_rows: int = 8,
    max_rows: int = 12,
    seed: int = 20260603,
    task_families: str | list[str] | tuple[str, ...] | None = None,
    **kwargs: Any,
):
    from datasets import Dataset
    import verifiers as vf

    examples = make_examples(
        seed=seed,
        num_examples=num_examples,
        min_rows=min_rows,
        max_rows=max_rows,
        task_families=task_families,
    )

    async def weighted_reward(completion, answer, **kwargs):
        return score_completion(completion, answer)

    async def parseable(completion, **kwargs):
        return completion_diagnostics(completion)["parseable"]

    async def exact_one_result(completion, **kwargs):
        return completion_diagnostics(completion)["exact_one_result"]

    async def multi_candidate(completion, **kwargs):
        return completion_diagnostics(completion)["multi_candidate"]

    async def code_fence(completion, **kwargs):
        return completion_diagnostics(completion)["code_fence"]

    async def mean_candidate_count(completion, **kwargs):
        return completion_diagnostics(completion)["candidate_count"]

    async def output_chars(completion, **kwargs):
        return completion_diagnostics(completion)["output_chars"]

    async def exact_answer(completion, answer, **kwargs):
        return answer_diagnostics(completion, answer)["exact_answer"]

    async def answer_score(completion, answer, **kwargs):
        return answer_diagnostics(completion, answer)["answer_score"]

    async def numeric_abs_error(completion, answer, **kwargs):
        return answer_diagnostics(completion, answer)["numeric_abs_error"]

    dataset = Dataset.from_list(examples)
    rubric = vf.Rubric()
    rubric.add_reward_func(weighted_reward, weight=1.0)
    rubric.add_metric(parseable)
    rubric.add_metric(exact_one_result)
    rubric.add_metric(multi_candidate)
    rubric.add_metric(code_fence)
    rubric.add_metric(mean_candidate_count)
    rubric.add_metric(output_chars)
    rubric.add_metric(exact_answer)
    rubric.add_metric(answer_score)
    rubric.add_metric(numeric_abs_error)
    return vf.SingleTurnEnv(dataset=dataset, rubric=rubric)

import json
import random
import re
from typing import Any


ACCOUNTS = ["cash", "food", "rent", "travel", "books", "utilities"]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def apply_update(balances: dict[str, int], update: dict[str, Any]) -> None:
    kind = update["kind"]
    amount = int(update["amount"])
    if kind == "credit":
        balances[update["account"]] += amount
    elif kind == "debit":
        balances[update["account"]] -= amount
    elif kind == "transfer":
        balances[update["from"]] -= amount
        balances[update["to"]] += amount
    else:
        raise ValueError(f"unknown update kind: {kind}")


def describe_update(update: dict[str, Any]) -> str:
    amount = int(update["amount"])
    if update["kind"] == "credit":
        return f"credit {update['account']} by {amount}"
    if update["kind"] == "debit":
        return f"debit {update['account']} by {amount}"
    return f"transfer {amount} from {update['from']} to {update['to']}"


def expected_payload(balances: dict[str, int]) -> dict[str, Any]:
    ordered_balances = {account: balances[account] for account in sorted(balances)}
    return {"balances": ordered_balances, "total": sum(ordered_balances.values())}


def make_examples(
    *,
    seed: int = 1337420,
    num_examples: int = 128,
    min_turns: int = 2,
    max_turns: int = 5,
    account_count: int = 4,
) -> list[dict[str, Any]]:
    if min_turns < 1:
        raise ValueError("min_turns must be at least 1")
    if max_turns < min_turns:
        raise ValueError("max_turns must be >= min_turns")
    if account_count < 2 or account_count > len(ACCOUNTS):
        raise ValueError(f"account_count must be between 2 and {len(ACCOUNTS)}")

    rng = random.Random(seed)
    examples: list[dict[str, Any]] = []
    for example_idx in range(num_examples):
        accounts = sorted(rng.sample(ACCOUNTS, account_count))
        balances = {account: rng.randint(-3, 8) * 5 for account in accounts}
        num_turns = rng.randint(min_turns, max_turns)
        updates: list[dict[str, Any]] = []
        ground_truths: list[dict[str, Any]] = []

        for _ in range(num_turns):
            kind = rng.choice(["credit", "debit", "transfer"])
            amount = rng.randint(1, 9) * 5
            if kind == "transfer":
                source, target = rng.sample(accounts, 2)
                update = {"kind": kind, "from": source, "to": target, "amount": amount}
            else:
                update = {
                    "kind": kind,
                    "account": rng.choice(accounts),
                    "amount": amount,
                }
            updates.append(update)
            apply_update(balances, update)
            ground_truths.append(expected_payload(balances))

        initial_balances = ground_truths[0]["balances"].copy()
        inverse_first = updates[0].copy()
        undo_balances = initial_balances.copy()
        if inverse_first["kind"] == "credit":
            undo_balances[inverse_first["account"]] -= int(inverse_first["amount"])
        elif inverse_first["kind"] == "debit":
            undo_balances[inverse_first["account"]] += int(inverse_first["amount"])
        else:
            undo_balances[inverse_first["from"]] += int(inverse_first["amount"])
            undo_balances[inverse_first["to"]] -= int(inverse_first["amount"])

        required_shape = {
            "balances": {account: 0 for account in accounts},
            "total": 0,
        }
        prompt = (
            "Maintain this pocket ledger across turns. Account balances are signed "
            "integers. After each update, reply only with JSON inside one "
            "<ledger>...</ledger> tag using exactly these keys: balances and total.\n\n"
            f"Tracked accounts: {', '.join(accounts)}\n"
            f"Starting balances: {json.dumps(undo_balances, sort_keys=True)}\n"
            f"Update 1: {describe_update(updates[0])}\n\n"
            "Required shape:\n"
            f"<ledger>{json.dumps(required_shape, sort_keys=True)}</ledger>"
        )
        follow_ups = [
            f"Update {turn_idx + 1}: {describe_update(update)}\nReturn the full ledger now."
            for turn_idx, update in enumerate(updates[1:], start=1)
        ]

        examples.append(
            {
                "prompt": [{"role": "user", "content": prompt}],
                "answer": json.dumps(
                    {
                        "ground_truths": ground_truths,
                        "updates": updates,
                        "accounts": accounts,
                    },
                    sort_keys=True,
                ),
                "task": "multi-turn-ledger-state",
                "info": {
                    "example_idx": example_idx,
                    "accounts": accounts,
                    "updates": updates,
                    "ground_truths": ground_truths,
                    "follow_ups": follow_ups,
                    "num_turns": num_turns,
                },
            }
        )
    return examples


def _extract_ledger_blocks(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r"<ledger>(.*?)</ledger>", text, flags=re.IGNORECASE | re.DOTALL)


def _json_payloads(candidate: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    payloads = []
    seen = set()
    for match in re.finditer(r"{", candidate):
        try:
            payload, _ = decoder.raw_decode(candidate[match.start() :])
        except Exception:
            continue
        if not isinstance(payload, dict) or not isinstance(payload.get("balances"), dict):
            continue
        marker = json.dumps(payload, sort_keys=True, default=str)
        if marker in seen:
            continue
        seen.add(marker)
        payloads.append(payload)
    return payloads


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if re.fullmatch(r"-?\d+", stripped):
            return int(stripped)
    return None


def _ledger_candidates(text: Any) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    base_meta = {
        "has_tag": False,
        "tag_count": 0,
        "candidate_in_tag": False,
        "valid_json": False,
        "fallback_pairs": False,
    }
    if not isinstance(text, str) or not text.strip():
        return []

    blocks = _extract_ledger_blocks(text)
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

    pairs = re.findall(r"\b([a-z][a-z_ -]{1,20})\b\s*[:=]\s*(-?\d+)", text.lower())
    if pairs:
        balances = {}
        total = None
        for name, value in pairs:
            key = name.strip().replace(" ", "_")
            if key == "total":
                total = int(value)
            else:
                balances[key] = int(value)
        if balances:
            meta = dict(base_meta)
            meta["fallback_pairs"] = True
            parsed.append(
                (
                    {
                        "balances": balances,
                        "total": total if total is not None else sum(balances.values()),
                    },
                    meta,
                )
            )

    return parsed


def response_diagnostics(text: Any) -> dict[str, float]:
    candidates = _ledger_candidates(text)
    blocks = _extract_ledger_blocks(text) if isinstance(text, str) else []
    candidate_count = len(candidates)
    tag_count = len(blocks)
    output_chars = len(text) if isinstance(text, str) else 0
    return {
        "candidate_count": float(candidate_count),
        "tag_count": float(tag_count),
        "parseable": 1.0 if candidate_count > 0 else 0.0,
        "exact_one_tag": 1.0 if tag_count == 1 else 0.0,
        "exact_one_candidate": 1.0 if candidate_count == 1 else 0.0,
        "exact_one_ledger": 1.0 if tag_count == 1 and candidate_count == 1 else 0.0,
        "multi_candidate": 1.0 if candidate_count > 1 else 0.0,
        "code_fence": 1.0 if isinstance(text, str) and "```" in text else 0.0,
        "output_chars": float(output_chars),
    }


def parse_ledger_response(text: Any) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    empty_meta = {
        "has_tag": False,
        "tag_count": 0,
        "candidate_in_tag": False,
        "valid_json": False,
        "fallback_pairs": False,
    }
    candidates = _ledger_candidates(text)
    if candidates:
        return candidates[0]

    if isinstance(text, str):
        blocks = _extract_ledger_blocks(text)
        empty_meta["has_tag"] = bool(blocks)
        empty_meta["tag_count"] = len(blocks)
    return None, empty_meta


def _score_payload(
    payload: dict[str, Any],
    meta: dict[str, Any],
    expected: dict[str, Any],
    accounts: list[str],
) -> float:
    balances = payload.get("balances")
    if not isinstance(balances, dict):
        return 0.0

    normalized: dict[str, int] = {}
    for key, value in balances.items():
        if not isinstance(key, str):
            continue
        parsed = _coerce_int(value)
        if parsed is not None:
            normalized[key.strip().lower()] = parsed

    expected_balances = expected.get("balances", {})
    if not isinstance(expected_balances, dict):
        return 0.0

    account_set = set(accounts)
    payload_keys = {key.strip().lower() for key in payload if isinstance(key, str)}
    required_payload_keys = {"balances", "total"}
    extra_top_keys = payload_keys - required_payload_keys
    missing_top_keys = required_payload_keys - payload_keys
    extra_accounts = [account for account in normalized if account not in account_set]
    schema_score = clamp(
        1.0
        - 0.45 * len(extra_accounts)
        - 0.30 * len(extra_top_keys)
        - 0.20 * len(missing_top_keys)
    )

    account_scores = []
    for account in accounts:
        expected_value = int(expected_balances.get(account, 0))
        actual_value = normalized.get(account)
        if actual_value is None:
            account_scores.append(0.0)
            continue
        if actual_value == expected_value:
            account_scores.append(1.0)
        else:
            scale = max(10, abs(expected_value))
            account_scores.append(clamp(1.0 - abs(actual_value - expected_value) / scale))
    balance_score = sum(account_scores) / len(accounts) if accounts else 0.0

    total_expected = int(expected.get("total", sum(expected_balances.values())))
    total_actual = _coerce_int(payload.get("total"))
    if total_actual is None:
        total_score = 0.0
    elif total_actual == total_expected:
        total_score = 1.0
    else:
        total_score = clamp(1.0 - abs(total_actual - total_expected) / max(10, abs(total_expected)))

    format_score = 0.0
    if meta.get("candidate_in_tag"):
        format_score += 0.08
    elif meta["has_tag"]:
        format_score += 0.02
    if meta["tag_count"] == 1 and meta.get("candidate_in_tag"):
        format_score += 0.04
    if meta["valid_json"]:
        format_score += 0.08
    elif meta["fallback_pairs"]:
        format_score += 0.03

    return clamp(0.50 * balance_score + 0.15 * total_score + 0.15 * schema_score + format_score)


def _selected_ledger_candidate(text: Any) -> tuple[dict[str, Any], dict[str, Any]] | None:
    candidates = _ledger_candidates(text)
    if not candidates:
        return None

    if isinstance(text, str):
        blocks = _extract_ledger_blocks(text)
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
                        "fallback_pairs": False,
                    },
                )

    return candidates[-1]


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
    if output_chars > 600:
        penalty *= max(0.65, 1.0 - (output_chars - 600.0) / 5000.0)
    return clamp(penalty)


def score_ledger_response(text: Any, expected: dict[str, Any], accounts: list[str]) -> float:
    selected = _selected_ledger_candidate(text)
    if selected is None:
        return 0.0
    payload, meta = selected
    return clamp(_score_payload(payload, meta, expected, accounts) * _response_penalty(text))


def _info_from_answer_or_state(answer_or_state: Any) -> dict[str, Any]:
    if isinstance(answer_or_state, dict) and isinstance(answer_or_state.get("info"), dict):
        return answer_or_state["info"]
    if isinstance(answer_or_state, dict) and isinstance(answer_or_state.get("ground_truths"), list):
        return answer_or_state
    if isinstance(answer_or_state, str):
        try:
            parsed = json.loads(answer_or_state)
        except Exception:
            return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _message_role(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("role")
    return getattr(message, "role", None)


def _message_content(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("content")
    return getattr(message, "content", None)


def _assistant_contents(completion: Any) -> list[Any]:
    if not isinstance(completion, list):
        return []
    return [
        _message_content(message)
        for message in completion
        if _message_role(message) == "assistant"
    ]


def completion_diagnostics(completion: Any) -> dict[str, float]:
    assistant_messages = _assistant_contents(completion)
    if not assistant_messages:
        return {
            "candidate_count": 0.0,
            "tag_count": 0.0,
            "parseable_turn_rate": 0.0,
            "exact_one_ledger_rate": 0.0,
            "multi_candidate_rate": 0.0,
            "code_fence_rate": 0.0,
            "output_chars": 0.0,
        }

    diagnostics = [response_diagnostics(content) for content in assistant_messages]
    count = float(len(diagnostics))
    return {
        "candidate_count": sum(item["candidate_count"] for item in diagnostics) / count,
        "tag_count": sum(item["tag_count"] for item in diagnostics) / count,
        "parseable_turn_rate": sum(item["parseable"] for item in diagnostics) / count,
        "exact_one_ledger_rate": sum(item["exact_one_ledger"] for item in diagnostics) / count,
        "multi_candidate_rate": sum(item["multi_candidate"] for item in diagnostics) / count,
        "code_fence_rate": sum(item["code_fence"] for item in diagnostics) / count,
        "output_chars": sum(item["output_chars"] for item in diagnostics) / count,
    }


def score_completion(completion: Any, answer_or_state: Any) -> float:
    info = _info_from_answer_or_state(answer_or_state)
    ground_truths = info.get("ground_truths", [])
    accounts = info.get("accounts", [])
    if not isinstance(ground_truths, list) or not isinstance(accounts, list):
        return 0.0
    if not isinstance(completion, list):
        return 0.0

    assistant_messages = _assistant_contents(completion)
    if not assistant_messages:
        return 0.0

    turn_scores = []
    for turn_idx, expected in enumerate(ground_truths):
        content = assistant_messages[turn_idx] if turn_idx < len(assistant_messages) else None
        turn_scores.append(score_ledger_response(content, expected, accounts))
    return sum(turn_scores) / len(turn_scores) if turn_scores else 0.0


def load_environment(
    min_turns: int = 2,
    max_turns: int = 5,
    num_examples: int = 128,
    account_count: int = 4,
    seed: int = 1337420,
    **kwargs: Any,
):
    from datasets import Dataset
    import verifiers as vf

    examples = make_examples(
        seed=seed,
        num_examples=num_examples,
        min_turns=min_turns,
        max_turns=max_turns,
        account_count=account_count,
    )

    class LedgerEnv(vf.MultiTurnEnv):
        @vf.stop
        async def max_turns_for_example(self, state: vf.State) -> bool:
            return len(state["trajectory"]) >= state["info"]["num_turns"]

        async def env_response(
            self, messages: vf.Messages, state: vf.State, **kwargs: Any
        ) -> vf.Messages:
            assistant_count = len(
                [message for message in messages if message["role"] == "assistant"]
            )
            follow_up_idx = assistant_count - 1
            return [vf.UserMessage(content=state["info"]["follow_ups"][follow_up_idx])]

    async def weighted_reward(completion, answer, **kwargs):
        return score_completion(completion, answer)

    async def parseable_turn_rate(completion, **kwargs):
        return completion_diagnostics(completion)["parseable_turn_rate"]

    async def exact_one_ledger_rate(completion, **kwargs):
        return completion_diagnostics(completion)["exact_one_ledger_rate"]

    async def multi_candidate_rate(completion, **kwargs):
        return completion_diagnostics(completion)["multi_candidate_rate"]

    async def code_fence_rate(completion, **kwargs):
        return completion_diagnostics(completion)["code_fence_rate"]

    async def mean_candidate_count(completion, **kwargs):
        return completion_diagnostics(completion)["candidate_count"]

    async def mean_output_chars(completion, **kwargs):
        return completion_diagnostics(completion)["output_chars"]

    dataset = Dataset.from_list(examples)
    rubric = vf.Rubric()
    rubric.add_reward_func(weighted_reward, weight=1.0)
    rubric.add_metric(parseable_turn_rate)
    rubric.add_metric(exact_one_ledger_rate)
    rubric.add_metric(multi_candidate_rate)
    rubric.add_metric(code_fence_rate)
    rubric.add_metric(mean_candidate_count)
    rubric.add_metric(mean_output_chars)
    return LedgerEnv(dataset=dataset, rubric=rubric, max_turns=max_turns)

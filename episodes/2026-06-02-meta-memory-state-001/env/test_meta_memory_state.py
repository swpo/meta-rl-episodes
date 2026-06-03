import json
from types import SimpleNamespace
import unittest

from meta_memory_state import (
    completion_diagnostics,
    make_examples,
    parse_ledger_response,
    response_diagnostics,
    score_completion,
    score_ledger_response,
)


class MetaMemoryStateTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        first = make_examples(seed=7, num_examples=3, min_turns=2, max_turns=3)
        second = make_examples(seed=7, num_examples=3, min_turns=2, max_turns=3)
        self.assertEqual(first, second)
        self.assertGreaterEqual(first[0]["info"]["num_turns"], 2)
        self.assertLessEqual(first[0]["info"]["num_turns"], 3)

    def test_exact_json_scores_one(self):
        example = make_examples(seed=11, num_examples=1)[0]
        expected = example["info"]["ground_truths"][0]
        response = f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>"
        self.assertEqual(
            score_ledger_response(response, expected, example["info"]["accounts"]),
            1.0,
        )

    def test_malformed_output_returns_zero(self):
        example = make_examples(seed=12, num_examples=1)[0]
        expected = example["info"]["ground_truths"][0]
        self.assertEqual(score_ledger_response(None, expected, example["info"]["accounts"]), 0.0)
        self.assertEqual(score_ledger_response("not a ledger", expected, example["info"]["accounts"]), 0.0)

    def test_partial_credit_for_close_balance(self):
        example = make_examples(seed=13, num_examples=1)[0]
        expected = example["info"]["ground_truths"][0]
        accounts = example["info"]["accounts"]
        payload = json.loads(json.dumps(expected))
        payload["balances"][accounts[0]] += 5
        response = f"<ledger>{json.dumps(payload, sort_keys=True)}</ledger>"
        score = score_ledger_response(response, expected, accounts)
        self.assertGreater(score, 0.5)
        self.assertLess(score, 1.0)

    def test_extra_balance_key_has_meaningful_penalty(self):
        example = make_examples(seed=13, num_examples=1, account_count=2)[0]
        expected = example["info"]["ground_truths"][0]
        payload = json.loads(json.dumps(expected))
        payload["balances"]["total"] = expected["total"]
        response = f"<ledger>{json.dumps(payload, sort_keys=True)}</ledger>"
        score = score_ledger_response(response, expected, example["info"]["accounts"])
        self.assertLess(score, 0.95)
        self.assertGreater(score, 0.80)

    def test_extra_top_level_key_has_schema_penalty(self):
        example = make_examples(seed=13, num_examples=1, account_count=2)[0]
        expected = example["info"]["ground_truths"][0]
        payload = json.loads(json.dumps(expected))
        payload["scratch"] = "ignored"
        response = f"<ledger>{json.dumps(payload, sort_keys=True)}</ledger>"
        score = score_ledger_response(response, expected, example["info"]["accounts"])
        self.assertLess(score, 0.98)
        self.assertGreater(score, 0.85)

    def test_completion_scores_average_turns(self):
        example = make_examples(seed=14, num_examples=1, min_turns=3, max_turns=3)[0]
        completion = []
        for expected in example["info"]["ground_truths"]:
            completion.append(
                {
                    "role": "assistant",
                    "content": f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>",
                }
            )
        self.assertEqual(score_completion(completion, {"info": example["info"]}), 1.0)

    def test_completion_scores_answer_signature(self):
        example = make_examples(seed=14, num_examples=1, min_turns=1, max_turns=1)[0]
        expected = example["info"]["ground_truths"][0]
        completion = [
            {
                "role": "assistant",
                "content": f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>",
            }
        ]
        self.assertEqual(score_completion(completion, example["answer"]), 1.0)

    def test_completion_accepts_message_objects(self):
        example = make_examples(seed=14, num_examples=1, min_turns=1, max_turns=1)[0]
        expected = example["info"]["ground_truths"][0]
        completion = [
            SimpleNamespace(
                role="assistant",
                content=f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>",
            )
        ]
        self.assertEqual(score_completion(completion, example["answer"]), 1.0)

    def test_parser_fallback_pairs_are_shaped_not_crashing(self):
        payload, meta = parse_ledger_response("cash: 10, food=-5, total: 5")
        self.assertEqual(payload["balances"]["cash"], 10)
        self.assertEqual(payload["total"], 5)
        self.assertTrue(meta["fallback_pairs"])

    def test_prompt_uses_concrete_account_keys(self):
        example = make_examples(seed=15, num_examples=1, account_count=2)[0]
        prompt = example["prompt"][0]["content"]
        self.assertNotIn('"account":0', prompt)
        for account in example["info"]["accounts"]:
            self.assertIn(f'"{account}": 0', prompt)

    def test_scores_json_outside_tag_with_format_penalty(self):
        example = make_examples(seed=16, num_examples=1, account_count=2)[0]
        expected = example["info"]["ground_truths"][0]
        response = f"```json\n{json.dumps(expected, sort_keys=True)}\n```"
        score = score_ledger_response(response, expected, example["info"]["accounts"])
        self.assertGreater(score, 0.7)
        self.assertLess(score, 0.9)

    def test_penalizes_multiple_ledger_candidates(self):
        example = make_examples(seed=17, num_examples=1, account_count=2)[0]
        expected = example["info"]["ground_truths"][0]
        bad = {"balances": {"account": 0}, "total": 0}
        response = (
            f"<ledger>{json.dumps(bad, sort_keys=True)}</ledger>\n"
            f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>"
        )
        score = score_ledger_response(response, expected, example["info"]["accounts"])
        self.assertGreater(score, 0.5)
        self.assertLess(score, 0.75)

    def test_scores_selected_last_candidate_not_best_candidate(self):
        example = make_examples(seed=18, num_examples=1, account_count=2)[0]
        expected = example["info"]["ground_truths"][0]
        bad = {"balances": {"account": 0}, "total": 0}
        good_then_bad = (
            f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>\n"
            f"<ledger>{json.dumps(bad, sort_keys=True)}</ledger>"
        )
        bad_then_good = (
            f"<ledger>{json.dumps(bad, sort_keys=True)}</ledger>\n"
            f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>"
        )
        self.assertLess(
            score_ledger_response(good_then_bad, expected, example["info"]["accounts"]),
            score_ledger_response(bad_then_good, expected, example["info"]["accounts"]),
        )

    def test_response_diagnostics_count_candidates(self):
        example = make_examples(seed=19, num_examples=1, account_count=2)[0]
        expected = example["info"]["ground_truths"][0]
        response = (
            f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>\n"
            f"<ledger>{json.dumps(expected, sort_keys=True)}</ledger>"
        )
        diagnostics = response_diagnostics(response)
        self.assertEqual(diagnostics["candidate_count"], 2.0)
        self.assertEqual(diagnostics["tag_count"], 2.0)
        self.assertEqual(diagnostics["multi_candidate"], 1.0)
        self.assertEqual(diagnostics["exact_one_ledger"], 0.0)

    def test_completion_diagnostics_average_assistant_turns(self):
        example = make_examples(seed=20, num_examples=1, min_turns=2, max_turns=2)[0]
        first, second = example["info"]["ground_truths"]
        completion = [
            {
                "role": "assistant",
                "content": f"<ledger>{json.dumps(first, sort_keys=True)}</ledger>",
            },
            {"role": "user", "content": "ignored"},
            {
                "role": "assistant",
                "content": (
                    f"<ledger>{json.dumps(second, sort_keys=True)}</ledger>\n"
                    f"<ledger>{json.dumps(second, sort_keys=True)}</ledger>"
                ),
            },
        ]
        diagnostics = completion_diagnostics(completion)
        self.assertEqual(diagnostics["parseable_turn_rate"], 1.0)
        self.assertEqual(diagnostics["exact_one_ledger_rate"], 0.5)
        self.assertEqual(diagnostics["multi_candidate_rate"], 0.5)
        self.assertEqual(diagnostics["candidate_count"], 1.5)


if __name__ == "__main__":
    unittest.main()

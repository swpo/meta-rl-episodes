import json
from types import SimpleNamespace
import unittest

from meta_data_analysis_lite import (
    TASK_FAMILIES,
    answer_diagnostics,
    completion_diagnostics,
    make_examples,
    response_diagnostics,
    score_completion,
    score_result_response,
    selected_result_candidate,
)


class MetaDataAnalysisLiteTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        first = make_examples(seed=7, num_examples=4, min_rows=6, max_rows=8)
        second = make_examples(seed=7, num_examples=4, min_rows=6, max_rows=8)
        self.assertEqual(first, second)
        self.assertGreaterEqual(first[0]["info"]["num_rows"], 6)
        self.assertLessEqual(first[0]["info"]["num_rows"], 8)

    def test_all_task_families_generate(self):
        for family in TASK_FAMILIES:
            examples = make_examples(
                seed=11,
                num_examples=3,
                min_rows=6,
                max_rows=6,
                task_families=[family],
            )
            self.assertEqual(examples[0]["info"]["task_family"], family)
            self.assertIn("Question:", examples[0]["prompt"][0]["content"])

    def test_mixed_task_families_are_arrow_compatible(self):
        try:
            from datasets import Dataset
        except Exception as exc:
            self.skipTest(f"datasets unavailable: {exc}")
        examples = make_examples(seed=11, num_examples=32, min_rows=8, max_rows=12)
        dataset = Dataset.from_list(examples)
        self.assertEqual(len(dataset), 32)

    def test_exact_numeric_json_scores_one(self):
        example = make_examples(
            seed=12,
            num_examples=1,
            task_families=["sum_revenue_by_product"],
        )[0]
        expected = json.loads(example["answer"])
        response = f"<result>{json.dumps({'answer': expected['answer']})}</result>"
        self.assertEqual(score_result_response(response, expected), 1.0)

    def test_exact_string_json_scores_one(self):
        example = make_examples(
            seed=13,
            num_examples=1,
            task_families=["max_region_revenue"],
        )[0]
        expected = json.loads(example["answer"])
        response = f"<result>{json.dumps({'answer': expected['answer']})}</result>"
        self.assertEqual(score_result_response(response, expected), 1.0)

    def test_malformed_output_returns_zero(self):
        example = make_examples(seed=14, num_examples=1)[0]
        expected = json.loads(example["answer"])
        self.assertEqual(score_result_response(None, expected), 0.0)
        self.assertEqual(score_result_response("not a result", expected), 0.0)

    def test_close_numeric_answer_gets_partial_credit(self):
        expected = {"answer": 100, "answer_type": "number"}
        response = '<result>{"answer": 90}</result>'
        score = score_result_response(response, expected)
        self.assertGreater(score, 0.8)
        self.assertLess(score, 1.0)

    def test_json_outside_tag_has_format_penalty(self):
        expected = {"answer": 25, "answer_type": "number"}
        score = score_result_response('{"answer": 25}', expected)
        self.assertGreater(score, 0.8)
        self.assertLess(score, 1.0)

    def test_extra_key_has_schema_penalty(self):
        expected = {"answer": 25, "answer_type": "number"}
        score = score_result_response(
            '<result>{"answer": 25, "scratch": "computed"}</result>',
            expected,
        )
        self.assertGreater(score, 0.9)
        self.assertLess(score, 1.0)

    def test_penalizes_multiple_candidates_and_selects_last(self):
        expected = {"answer": 25, "answer_type": "number"}
        good_then_bad = '<result>{"answer": 25}</result><result>{"answer": 0}</result>'
        bad_then_good = '<result>{"answer": 0}</result><result>{"answer": 25}</result>'
        self.assertLess(
            score_result_response(good_then_bad, expected),
            score_result_response(bad_then_good, expected),
        )
        self.assertLess(score_result_response(bad_then_good, expected), 1.0)

    def test_completion_scores_answer_signature(self):
        example = make_examples(seed=15, num_examples=1)[0]
        expected = json.loads(example["answer"])
        completion = [
            {
                "role": "assistant",
                "content": f"<result>{json.dumps({'answer': expected['answer']})}</result>",
            }
        ]
        self.assertEqual(score_completion(completion, example["answer"]), 1.0)

    def test_completion_accepts_message_objects(self):
        example = make_examples(seed=16, num_examples=1)[0]
        expected = json.loads(example["answer"])
        completion = [
            SimpleNamespace(
                role="assistant",
                content=f"<result>{json.dumps({'answer': expected['answer']})}</result>",
            )
        ]
        self.assertEqual(score_completion(completion, example["answer"]), 1.0)

    def test_completion_diagnostics_read_last_assistant_message(self):
        completion = [
            {"role": "assistant", "content": '<result>{"answer": 1}</result>'},
            {"role": "user", "content": "ignored"},
            {
                "role": "assistant",
                "content": '<result>{"answer": 2}</result><result>{"answer": 3}</result>',
            },
        ]
        diagnostics = completion_diagnostics(completion)
        self.assertEqual(diagnostics["candidate_count"], 2.0)
        self.assertEqual(diagnostics["multi_candidate"], 1.0)

    def test_answer_diagnostics_report_exact_and_error(self):
        completion = [{"role": "assistant", "content": '<result>{"answer": 95}</result>'}]
        diagnostics = answer_diagnostics(
            completion,
            json.dumps({"answer": 100, "answer_type": "number"}),
        )
        self.assertEqual(diagnostics["exact_answer"], 0.0)
        self.assertEqual(diagnostics["numeric_abs_error"], 5.0)
        self.assertEqual(diagnostics["answer_score"], 0.95)

    def test_selected_candidate_handles_single_tag_with_extra_json(self):
        selected = selected_result_candidate(
            '<result>{"scratch": 1} {"answer": 4}</result>'
        )
        self.assertEqual(selected[0]["answer"], 4)

    def test_response_diagnostics_track_format(self):
        diagnostics = response_diagnostics(
            '```json\n<result>{"answer": 1}</result>\n```'
        )
        self.assertEqual(diagnostics["parseable"], 1.0)
        self.assertEqual(diagnostics["exact_one_result"], 1.0)
        self.assertEqual(diagnostics["code_fence"], 1.0)


if __name__ == "__main__":
    unittest.main()

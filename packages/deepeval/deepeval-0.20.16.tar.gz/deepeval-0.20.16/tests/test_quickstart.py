"""This is the ideal user flow
"""
import pytest

from deepeval.metrics.factual_consistency import assert_factual_consistency
from deepeval.metrics.overall_score import OverallScoreMetric
from deepeval.test_case import LLMTestCase
from deepeval.run_test import assert_test, run_test


def generate_llm_output(query: str):
    expected_output = "Our customer success phone line is 1200-231-231."
    return expected_output


def test_llm_output():
    query = "What is the customer success phone line?"
    expected_output = "Our customer success phone line is 1200-231-231."
    output = generate_llm_output(query)
    assert_factual_consistency(output, expected_output)


def test_llm_output_custom():
    query = "What is the customer success phone line?"
    expected_output = "Dogs and cats love to walk around the beach."
    with pytest.raises(AssertionError):
        assert_factual_consistency(query, expected_output)


def test_0():
    query = "How does photosynthesis work?"
    output = "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll pigment."
    expected_output = "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize food with the help of chlorophyll pigment."
    context = "Biology"

    test_case = LLMTestCase(
        input=query,
        actual_output=output,
        expected_output=expected_output,
        context=context,
    )
    metric = OverallScoreMetric()
    # if you want to make sure that the test returns an error
    assert_test(test_case, metrics=[metric])

    # If you want to run the test
    test_result = run_test(test_case, metrics=[metric])
    # You can also inspect the test result class
    print(test_result[0].success)
    print(test_result[0].score)

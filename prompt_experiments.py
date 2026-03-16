#!/usr/bin/env python3
"""
Primary Research: Prompt Efficiency Experiments
================================================
Tests 12 prompt techniques against a baseline using Claude Haiku 4.5
to measure actual token usage and response quality differences.

Author: Sam Matharu | Date: March 2026
"""

import anthropic
import json
import time
import os

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5-20251001"  # Use Haiku for cost-efficient testing

# ============================================================
# TEST QUESTIONS (5 diverse questions across domains)
# ============================================================
TEST_QUESTIONS = [
    {
        "id": "Q1",
        "domain": "Business",
        "question": "What are the key factors that determine whether a company should pursue organic growth versus growth through acquisitions?"
    },
    {
        "id": "Q2",
        "domain": "Science",
        "question": "Explain how mRNA vaccines work and why they were significant during the COVID-19 pandemic."
    },
    {
        "id": "Q3",
        "domain": "Technology",
        "question": "What is the difference between supervised and unsupervised machine learning, and when should each be used?"
    },
    {
        "id": "Q4",
        "domain": "Finance",
        "question": "Explain the concept of compound interest and provide a practical example of how it affects long-term savings."
    },
    {
        "id": "Q5",
        "domain": "History",
        "question": "What were the main causes of the Industrial Revolution in Britain?"
    },
]

# ============================================================
# EXPERIMENT DEFINITIONS
# ============================================================
experiments = {
    "baseline": {
        "name": "Baseline (No Optimisation)",
        "system": None,
        "prefix": "",
        "suffix": "",
    },
    "P1_token_economist": {
        "name": "P1: Token Economist (Miserly Prompt)",
        "system": "You are a miserly person, use tokens sparingly. Imagine each token is £1. Be careful with your money. Give me a receipt of token use and money saved because of this method, for each answer.",
        "prefix": "",
        "suffix": "",
    },
    "P2_role_specialist": {
        "name": "P2: Role Specialist",
        "system": "You are a senior academic researcher with 20 years of experience. You provide precise, evidence-based answers drawing on deep domain expertise.",
        "prefix": "",
        "suffix": "",
    },
    "P3_xml_tags": {
        "name": "P3: XML Structure Tags",
        "system": None,
        "prefix": "<instructions>\nAnswer the following question accurately and helpfully.\n</instructions>\n\n<input>\n",
        "suffix": "\n</input>\n\n<output_format>\nProvide a clear, well-structured answer.\n</output_format>",
    },
    "P4_few_shot": {
        "name": "P4: Few-Shot Examples",
        "system": None,
        "prefix": """<examples>
<example>
<question>What is GDP?</question>
<answer>GDP (Gross Domestic Product) measures the total monetary value of all finished goods and services produced within a country's borders in a specific period. It serves as a comprehensive scorecard of a country's economic health. GDP can be calculated via three approaches: expenditure (C+I+G+NX), income, or production. It is typically reported quarterly and annually, with real GDP adjusting for inflation to enable meaningful comparisons over time.</answer>
</example>
</examples>

Now answer this question in the same style:
""",
        "suffix": "",
    },
    "P5_concise_cot": {
        "name": "P5: Concise Chain-of-Thought",
        "system": None,
        "prefix": "",
        "suffix": "\n\nThink through this step-by-step, but be concise. Show reasoning in brief bullet points, then give your final answer.",
    },
    "P6_output_format": {
        "name": "P6: Output Format Constraint",
        "system": None,
        "prefix": "",
        "suffix": "\n\nRespond in exactly 3 bullet points. Each bullet must be under 25 words. No preamble, no conclusion.",
    },
    "P7_positive_framing": {
        "name": "P7: Positive Framing",
        "system": "Respond in plain prose paragraphs. Start directly with the answer. State facts without caveats or hedging. Use an authoritative, direct tone throughout.",
        "prefix": "",
        "suffix": "",
    },
    "P1_P6_combined": {
        "name": "P1+P6: Token Economist + Output Format",
        "system": "You are a miserly person, use tokens sparingly. Imagine each token is £1.",
        "prefix": "",
        "suffix": "\n\nRespond in exactly 3 bullet points. Each bullet under 25 words. No preamble.",
    },
    "P1_P3_P6_combined": {
        "name": "P1+P3+P6: Economist + XML + Format",
        "system": "You are a miserly person, use tokens sparingly. Imagine each token is £1.",
        "prefix": "<instructions>\nAnswer concisely in exactly 3 bullet points, each under 25 words.\n</instructions>\n\n<input>\n",
        "suffix": "\n</input>",
    },
    "full_stack": {
        "name": "Full Stack (P1+P2+P3+P5+P6+P7)",
        "system": "You are a senior academic researcher. Be extremely concise — each token costs £1. Respond in plain prose, start directly with the answer, no hedging.",
        "prefix": "<instructions>\nAnswer in exactly 3 concise bullet points (under 25 words each).\nThink briefly, then answer.\n</instructions>\n\n<input>\n",
        "suffix": "\n</input>",
    },
}

# ============================================================
# RUN EXPERIMENTS
# ============================================================
def run_experiment(exp_key, exp_config, question_data):
    """Run a single experiment and return results."""
    question = question_data["question"]

    # Build the user message
    user_content = exp_config["prefix"] + question + exp_config["suffix"]

    # Build messages
    messages = [{"role": "user", "content": user_content}]

    # Build kwargs
    kwargs = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": messages,
    }

    if exp_config["system"]:
        kwargs["system"] = exp_config["system"]

    try:
        start_time = time.time()
        response = client.messages.create(**kwargs)
        elapsed = time.time() - start_time

        # Extract metrics
        output_text = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens

        # Count words in response
        word_count = len(output_text.split())

        return {
            "experiment": exp_key,
            "experiment_name": exp_config["name"],
            "question_id": question_data["id"],
            "domain": question_data["domain"],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "word_count": word_count,
            "response_time_s": round(elapsed, 2),
            "response_text": output_text[:500],  # First 500 chars for review
            "success": True,
        }
    except Exception as e:
        return {
            "experiment": exp_key,
            "experiment_name": exp_config["name"],
            "question_id": question_data["id"],
            "domain": question_data["domain"],
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "word_count": 0,
            "response_time_s": 0,
            "response_text": f"ERROR: {str(e)}",
            "success": False,
        }


def main():
    print("=" * 70)
    print("PRIMARY RESEARCH: Prompt Efficiency Experiments")
    print(f"Model: {MODEL}")
    print(f"Questions: {len(TEST_QUESTIONS)}")
    print(f"Experiments: {len(experiments)}")
    print(f"Total API calls: {len(TEST_QUESTIONS) * len(experiments)}")
    print("=" * 70)

    all_results = []

    for exp_key, exp_config in experiments.items():
        print(f"\n--- Running: {exp_config['name']} ---")

        for q in TEST_QUESTIONS:
            result = run_experiment(exp_key, exp_config, q)
            all_results.append(result)

            status = "OK" if result["success"] else "FAIL"
            print(f"  {q['id']} ({q['domain']}): "
                  f"in={result['input_tokens']} out={result['output_tokens']} "
                  f"total={result['total_tokens']} words={result['word_count']} "
                  f"time={result['response_time_s']}s [{status}]")

            # Small delay to respect rate limits
            time.sleep(0.5)

    # ============================================================
    # ANALYSIS
    # ============================================================
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    # Calculate averages per experiment
    exp_averages = {}
    for exp_key in experiments:
        exp_results = [r for r in all_results if r["experiment"] == exp_key and r["success"]]
        if exp_results:
            avg_input = sum(r["input_tokens"] for r in exp_results) / len(exp_results)
            avg_output = sum(r["output_tokens"] for r in exp_results) / len(exp_results)
            avg_total = sum(r["total_tokens"] for r in exp_results) / len(exp_results)
            avg_words = sum(r["word_count"] for r in exp_results) / len(exp_results)
            avg_time = sum(r["response_time_s"] for r in exp_results) / len(exp_results)

            exp_averages[exp_key] = {
                "name": experiments[exp_key]["name"],
                "avg_input_tokens": round(avg_input, 1),
                "avg_output_tokens": round(avg_output, 1),
                "avg_total_tokens": round(avg_total, 1),
                "avg_words": round(avg_words, 1),
                "avg_time_s": round(avg_time, 2),
                "n": len(exp_results),
            }

    # Calculate savings vs baseline
    baseline = exp_averages.get("baseline", {})
    baseline_output = baseline.get("avg_output_tokens", 1)
    baseline_total = baseline.get("avg_total_tokens", 1)
    baseline_words = baseline.get("avg_words", 1)

    print(f"\n{'Technique':<45} {'Avg Out':>8} {'Saving':>8} {'Avg Words':>10} {'Word Save':>10} {'Time(s)':>8}")
    print("-" * 95)

    for exp_key, avg in exp_averages.items():
        output_saving = ((baseline_output - avg["avg_output_tokens"]) / baseline_output) * 100
        word_saving = ((baseline_words - avg["avg_words"]) / baseline_words) * 100

        print(f"{avg['name']:<45} {avg['avg_output_tokens']:>8.1f} {output_saving:>7.1f}% "
              f"{avg['avg_words']:>10.1f} {word_saving:>9.1f}% {avg['avg_time_s']:>8.2f}")

    # Save full results
    output_path = "/Users/samrajmatharu/Desktop/prompt_experiment_results.json"
    with open(output_path, "w") as f:
        json.dump({
            "metadata": {
                "model": MODEL,
                "date": "2026-03-16",
                "n_questions": len(TEST_QUESTIONS),
                "n_experiments": len(experiments),
            },
            "averages": exp_averages,
            "baseline_output_tokens": baseline_output,
            "baseline_total_tokens": baseline_total,
            "baseline_words": baseline_words,
            "raw_results": all_results,
        }, f, indent=2)

    print(f"\nFull results saved to: {output_path}")
    print("Done!")


if __name__ == "__main__":
    main()

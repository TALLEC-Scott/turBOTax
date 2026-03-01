#!/usr/bin/env python
"""
LLM-based evaluation of the Turbo Tax knowledge base against the IRS Q&A dataset.

Uses an LLM judge to compare KB answers with ground truth answers.
"""

import json
from pathlib import Path


def load_dataset():
    """Load the IRS Q&A evaluation dataset."""
    data_path = Path(__file__).parent.parent / "data" / "irs_qa_eval.json"
    with open(data_path) as f:
        return json.load(f)


def create_judge_prompt(qa: dict, kb_content: str | None) -> str:
    """Create a prompt for the LLM judge."""
    prompt = f"""You are a tax expert judge. Evaluate whether the knowledge base answer correctly answers the question compared to the ground truth.

QUESTION: {qa['question']}

GROUND TRUTH ANSWER: {qa['answer']}

KNOWLEDGE BASE CONTENT:
{kb_content if kb_content else "No relevant content found in knowledge base."}

INSTRUCTIONS:
1. Compare the knowledge base content to the ground truth answer
2. Determine if the KB content would allow someone to arrive at the correct answer
3. Judge the quality of the KB content for answering this question

RESPONSE FORMAT (JSON):
{{
  "judgment": "CORRECT" | "PARTIALLY_CORRECT" | "INCORRECT" | "NOT_COVERED",
  "explanation": "Brief explanation of your judgment",
  "kb_answer": "The answer that could be derived from the KB (if applicable)",
  "key_missing_info": "Key information missing from KB (if applicable)"
}}

JUDGMENT CRITERIA:
- CORRECT: KB contains the specific answer or equivalent information
- PARTIALLY_CORRECT: KB has relevant info but lacks specificity or completeness
- INCORRECT: KB has related content but would lead to wrong answer
- NOT_COVERED: KB has no relevant content for this question

Respond ONLY with valid JSON, no other text."""
    return prompt


def create_summary_prompt(results: list[dict]) -> str:
    """Create a prompt for summarizing evaluation results."""
    correct = sum(1 for r in results if r.get("judgment") == "CORRECT")
    partial = sum(1 for r in results if r.get("judgment") == "PARTIALLY_CORRECT")
    incorrect = sum(1 for r in results if r.get("judgment") == "INCORRECT")
    not_covered = sum(1 for r in results if r.get("judgment") == "NOT_COVERED")
    
    # Build examples string
    examples = []
    for r in results[:10]:
        examples.append(f"""
Q: {r['question']}
Ground Truth: {r['ground_truth'][:200]}...
Judgment: {r.get('judgment', 'N/A')}
Explanation: {r.get('explanation', 'N/A')[:150]}...
""")
    
    prompt = f"""Summarize this LLM evaluation of a tax knowledge base:

TOTAL QUESTIONS: {len(results)}
- CORRECT: {correct} ({correct/len(results)*100:.1f}%)
- PARTIALLY_CORRECT: {partial} ({partial/len(results)*100:.1f}%)
- INCORRECT: {incorrect} ({incorrect/len(results)*100:.1f}%)
- NOT_COVERED: {not_covered} ({not_covered/len(results)*100:.1f}%)

SAMPLE EVALUATIONS:
{''.join(examples)}

Provide:
1. Overall assessment (1-2 sentences)
2. Key strengths of the knowledge base
3. Main gaps/weaknesses
4. Top 3 recommendations for improvement

Be concise and actionable."""
    return prompt


def main():
    """Run the LLM-judged evaluation."""
    print("Loading dataset...")
    questions = load_dataset()
    print(f"Loaded {len(questions)} questions")
    
    # Sample a subset for evaluation (we'll evaluate 20 questions)
    sample_size = 20
    # Sample diverse questions
    import random
    random.seed(42)
    sample = random.sample(questions, min(sample_size, len(questions)))
    
    print(f"\nSampled {len(sample)} questions for LLM evaluation")
    print("\nTo run the actual LLM evaluation, you would call this script")
    print("with an LLM API (OpenAI, Anthropic, or local model).")
    print("\nFor now, generating evaluation prompts...\n")
    
    # Save prompts for manual evaluation
    prompts = []
    for i, qa in enumerate(sample):
        prompt = create_judge_prompt(qa, None)  # No KB content - would need to search
        prompts.append({
            "id": i,
            "question": qa["question"],
            "ground_truth": qa["answer"],
            "source": qa["source"],
            "prompt": prompt,
        })
    
    output_path = Path(__file__).parent.parent / "data" / "llm_eval_prompts.json"
    with open(output_path, "w") as f:
        json.dump(prompts, f, indent=2)
    
    print(f"Saved {len(prompts)} evaluation prompts to {output_path}")
    print("\nSample prompt:")
    print("-" * 60)
    print(prompts[0]["prompt"][:500] + "...")


if __name__ == "__main__":
    main()

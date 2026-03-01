#!/usr/bin/env python
"""
Evaluate the Turbo Tax agent against the IRS Q&A dataset.

This script tests how well the knowledge base can answer questions from the
QUOTIENTAI/IRS_FORM_INSTRUCTION_QA_PAIRS dataset.
"""

import json
from pathlib import Path


def load_dataset():
    """Load the IRS Q&A evaluation dataset."""
    data_path = Path(__file__).parent.parent / "data" / "irs_qa_eval.json"
    with open(data_path) as f:
        return json.load(f)


def check_kb_coverage(questions: list[dict]) -> dict:
    """
    Analyze which questions might be answerable from the knowledge base.
    
    This is a keyword-based heuristic check - in practice, we'd use
    the actual search tools.
    """
    # Topics we have in our knowledge base
    kb_topics = [
        "ira", "roth", "traditional ira", "401k", "401(k)", "403b", "sep",
        "simple", "pension", "annuity", "retirement",
        "social security", "medicare", "niit", "net investment",
        "capital gains", "capital loss", "dividend", "interest",
        "deduction", "credit", "exclusion", "exemption",
        "filing status", "head of household", "surviving spouse",
        "dependent", "child", "qualifying child",
        "gift", "estate", "inherit", "step-up", "basis",
        "charitable", "qcd", "donation",
        "home", "mortgage", "real estate", "sale of home",
        "business", "schedule c", "self-employment", "sole proprietor",
        "bankruptcy", "canceled debt", "foreclosure",
        "education", "student", "scholarship", "coverdell", "esa",
        "hsa", "health savings", "fsa", "medical",
        "passive activity", "at-risk", "rental",
        "household employee", "schedule h",
        "nonprofit", "501(c)(3)", "tax-exempt",
        "opportunity zone", "like-kind", "1031",
        "installment sale", "oid", "original issue discount",
        "expatriate", "foreign", "territory",
    ]
    
    results = {
        "total_questions": len(questions),
        "likely_covered": [],
        "likely_not_covered": [],
        "by_source": {},
    }
    
    for qa in questions:
        question_lower = qa["question"].lower()
        source = qa["source"]
        
        # Check if any KB topic appears in the question
        is_covered = any(topic in question_lower for topic in kb_topics)
        
        if is_covered:
            results["likely_covered"].append(qa)
        else:
            results["likely_not_covered"].append(qa)
        
        # Track by source
        if source not in results["by_source"]:
            results["by_source"][source] = {"covered": 0, "not_covered": 0}
        
        if is_covered:
            results["by_source"][source]["covered"] += 1
        else:
            results["by_source"][source]["not_covered"] += 1
    
    return results


def print_evaluation_report(results: dict):
    """Print a detailed evaluation report."""
    total = results["total_questions"]
    covered = len(results["likely_covered"])
    not_covered = len(results["likely_not_covered"])
    
    print("=" * 60)
    print("IRS Q&A DATASET EVALUATION REPORT")
    print("=" * 60)
    print()
    print(f"Total Questions: {total}")
    print(f"Likely Covered by KB: {covered} ({covered/total*100:.1f}%)")
    print(f"Likely Not Covered: {not_covered} ({not_covered/total*100:.1f}%)")
    print()
    
    print("-" * 60)
    print("COVERAGE BY SOURCE")
    print("-" * 60)
    for source, counts in sorted(results["by_source"].items()):
        total_source = counts["covered"] + counts["not_covered"]
        pct = counts["covered"] / total_source * 100 if total_source > 0 else 0
        print(f"\n{source}")
        print(f"  Covered: {counts['covered']}/{total_source} ({pct:.1f}%)")
    
    print()
    print("-" * 60)
    print("SAMPLE QUESTIONS LIKELY COVERED")
    print("-" * 60)
    for qa in results["likely_covered"][:5]:
        print(f"\nQ: {qa['question']}")
        print(f"A: {qa['answer'][:150]}..." if len(qa['answer']) > 150 else f"A: {qa['answer']}")
    
    print()
    print("-" * 60)
    print("SAMPLE QUESTIONS LIKELY NOT COVERED")
    print("-" * 60)
    for qa in results["likely_not_covered"][:5]:
        print(f"\nQ: {qa['question']}")
        print(f"A: {qa['answer'][:150]}..." if len(qa['answer']) > 150 else f"A: {qa['answer']}")


def main():
    print("Loading IRS Q&A dataset...")
    questions = load_dataset()
    print(f"Loaded {len(questions)} questions\n")
    
    print("Analyzing knowledge base coverage...")
    results = check_kb_coverage(questions)
    
    print_evaluation_report(results)
    
    # Save detailed results
    output_path = Path(__file__).parent.parent / "data" / "qa_eval_results.json"
    # Convert to serializable format
    serializable = {
        "total_questions": results["total_questions"],
        "likely_covered_count": len(results["likely_covered"]),
        "likely_not_covered_count": len(results["likely_not_covered"]),
        "by_source": results["by_source"],
    }
    with open(output_path, "w") as f:
        json.dump(serializable, f, indent=2)
    print(f"\nDetailed results saved to {output_path}")


if __name__ == "__main__":
    main()

import json

from neuro_san.interfaces.coded_tool import CodedTool


class FAQSearchTool(CodedTool):
    def run(self, query: str):
        with open("data/faq.json", "r") as f:
            faqs = json.load(f)

        # Simple Logic: Find the FAQ that shares the most keywords with the query
        query_words = set(query.lower().split())
        best_match = None
        max_overlap = 0

        for item in faqs:
            question_words = set(item["question"].lower().split())
            overlap = len(query_words.intersection(question_words))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = item

        if best_match:
            return f"Question: {best_match['question']}\nAnswer: {best_match['answer']}"
        return "I couldn't find a specific answer in the FAQ. Would you like to speak to an agent?"

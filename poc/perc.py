from ahocorasick import Automaton
from typing import List

class Percolator:
    def __init__(self):
        self.automaton = Automaton()
        self.terms_count = 0
        self.minimum_matches = {}

    def add_query(self, query: list[str], category: str, minimum_match: int):
        for term in query:
            self.automaton.add_word(term, (self.terms_count, category))
            self.terms_count += 1
        self.minimum_matches[category] = minimum_match

    def finalize(self):
        self.automaton.make_automaton()

    def percolate(self, document: str) -> List[str]:
        category_matches = {}
        for _, (_, category) in self.automaton.iter(document):
            category_matches[category] = category_matches.get(category, 0) + 1

        return [cat for cat, count in category_matches.items() if count >= self.minimum_matches.get(cat, 1)]
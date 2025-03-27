from ahocorasick import Automaton
from typing import List
import string
import unicodedata


class Percolator:
    def __init__(self):
        self.automaton = Automaton()
        self.minimum_matches = {}
        self.category_terms = {}
        self.unique_term_count = {}
        self.terms_count = 0
        self.punctuation_set = set(string.punctuation + " ")

    def add_query(self, query: list[str], category: str, minimum_match: int, unique_term_count:bool):
        if category not in self.category_terms:
            self.category_terms[category] = set()

        for term in query:
            self.automaton.add_word(term, (term, category))
            self.category_terms[category].add(term)
            self.terms_count += 1

        self.minimum_matches[category] = minimum_match
        self.unique_term_count[category] = unique_term_count

    def finalize(self):
        self.automaton.make_automaton()

    def is_boundary(self, char: str) -> bool:
        return not char or char in self.punctuation_set or unicodedata.category(char).startswith("P")

    def percolate(self, document: str) -> List[str]:
        category_matches = {category: 0 for category in self.category_terms}
        matched_terms = set()

        for pos, (term, category) in self.automaton.iter(document):
            if term in matched_terms and self.unique_term_count[category]:
                continue

            matched_terms.add(term)
            next_char = document[pos + 1] if pos + 1 < len(document) else ""
            before_char = document[pos - len(term)] if pos - len(term) >= 0 else ""

            if self.is_boundary(before_char) and self.is_boundary(next_char):
                category_matches[category] += 1

        return [cat for cat, count in category_matches.items() if count >= self.minimum_matches.get(cat, 1)]

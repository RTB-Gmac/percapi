from perc import Percolator
from time import perf_counter
import random

def test_add_query():
    # GIVEN
    perc = Percolator()
    perc.add_query(["test", "example"], "1", 2, True)

    # WHEN & THEN
    assert perc.terms_count == 2
    assert perc.minimum_matches["1"] == 2

def test_finalize():
    # GIVEN
    perc = Percolator()
    perc.add_query(["test"], "1", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert hasattr(perc.automaton, 'make_automaton')

def test_percolate_single_match():
    # GIVEN
    perc = Percolator()
    perc.add_query(["hello", "world"], "1", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("hello everyone") == ["1"]
    assert perc.percolate("worldwide news") == []
    assert perc.percolate("world wide news") == ["1"]

def test_percolate_minimum_match():
    # GIVEN
    perc = Percolator()
    perc.add_query(["apple", "banana", "cherry"], "2", 2, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("apple and banana") == ["2"]
    assert perc.percolate("banana only") == []

def test_percolate_unique_term_count():
    # GIVEN
    perc = Percolator()
    perc.add_query(["apple", "banana",], "2", 2, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("banana and banana and banana") == []
    assert perc.percolate("apple and banana") == ["2"]
    assert perc.percolate("banana only") == []

def test_percolate_every_term_count():
    # GIVEN
    perc = Percolator()
    perc.add_query(["apple", "banana",], "2", 2, False)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("banana and banana and banana") == ["2"]
    assert perc.percolate("banana only") == []

def test_percolate_lowercase_uppercase():
    # GIVEN
    perc = Percolator()
    perc.add_query(["Jan"], "upper", 1, True)
    perc.add_query(["jan"], "lower", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("Names like 'jan' should be written uppercase") == ["lower"]
    assert perc.percolate("trojan is kind of computer virus") == []
    assert perc.percolate("Jan is popular polish name.") == ["upper"]

def test_percolate_multiple_queries():
    # GIVEN
    perc = Percolator()
    perc.add_query(["car", "bike"], "3", 1, True)
    perc.add_query(["plane", "train"], "4", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert set(perc.percolate("I have a car and a train")) == {"3", "4"}
    assert perc.percolate("Only bikes") == []
    assert perc.percolate("Only bike") == ["3"]
    assert perc.percolate("Just a train") == ["4"]

def test_percolate_no_match():
    # GIVEN
    perc = Percolator()
    perc.add_query(["dog", "cat"], "5", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("fish and bird") == []

def test_percolate_phrases():
    # GIVEN
    perc = Percolator()
    perc.add_query(["two words", "three words query"], "1", 1, True)
    perc.add_query(["four words are here", "five words is a charm"], "2", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("two words have this document") == ["1"]
    assert perc.percolate("is there three words query?") == ["1"]
    assert perc.percolate("four words are here with us?") == ["2"]
    assert perc.percolate("True sentence is five words is a charm...") == ["2"]
    assert perc.percolate("six words is a charm but no query here match this document") == []

def test_percolate_large_query():
    # GIVEN
    perc = Percolator()
    large_query = [f"term_{i}" for i in range(20000)]
    perc.add_query(large_query, "large", 5000, True)
    perc.finalize()
    test_document = " ".join(large_query[:5000])

    # WHEN & THEN
    assert perc.percolate(test_document) == ["large"]
    assert perc.percolate("random text") == []

def test_percolate_multilingual():
    # GIVEN
    perc = Percolator()
    perc.add_query(["hello", "bonjour", "hola", "hallo", "ciao"], "lang", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("bonjour tout le monde") == ["lang"]
    assert perc.percolate("hola amigo") == ["lang"]
    assert perc.percolate("guten tag") == []

def test_percolate_with_punctuation():
    # GIVEN
    perc = Percolator()
    perc.add_query(["hello"], "punctuation", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("hello!") == ["punctuation"]
    assert perc.percolate("hello?") == ["punctuation"]
    assert perc.percolate("hello, how are you today?") == ["punctuation"]
    assert perc.percolate("hello: welcome") == ["punctuation"]
    assert perc.percolate("whathello") == []
    assert perc.percolate("hellothere") == []
    assert perc.percolate("whathellothere") == []

def test_percolate_non_latin():
    # GIVEN
    perc = Percolator()
    perc.add_query(["مرحبا", "你好", "こんにちは", "привет"], "nonlatin", 1, True)
    perc.finalize()

    # WHEN & THEN
    assert perc.percolate("مرحبا بالعالم") == ["nonlatin"]
    assert perc.percolate("你好，世界") == ["nonlatin"]
    assert perc.percolate("こんにちは、みんなさん") == ["nonlatin"]
    assert perc.percolate("привет, друзья") == ["nonlatin"]
    assert perc.percolate("random english text") == []

def test_percolation_performance():
    # GIVEN
    perc = Percolator()
    number_of_docs = 2000
    average_query = []
    for num in range(120): # average terms in query ~114
        term = f"test___{num}" # average terms length ~10 chars
        average_query.append(term)

    for num in range(10000): # check for 10k queries in index
        random.shuffle(average_query) # shuffle data for less synthetic tests
        perc.add_query(average_query, f"test_{num}", 1, True)

    perc.add_query(["testsss12"], "perf_0", 1, True) # add query which will be labeled
    perc.finalize()

    test_document = "testsss12 " * 1000 # test documents with 10k chars

    # WHEN
    start_time = perf_counter()
    for _ in range(number_of_docs):
        perc.percolate(test_document)
    end_time = perf_counter()
    exec_time = (end_time - start_time)
    docs_per_second = number_of_docs / exec_time
    print(f"\nPerformance: {round(docs_per_second)} [docs / sec.]")

    # THEN
    assert docs_per_second > 1000 # performance on my machine is ~1.2k per second. Single thread.

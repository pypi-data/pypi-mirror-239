import unittest
from sentencesplitter.splitter import split_sentences

class TestSentenceSplitter(unittest.TestCase):
    
    def test_split_sentences_basic(self):
        text = "This is a sample sentence. It should be split into two sentences."
        expected = ["This is a sample sentence.", "It should be split into two sentences."]
        result = split_sentences(text)
        self.assertEqual(result, expected)

    def test_split_sentences_edge_cases(self):
        # Test empty input
        text = ""
        expected = []
        result = split_sentences(text)
        self.assertEqual(result, expected)

        # Test input with no sentences (single line)
        text = "This is not a sentence without punctuation"
        expected = ["This is not a sentence without punctuation"]
        result = split_sentences(text)
        self.assertEqual(result, expected)

        # Test input with multiple spaces
        text = "Sentence 1.  Sentence 2."
        expected = ["Sentence 1.", "Sentence 2."]
        result = split_sentences(text)
        self.assertEqual(result, expected)

    def test_split_sentences_punctuation(self):
        text = "This is a sentence! It ends with an exclamation mark."
        expected = ["This is a sentence!", "It ends with an exclamation mark."]
        result = split_sentences(text)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()

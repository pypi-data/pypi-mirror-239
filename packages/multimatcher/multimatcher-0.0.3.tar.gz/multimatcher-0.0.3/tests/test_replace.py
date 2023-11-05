import unittest
import json
from pathlib import Path

from multimatcher import Multimatcher


class TestMultimatcherFind(unittest.TestCase):
    def setUp(self):
        file_path = Path(__file__).parent
        with open(file_path.joinpath('test_cases_replace.json')) as file:
            self.test_cases = json.load(file)

    def test_replace_words(self):
        for setting in self.test_cases:
            whole_words_only = setting.get('whole_words_only', True)
            separator = setting['separator']
            patterns = setting['patterns']
            test_cases = setting['test_cases']
            matcher = Multimatcher(separator=separator, whole_words_only=whole_words_only)
            matcher.set_search_patterns(patterns)
            matcher.set_replacement_method(lambda x: f"<FOUND>{x}</FOUND>")
            for test_case in test_cases:
                test_input = test_case['input']
                expected_output = test_case['expected_output']
                actual_output = matcher.replace(test_input)
                self.assertEqual(expected_output, actual_output)

    def test_delete(self):
        test_input = 'x a y b z c'
        whole_words_expected = 'x y z'
        mm = Multimatcher(separator=' ')
        mm.set_replacement_text("")
        mm.set_search_patterns(['a', 'b', 'c'])
        self.assertEqual(mm.replace(test_input), whole_words_expected)

        not_whole_words_expected = 'x  y  z '
        mm.whole_words_only = False
        mm.set_separator("")
        self.assertEqual(mm.replace(test_input), not_whole_words_expected)

    def test_complex_separator(self):
        test_input = 'xabcaabcyabcbabczabcc'
        whole_words_expected = 'xabcyabcz'
        mm = Multimatcher(separator='abc', whole_words_only=False)
        mm.set_replacement_text("")
        mm.set_search_patterns(['a', 'b', 'c'])
        self.assertEqual(mm.replace(test_input), whole_words_expected)

        mm.whole_words_only = True
        self.assertEqual(mm.replace(test_input), test_input)

        mm.set_separator("")
        mm.whole_words_only = False
        self.assertEqual(mm.replace(test_input), "xyz")




if __name__ == '__main__':
    unittest.main()

import unittest
import json
from pathlib import Path

from multimatcher import Multimatcher


class TestMultimatcherFind(unittest.TestCase):
    def setUp(self):
        file_path = Path(__file__).parent
        with open(file_path.joinpath('test_cases_find.json')) as file:
            self.test_cases = json.load(file)

    def test_find_words(self):
        for setting in self.test_cases:
            whole_words_only = setting.get('whole_words_only', True)
            separator = setting['separator']
            patterns = setting['patterns']
            test_cases = setting['test_cases']
            matcher = Multimatcher(separator=separator, whole_words_only=whole_words_only)
            matcher.set_search_patterns(patterns)
            for test_case in test_cases:
                test_input = test_case['input']
                expected_output = test_case['expected_output']
                actual_output = [match.string for match in matcher.find(test_input)]
                self.assertEqual(sorted(expected_output), sorted(actual_output))


if __name__ == '__main__':
    unittest.main()

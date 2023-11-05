from typing import Iterable, Dict, Callable, List

from multimatcher.match_mode import MatchMode
from multimatcher.trie import Trie
from multimatcher.match import Match
from multimatcher.replacer import SimpleReplacer, MapReplacer, TransformerReplacer


class Multimatcher:
    """
        Multimatcher is an implementation of the Aho-Corasick (Aho & Corasick 1975) search algorithm.
        It efficiently finds multiple keywords in an input string, without having to loop
        over the input string multiple times.
        The rationale behind the Multimatcher is that most often we want to do something with the found matches, and
        the Multimatcher provides a flexible "replace" method that allows different use cases such as:
            - find and delete
            - find and replace
            - tag with a global label (i.e. all matches get the same label)
            - tag with custom label (i.e. each match gets its own label)
            - count matches
        When possible, it's recommended to set whole_words_only to True, which makes matching significantly faster.

        Examples:
            from multimatcher import Multimatcher
            mm = Multimatcher(separator=' ')
            mm.set_replacement_text("") # matches will be deleted
            mm.set_search_patterns(['a', 'b', 'c'])
            mm.replace("x a y b z c") # produces "x y z"

            from multimatcher import Multimatcher
            mm = Multimatcher(separator=' ')
            mm.set_replacement_method(lambda x: x.capitalize()) # matches will be capitalized
            mm.set_search_patterns(['a', 'b', 'c'])
            mm.replace("x a y b z c") # produces "x A y B z C"

            from multimatcher import Multimatcher
            mm = Multimatcher(separator=' ')
            mm.set_replacement_text("0") # all matches will be replaced with 0
            mm.set_search_patterns(['a', 'b', 'c'])
            mm.replace("x a y b z c") # produces "x 0 y 0 z 0"

            from multimatcher import Multimatcher
            mm = Multimatcher(separator=' ')
            mm.set_replacement_map({"a": "1", "b": "2", "c": "3"}) # replaces a > 1, b > 2, c > 3
            mm.set_search_patterns(['a', 'b', 'c'])
            mm.replace("x a y b z c") # produces "x 1 y 2 z 3"

            from multimatcher import Multimatcher
            mm = Multimatcher(separator='')
            mm.set_search_patterns(['a', 'b', 'c'])
            mm.count("aa xx bb yy cc zz") # produces {'a': 2, 'b': 2, 'c': 2}


        References:
            Aho, A. V., & Corasick, M. J. (1975). Efficient string matching: an aid to bibliographic search.
            Communications of the ACM, 18(6), 333-340.
    """

    def __init__(self, separator=" ", match_mode=MatchMode.LONGEST_NON_OVERLAPPING, whole_words_only=True):
        self.replacement_map = {}
        self.root_trie = None
        self.whole_words_only = whole_words_only
        self.replacer = SimpleReplacer("MATCH")
        self.separator = ""
        self.set_separator(separator)
        self.match_mode = match_mode

    def set_separator(self, sep: str):
        """Set separator.

        This should be a string, of any length (including 0).

        :param sep: Separator string
        :return: None
        """
        if sep is not None and type(sep) == str:
            self.separator = sep

    def split(self, string: str):
        """Split string into tokens, using self.separator.

        :param string: Input string to be split
        :return: A list of string tokens.
        """
        if len(self.separator) == 0:
            return list(string)
        else:
            return string.split(self.separator)

    def set_search_patterns(self, search_patterns: Iterable[str]):
        """Set the patterns to be searched.

        :param search_patterns: An iterable of strings, representing the patterns to find.
        :return: None
        """
        self.root_trie = Trie.create(search_patterns, self.split)

    def set_replacement_map(self, replacement_map: Dict[str, str]):
        """Set replacement map. This map defines the values to be used as replacements for the found matches.

        :param replacement_map: A dictionary of string -> string, where keys are the search patterns, and the
        values are the replacement strings. This method automatically sets the search patterns, using the keys
        of replacement_map.
        :return: None
        """
        self.set_search_patterns(list(replacement_map.keys()))
        self.replacer = MapReplacer(replacement_map)

    def set_replacement_method(self, replacement_method: Callable[[str], str]):
        """Set the replacement method.

        :param replacement_method: A method that takes a string as input, and returns a transformed string as output.
        :return: None
        """
        self.replacer = TransformerReplacer(replacement_method)

    def set_replacement_text(self, replacement_text: str):
        """Set replacement text.

        :param replacement_text: Text that will be used to replace all matches.
        :return: None
        """
        self.replacer = SimpleReplacer(replacement_text)

    def __replace(self, string: str):
        """Use the defined replacer to get the replacement for the input string.

        :param string: Input string for which a replacement is needed.
        :return: The replacement string for the input string.
        """
        return self.replacer.replace(string)

    def replace(self, string: str):
        """Find and replace in the input string.

        :param string: The input string where matches are to be found and replaced (using the defined replacer).
        :return: The transformed input string, after replacing all matches.
        """
        matches = self.find(string)
        return self.apply_replace(matches, string)

    def is_whole_word(self, string: str, from_ix: int, to_ix: int):
        """Checks whether the substring from from_ix to to_ix in string represents a whole word.
        A whole word is defined a substring bordered by either string boundary (beginning or end of string) or a
        non-alphanumeric character.

        :param string: Entire string, in which to test the substring.
        :param from_ix: The start index of the substring
        :param to_ix: The end index of the substring
        :return: True if the substring is a whole word, False otherwise.
        """
        before_ix = from_ix - 1
        if before_ix >= 0 and string[before_ix].isalnum():
            return False
        after_ix = to_ix  # to_index is not inclusive
        if after_ix < len(string) and string[after_ix].isalnum():
            return False
        return True

    def find(self, string: str):
        """Find and return matches in the input string, according to the matching mode defined.

        :param string: Input string where matches are to be found.
        :return: A list of matches, according to the match mode defined.
        """
        matches = []
        current_trie = self.root_trie
        current_index = 0
        for token in self.split(string):
            current_trie = current_trie.next(token)
            for match in current_trie.matches:
                end_index = current_index + len(token)
                start_index = end_index - len(match.string)
                if not self.whole_words_only:
                    matches.append(Match(start_index, end_index, match.length, match.string))
                elif self.is_whole_word(string, start_index, end_index):
                    matches.append(Match(start_index, end_index, match.length, match.string))
            current_index += len(token) + len(self.separator)
        return self.match_mode.value(matches)

    def apply_replace(self, matches: List[Match], string: str):
        """Use a list of matches to transform the input string, using the defined replacer.

        :param matches: A list of matched patterns.
        :param string: The input string where matches are to be replaced.
        :return: The transformed input string.
        """
        parts = []
        previous_end = 0
        for match in matches:
            start_ix = match.start_ix
            end_ix = match.end_ix
            local_match = match.string
            replacement = self.__replace(local_match)
            previous_without_separator = string[previous_end:max(0, start_ix - len(self.separator))]
            parts.extend([previous_without_separator, replacement])
            previous_end = end_ix + len(self.separator)
        parts.append(string[previous_end:])
        return self.separator.join(p for p in parts if p)

    def count(self, string: str, count_dict=None):
        """Find and count matches in the input string.

        :param string: The input string where matches are to be found and counted.
        :param count_dict: The dictionary where the counts will be stored. If count_dict is None,
        a new Python dict will be created.
        :return: The count_dict. If count_dict is not None, it will be updated and returned.
        """
        if count_dict is None:
            count_dict = {}
        matches = self.find(string)
        for match in matches:
            text = match.string
            if text not in count_dict:
                count_dict[text] = 0
            count_dict[text] += 1
        return count_dict

from typing import Callable, Iterable, List

from multimatcher.match import Match
from queue import Queue


class Trie:
    """
        A Trie that stores the search patterns and the transitions.
    """

    def __init__(self, root=False):
        self.root = root
        self.transitions = {}
        self.failure = None
        self.matches = []

    def __add(self, token: str):
        """Add the input token to the trie.

        :param token: Input token to be added to the trie.
        :return: The sub-trie of the token.
        """
        if token not in self.transitions:
            self.transitions[token] = Trie()
        return self.transitions[token]

    def add(self, pattern: str, splitter: Callable[[str], Iterable[str]]):
        """Add a pattern to the trie.

        :param pattern: The pattern to be added to the trie.
        :param splitter: A function that tokenizes the input pattern.
        :return: None
        """
        current = self
        for token in splitter(pattern):
            current = current.__add(token)
        current.matches.append(Match(string=pattern, length=len(pattern)))

    def next(self, token: str):
        """Returns the sub-trie reached after the token was accepted.
        If the token couldn't be accepted by any sub-trie, returns the root trie.

        :param token: Input token.
        :return: A sub-trie reached after the token was accepted,
        or the root trie if the token couldn't be accepted.
        """
        current_trie = self
        new_trie = current_trie.transitions.get(token)
        while new_trie is None and not current_trie.root:
            current_trie = current_trie.failure
            new_trie = current_trie.transitions.get(token)
        if new_trie is None:
            new_trie = current_trie
        return new_trie

    def build(self):
        """ Build failure tries using breadth-first search (BDS).
        A failure trie can be thought of as the longest sub-trie that starts at the root and ends at the current node.

        For more details, check the original Aho & Corasick paper:
        Aho, A. V., & Corasick, M. J. (1975). Efficient string matching: an aid to bibliographic search.
        Communications of the ACM, 18(6), 333-340.

        :return: None
        """
        if self.root:
            root = self
            queue = Queue()
            queue.put(root)
            allow_root = False
            while not queue.empty():
                current = queue.get()
                if current.failure is None:
                    current.failure = root
                for t in current.transitions:
                    next_transition = current.transitions.get(t)
                    next_failure = current.failure.next(t)
                    if next_failure is not None and allow_root:
                        next_transition.failure = next_failure
                        next_transition.matches.extend(next_failure.matches)
                    queue.put(next_transition)
                allow_root = True

    @staticmethod
    def create(patterns: Iterable[str], splitter: Callable[[str], List[str]]):
        """Create and return a Trie.

        :param patterns: Search patterns that will be stored in the trie.
        :param splitter: A function that tokenizes each of the patterns.
        :return: A trie that represents the input patterns.
        """
        trie = Trie(True)
        for pattern in patterns:
            trie.add(pattern, splitter)
        trie.build()
        return trie

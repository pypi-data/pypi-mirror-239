from typing import Dict, Callable


class Replacer:
    """
        An abstract class to implement different replacement behaviors.
    """

    def replace(self, string: str):
        raise NotImplemented("This method is not implemented for this class.")


class SimpleReplacer(Replacer):
    """
        An object that replaces all matches with the same replacement text.
    """

    def __init__(self, replacement_string: str):
        super().__init__()
        self.replacement = replacement_string

    def replace(self, string: str):
        """
            Replace the input string with the replacement text.
        :param string: Input string.
        :return: The replacement text defined in the object.
        """
        return self.replacement


class MapReplacer(Replacer):
    """
        An object that uses a map to associate matches with their replacement text.
    """

    def __init__(self, replacement_map: Dict[str, str]):
        super().__init__()
        self.replacement_map = replacement_map

    def replace(self, string: str):
        """
            Replace the input string using the replacement map. Return the input string
            if it's not defined in the replacement map.
        :param string: The input string.
        :return: The corresponding replacement text if defined in the replacement map;
        the input string otherwise.
        """
        return self.replacement_map.get(string, string)


class TransformerReplacer(Replacer):
    """
        An object that transforms the matches using a function. The function must take only one parameter
        as input, which must be a string; it must return only one value, which must also be a string.
    """

    def __init__(self, transforming_method: Callable[[str], str]):
        super().__init__()
        self.transformer = transforming_method

    def replace(self, string: str):
        """
            Apply the defined function on the input string, and return the result.
        :param string: The input string.
        :return: The transformed string.
        """
        return self.transformer(string)

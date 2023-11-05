class Match:
    """
        A simple object that represents a matched pattern.
    """

    def __init__(self, start_ix=-1, end_ix=-1, length=-1, string=None):
        self.start_ix = start_ix
        self.end_ix = end_ix
        self.length = length
        self.string = string

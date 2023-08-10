class SalaryNotInRangeError(Exception):
    """Exception raised when multiple rows have the same tag_set in TagSetMapping table"""

    def __init__(self, tag_set, occurence):
        self.tag_set = tag_set
        self.occurence = occurence
        self.message = f"tags set: {tag_set} have {occurence} occurences"
        super().__init__(self.message)

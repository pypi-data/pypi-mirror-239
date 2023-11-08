
class SampleClass():
    """
    Some summary with link https://www.microsoft.com
    """
    def dummy_param(self):
        """
        This is a content issue link [microsoft](https://www.microsoft.com)
        We should not generate nested parenthesis causing docs validation warnings
        """
        pass

    pass
    
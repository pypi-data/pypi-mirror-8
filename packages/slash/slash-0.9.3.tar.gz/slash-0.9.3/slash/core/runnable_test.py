class RunnableTest(object):

    """
    This class is meant to serve as a base class to any test that can
    actually be executed by the Slash runner.
    """
    __slash__ = None

    def run(self):
        """
        This method is meant to be overriden by derived classes to actually
        perform the test logic
        """
        raise NotImplementedError()  # pragma: no cover

    def __repr__(self):
        return repr(self.__slash__)

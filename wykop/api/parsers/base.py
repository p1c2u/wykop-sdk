class BaseParser(object):

    def __init__(self, exception_resolver):
        self.exception_resolver = exception_resolver

    def _resolve_exception(self, code, message, default_class):
        return self.exception_resolver.resolve(code, message, default_class)

    def parse(self, data):
        raise NotImplementedError(
            "%s: `parse` method must be implemented" %
            self.__class__.__name__)

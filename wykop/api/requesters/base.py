class BaseRequester(object):

    def make_request(self, url, data=None, headers=None, files=None):
        raise NotImplementedError(
            "%s: `make_request` method must be implemented" %
            self.__class__.__name__)

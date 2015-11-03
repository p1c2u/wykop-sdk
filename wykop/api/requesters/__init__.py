# try requests module
try:
    import requests

    from wykop.api.requesters.requests import RequestsRequester as Requester
except ImportError:
    from wykop.api.requesters.urllib import UrllibRequester as Requester

default_requester = Requester()

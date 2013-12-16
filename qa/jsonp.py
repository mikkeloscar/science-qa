import json
from django.http import HttpResponse

class JsonpResponse(HttpResponse):
    """
    Implements jsonp HTTP response
    """
    def __init__(self, data, callback):
        _json = json.dumps(data)
        jsonp = "%s(%s)" % (callback, _json)
        HttpResponse.__init__(
            self, jsonp,
            content_type='application/json'
        )

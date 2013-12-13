from django.core.paginator import Paginator, Page

class PageFilter(Paginator):

    def __init__(self, get_request, *args, **kwargs):
        super(PageFilter, self).__init__(*args, **kwargs)
        self.get_request = get_request

    def _get_page(self, *args, **kwargs):
        return Filter(self.get_request, *args, **kwargs)


class Filter(Page):
    def __init__(self, get_request, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)
        self.get_request = get_request

    def page_link(self):
        return self._query_string(['p']) + "p="

    def _query_string(self, keys=[]):
        """
        Create a querystring from get_request
        """
        queries = []
        for key, val in self.get_request.iteritems():
            if key not in keys:
                query = key + '=' + val
                queries.append(query)
        queries = '&'.join(queries)
        if len(queries) > 0:
            queries = '?' + queries + '&'
        else:
            queries = '?'
        return queries

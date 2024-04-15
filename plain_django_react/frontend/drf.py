from rest_framework import pagination, response
from rest_framework.filters import BaseFilterBackend as DRFBaseFilterBackend
import json

class ContentRangeHeaderPagination(pagination.BasePagination):
    """
    A custom Pagination class to send Content-Range header in the
    response and paginate the qs by this querystring '?range=[0, 9]'
    """
    range_query_param = 'range'  # ra-data-simple-rest Data Provider

    def paginate_queryset(self, queryset, request, view=None):
        self.count = len(queryset) if type(queryset) is list else queryset.count()
        range_param = request.query_params.get(self.range_query_param, f'[0, {self.count}]')
        range_list = json.loads(range_param)

        self.from_page = int(range_list[0])
        self.to_page = int(range_list[1])
        return list(queryset[self.from_page:self.to_page+1])

    def get_paginated_response(self, data):
        content_range = f'items {self.from_page}-{self.to_page}/{self.count}'
        headers = {'Content-Range': content_range}
        return response.Response(data, headers=headers)
    
class BaseFilterBackend(DRFBaseFilterBackend):
    """
    A custom Filter Class to filter queryset's by react-admin.
    ra sorts resources by this querystring '?filter={<field_name>: <value>}'
    In order to implement custom filters add 'exclude_filters' to the View as a list.
    """
    filtering_param = 'filter'
    exclude_filters = []

    def filter_queryset(self, request, queryset, view):
        params = request.query_params.get(self.filtering_param, None)
        if params:
            filter_json = json.loads(params)
            queryset = queryset.filter(**filter_json)

        return queryset.distinct()

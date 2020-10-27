from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        custom_paginator = {
            "count":        self.page.paginator.count,
            "total_pages":  self.page.paginator.num_pages,
            "per_page":     int(self.request.GET.get('per_page', self.page_size)),
            "current_page": int(self.request.GET.get('page', DEFAULT_PAGE)),
            "results":      data
        }
        return Response(custom_paginator)

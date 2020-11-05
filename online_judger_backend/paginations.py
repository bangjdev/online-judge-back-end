from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    def __init__(self, page_size, page_size_query_param, page_query_param):
        self.page_size = page_size
        self.page_size_query_param = page_size_query_param
        self.page_query_param = page_query_param

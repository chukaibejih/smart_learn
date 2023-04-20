from rest_framework.pagination import PageNumberPagination 

class CustomPagination(PageNumberPagination):
    page_size = 8
    page_query_param = "record"
    page_size_query_param = "records per page"
    max_page_size = 15
    
    
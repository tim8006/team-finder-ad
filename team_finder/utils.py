from django.core.paginator import Paginator

PAGINATION_PAGE_SIZE = 12


def get_query_prefix(request):
    params = request.GET.copy()
    params.pop("page", None)
    query_string = params.urlencode()
    return f"{query_string}&" if query_string else ""


def paginate_queryset(queryset, request, page_size=PAGINATION_PAGE_SIZE, page_query_param="page"):
    paginator = Paginator(queryset, page_size)
    return paginator.get_page(request.GET.get(page_query_param))

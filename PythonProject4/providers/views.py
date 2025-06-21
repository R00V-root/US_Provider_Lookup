from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import ProviderSearchForm
from .models import Provider
from .filters import ProviderFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import ProviderSerializer

class ProviderSearchFormView(FormView):
    form_class = ProviderSearchForm
    template_name = 'providers/search.html'
    success_url = reverse_lazy('provider-search')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            provider_filter = ProviderFilter(self.request.GET, queryset=Provider.objects.select_related('taxonomy').all())
            paginator = Paginator(provider_filter.qs, 50)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context.update({
                'filter': provider_filter,
                'page_obj': page_obj,
                'paginator': paginator,
            })
        return context

class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'providers/detail.html'
    context_object_name = 'provider'

class ProviderPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500

class ProviderSearchView(ListAPIView):
    serializer_class = ProviderSerializer
    pagination_class = ProviderPagination
    filterset_class = ProviderFilter

    def get_queryset(self):
        return Provider.objects.select_related('taxonomy').all()

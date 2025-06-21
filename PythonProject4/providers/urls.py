from django.urls import path
from .views import ProviderSearchFormView, ProviderSearchView, ProviderDetailView

urlpatterns = [
    path('', ProviderSearchFormView.as_view(), name='provider-search'),
    path('provider/<int:pk>/', ProviderDetailView.as_view(), name='provider-detail'),
    path('api/search/', ProviderSearchView.as_view(), name='provider-search-api'),
]

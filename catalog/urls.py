from django.urls import path, re_path
from django.conf.urls import include, url
from catalog import views

from .views import ContractView

urlpatterns = [
    path('rest_contract/',  views.ContractView.as_view()),
    path('rest_client/', views.client),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main, name='main'),
    # url(r'^book/(?P<pk>\d+)$', views.list_contract_names.as_view(), name='book-detail'),
]

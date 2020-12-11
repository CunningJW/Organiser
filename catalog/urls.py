from django.urls import path, re_path
from django.conf.urls import include
from catalog import views


urlpatterns = [
    path('rest_contract/',  views.list_contract_names),
    re_path('rest_contract/(?P<contractName>\w+)/$', views.contract_details),
    path('rest_client/', views.client),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    # path('', views.index, name='index'),
    # path('catalog/', include('catalog.urls'))
]

# urlpatterns = [
#
# ]
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
#
# urlpatterns += [
#     path('catalog/', include('catalog.urls')),
# ]

from django.urls import path, re_path
from django.conf.urls import include
from catalog import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('rest_contract/',  views.ContractView.as_view()),
    # path('rest_task/',  views.list_task),
    # re_path('rest_contract/(?P<contractName>\w+)/$', views.contract_details),
    path('rest_client/', views.client),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main, name='main'),
    # path('', views.index, name='index'),
    # path('catalog/', include('catalog.urls'))
]
urlpatterns += staticfiles_urlpatterns()  
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

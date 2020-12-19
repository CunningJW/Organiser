from django.urls import path, re_path
from django.conf.urls import include
from catalog import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('rest_contract/',  views.ContractView.as_view()),
    re_path('rest_contract/(?P<code>\w+)/$', views.ContractDetailView.as_view()),
    path('rest_tasks/',  views.TaskView.as_view()),
    re_path('rest_tasks/(?P<code>\w+)/$', views.TaskDetailView.as_view()),
    re_path('rest_tasks/currentuser', views.TaskUserFilteringView.as_view()),
    path('rest_user/', views.UserView.as_view()),
    # path('rest_task/',  views.list_task),
    # re_path('rest_contract/(?P<contractName>\w+)/$', views.contract_details),
    path('all_contracts/', views.contractlink, name = 'allContracts'),
    path('all_tasks/', views.tasklink, name = 'allTasks'),
    re_path('all_contracts/(?P<pk>\w+)/$', views.contractDetailLink, name = 'contractDetail'),
    path('task_add/', views.taskaddlink, name = 'addTask'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main, name='main'),
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
urlpatterns += staticfiles_urlpatterns()

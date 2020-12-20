from django.urls import path, re_path
from django.conf.urls import include
from catalog import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('all_contracts/',  views.ContractView.as_view(), name = 'allContracts'),
    path('my_tasks/',  views.TaskUserFilteringView.as_view(), name = 'myTasks'),
    path('add_task/', views.TaskAddNew.as_view(), name = 'addTask'),

    re_path('rest_contract/(?P<code>\w+)/$', views.ContractDetailView.as_view()),
    re_path('rest_contract/currentuser', views.ContractFilteringView.as_view()),

    re_path('rest_tasks/(?P<code>\w+)/$', views.TaskDetailView.as_view()),
    re_path('rest_tasks/currentuser', views.TaskUserFilteringView.as_view()),
    # path('rest_user/', views.UserView.as_view()),
    # path('rest_currentuser/', views.CurrentUserView.as_view()),


    re_path('all_contracts/(?P<pk>\w+)/$', views.contractDetailLink, name = 'contractDetail'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main, name='main'),

]

urlpatterns += staticfiles_urlpatterns()

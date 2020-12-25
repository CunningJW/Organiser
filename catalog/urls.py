from django.urls import path, re_path
from django.conf.urls import include
from catalog import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('all_contracts/',  views.ContractView.as_view(), name = 'allContracts'),
    path('my_tasks/',  views.TaskUserFilteringView.as_view(), name = 'myTasks'),
    path('add_task/', views.TaskAddNew.as_view(), name = 'addTask'),
    path('add_document/', views.DocumentView.as_view(), name = 'addDocument'),
    re_path('all_contracts/(?P<pk>\w+)/$', views.ContractDetailView.as_view(), name = 'contractDetail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.main, name='main'),
    path('Proba/', views.Proba, name = 'Proba'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_DIRS)
urlpatterns += staticfiles_urlpatterns()

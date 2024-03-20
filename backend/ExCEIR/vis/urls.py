from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('test', views.getData, name='test'),
    path('api-auth/', include('rest_framework.urls'), name='api'),
    path('', views.index, name='index'),
    path('queries', views.queries, name='queries'),
    path('systems', views.systems, name='systems'),
	#ex: vis/1/
	path('<int:ee>/', views.ee_detail, name='ee_detail'),
	#ex: vis/1/1
	# path('<int:ee>/<int:system_id>/', views.system_detail, name='system_detail'),
	# path('<int:system_id>/', views.system_detail, name='system_detail'),
]
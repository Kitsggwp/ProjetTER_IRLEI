from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('eval', views.EvalViewSet, basename='eval')
router.register('team', views.TeamViewSet, basename='team')
router.register('user', views.CustomUserCreateView, basename='user')

urlpatterns = [
    # path('', views.index, name='index'),
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('api/', include(router.urls)),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
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
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name='home_page'),
    re_path('profile/(?P<username>\w+)', views.profile, name='profile'),
    path('upload/', views.upload_project, name='upload_project'),
    path('search/', views.search_results, name='search_results'),
    path('edit', views.edit, name='edit_profile'),
    re_path('rate/(?P<project_id>\d+)', views.rate_project, name='rate'),
    re_path('vote/(?P<project_id>\d+)', views.vote, name='vote'),
    path('api/profile/', views.ProfileList.as_view()),
    path('logout/', views.logout_view, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.urls import path

from django.conf import settings
from . import views
from .views import SearchResultsView, HomePageView, dev_password_page
from django.conf.urls.static import static

from django.urls import path


app_name = 'ads'

urlpatterns = [
    path('dev-auth/', dev_password_page, name='dev_password_page'),
    path('', views.add_ad, name='add_ad'),
    path('ad_list/', views.ad_list, name='ad_list'),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
    path('search/', HomePageView.as_view(), name='search'),
    path('edit/<int:pk>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:pk>/', views.delete_ad, name='delete_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('create_proposal', views.create_proposal, name='create_proposal'),
    path('add_proposal', views.add_proposal, name='add_proposal'),
    path('profile/', views.logout_view, name='logout_view'),
    path('edit_exc/<int:pk>/', views.edit_exc, name='edit_exc'),
    path("signup/viewer/", views.signup_viewer, name="signup_viewer"),
    path("signup/streamer/", views.signup_streamer, name="signup_streamer"),
    # path('upload/', views.upload_video, name='upload_video'),
    # path('videos/', views.video_list, name='video_list'),
    path('go-live/', views.go_live, name='go_live'),          # страница запуска камеры (только для залогиненных)
    path('watch/<int:user_id>/', views.watch_stream, name='watch_stream'),  # страница просмотра стрима конкретного пользователя
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.RegistrationAPIView.as_view()),
    path('job/', views.AnnouncementView.as_view()),
    path('jobcreate/', views.AnnouncementViewCreate.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('favorite-vacancies/', views.get_favorite_vacancies, name='get_favorite_vacancies'),
    path('manage-favorite-vacancy/', views.manage_favorite_vacancy, name='manage_favorite_vacancy'),


]

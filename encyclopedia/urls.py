# encyclopedia/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("history/<str:title>", views.history, name="history"),
    
    # AI Image URLs
    path("ai-image/", views.generate_ai_image, name="generate_ai_image"),
    path("ai-image/process/", views.generate_ai_image_process, name="generate_ai_image_process"),
    path("ai-image/result/", views.ai_image_result, name="ai_image_result"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name = 'admin'),
    path('posts/', views.posts, name="admin.posts"),
    path('posts/create/', views.post_create, name="admin.posts.create"),
    path('posts/edit/<int:id>/', views.post_edit, name="admin.posts.edit"),
    path('posts/delete/<int:id>/', views.post_delete, name="admin.posts.delete"),
    path('posts/show/<int:id>/', views.post_show, name="admin.posts.show"),
    path('posts/show/<int:id>/attach-gallery/', views.attach_to_post, name="attach_to_post"),
    path('posts/moderated/<int:id>/', views.post_moderated, name="admin.posts.moderated"),
    # Categories
    path('categories/', views.categories, name="admin.categories"),
    path('categories/create/', views.category_create, name="admin.categories.create"),
    path('categories/edit/<int:id>/', views.category_edit, name="admin.categories.edit"),
    path('categories/delete/<int:id>/', views.category_delete, name="admin.categories.delete"),
    # Users
    path('users/', views.users, name="admin.users"),
    path('users/create/', views.user_create, name="admin.users.create"),
    path('users/edit/<int:id>/', views.user_edit, name="admin.users.edit"),
    path('users/delete/<int:id>/', views.user_delete, name="admin.users.delete"),
    path('users/show/<int:id>/', views.user_show, name="admin.users.show"),
    # Regions
    path('regions/', views.regions, name="admin.regions"),
    path('regions/create/', views.region_create, name="admin.regions.create"),
    path('regions/edit/<int:id>/', views.region_edit, name="admin.regions.edit"),
    path('regions/delete/<int:id>/', views.region_delete, name="admin.regions.delete"),
    # Galleries
    path('galleries/', views.galleries, name="admin.galleries.index"),
    path('galleries/create/', views.gallery_create, name="admin.galleries.create"),
    path('galleries/delete/', views.gallery_delete, name="admin.galleries.delete"),
]

from  django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name = 'index'),
    # <--- | Posts | ---> #
    path('posts', views.allpost , name = 'allpost'),
    path('posts/<slug:slug>/', views.post_detail , name = 'post_detail_url'),
    path('posts/<slug:slug>/show-phone/', views.show_phone , name = 'show_phone'),
    path('profile/post_create/', views.post_create , name = 'post_create'),
    path('profile/post_edit/<int:id>/', views.post_edit , name = 'post_edit'),
    path('profile/post_delete/<int:id>/', views.post_delete , name = 'post_delete'),
    # <--- | Profile | ---> #
    path('profile/', views.profile , name = 'profile'),   
    path('profile/posts/', views.profile_posts , name = 'profile_posts'),
    path('profile/posts/archieved/', views.profile_archieved_posts , name = 'profile_archieved'),
    path('profile/posts/moderating/', views.profile_moderating_posts , name = 'profile_moderating'),
    path('profile/posts/gallery/<int:id>/', views.profile_post_gallery, name="profile_post_gallery"),
    path('profile/posts/gallery-create/<int:id>/', views.gallery_create, name="gallery_create"),
    path('profile/posts/gallery-delete/', views.gallery_delete, name="gallery_delete"),
    # <--- | Filters | ---> #, 
    path('filter/', views.filter , name = 'filter'),
    path('search/', views.search , name = 'search'),
    path('category/<slug:slug>/', views.category_detail , name = 'category_detail_url'),
    path('region/<slug:slug>/', views.region_detail , name = 'region_detail_url'),
    # <--- | Chats | ---> #
    path('profile/send-chat/user=<int:user_id>/product=<int:post_id>/', views.send_chat, name="send_chat"),
    path('profile/chats/', views.chats, name="chats"),
    path('profile/chats/<int:chat_id>/', views.chat_detail, name="chat_detail_url"),
    path('profile/chats/send/<int:chat_id>/message/', views.send_message , name='send_message'),
    path('profile/chats/delete/<int:chat_id>/', views.delete_chat_detail , name='delete_chat_detail_url'),
    # <--- | Favourite | ---> #
    path('profile/favourite/' , views.favourite , name = 'favourite'),
    path('profile/favourite/add/<int:post_id>/', views.add_to_favourite , name= 'add_to_favourite'),
    path('profile/favourite/detele/<int:item_id>/', views.delete_favourite , name= 'delete_favourite'),
    # <--- | Regisration | ---> #
    path('register/' , views.register , name = 'register'),
    path('login/' , views.login , name = 'login'),
    path('logout/' , views.logout , name = 'logout'),
    
]

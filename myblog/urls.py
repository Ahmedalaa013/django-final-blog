from django.urls import path
from myblog.admin import blog_site
from . import views
from .views import HomeView,Post_detailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('manage/', blog_site.urls),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('post/<int:pk>',Post_detailView.as_view(),name='post_details'),
    path('subscribe/<int:pk>', views.subscribe, name='cat_sub'),
    path('subscribe/', views.subscriptionPostView, name='sub_list'),
    path('like/<int:pk>', views.like, name='post_like'),
    path('dislike/<int:pk>', views.dislike,name='post_dislike'),
    path('comment/<int:pk>', views.comment,name='post_comment'),
    path("cats/<int:id>", views.get_category, name='category_details'),
    path("tags/<int:id>", views.get_tag, name='tag_details'),
    path("search/", views.search, name='search'),
]
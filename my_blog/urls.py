from django.urls import path
from my_blog import views

app_name = 'my_blog'  # App_Blog
urlpatterns = [
    path('', views.BlogList.as_view(), name='blog_list'),
    path('home/', views.home_page, name='home'),
    path('create-blog/', views.CreateBlog.as_view(), name='create_blog'),
    path('blog-details/<slug:slug>', views.blog_details, name='blog_details'),
    path('my-blogs/', views.MyBlogs.as_view(), name='my_blogs'),
    path('liked/<pk>/', views.liked, name='liked-post'),
    path('un-liked/<pk>/', views.unliked, name='unliked-post'),
    path('edit-blog/<pk>/', views.UpdateBlog.as_view(), name='edit_blog'),
    path('author-blogs/<str:username>/', views.author_blogs, name='author_blogs'),

]

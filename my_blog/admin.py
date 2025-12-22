from django.contrib import admin
from my_blog.models import Blog, Blog_comment, Likes

# Register your models here.
admin.site.register(Blog)
admin.site.register(Blog_comment)
admin.site.register(Likes)

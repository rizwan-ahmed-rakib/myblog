import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DetailView, DeleteView

from my_blog.forms import CommentForm
from my_blog.models import Blog, Likes
from django.contrib.auth.models import User
from login_app.models import UserProfile


# Create your views here.
def blog_list(request):
    return render(request, 'My_blog/blog_list.html', context={})


def home_page(request):
    return render(request, 'My_blog/home.html', context={})


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'My_blog/create_blog.html'
    fields = {'blog_title', 'blog_image', 'blog_content', }

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'My_blog/blog_list.html'


#  queryset = Blog.objects.order_by('-publish_date')

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('my_blog:blog_details', kwargs={'slug': slug}))

    return render(request, 'My_blog/blog_details.html',
                  context={'blog': blog, 'comment_form': comment_form, 'liked': liked, })


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('my_blog:blog_details', kwargs={'slug': blog.slug}))


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('my_blog:blog_details', kwargs={'slug': blog.slug}))


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'My_blog/my_blogs.html'


class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'My_blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def get_success_url(self, **kwargs):
        return reverse_lazy('my_blog:blog_details', kwargs={'slug': self.object.slug})

def author_blogs(request, username):
    author = User.objects.get(username=username)
    blogs = Blog.objects.filter(author=author).order_by('-publish_date')
    
    try:
        author_profile = UserProfile.objects.get(user=author)
    except UserProfile.DoesNotExist:
        author_profile = None
        
    context = {
        'author': author,
        'blogs': blogs,
        'author_profile': author_profile,
    }
    return render(request, 'My_blog/author_blogs.html', context)
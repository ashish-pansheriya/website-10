from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import blogbank
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    users = {
        'post': blogbank.objects.all()
    }

    return render(request, 'home.html', users)


# check for logged user to update their profile and to see all their profile post
class blogListView(ListView):
    model = blogbank
    template_name = 'blogs/blog_home.html'
    context_object_name = 'post' #it takes object in post for
    ordering = ['-date_posted']

BLOG_POST_PER_PAGE = 12
class blogsearchview(View):

    def get(self, request, *args, **kwargs):
        queryset=blogbank.objects.all().order_by('-date_posted')
        query = request.GET.get('q')
        if query:
            queryset=queryset.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query)
            ).distinct()

        page = request.GET.get('page', 1)
        blog_posts_paginator = Paginator(queryset, BLOG_POST_PER_PAGE)
        try:
            queryset = blog_posts_paginator.page(page)
        except PageNotAnInteger:
            queryset = blog_posts_paginator.page(BLOG_POST_PER_PAGE)
        except EmptyPage:
            queryset = blog_posts_paginator.page(blog_posts_paginator.num_pages)

        context = {
            'queryset':queryset
        }
        return render(request, 'cashtreats/home.html', context)

class blogDetailView(DetailView):
    model = blogbank
    template_name = 'blogs/blog_detail.html'


class blogCreateView(LoginRequiredMixin, CreateView ):
    model = blogbank
    fields = ['title', 'category', 'content', 'photo', 'name', 'location','email', ]
    template_name = 'blogs/blog_form.html'

    def form_valid(self, form):
 #       ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)

        form.instance.author = self.request.user #login must be required to run function with author
        return super().form_valid(form)




class blogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView ): # prevent from unauthorised update
    model = blogbank
    fields = ['title', 'category', 'content', 'photo', 'name', 'location','email', ]
    template_name = 'blogs/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user #login must be required to run function with author
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class blogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView ): # prevent from unauthorised update
    model = blogbank
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

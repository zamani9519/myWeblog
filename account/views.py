from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , CreateView
from blog.models import Article


class ArticleList(LoginRequiredMixin,ListView):
#     queryset = Article.objects.all()
    template_name = "registration/home.html"
    def get_queryset(self):
        if self.request.user.is_superuser:
             return Article.objects.all()
        else:
             return Article.objects.filter(author = self.request.user)
        pass

class ArticleCreate(LoginRequiredMixin,CreateView):
    model = Article
    fields = ["author","title","slug","category","description","thumbnail","publish","status"]
    template_name = "registration/article-create-update.html"




















# @login_required
# def home(request):
#     return render(request,'registration/home.html')

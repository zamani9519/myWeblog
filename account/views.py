from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FieldMixin,FormValidMixin,AuthorAccessMixin,SuperUserAccessMixin
from django.views.generic import ListView , CreateView,UpdateView,DeleteView
from blog.models import Article
from django.contrib.auth import logout
from .models import User



class ArticleList(LoginRequiredMixin,ListView):
#     queryset = Article.objects.all()
    template_name = "registration/home.html"
    def get_queryset(self):
        if self.request.user.is_superuser:
             return Article.objects.all()
        else:
             return Article.objects.filter(author = self.request.user)
        pass

class ArticleCreate(LoginRequiredMixin,FormValidMixin,FieldMixin,CreateView):
    model = Article
#     fields = ["author","title","slug","category","description","thumbnail","publish","status"]
    template_name = "registration/article-create-update.html"

class ArticleUpdate(AuthorAccessMixin,FormValidMixin,FieldMixin,UpdateView):
    model = Article
#     fields = ["author","title","slug","category","description","thumbnail","publish","status"]
    template_name = "registration/article-create-update.html"

class ArticleDelete(SuperUserAccessMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    template_name= "registration/article_confirm_delete.html"

class Profile(UpdateView):
    model = User
    fields = ['username','email','first_name','last_name','special_user','is_author']
    template_name = "registration/profile.html"
    success_url = reverse_lazy("profile")
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
















# @login_required
# def home(request):
#     return render(request,'registration/home.html')

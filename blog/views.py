from django.shortcuts import render, get_object_or_404
from account.models import User
from django.views.generic.list import ListView
from .models import Article, Category
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from account.mixins import AuthorAccessMixin

# from django.http import JsonResponse

# *************************************************************
class ArticleList(ListView):
    template_name = "blog/list.html"
    queryset = Article.objects.published()
    paginate_by = 6
#     context_object_name = "articles"
    # model = Article


# *************************************************************
class ArticleDetail(DetailView):
    template_name = "blog/detail.html"

    def get_object(self):
        slug = self.kwargs.get('slug')
        article= get_object_or_404(Article, slug=slug, status='p')

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article

# *************************************************************
class CategoryList(ListView):
    template_name = "blog/category_list.html"
    paginate_by = 2

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
# *************************************************************
class AuthorList(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
# *************************************************************
class ArticlePreview(AuthorAccessMixin,DetailView):
    template_name = "blog/detail.html"
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)
# *************************************************************

# def home(request, page=1):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 6)
#     # page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         "articles": articles,
#     }
#     return render(request, "blog/home.html", context)
# Article.objects.published(),
# filter(status='p').order_by('-publish')[2:]
# اگر بخواهیم 2 تای اخر را نمایش بدهد ازین استفاده میکنیم [2:]
# اگر این فیلتر را بزاریم بهش دستور داده ایم که اگر فقط publish بود تمایش بده /این قطعه کد برای نمایش محتویات داخل models در viewsهست
# "category":Category.objects.filter(status=True)

# *************************************************************
# def detail(request,
#            slug):  # تابعی تشکیل دادم که 2 متغییر بگیره بعد این 2 تا ساگو بگیره بعدش بیارتشون تو این آدرسی که پااین نوشتم
#     context = {
#         "article": get_object_or_404(Article, slug=slug,
#                                      status='p')}  # اسلاگ سمت چپی برای مدل است و اسلاگ راستی برای ویو جدیده
#     return render(request, "blog/detail.html", context)
# def api(request):
#         data = {
#             "1":{
#             "tatle": "سلام عزیزم",
#              "author": "محمد زمانی ",
#              "age": 30
#              },
#             "2":{
#                 "tatle": "سلام عزیزم",
#                  "author": "محمد زمانی ",
#                  "age": 30
#             },
#             "3":{
#             "tatle": "سلام عزیزم",
#              "author": "محمد زمانی ",
#              "age": 30
#         },
#         }
#         return JsonResponse(data)

# noinspection PyUnboundLocalVariable
# این دسته کد برای اینه که بتونیم برای کتگوری ها هم پیج نیشن بزاریم
# *************************************************************
# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 2)
#     articles = paginator.get_page(page)
#     context = {
#         "category": category,
#         "articles": articles
#     }
#     # بااین کد میخواهیم وقتی اسلاگ کتگوری را فراخوان میکنیم برای مان همان محتوا را بیاورد
#     return render(request, "blog/category.html", context)
# *************************************************************

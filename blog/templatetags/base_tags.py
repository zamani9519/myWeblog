from ..models import Article, Category
from django.db.models import Count ,Q
from datetime import datetime,timedelta


# اینجا تگ ها را قرار میدیم

from django import template
from ..models import Category
register = template.Library()

@register.simple_tag
def title():
    return "وبلاگ خبری ایران و جهان"

@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return{
        "category":Category.objects.filter(status=True)
    }

@register.inclusion_tag("blog/partials/popular_articles.html")
def popular_articles():
    last_month = datetime.today() - timedelta(days=30)
    return{
        "popular_articles":Article.objects.published().annotate(
            count=Count('hits',filter=Q(articlehit__created__gt = last_month))
        ).order_by('-count','-publish')[:5]
    }
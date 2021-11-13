from django.contrib import admin
from .models import Article, Category
from django.utils.translation import ngettext
from django.contrib import messages

admin.site.disable_action = 'حذف مقالات '


def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله با موفقیت منتشر شد. ',
        '%d مقاله با موفقیت منشتر شدند. ',
        updated,
    ) % updated, messages.SUCCESS)


make_published.short_description = "انتشار مقالات انتخاب شده "


def make_daft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله با موفقیت پیش نویس شد. ',
        '%d مقاله با موفقیت پیش نویس شدند. ',
        updated,
    ) % updated, messages.SUCCESS)


make_daft.short_description = "پیش نویس شدن مقالات انتخاب شده "


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'status', 'parent')  # آوردن منو
    list_filter = (['status'])  # گذاشتن سرچ
    search_fields = ('title', 'slug')  # گذاشتن فیلتر
    prepopulated_fields = {
        'slug': ('title',)}  # اگر بخواهیم که هرچه در title خودمان مینویسیم در slug ماهم بیاید باید ازین استفاده کنیم
    ordering = ['position']  # اگر بخواهیم نزولی مرتب کند باید قبل آن یک - بگذاریم


admin.site.register(Category, CategoryAdmin)


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'thumbnail_tag', 'slug', 'author', 'description', 'jpublish','is_special' ,'status', 'category_to_str')  # آوردن منو
    list_filter = ('publish', 'status','author')  # گذاشتن سرچ
    search_fields = ('title', 'description')  # گذاشتن فیلتر
    prepopulated_fields = {
        'slug': ('title',)}  # اگر بخواهیم که هرچه در title خودمان مینویسیم در slug ماهم بیاید باید ازین استفاده کنیم
    ordering = ['-publish']  # اگر بخواهیم نزولی مرتب کند باید قبل آن یک - بگذاریم
    actions = [make_published, make_daft]

admin.site.register(Article, ArticleAdmin)

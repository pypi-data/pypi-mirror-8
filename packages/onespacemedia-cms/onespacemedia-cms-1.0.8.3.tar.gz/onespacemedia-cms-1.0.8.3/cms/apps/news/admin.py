"""Admin settings for the CMS news app."""

from django.contrib import admin

from cms import externals
from cms.admin import PageBaseAdmin
from cms.apps.news.models import Category, Article


class CategoryAdmin(PageBaseAdmin):

    """Admin settings for the Category model."""

    fieldsets = (
        PageBaseAdmin.TITLE_FIELDS,
        ("Content", {
            "fields": ("content_primary",),
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
    )


admin.site.register(Category, CategoryAdmin)


class ArticleAdminBase(PageBaseAdmin):

    """Admin settings for the Article model."""

    date_hierarchy = "date"

    search_fields = PageBaseAdmin.search_fields + ("content", "summary",)

    list_display = ("title", "date", "is_online",)

    list_filter = ("is_online", "categories",)

    fieldsets = (
        (None, {
            "fields": ("title", "url_title", "news_feed", "date",),
        }),
        ("Content", {
            "fields": ("image", "content", "summary",),
        }),
        ("Publication", {
            "fields": ("categories", "authors", "is_online",),
            "classes": ("collapse",),
        }),
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
    )

    raw_id_fields = ("image",)

    filter_horizontal = ("categories", "authors",)

    def save_related(self, request, form, formsets, change):
        """Saves the author of the article."""
        super(ArticleAdminBase, self).save_related(request, form, formsets, change)
        # For new articles, add in the current author.
        if not change and not form.cleaned_data["authors"]:
            form.instance.authors.add(request.user)


if externals.reversion:
    class ArticleAdmin(ArticleAdminBase, externals.reversion["admin.VersionMetaAdmin"]):
        list_display = ArticleAdminBase.list_display + ("get_date_modified",)
else:
    class ArticleAdmin(ArticleAdminBase):
        pass


admin.site.register(Article, ArticleAdmin)

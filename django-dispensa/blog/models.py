from django.db import models
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import ugettext as _

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import Tag, TaggedItemBase

from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from .fields import PostStreamBlock


class BlogIndex(Page):
    @property
    def articles(self):
        """
        Returns a queryset of live blog articles, ordered from the most recent
        """
        articles = BlogPost.objects.live().descendant_of(self)
        articles = articles.order_by('-date')

        return articles

    @property
    def tags(self):
        """
        Returns a queryset of all available tag ordered by use
        """
        tags = Tag.objects.all()
        tags = tags.annotate(num_times=models.Count('blog_posttag_items'))
        tags = tags.order_by('-num_times')

        return tags

    def get_context(self, request):
        """
        Populates the context with a paginated articles list.
        They are filtered using the querystring; available filters are:
            - tag: fetch articles for the chosen tag
            - page: fetch a list of articles for the selected page number
        """
        articles = self.articles

        # Filtering by tag
        tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__name=tag)

        # Pagination, using the blog settings
        page = request.GET.get('page')
        page_number = BlogSettings.for_site(request.site).page_number
        paginator = Paginator(articles, page_number)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        # Updating the template context
        context = super().get_context(request)
        context['articles'] = articles
        context['current_tag'] = tag
        return context


class PostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items')


class BlogPost(Page):
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(PostStreamBlock())
    intro = models.TextField(max_length=600)
    tags = ClusterTaggableManager(through=PostTag, blank=True)
    date = models.DateField(_('Post date'))

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('cover'),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
        FieldPanel('date'),
    ]

    def get_context(self, request):
        """
        Provides the site setting used by the Sharing Buttons
        """
        context = super().get_context(request)
        context['site_domain'] = request.build_absolute_uri()
        return context


@register_setting
class BlogSettings(BaseSetting):
    page_number = models.IntegerField(
        help_text=_('The articles that are shown in the blog index page before using a paginator'),
        default=10
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('page_number'),
            ],
            heading=_('Blog configuration'),
            classname='collapsible',
        ),
    ]

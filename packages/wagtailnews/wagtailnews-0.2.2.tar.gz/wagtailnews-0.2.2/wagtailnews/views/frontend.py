from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..conf import paginate


def _newsitem_list(request, newsindex, newsitem_list, extra_context):
    paginator, page = paginate(request, newsitem_list)
    context = {
        'self': newsindex,
        'paginator': paginator,
        'page': page,
        'newsitem_list': page.object_list,
    }
    context.update(extra_context)
    return render(request, newsindex.get_template(request), context)


def news_index(request, newsindex):
    now = timezone.now()
    NewsItem = newsindex.get_newsitem_model()
    newsitem_list = NewsItem.objects.filter(
        newsindex=newsindex, date__lte=now)
    return _newsitem_list(request, newsindex, newsitem_list, {
        'list_type': 'index',
    })


def news_year(request, newsindex, year):
    NewsItem = newsindex.get_newsitem_model()
    newsitem_list = NewsItem.objects.filter(
        newsindex=newsindex, date__year=year)
    return _newsitem_list(request, newsindex, newsitem_list, {
        'list_type': 'index',
    })


def news_month(request, newsindex, year, month):
    NewsItem = newsindex.get_newsitem_model()
    newsitem_list = NewsItem.objects.filter(
        newsindex=newsindex, date__year=year, date__month=month)
    return _newsitem_list(request, newsindex, newsitem_list, {
        'list_type': 'index',
    })


def news_day(request, newsindex, year, month, day):
    NewsItem = newsindex.get_newsitem_model()
    newsitem_list = NewsItem.objects.filter(
        newsindex=newsindex, date__year=year, date__month=month, date__day=day)
    return _newsitem_list(request, newsindex, newsitem_list, {
        'list_type': 'index',
    })


def newsitem_detail(request, newsindex, year, month, day, pk,
                    slug):
    NewsItem = newsindex.get_newsitem_model()
    newsitem = get_object_or_404(NewsItem, newsindex=newsindex, pk=pk)

    if request.path != newsitem.url():
        return redirect(newsitem.url())

    return render(request, newsitem.get_template(request), {
        'self': newsindex,
        'newsitem': newsitem,
    })

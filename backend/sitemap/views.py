import datetime
from calendar import timegm

from django.contrib.sitemaps.views import x_robots_tag
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.http import http_date

from .sitemaps import SiteSitemap


@x_robots_tag
def sitemap(request: WSGIRequest) -> TemplateResponse:
    """Получение sitemap."""
    template = "sitemap/sitemap.xml"
    content_type = "text/xml"

    request_protocol = request.scheme
    request_site = get_current_site(request)
    if str(request_site) == "example.com":
        msg = "Вы не поменяли стандартный site в django sites"
        raise AssertionError(msg)
    sitemaps = SiteSitemap.maps

    maps = sitemaps.values()

    page = request.GET.get("p", 1)
    all_sites_lastmod = True
    lastmod = None
    urls = []
    cache.get("lastmod")

    for site in maps:
        try:
            if callable(site):
                site = site(request)  # noqa: PLW2901
            urls.extend(site.get_urls(page=page, site=request_site, protocol=request_protocol))

            if all_sites_lastmod:
                site_lastmod = getattr(site, "latest_lastmod", None)
                if site_lastmod is not None:
                    site_lastmod = (
                        site_lastmod.utctimetuple()
                        if isinstance(site_lastmod, datetime.datetime)
                        else site_lastmod.timetuple()
                    )
                    lastmod = site_lastmod if lastmod is None else max(lastmod, site_lastmod)
                else:
                    all_sites_lastmod = False
        except EmptyPage as exc:
            msg = f"Page {page} empty"
            raise Http404(msg) from exc
        except PageNotAnInteger as exc:
            msg = f"No page '{page}'"
            raise Http404(msg) from exc
    if all_sites_lastmod and lastmod is not None:
        lastmod_utc = lastmod.utctimetuple() if isinstance(lastmod, datetime.datetime) else lastmod
    else:
        lastmod_utc = datetime.datetime.now(tz=datetime.UTC)
        lastmod = lastmod_utc.utctimetuple()

    context = {"urlset": urls, "lastmod": lastmod_utc}
    response = TemplateResponse(request, template, context, content_type)
    if all_sites_lastmod and lastmod is not None:
        response["Last-Modified"] = http_date(timegm(lastmod))
    cache.set("lastmod", lastmod, 86400)

    return response

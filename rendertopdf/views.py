from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, response

from django.template.loader import get_template
# Create your views here.

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from blog.models import Article


def l(request, slug):  # تابعی تشکیل دادم که 2 متغییر بگیره بعد این 2 تا ساگو بگیره بعدش بیارتشون تو این آدرسی که پااین نوشتم
    context = {"article": get_object_or_404(Article, slug=slug, status='p')}  # اسلاگ سمت چپی برای مدل است و اسلاگ راستی برای ویو جدیده
    return render(request, "pdf/pdf.html", context)


# *************************************************************
def topdf(request,slug):
    data = dict()

    data['data'] = Article.objects.get(slug=slug)
#     return render(request, "pdf/pdf.html", data)

    template_path = 'pdf/pdf.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)

    html = template.render(data)

    # create a pdf
    pisa_status = pisa.CreatePDF( html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#     return HttpResponse(request, 'blog/detail.html', data)


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path
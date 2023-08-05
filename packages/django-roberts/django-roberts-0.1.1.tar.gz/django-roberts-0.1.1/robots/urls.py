from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^robots.txt$',
        TemplateView.as_view(
            template_name='robots/robots.txt',
            content_type='text/plain',
            ),
        name='views.robots.txt'
        ),

    ]

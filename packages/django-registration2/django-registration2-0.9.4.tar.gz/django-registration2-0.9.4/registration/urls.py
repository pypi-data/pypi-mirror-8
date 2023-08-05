from django.conf.urls import url, patterns, include
from django.views.generic.base import TemplateView
from registration.views import verify, register

urlpatterns = patterns('',
    url(r'^register/$', register, name='register'),

    url(r'^register/complete/$', TemplateView.as_view(
        template_name='registration/registration_complete.html'
    ), name='registration-complete'),

    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^verify/(?P<activation_key>\w+)/$', verify,
        name='verify-registration'),

    url(r'^register/closed/$', TemplateView.as_view(
        template_name='registration/registration_closed.html'
    ), name='registration-disabled'),

    url(r'^moderate/(?P<activation_key>\w+)/$', 'registration.views.moderate',
        name='moderate-registration'),

    url(r'^moderate/$', 'registration.views.moderate_list',
        name='moderate-registration-list'),

    url(r'', include('registration.auth_urls')),
)

from django import forms
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static
from django.views.generic.base import RedirectView
from django.template import defaultfilters as filters

from registration.forms import RegistrationForm, TOS_REQUIRED
from registration.backends.hmac.views import RegistrationView


url_tos = r"https://github.com/mnieber/shared-goals/blob/master/TERMS.md"
url_about = r"https://github.com/mnieber/shared-goals/blob/master/README.md"
url_feedback = r"https://github.com/mnieber/shared-goals/issues"


class RegistrationFormWithTerms(RegistrationForm):
    # Subclass of ``RegistrationForm`` which adds a required checkbox
    # for agreeing to a site's Terms of Service.

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=filters.safe((
            'I have read and agree to the '
            '<a href=%s>Terms of Service<a>'
        ) % url_tos),
        error_messages={
            'required': TOS_REQUIRED,
        }
    )


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^accounts/register/$',
        RegistrationView.as_view(form_class=RegistrationFormWithTerms),
        name='registration_register'
    ),
    url(r'^tos/', RedirectView.as_view(url=url_tos), name='tos'),
    url(r'^about/', RedirectView.as_view(url=url_about), name='about'),
    url(
        r'^feedback/',
        RedirectView.as_view(url=url_feedback),
        name='feedback'
    ),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'', include('goal.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(
            r'^media/(?P<path>.*)$',
            static.serve,
            {
                'document_root': settings.MEDIA_ROOT, 'show_indexes': True
            }
        ),
    ]

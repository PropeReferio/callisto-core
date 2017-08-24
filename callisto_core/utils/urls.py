from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from ..delivery import views as delivery_views, wizard as delivery_wizard
from ..reporting import views as reporting_views

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('report_new')),
        name='index',
        ),
    url(r'^reports/new/$',
        delivery_views.ReportCreateView.as_view(),
        name='report_new',
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/wizard/step/(?P<step>.+)/$',
        delivery_wizard.EncryptedWizardView.as_view(),
        name='report_update',
        ),
    # TODO: a /review url that redirects here
    url(r'^reports/uuid/(?P<uuid>.+)/wizard/step/done/$',
        delivery_wizard.EncryptedWizardView.as_view(),
        name="report_view",
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/review/pdf/$',
        delivery_wizard.WizardPDFView.as_view(),
        name="report_view_pdf",
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/review/delete/$',
        delivery_views.ReportDeleteView.as_view(),
        name="report_delete",
        ),
    # reporting flow
    url(r'^reports/uuid/(?P<uuid>.+)/reporting/prep/$',
        reporting_views.ReportingPrepView.as_view(),
        name="reporting_prep",
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/reporting/matching/$',
        reporting_views.ReportingMatchingView.as_view(),
        name="reporting_matching_enter",
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/reporting/confirmation/$',
        reporting_views.ReportingConfirmationView.as_view(),
        name="reporting_confirmation",
        ),
    # /end reporting flow
    # matching flow
    url(r'^reports/uuid/(?P<uuid>.+)/matching/prep/$',
        reporting_views.MatchingPrepView.as_view(),
        name="matching_prep",
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/matching/enter/$',
        reporting_views.MatchingEnterView.as_view(),
        name="matching_enter",
        ),
    url(r'^reports/uuid/(?P<uuid>.+)/review/matching/withdraw/$',
        reporting_views.MatchingWithdrawView.as_view(),
        name="report_matching_withdraw",
        ),
    # /end matching flow
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
]

__title__ = 'fobi.contrib.apps.feincms_integration.widgets'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FobiFormWidget',)

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect
#from django.core.urlresolvers import reverse
from django.conf import settings

from fobi.dynamic import assemble_form_class
from fobi.base import (
    fire_form_callbacks, run_form_handlers, 
    submit_plugin_form_data, get_theme
    )
from fobi.constants import (
    CALLBACK_BEFORE_FORM_VALIDATION, CALLBACK_FORM_INVALID,
    CALLBACK_FORM_VALID_BEFORE_SUBMIT_PLUGIN_FORM_DATA, CALLBACK_FORM_VALID,
    CALLBACK_FORM_VALID_AFTER_FORM_HANDLERS
    )
from fobi.contrib.apps.feincms_integration.settings import (
    WIDGET_FORM_SENT_GET_PARAM
    )
from fobi.contrib.apps.feincms_integration.helpers import (
    get_form_template_choices, get_success_page_template_choices
)

class FobiFormWidget(models.Model):
    """
    Widget for to FeinCMS.

    :property fobi.models.FormEntry form_entry: Form entry to be rendered.
    :property str template: If given used for rendering the form.
    """
    form_entry = models.ForeignKey('fobi.FormEntry', verbose_name=_("Form"))

    form_template_name = models.CharField(
        _("Form template name"), max_length=255, null=True, blank=True,
        choices=get_form_template_choices(),
        help_text=_("Template to render the form with.")
        )

    hide_form_title = models.BooleanField(
        _("Hide form title"), default=False,
        help_text=_("If checked, no form title is shown.")
        )

    form_title = models.CharField(
        _("Form title"), max_length=255, null=True, blank=True,
        help_text=_("Overrides the default form title.")
        )

    form_submit_button_text = models.CharField(
        _("Submit button text"), max_length=255, null=True, blank=True,
        help_text=_("Overrides the default form submit button text.")
        )

    success_page_template_name = models.CharField(
        _("Success page template name"), max_length=255, null=True, blank=True,
        choices=get_success_page_template_choices(),
        help_text=_("Template to render the success page with.")
        )

    hide_success_page_title = models.BooleanField(
        _("Hide success page title"), default=False,
        help_text=_("If checked, no success page title is shown.")
        )

    success_page_title = models.CharField(
        _("Succes page title"), max_length=255, null=True, blank=True,
        help_text=_("Overrides the default success page title.")
        )

    success_page_text = models.TextField(
        _("Succes page text"), null=True, blank=True,
        help_text=_("Overrides the default success page text.")
        )

    class Meta:
        abstract = True
        app_label = 'fobi'

    def __unicode__(self):
        return _('Fobi form')

    def process(self, request, **kwargs):
        """
        This is where most of the form handling happens.

        :param django.http.HttpRequest request:
        :return django.http.HttpResponse | str:
        """
        if WIDGET_FORM_SENT_GET_PARAM in request.GET:
            return self._show_thanks_page(request, **kwargs)
        else:
            return self._process_form(request, **kwargs)

    def _process_form(self, request, **kwargs):
        """
        Handle the form if no "sent" GET argument (see the 
        ``WIDGET_FORM_SENT_GET_PARAM`` setting).

        :param django.http.HttpRequest request:
        :return django.http.HttpResponse | str:
        """
        template_name = self.form_template_name or None

        # Handle public/non-public forms. If form requires user authentication
        # redirect to login form with next parameter set to current request
        # path.
        if not request.user.is_authenticated() and not self.form_entry.is_public:
            return redirect("{0}?next={1}".format(settings.LOGIN_URL, request.path))

        form_element_entries = self.form_entry.formelemententry_set.all()[:]
        # This is where the most of the magic happens. Our form is being built
        # dynamically.
        FormClass = assemble_form_class(
            self.form_entry,
            form_element_entries = form_element_entries
            )

        if 'POST' == request.method:
            form = FormClass(request.POST, request.FILES)

            # Fire pre form validation callbacks
            fire_form_callbacks(
                form_entry = self.form_entry,
                request = request,
                form = form,
                stage = CALLBACK_BEFORE_FORM_VALIDATION)

            if form.is_valid():
                # Fire form valid callbacks, before handling sufrom
                # django.http import HttpResponseRedirectbmitted plugin
                # form data
                form = fire_form_callbacks(
                    form_entry = self.form_entry,
                    request = request,
                    form = form,
                    stage = CALLBACK_FORM_VALID_BEFORE_SUBMIT_PLUGIN_FORM_DATA
                    )

                # Fire plugin processors
                form = submit_plugin_form_data(
                    form_entry = self.form_entry,
                    request = request,
                    form = form
                    )

                # Fire form valid callbacks
                form = fire_form_callbacks(
                    form_entry = self.form_entry,
                    request = request,
                    form = form,
                    stage = CALLBACK_FORM_VALID
                    )

                # Run all handlers
                run_form_handlers(
                    form_entry = self.form_entry,
                    request = request,
                    form = form
                    )

                # Fire post handler callbacks
                fire_form_callbacks(
                    form_entry = self.form_entry,
                    request = request,
                    form = form,
                    stage = CALLBACK_FORM_VALID_AFTER_FORM_HANDLERS
                    )

                messages.info(
                    request,
                    _('Form {0} was submitted successfully.').format(self.form_entry.name)
                    )

                return redirect(
                    "{0}?{1}={2}".format(request.path, WIDGET_FORM_SENT_GET_PARAM, \
                                         self.form_entry.slug)
                    )

            else:
                # Fire post form validation callbacks
                fire_form_callbacks(
                    form_entry = self.form_entry,
                    request = request,
                    form = form,
                    stage = CALLBACK_FORM_INVALID
                    )

        else:
            form = FormClass()

        theme = get_theme(request=request, as_instance=True)
        theme.collect_plugin_media(form_element_entries)

        context = {
            'form': form,
            'form_entry': self.form_entry,
            'fobi_theme': theme,
            'fobi_form_title': self.form_title,
            'fobi_hide_form_title': self.hide_form_title,
            'fobi_form_submit_button_text': self.form_submit_button_text
        }

        if not template_name:
            template_name = theme.view_embed_form_entry_ajax_template

        self.rendered_output = render_to_string(
            template_name, context, context_instance=RequestContext(request)
            )

    def _show_thanks_page(self, request, **kwargs):
        """
        Renders the thanks page after successful form submission.

        :param django.http.HttpRequest request:
        :return str:
        """
        template_name = self.success_page_template_name or None

        theme = get_theme(request=request, as_instance=True)

        context = {
            'form_entry': self.form_entry,
            'fobi_theme': theme,
            'fobi_hide_success_page_title': self.hide_success_page_title,
            'fobi_success_page_title': self.success_page_title,
            'fobi_success_page_text': self.success_page_text,
        }

        if not template_name:
            template_name = theme.embed_form_entry_submitted_ajax_template

        self.rendered_output = render_to_string(
            template_name, context, context_instance=RequestContext(request)
            )

    def render(self, **kwargs):
        return getattr(self, 'rendered_output', '')

    def finalize(self, request, response):
        # Always disable caches if this content type is used somewhere
        response['Cache-Control'] = 'no-cache, must-revalidate'

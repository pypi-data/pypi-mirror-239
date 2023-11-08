from cacheops import invalidate_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from ...constants import region_status
from ...forms import RegionForm
from ...models import Page
from ..form_views import CustomUpdateView


class RegionUpdateView(CustomUpdateView):
    """
    View for updating regions
    """

    #: The form class for this update view
    form_class = RegionForm

    def get(self, request, *args, **kwargs):
        r"""
        Render region form for HTTP GET requests

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        # Populate self.object
        response = super().get(request, *args, **kwargs)
        # Show warning when locations are enabled without bounding box
        if self.object.locations_enabled and not self.object.has_bounding_box:
            messages.warning(
                request,
                _(
                    "Locations are enabled but the bounding box coordinates are incomplete."
                ),
            )
        return response

    def post(self, request, *args, **kwargs):
        r"""
        Updates region and removes mirrored pages from all pages of the region when it gets archived

        :param request: The current request
        :type request: ~django.http.HttpRequest

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """

        response = super().post(request, *args, **kwargs)

        if self.object.status == region_status.ARCHIVED:
            self.object.get_pages().update(mirrored_page=None)
            invalidate_model(Page)

        return response

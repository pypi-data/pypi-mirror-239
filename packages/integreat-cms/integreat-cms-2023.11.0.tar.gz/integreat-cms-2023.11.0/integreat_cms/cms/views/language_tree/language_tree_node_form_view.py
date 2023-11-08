import logging

from django.urls import reverse

from ...forms import LanguageTreeNodeForm
from ...models import EventTranslation, PageTranslation, POITranslation
from ..form_views import CustomCreateView, CustomUpdateView

logger = logging.getLogger(__name__)


class LanguageTreeNodeCreateView(CustomCreateView):
    """
    Class that handles creating language tree nodes.
    This view is available within regions.
    """

    #: The form class of this form view
    form_class = LanguageTreeNodeForm

    def get_success_url(self):
        """
        Determine the URL to redirect to when the form is successfully validated

        :return: The url to redirect on success
        :rtype: str
        """
        if "submit_add_new" in self.request.POST:
            # If the "Create and add more" button was clicked, redirect to the new creation form
            return reverse(
                "new_languagetreenode",
                kwargs={"region_slug": self.request.region.slug},
            )
        return super().get_success_url()

    def get_form_kwargs(self):
        """
        Return the keyword arguments for instantiating the form

        :return: The form kwargs
        :rtype: dict
        """
        kwargs = super().get_form_kwargs()
        kwargs["region"] = self.request.region
        return kwargs


class LanguageTreeNodeUpdateView(CustomUpdateView):
    """
    Class that handles activating/deactivating of a language tree node
    """

    def form_valid(self, form):
        response = super().form_valid(form)

        language_tree_node = self.get_object()

        if "active" in form.changed_data:
            models = [PageTranslation, EventTranslation, POITranslation]
            for model in models:
                filters = {
                    f"{model.foreign_field()}__region": language_tree_node.region,
                    "language": language_tree_node.language,
                }
                distinct = [f"{model.foreign_field()}__pk", "language__pk"]
                for translation in model.objects.filter(**filters).distinct(*distinct):
                    if language_tree_node.active:
                        translation.save(update_timestamp=False)
                    else:
                        translation.links.all().delete()
        return response

import logging

from ...models import LanguageTreeNode
from ..list_views import ModelListView
from .language_tree_context_mixin import LanguageTreeContextMixin

logger = logging.getLogger(__name__)


# pylint: disable=too-many-ancestors
class LanguageTreeView(LanguageTreeContextMixin, ModelListView):
    """
    View for rendering the language tree view.
    This view is available in regions.
    """

    #: The model of this list view
    model = LanguageTreeNode
    #: Disable pagination for language tree
    paginate_by = None

    def get_queryset(self):
        """
        Get language tree queryset

        :return: The language tree of the current region
        :rtype: ~django.db.models.query.QuerySet [ ~integreat_cms.cms.models.languages.language_tree_node.LanguageTreeNode ]
        """
        # Return the annotated language tree of the current region to save a few database queries
        return self.request.region.language_tree

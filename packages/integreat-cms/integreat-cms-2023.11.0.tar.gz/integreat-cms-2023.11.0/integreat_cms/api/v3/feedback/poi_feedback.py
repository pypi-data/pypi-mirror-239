import logging

from django.http import Http404, JsonResponse

from ....cms.models import POIFeedback
from ...decorators import feedback_handler, json_response

logger = logging.getLogger(__name__)


@feedback_handler
@json_response
def poi_feedback(data, region, language, comment, rating, is_technical):
    """
    Store feedback about single POI in database

    :param data: HTTP request body data
    :type data: dict

    :param region: The region of this sitemap's urls
    :type region: ~integreat_cms.cms.models.regions.region.Region

    :param language: The language of this sitemap's urls
    :type language: ~integreat_cms.cms.models.languages.language.Language

    :param comment: The comment sent as feedback
    :type comment: str

    :param rating: up or downvote, neutral
    :type rating: str

    :param is_technical: is feedback on content or on tech
    :type is_technical: bool

    :raises ~django.http.Http404: HTTP status 404 if no POI with the given slug exists.

    :return: decorated function that saves feedback in database
    :rtype: ~collections.abc.Callable
    """
    poi_translation_slug = data.get("slug")

    pois = region.pois.filter(
        translations__slug=data.get("slug"),
        translations__language=language,
    ).distinct()

    if len(pois) > 1:
        logger.error(
            "POI translation slug %r is not unique per region and language, found multiple: %r",
            poi_translation_slug,
            pois,
        )
        return JsonResponse({"error": "Internal Server Error"}, status=500)

    poi = None
    if len(pois) == 1:
        poi = pois[0]
    elif region.fallback_translations_enabled:
        poi = region.pois.filter(
            translations__slug=data.get("slug"),
            translations__language=region.default_language,
        ).first()

    if not poi:
        raise Http404("No matching location found for slug.")

    poi_translation = poi.get_translation(language.slug) or poi.get_translation(
        region.default_language.slug
    )

    POIFeedback.objects.create(
        poi_translation=poi_translation,
        region=region,
        language=language,
        rating=rating,
        comment=comment,
        is_technical=is_technical,
    )
    return JsonResponse({"success": "Feedback successfully submitted"}, status=201)

"""
This module includes functions related to the push notification that are sent via firebase.
"""
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from ...cms.models import PushNotificationTranslation
from ..decorators import json_response


@json_response
def sent_push_notifications(request, region_slug, language_slug):
    """
    Function to iterate through all sent push notifications related to a region and adds them to a JSON.

    :param request: Django request
    :type request: ~django.http.HttpRequest
    :param region_slug: slug of a region
    :type region_slug: str
    :param language_slug: language slug
    :type language_slug: str

    :return: JSON object according to APIv3 push notifications definition
    :rtype: ~django.http.JsonResponse
    """
    channel = request.GET.get("channel", "all")
    query_result = (
        PushNotificationTranslation.objects.filter(
            push_notification__regions__slug=region_slug
        )
        .filter(
            push_notification__sent_date__gte=timezone.now()
            - timezone.timedelta(days=settings.FCM_HISTORY_DAYS)
        )
        .filter(language__slug=language_slug)
        .filter(push_notification__draft=False)
        .order_by("-last_updated")
    )
    if channel != "all":
        query_result = query_result.filter(push_notification__channel=channel)
    result = list(map(transform_notification, query_result))
    return JsonResponse(result, safe=False)


def transform_notification(pnt):
    """
    Function to create a JSON from a single push notification translation Object.

    :param pnt: A push notification translation
    :type pnt: ~integreat_cms.cms.models.push_notifications.push_notification_translation.PushNotificationTranslation

    :return: data necessary for API
    :rtype: dict
    """
    return {
        "id": str(pnt.pk),
        "title": pnt.get_title(),
        "message": pnt.get_text(),
        "timestamp": pnt.last_updated,  # deprecated field in the future
        "last_updated": timezone.localtime(pnt.last_updated),
        "channel": pnt.push_notification.channel,
    }

import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from ...utils.content_edit_lock import get_locking_user, lock_content, unlock_content

logger = logging.getLogger(__name__)


@require_POST
# pylint: disable=unused-argument
def content_edit_lock_heartbeat(request, region_slug=None):
    """
    This function handles heartbeat requests.
    When a heartbeat is received, this function tries to extend the lock for a user
    who is editing some content.

    :param request: The current request
    :type request: ~django.http.HttpRequest

    :param region_slug: The slug of the current region, unused
    :type region_slug: str

    :return: Json object containing `success: true` if the lock could be acquired
    :rtype: ~django.http.JsonResponse
    """
    body = json.loads(request.body.decode("utf-8"))
    id_, type_ = json.loads(body["key"])

    if body["force"] and (locking_user := get_locking_user(id_, type_)):
        logger.debug(
            "User %r took control over %s with id %s from %r",
            request.user,
            type_,
            id_,
            locking_user,
        )
        unlock_content(id_, type_, locking_user)

    success = lock_content(id_, type_, request.user)
    locking_user = request.user if success else get_locking_user(id_, type_)
    return JsonResponse(
        {"success": success, "lockingUser": locking_user.full_user_name}
    )


@require_POST
# pylint: disable=unused-argument
def content_edit_lock_release(request, region_slug=None):
    """
    This function handles unlock requests

    :param request: The current request
    :type request: ~django.http.HttpRequest

    :param region_slug: The slug of the current region, unused
    :type region_slug: str

    :return: Json object containing `success: true` if the content object could be unlocked
    :rtype: ~django.http.JsonResponse
    """
    body = json.loads(request.POST.get("body"))
    id_, type_ = body

    success = unlock_content(id_, type_, request.user)
    return JsonResponse({"success": success})

import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

def create_action(user, verb, target=None):
    """
    Сохдание действия пользователя и связывание 2-х моделей.
    Если действие - создание пользователя или завязано на одной модели,
    то target=None.
    Ограничение на создание одинаковых действий раз в минуту.
    """
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = Action.objects.filter(
            target_ct=target_ct,
            target_id=target.id
        )
    else:
        similar_actions = Action.objects.filter(
            user_id=user.id, verb=verb, created__gte=last_minute
        )
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
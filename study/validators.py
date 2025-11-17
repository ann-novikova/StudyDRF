from rest_framework.serializers import ValidationError

valid_url = "youtube.com"


def validate_url(value):
    """Валидация ссылки на ресурс для урока"""
    if valid_url not in value:
        raise ValidationError("Допускаются только ссылки на youtube.com")

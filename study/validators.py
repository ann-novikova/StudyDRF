from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        valid_url = "youtube.com"
        tmp_val = dict(value).get(self.field)
        if valid_url not in tmp_val:
            raise ValidationError(
                {self.field: "Допускаются только ссылки на youtube.com"}
            )

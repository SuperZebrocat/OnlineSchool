from rest_framework import serializers


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = "www.youtube.com"
        tmp_value = dict(value).get(self.field)
        if tmp_value and pattern not in tmp_value:
            raise serializers.ValidationError(
                "Запрещены ссылки на сторонние ресурсы. Используйте только ссылки на видео с YouTube."
            )

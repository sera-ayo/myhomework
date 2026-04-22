from rest_framework import serializers


class SessionUploadSerializer(serializers.Serializer):
    package_name = serializers.CharField(max_length=255)
    app_name = serializers.CharField(max_length=128)
    category = serializers.CharField(max_length=32, required=False, allow_blank=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    duration_sec = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        if attrs["end_time"] <= attrs["start_time"]:
            raise serializers.ValidationError("结束时间必须晚于开始时间。")
        return attrs


class BulkUsageUploadSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=128)
    source = serializers.ChoiceField(
        choices=["android", "sample"],
        required=False,
        default="android",
    )
    sessions = SessionUploadSerializer(many=True)

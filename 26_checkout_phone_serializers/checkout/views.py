"""Checkout-shaped: _validate_phone only from nested Serializer.validate_phone."""


class serializers:
    class ValidationError(Exception):
        pass

    class Serializer:
        pass

    class CharField:
        def __init__(self, **kwargs):
            pass

    class EmailField:
        def __init__(self, **kwargs):
            pass

    class ChoiceField:
        def __init__(self, **kwargs):
            pass


COACH_LEVEL_MAP = {"Head Coach": 0, "Athletic Director": 2}


def _validate_phone(value):
    raw = (value or "").strip()
    if not raw:
        raise serializers.ValidationError("Enter a phone number.")
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) < 10:
        raise serializers.ValidationError("Enter a valid phone number.")
    return f"+1{digits[-10:]}"


class QuoteRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=40)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=list(COACH_LEVEL_MAP))

    def validate_phone(self, value):
        return _validate_phone(value)


class QuoteCustomerSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=40)

    def validate_phone(self, value):
        return _validate_phone(value)


class DemoLeadRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=40)

    def validate_phone(self, value):
        return _validate_phone(value)


class APIView:
    pass


class QuoteRequestView(APIView):
    serializer_class = QuoteRequestSerializer

    def post(self, request):
        return self.serializer_class()

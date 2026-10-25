"""Checkout-shaped extract: module-level _validate_phone only called from nested
Serializer.validate_phone methods. No module-level run_checks() entry that makes
the helper trivially reachable (that toy goes quiet while production still FLAGs).
"""


class ValidationError(Exception):
    pass


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

    class JSONField:
        def __init__(self, **kwargs):
            pass


COACH_LEVEL_MAP = {
    "Head Coach": 0,
    "Athletic Director": 2,
}


def _validate_phone(value):
    """Private helper — production canary: called_by set, references: 0."""
    raw = (value or "").strip()
    if not raw:
        raise serializers.ValidationError("Enter a phone number.")
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) < 10:
        raise serializers.ValidationError("Enter a valid phone number.")
    return f"+1{digits[-10:]}"


class QuoteRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=40)
    organization = serializers.CharField(max_length=150)
    role = serializers.ChoiceField(choices=list(COACH_LEVEL_MAP))
    venues = serializers.JSONField(required=False, default=list)

    def validate_email(self, value):
        return value.strip().lower()

    def validate_phone(self, value):
        return _validate_phone(value)

    def validate(self, attrs):
        return attrs


class QuoteCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=40)
    organization = serializers.CharField(max_length=150)
    role = serializers.ChoiceField(choices=list(COACH_LEVEL_MAP))

    def validate_email(self, value):
        return value.strip().lower()

    def validate_phone(self, value):
        return _validate_phone(value)


class DemoLeadRequestSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=80)
    phone = serializers.CharField(max_length=40)
    email = serializers.EmailField()

    def validate_phone(self, value):
        return _validate_phone(value)


class APIView:
    def __init__(self, **kwargs):
        pass


class QuoteRequestView(APIView):
    serializer_class = QuoteRequestSerializer

    def post(self, request):
        ser = self.serializer_class(data=getattr(request, "data", {}))
        return {"ok": True, "serializer": ser}


class DemoLeadView(APIView):
    serializer_class = DemoLeadRequestSerializer

    def post(self, request):
        ser = self.serializer_class(data=getattr(request, "data", {}))
        return {"ok": True, "serializer": ser}

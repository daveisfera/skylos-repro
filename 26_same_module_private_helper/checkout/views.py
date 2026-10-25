from django.views import View


def _validate_phone(value):
    return bool(value) and str(value).isdigit()


class CheckoutSerializer:
    def validate_phone(self, value):
        return _validate_phone(value)


class GuestSerializer:
    def validate_phone(self, value):
        return _validate_phone(value)


class OrderView(View):
    def post(self, request):
        phone = request.POST.get("phone")
        return CheckoutSerializer().validate_phone(phone)

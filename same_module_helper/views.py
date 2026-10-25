"""Same-file private helper with in-module callers — P3.1 / checkout _validate_phone canary."""


def _validate_phone(value: str) -> str:
    digits = "".join(c for c in value if c.isdigit())
    if len(digits) < 10:
        raise ValueError("invalid phone")
    return digits


class CheckoutSerializer:
    def validate_phone(self, value: str) -> str:
        return _validate_phone(value)

    def validate_billing_phone(self, value: str) -> str:
        return _validate_phone(value)


class NestedValidators:
    class Inner:
        def clean_phone(self, value: str) -> str:
            return _validate_phone(value)


def run_checks(phone: str) -> str:
    ser = CheckoutSerializer()
    nested = NestedValidators.Inner()
    a = ser.validate_phone(phone)
    b = ser.validate_billing_phone(phone)
    c = nested.clean_phone(phone)
    return a or b or c

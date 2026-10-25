"""Wire serializers via API views the same way production checkout urls do."""

from checkout_phone.views import DemoLeadView, QuoteRequestView

urlpatterns = [
    ("quote-request/", QuoteRequestView.as_view() if hasattr(QuoteRequestView, "as_view") else QuoteRequestView),
    ("demo-lead/", DemoLeadView.as_view() if hasattr(DemoLeadView, "as_view") else DemoLeadView),
]

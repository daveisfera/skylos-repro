"""View keeps JoinFacilityForm + type_map live; FacilityChoiceField class still FLAGs."""

from django.http import HttpResponse

from django_form_field.forms import JoinFacilityForm
from django_form_field.type_map import form_field_type


def join_facility(request):
    form = JoinFacilityForm(request.POST or None)
    _ = [form_field_type(f) for f in form.fields.values()]
    if form.is_valid():
        return HttpResponse("ok")
    return HttpResponse(form.as_p())

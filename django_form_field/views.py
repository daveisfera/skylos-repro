"""View that uses the form — keeps JoinFacilityForm live so the field class is the FP."""

from django.http import HttpResponse

from django_form_field.forms import JoinFacilityForm


def join_facility(request):
    form = JoinFacilityForm(request.POST or None)
    if form.is_valid():
        return HttpResponse("ok")
    return HttpResponse(form.as_p())

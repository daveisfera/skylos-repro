"""Django path converter protocol — regex is read by register_converter."""

from enum import Enum


class PerformanceDataType(str, Enum):
    GAME = "mg"
    EVENT = "te"


class PerformanceDataKey:
    def __init__(self, type_: PerformanceDataType, id_: int) -> None:
        self.type = type_
        self.id = id_

    def __str__(self):
        return f"{self.type.value}_{self.id}"


class PerformanceDataKeyDjango:
    # register_converter dispatches to regex/to_python/to_url reflectively.
    regex = "({})_[0-9]+".format("|".join(x.value for x in PerformanceDataType))

    @staticmethod
    def to_python(value: str) -> PerformanceDataKey:
        type_, id_ = value.split("_")
        return PerformanceDataKey(PerformanceDataType(type_), int(id_))

    @staticmethod
    def to_url(value: PerformanceDataKey) -> str:
        return str(value)


def register_converter():
    # Stand-in for django.urls.register_converter(PerformanceDataKeyDjango, "perfkey")
    from django_urls import register_converter as django_register_converter

    django_register_converter(PerformanceDataKeyDjango, "perfkey")

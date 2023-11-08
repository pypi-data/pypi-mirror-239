from typing import ClassVar, List

from wagtail.api.v2.views import BaseAPIViewSet

from .models import ExhibitPage


class ExhibitsAPIViewSet(BaseAPIViewSet):
    model = ExhibitPage

    listing_default_fields: ClassVar[List[str]] = [
        *BaseAPIViewSet.listing_default_fields,
        'title',
        'body',
        'authors',
        'cover_image',
        'cover_thumb',
        'hero_image',
        'hero_thumb',
    ]

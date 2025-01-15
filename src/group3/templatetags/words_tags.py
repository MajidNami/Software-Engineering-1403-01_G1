# templatetags/words_tags.py

from django import template
from group3.models import BOXES, Word
from django.urls import reverse

register = template.Library()

@register.inclusion_tag("group3/box_links.html")
def boxes_as_links():
    boxes = []
    for box_num in BOXES:
        word_count = Word.objects.filter(box=box_num).count()
        boxes.append({
            "number": box_num,
            "word_count": word_count,
        })

    return {"boxes": boxes}
from .models import StudentRating
from registration.utils import mixins as mixins_utils


class StudentRatingForm(mixins_utils.HideCreatedByFieldFormMixin):
    
    class Meta(mixins_utils.HideCreatedByFieldFormMixin.Meta):
        model = StudentRating
        fields = ("created_by", "rate", "comment",)

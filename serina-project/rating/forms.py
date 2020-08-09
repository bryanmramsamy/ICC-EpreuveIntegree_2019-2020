from .models import StudentRating
from management.models import Module
from registration.utils import mixins as mixins_utils


class StudentRatingForm(mixins_utils.HideCreatedByFieldFormMixin):
    """ModelForm for StudentRating."""

    module = mixins_utils.VerboseDegreeModuleChoiceField(
        queryset=Module.objects.all(),
        empty_label=None,
    )

    class Meta(mixins_utils.HideCreatedByFieldFormMixin.Meta):
        """Meta definition for StudentRegistrationForm."""

        model = StudentRating
        fields = ("created_by", "module", "rate", "comment",)

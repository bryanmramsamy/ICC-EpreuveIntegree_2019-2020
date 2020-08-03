from ..models import StudentRegistrationReport
from ..utils.mixins import HideCreatedByFieldFormMixin


class StudentRegistrationReportCreateFrom(HideCreatedByFieldFormMixin):
    """ModelForm for Module."""

    class Meta(HideCreatedByFieldFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = StudentRegistrationReport
        fields = "__all__"

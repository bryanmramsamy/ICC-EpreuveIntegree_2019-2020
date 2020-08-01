from django import forms

from ..models import Module, ModuleLevel


class ResourceForm(forms.ModelForm):
    """"""

    class Meta:
        """"""

        exclude = ["created_by", "reference"]


class ModuleForm(ResourceForm):
    
    class Meta(ResourceForm.Meta):
        model = Module



# class ModuleLevelForm(ResourceForm):
    
#     class Meta(ResourceForm.Meta):
#         model = ModuleLevel

class BackOfficeResourceFormMixin(forms.ModelForm):

    class Meta:
        fields = "__all__"

        widgets = {
            'created_by': forms.HiddenInput(),
        }


class ModuleLevelForm(BackOfficeResourceFormMixin):
    class Meta(BackOfficeResourceFormMixin.Meta):
        model = ModuleLevel

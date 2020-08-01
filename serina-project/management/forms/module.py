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

class ModuleLevelForm(forms.ModelForm):
    class Meta:
        model = ModuleLevel
        exclude = ["created_by"]

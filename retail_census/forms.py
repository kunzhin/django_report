from importlib.metadata import requires
from django import forms
from .models import Outlet, PresenceNestle, Competitors


class OutletInsertForm(forms.ModelForm):
    #presenceNestle = forms.ModelMultipleChoiceField(queryset=PresenceNestle.objects,
    #                    widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    class Meta:
        model = Outlet
        fields = (
            'esr',
            'corporateBodyName',
            'taxIdentificationNumber',
            'count_tt',
            'contactName',
            'phoneNumber',
            'deliveryContract',
            'name_tt',
            'city',
            'street',
            'houseNumber',
            'channel_tt',
            'photo',
            'presenceNestle',
            'competitors',
            'comment',
            'dateConversation',
            'statusWorkedOut',
        )

        widgets = {
            'esr': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'corporateBodyName': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'taxIdentificationNumber': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'count_tt': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'contactName': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'phoneNumber': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'deliveryContract': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'name_tt': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'houseNumber': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'channel_tt': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'photo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'presenceNestle': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'competitors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 5}),
            #'dateConversation': forms.SplitDateTimeField(),
            'statusWorkedOut': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }
from django import forms
# from django.forms.widgets import SelectDateWidget

from .models import Project, Team, Bug


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['team', ]
        widgets = {
            'start_date': forms.widgets.DateTimeInput(
                attrs={'type': 'date'},
            ),
            'end_date': forms.widgets.DateTimeInput(
                attrs={'type': 'date'},
            ),
        }


class BugForm(forms.ModelForm):

    class Meta:
        model = Bug
        fields = '__all__'
        widgets = {
            'date_reported': forms.widgets.DateTimeInput(
                attrs={'type': 'date'},
            )
        }


class ProjectTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        exclude = ()


class BootstrapFormset(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BootstrapFormset, self).__init__(*args, **kwargs)

        for form in self.forms:
            for field in form.fields:
                form.fields[field].widget.attrs.update(
                    {'class': 'form-control'})


# Inline formset for team members
ProjectTeamFormSet = forms.inlineformset_factory(Project, Team,
                                                 form=ProjectTeamForm, extra=1,
                                                 formset=BootstrapFormset)

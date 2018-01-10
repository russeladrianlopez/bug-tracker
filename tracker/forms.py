from django import forms
# from django.forms.widgets import SelectDateWidget

from .models import Project, Team, Bug, BugClassification


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


class ProjectTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        exclude = ()


class BugForm(forms.ModelForm):

    class Meta:
        model = Bug
        fields = '__all__'
        widgets = {
            'date_reported': forms.widgets.DateTimeInput(
                attrs={'type': 'date'},
            )
        }


class BugClassForm(forms.ModelForm):

    class Meta:
        model = BugClassification
        exclude = ()


# Added bootstrap form-control class in the Inline formset input fields
class BootstrapFormset(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BootstrapFormset, self).__init__(*args, **kwargs)

        for form in self.forms:
            for field in form.fields:
                form.fields[field].widget.attrs.update(
                    {'class': 'form-control'})


# Inline formsets
# ProjectTeamFormSet max_num is based on an article with 13 being the magic
# number this excluding the Product Owner and ScrumMaster so I settled with 15
# http://rgalen.com/agile-training-news/2015/8/22/the-3-bears-of-agile-team-size
ProjectTeamFormSet = forms.inlineformset_factory(Project, Team,
                                                 form=ProjectTeamForm,
                                                 min_num=1,
                                                 extra=1,
                                                 max_num=15,
                                                 formset=BootstrapFormset)

BugClassFormSet = forms.inlineformset_factory(Bug, BugClassification,
                                              form=BugClassForm, max_num=1,
                                              min_num=1, can_delete=False,
                                              formset=BootstrapFormset)

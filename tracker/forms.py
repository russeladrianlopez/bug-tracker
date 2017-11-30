from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Project, Bug


class ProjectForm(forms.ModelForm):
    # use DateWidget for date input fields
    start_date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    end_date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    class Meta:
        model = Project
        fields = '__all__'


class BugForm(forms.ModelForm):
    # use DateWidget for date input fields
    date_reported = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    class Meta:
        model = Bug
        fields = '__all__'

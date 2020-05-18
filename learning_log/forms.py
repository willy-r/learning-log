"""Forms for the learning_log app."""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Entry, Topic


class TopicForm(forms.ModelForm):
    """Form for add a new topic."""

    class Meta:
        model = Topic
        fields = ('topic_text', 'public')
        labels = {
            'topic_text': _('Topic name'),
            'public': _('Do you want make this topic public?'),
        }
        help_texts = {
            'public': _('Anyone will can see the entries for this topic.\
                        <br><strong>You can change this later.</strong>'),
        }


class EntryForm(forms.ModelForm):
    """Form for add a new entry for a specific topic."""

    class Meta:
        model = Entry
        fields = ('entry_text',)
        widgets = {
            'entry_text': forms.Textarea(attrs={'cols': 80, 'rows': 15}),
        }

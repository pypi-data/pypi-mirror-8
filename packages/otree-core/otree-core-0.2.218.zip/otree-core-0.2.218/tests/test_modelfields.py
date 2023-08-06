from django.test import TestCase
import otree.forms

from .models import SimpleModel, FormFieldModel


class TestModelForm(otree.forms.ModelForm):
    class Meta:
        model = FormFieldModel
        exclude = ()


class WidgetArgumentTests(TestCase):
    def test_widget_argument(self):
        self.assertEqual(TestModelForm.base_fields['char'].widget.__class__, otree.forms.TextInput)
        self.assertEqual(TestModelForm.base_fields['alt_date_time'].widget.__class__, otree.forms.SplitDateTimeWidget)
        self.assertEqual(TestModelForm.base_fields['text'].widget.__class__, otree.forms.Textarea)
        self.assertEqual(TestModelForm.base_fields['alt_text'].widget.__class__, otree.forms.TextInput)


class ModelTests(TestCase):
    def test_get_FIELD_display(self):
        obj = SimpleModel(name='bob')
        self.assertEqual(obj.get_name_display(), 'BOB')

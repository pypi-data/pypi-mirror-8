from django import forms
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.forms.models import ModelForm
from django.utils.translation import ugettext as _

from .models import Translation


class TranslationAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'lang', 'field')
    search_fields = ('lang', 'field', 'translation')
    list_filter = ('lang', 'field', 'content_type')

admin.site.register(Translation, TranslationAdmin)


def create_translations(modeladmin, request, queryset):
    for obj in queryset:
        obj.translate()
create_translations.short_description = _('Create translations for selected objects')


class TranslationInlineForm(ModelForm):
    widgets = {
        'CharField': forms.TextInput(),
        'TextField': forms.Textarea(),
    }

    class Meta:
        model = Translation

    def __init__(self, *args, **kwargs):
       res = super(TranslationInlineForm, self).__init__(*args, **kwargs)
       # overwrite the widgets for each form instance depending on the object and widget dict
       if self.widgets and self.instance and hasattr(self.instance, 'content_type'):
           model = self.instance.content_type.model_class()
           field = model._meta.get_field(self.instance.field)
           # get widget for field if any
           widget = self.widgets.get(field.get_internal_type())
           if widget:
               translation = self.fields['translation']
               # overwrite widget to field
               translation.widget = widget
       return res

    def clean_translation(self):
        """
        Do not allow translations longer than the max_lenght of the field to
        be translated.
        """
        translation = self.cleaned_data['translation']
        if self.instance and self.instance.content_object:
            # do not allow string longer than translatable field
            obj = self.instance.content_object
            field = obj._meta.get_field(self.instance.field)
            max_length = field.max_length
            if max_length and len(translation) > max_length:
                raise forms.ValidationError(
                    _('The entered translation is too long. You entered '\
                    '%(entered)s chars, max length is %(maxlength)s') % {
                        'entered': len(translation),
                        'maxlength': max_length,
                    }
                )
        else:
            raise forms.ValidationError(
                _('Can not store translation. First create all translation'\
                ' for this object')
            )
        return translation


class TranslationInline(GenericTabularInline):
    model = Translation
    form = TranslationInlineForm

    extra = 0
    readonly_fields = ('lang', 'field')
    exclude = ('lang', 'field')
    can_delete = False


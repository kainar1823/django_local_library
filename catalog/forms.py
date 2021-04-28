from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

from .models import BookInstance

# 使用 Form


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).")

    # 表单和字段验证
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past."))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead.'))

        return data
    # 在表单和字段验证（Django docs）中验证表单还有其他很多方法和示例。例如
    # 如果有多个相互依赖的字段，则可以覆盖 Form.clean() 函数并再次引发ValidationError。


# 使用 ModelForm
# 该示例与以上原始形式的唯一区别，是模型字段名为 due_back 而不是 renewal_date
class RenewBookModelForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back', ]
        labels = {'due_back': _('Renewal date'), }
        help_texts = {'due_back': _(
            'Enter a date between now and 4 weeks (default 3).'), }

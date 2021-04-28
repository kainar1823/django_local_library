from django.test import TestCase
'''
测试表单的理念，与测试模型的理念相同；您需要测试您编码、或设计指定的任何内容，但不测试底层框架，和其他第三方库的行为。

通常，这意味着您应该测试表单，是否包含您想要的字段，并使用适当的标签和帮助文本，显示这些字段。
您无需验证 Django 是否正确验证了字段类型（除非您创建了自己的自定义字段和验证） - 即您不需要测试电子邮件字段，是否只接受电子邮件。
但是，您需要测试，您希望在字段上执行的任何其他验证，以及您的代码将为错误生成的任何消息。
'''

import datetime
from django.utils import timezone
from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label ==
                        None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text,
                         'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + \
            datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

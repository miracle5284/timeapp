import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PasswordValidator:
    @staticmethod
    def validate(password, user=None):
        if len(password) > 64:
            raise ValidationError(
                _("Password must be 64 characters or less."),
                code='password_too_long',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_uppercase',
            )

        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code='password_no_lowercase',
            )

        if not re.search(r'\d', password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )

        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )

    @staticmethod
    def get_help_text(self):
        return _(
            "Password must be 8–64 characters long, and include at least 1 uppercase letter, "
            "1 lowercase letter, 1 digit, and 1 special character."
        )
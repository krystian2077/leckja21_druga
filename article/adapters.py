from allauth.account.adapter import DefaultAccountAdapter


class EmailAsUsernameAdapter(DefaultAccountAdapter):
    """
    Adapter który automatycznie używa email jako username
    """

    def save_user(self, request, user, form, commit=True):
        """
        Zapisuje użytkownika z email jako username
        """
        user = super().save_user(request, user, form, commit=False)
        # Ustaw email jako username
        user.username = user.email
        if commit:
            user.save()
        return user

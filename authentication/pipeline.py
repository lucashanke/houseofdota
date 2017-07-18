from django.contrib.auth.models import User

def _useful_details(details):
    return {
        "username": details["player"]["steamid"],
        "first_name": details["player"]["personaname"],
    }

def user_details(user, details, strategy, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        changed = False  # flag to track changes
        protected = ('id', 'pk') + tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

        # Update user model attributes with the new data sent by the current
        # provider. Update on some attributes is disabled by default, for
        # example username and id fields. It's also possible to disable update
        # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.

        player_details = _useful_details(details)
        if player_details:
            for name, value in player_details.items():
                if value is not None and hasattr(user, name):
                    current_value = getattr(user, name, None)
                    if not current_value or name not in protected:
                        changed |= current_value != value
                        setattr(user, name, value)
        if changed:
            strategy.storage.user.changed(user)


def associate_existing_user(uid, *args, **kwargs):
    """If there already is an user with the given steamid, hand it over to the pipeline"""
    if User.objects.filter(username=uid).exists():
        return {
            'user': User.objects.get(username=uid)
        }

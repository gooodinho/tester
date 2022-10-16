from .service import create_profile

def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created is True:
        user = instance
        create_profile(user)
from django.contrib.auth.models import User

def create_user_account(username, email, password):
    """
    Utility function for creating a new user account.
    """
    # Use the create_user method to create a new user with a hashed password
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return user

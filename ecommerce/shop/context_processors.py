from .models import Customer

def profile_picture(request):
    """
    Adds the user's profile (Customer) to the context if authenticated.
    Returns None if not logged in or no profile exists.
    """
    if request.user.is_authenticated:
        try:
            return {'profile': request.user.profile.first()}  # ForeignKey (many-to-one)
        except Customer.DoesNotExist:
            return {'profile': None}
    return {'profile': None}
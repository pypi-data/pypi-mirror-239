from functools import wraps

def root_access_required(func):
    @wraps(func)
    def wrapper(service_instance, *args, **kwargs):
        # Get the session from the service_instance
        session = service_instance._ssh
        # Login as root
        session.login_as_root()
        # Call the original function with the given arguments and keyword arguments
        result = func(service_instance, *args, **kwargs)
        # Logout from root
        session.logout_from_root()

        return result

    return wrapper
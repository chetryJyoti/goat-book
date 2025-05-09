from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

# Get the custom or default user model
User = get_user_model()

# Django management command to create a pre-authenticated session
class Command(BaseCommand):
    # Accept email as a command-line argument
    def add_arguments(self, parser):
        parser.add_argument("email")

    # This function is called when the command runs
    def handle(self, *args, **options):
        # Create the session for the given email
        session_key = create_pre_authenticated_session(options['email'])
        # Output the session key to the console
        self.stdout.write(session_key)

# Creates a session that simulates a logged-in user
def create_pre_authenticated_session(email):
    # Create a new user with the provided email (no password)
    user = User.objects.create(email=email)
    # Start a new session
    session = SessionStore()
    # Mark this session as authenticated for the user
    session[SESSION_KEY] = user.pk
    # Specify the backend used for authentication
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    # Save the session to the database
    session.save()
    # Return the session key so it can be used elsewhere
    return session.session_key

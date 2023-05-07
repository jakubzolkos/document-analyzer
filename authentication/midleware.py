from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout


class SessionIdleTimeout:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now()

        # Check if the user is authenticated
        if request.user.is_authenticated:

            # Check if the last activity time is set
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity_time = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')

                # Calculate the idle time
                idle_time = current_time - last_activity_time

                # Check if the idle time is greater than the session timeout
                if idle_time > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    logout(request)

        # Update the last activity time
        request.session['last_activity'] = str(current_time)

        response = self.get_response(request)
        return response
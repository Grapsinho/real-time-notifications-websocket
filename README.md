# Django Blog with Real-Time Notifications

This project is a blog application built with Django, showcasing how to implement real-time notifications using WebSockets. Notifications are sent when users comment on posts, allowing the post author to receive updates instantly.

## Features

- Real-time WebSocket notifications for post comments.
- Use of Django Channels and Redis for WebSocket support.
- A user receives notifications in a dropdown menu when a comment is added to their post.
- Notifications include the comment message, timestamp, and a link to the relevant post.

## Prerequisites

- Python 3.x
- Django 3.x or higher
- Django Channels
- Redis (for channel layers)
- Bootstrap (for styling the frontend)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Grapsinho/real-time-notifications-websocket.git
   cd real-time-notifications-websocket
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Channels and Redis:

   ```bash
   pip install channels-redis
   python -m pip install -U 'channels[daphne]'
   ```

4. Set up the database and run migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

## Configuration

1. Add `daphne` at the top of the `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       "daphne",
       # other apps
   ]
   ```

2. Configure Channels and Redis in `settings.py`:

   ```python
   ASGI_APPLICATION = 'your_project_name.asgi.application'

   CHANNEL_LAYERS = {
       'default': {
           'BACKEND': 'channels_redis.core.RedisChannelLayer',
           'CONFIG': {
               "hosts": [('127.0.0.1', 6379)],
           },
       },
   }
   ```

3. Update `asgi.py` to include the routing for WebSockets:

   ```python
   from channels.routing import ProtocolTypeRouter, URLRouter
   from channels.auth import AuthMiddlewareStack
   from your_app_name.routing import websocket_urlpatterns

   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       "websocket": AuthMiddlewareStack(
           URLRouter(
               websocket_urlpatterns
           )
       ),
   })
   ```

## Usage

1. Run the development server:

   ```bash
   python manage.py runserver
   ```

2. Navigate to the homepage to view the list of blog posts. Click on a post to view details and leave a comment.

3. Logged-in users can view real-time notifications when comments are made on their posts.

## Project Structure

- **models.py**: Defines the `Post`, `Comment`, and `Notification` models.
- **views.py**: Handles displaying posts and managing comments.
- **consumers.py**: Manages WebSocket connections and sending notifications.
- **routing.py**: Defines URL patterns for WebSocket connections.
- **signals.py**: Uses Django signals to trigger notifications when a comment is created.
- **templates/**: Contains HTML files for displaying posts, notifications, and comment forms.

## Frontend

The frontend uses Bootstrap for styling. Notifications are displayed in a dropdown menu in the navigation bar and updated in real time via WebSockets.

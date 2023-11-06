# FlaskAuth2FA Package

This package provides a Flask extension for handling user authentication.

## Installation

To install FlaskAuth2FA, run:

```
pip install FlaskAuth2FA
```

## Usage

To use FlaskAuth2FA in your Flask application, register the authentication Blueprint:

```python
from flask_auth import auth

app.register_blueprint(auth, url_prefix='/auth')

```
### Next, specify where to redirect the user after successful logins:
```
# Set a default or specific success URL for each project
app.config['LOGIN_SUCCESS_URL'] = 'dashboard'  # Use the endpoint name here
- !!Note!! This should be a route that actually routes to something in your project. Otherwise, you will get a 500 or 404. 
```
See the documentation for more details.

from django.dispatch import Signal

# instance = menuitem canhchua with ID = 1, request = actual request for get client id from utils.py
user_logged_in = Signal(providing_args=["instance", "request"])
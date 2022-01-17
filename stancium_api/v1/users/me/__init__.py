"""
if your curious, this endpoint is just meant to 
give the bot user with the token in their headers.
"""
from django import http

from stancium_api import headers


def check_headers():
    if headers.auth == "valid":
        ...

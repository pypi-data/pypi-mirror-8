# coding=utf-8
"""Configurations file for User Map.

..note: By design, you can override these settings from your project's
    settings.py with prefix 'USER_MAP' on the variable e.g
    'USER_MAP_USER_ICONS'.

    For mailing. as the default, it wil use 'DEFAULT_FROM_MAIL' setting from
    the project.
"""
from django.conf import settings

# PROJECT_NAME: The project name for this apps e.g InaSAFE
default_project_name = 'InaSAFE'
PROJECT_NAME = getattr(settings, 'USER_MAP_PROJECT_NAME', default_project_name)

# LOGO/BRAND
default_brand_logo = 'user_map/img/logo.png'
BRAND_LOGO = getattr(settings, 'USER_MAP_BRAND_LOGO', default_brand_logo)

# FAVICON_FILE: Favicon for this apps
default_favicon_file = 'user_map/img/user-icon.png'
FAVICON_FILE = getattr(settings, 'USER_MAP_FAVICON_FILE', default_favicon_file)

#  USER ROLES: All user roles and their icons
default_user_roles = [
    dict(
        name='User',
        icon='user_map/img/user-icon.png',
        shadow_icon='user_map/img/shadow-icon.png'),
    dict(
        name='Trainer',
        icon='user_map/img/trainer-icon.png',
        shadow_icon='user_map/img/shadow-icon.png'),
    dict(
        name='Developer',
        icon='user_map/img/developer-icon.png',
        shadow_icon='user_map/img/shadow-icon.png')]
USER_ROLES = getattr(settings, 'USER_MAP_USER_ROLES', default_user_roles)

# MAIL SENDER
default_mail_sender = 'noreply@inasafe.org'
DEFAULT_FROM_MAIL = getattr(settings, 'DEFAULT_FROM_MAIL', default_mail_sender)

# LEAFLET CONFIG
default_leaflet_tiles = (
    'OpenStreetMap',
    'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    ('© <a href="http://www.openstreetmap.org" target="_parent">OpenStreetMap'
     '</a> and contributors, under an <a '
     'href="http://www.openstreetmap.org/copyright" target="_parent">open '
     'license</a>')
)
LEAFLET_TILES = getattr(settings, 'LEAFLET_TILES', default_leaflet_tiles)

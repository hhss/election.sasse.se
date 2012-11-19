#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"SASSE"
SITENAME = u"SASSE Election 2012"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

PAGE_URL = "pages/{category}/{slug}.html"
PAGE_SAVE_AS = "pages/{category}/{slug}.html"

PLUGIN_PATH = "sasse/plugins"
PLUGINS = ["sasse.plugins.candidates"]

FEED_DOMAIN = "http://election.sasse.se"
SITEURL = "http://0.0.0.0:8000"

ARTICLE_EXCLUDES = ('pages', 'candidates')

THEME = 'themes/election.sasse.se'
STATIC_PATHS = ['images']

# -*- extra stuff goes here -*-

import logging
logger = logging.getLogger('rt.friendlyzcatalog')

import patches


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

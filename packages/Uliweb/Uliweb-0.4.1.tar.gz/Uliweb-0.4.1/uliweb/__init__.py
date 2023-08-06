####################################################################
# Author: Limodou@gmail.com
# License: BSD
####################################################################

__author__ = 'limodou'
__author_email__ = 'limodou@gmail.com'
__url__ = 'https://github.com/limodou/uliweb'
__license__ = 'BSD'
version = __version__ = '0.4.1'

import os, sys
workpath = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(workpath, 'lib'))

class UliwebError(Exception): pass

from .core.SimpleFrame import (Request, Response, redirect, Redirect, error, json, jsonp,
        POST, GET, url_for, expose, get_app_dir, get_apps, function, Finder, decorators,
        functions, response, request, settings, application, NotFound, HTTPException,
        is_in_web,
    )
from .core.js import json_dumps
from .utils.storage import Storage
from .core.rules import get_endpoint

class Middleware(object):
    ORDER = 500
    
    def __init__(self, application, settings):
        self.application = application
        self.settings = settings
        
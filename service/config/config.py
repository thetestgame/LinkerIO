"""
MIT License

Copyright (c) 2019 Jordan Maxwell
Written 10/20/2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from logging.config import dictConfig

class Config(object):
    """
    Base service configuration object
    """

    # Application
    APP_NAME = 'MagicUrl'

    # Debug Toolbar
    DEBUG_TOOLBAR = False
    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel'
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Exception handling
    TRAP_HTTP_EXCEPTIONS = True

    # Logging 
    LOG_CONFIG = dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s][%(levelname)s][%(module)s]: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        },
        'requests': {
            'level': 'INFO',
            'handlers': ['wsgi']
        },
        'werkzeug': {
            'level': 'INFO',
            'handlers': ['wsgi']            
        }   
    })

    # Cloudwatch
    LOG_METRICS = False

    # S3
    FLASKS3_BUCKET_NAME = 'magicurl-cdn-us-east-1'

    # API
    DUMP_YOUTUBE_DL_REQUESTS = False
    ALLOW_LIVE_CONVERTS = False
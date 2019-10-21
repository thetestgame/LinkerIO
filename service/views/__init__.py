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

import logging

# Load modules
from service.util import modules
modules = modules.find_scripts_in_module(__file__)
logging.debug('Loading view modules: %s' % str(modules))
for module in modules:
    logging.debug('Loading module: %s' % module)
    __import__('service.views.%s' % module, locals(), globals())

def load_views():
    """
    Loads the views into the current flask app
    """

    logging.info('Loading views')

    from flask import current_app
    from service.decorators import view

    view_details = view.view_book.views
    for view_url in view_details:
        details = view_details[view_url]

        logging.info('Registering view url rule; Url: %s; View: %s' % (
            view_url, details.view_name))
        
        current_app.add_url_rule(
            view_url, 
            view_func=details.view_cls.as_view(details.view_name),
            **details.kwargs)

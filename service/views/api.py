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

import re
import json
import logging
import traceback
from youtube_dl import YoutubeDL

import flask
from flask import render_template, jsonify
from flask.views import MethodView

from service.decorators import view

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

class RestfulView(MethodView):
    """
    Base class for all restful views
    """

    INVALID_METHOD = 405
    INTERNAL_ERROR = 500

    def __default_response(self):
        """
        Returns the default response
        """

        return self.api_results(code=self.INVALID_METHOD, message='Invalid method requested')

    def get(self):
        """
        Default handler for GET requests
        """

        return self.__default_response()

    def post(self):
        """
        Default handler for POST requests
        """

        return self.__default_response()

    def api_results(self, code=200, message='Success', data={}):
        """
        Constructs and returns the api results
        """

        response = {
            'code': code,
            'message': message,
            'data': data
        }

        logging.debug('Returning results: %s' % response)
        return jsonify(response)


@view.view_details(url='/api/convert')
class ConvertApiView(RestfulView):
    """
    """

    INVALID_URL = 401
    UNSUPPORTED_URL = 402

    def __validate_url(self, url):
        """
        Checks for a valid url
        """

        return re.match(url_regex, url) is not None

    def post(self):
        """
        Handles all POST requests
        """

        values = flask.request.values
        url = values.get('url', None)
        logging.debug('Convert Request received. Url: %s' % url)

        valid = self.__validate_url(url)
        if not valid:
            return self.api_results(self.INVALID_URL, 'Invalid URL')

        ydl_opts = {
            'format': 'all'
        }

        data = {
            'title': '',
            'image': '',
            'duration': 0,
            'formats': []
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)

                # Parse base data
                data['title'] = info_dict.get('title', None)
                data['image'] = info_dict.get('thumbnail', None)
                data['duration'] = info_dict.get('duration', None)

                # Parse formats
                formats = info_dict.get('formats', [])
                for format_info in formats:
                    result_info = {}

                    acodec = format_info.get('acodec', 'none')
                    vcodec = format_info.get('vcodec', 'none')

                    result_info['has-audio'] = acodec != 'none'
                    result_info['has-video'] = vcodec != 'none'

                    format_string = format_info.get('format', '')
                    result_info['format'] = format_string
                    result_info['url'] = format_info.get('url', None)
                    result_info['ext'] = format_info.get('ext', None)
                    result_info['note'] = format_info.get('format_note', None)
                    result_info['size'] = format_info.get('filesize', None)

                    data['formats'].append(result_info)
        except:
            logging.error(traceback.format_exc())
            return self.api_results(code=self.INTERNAL_ERROR, message='An internal error has occured')

        # Check for valid results
        if len(data['formats']) == 0:
            return self.api_results(code=self.UNSUPPORTED_URL, message='Unsupported website')

        return self.api_results(data=data)
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

class ViewBookException(Exception):
    """
    Custom exception for the view book system
    """

class ViewBook(object):
    """
    Contains all registered views
    """

    def __init__(self):
        self._views = {}

    @property
    def views(self):
        return self._views

    def add_view(self, view_details):
        """
        Registers a new view with the view book
        """

        url = view_details.url
        if url in self._views:
            raise ViewBookException('url %s is already assigned!' % url)

        self._views[url] = view_details

view_book = ViewBook()
        
class ViewDetailsDecorator(object):
    """
    Custom decorator for registering views with the ViewBook
    """

    def __init__(self, url='/',  view_name=None, **kwargs):
        self._url = url
        self._view_name = view_name
        self._kwargs = kwargs
        self._view_cls = None

    @property
    def url(self):
        return self._url

    @property
    def view_name(self):
        return self._view_name

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def view_cls(self):
        return self._view_cls

    def __call__(self, view_cls):
        self._view_cls = view_cls
        if self._view_name == None:
            self._view_name = self._view_cls.__name__
        view_book.add_view(self)

view_details = ViewDetailsDecorator
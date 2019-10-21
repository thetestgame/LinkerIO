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

class ModelBookException(Exception):
    """
    Custom exception for the model book system
    """

class ModelBook(object):
    """
    Contains all registered models
    """

    def __init__(self):
        self._models = []

    @property
    def models(self):
        return self._models

    def add_model(self, model_details):
        """
        Registers a new model with the model book
        """

        if model_details in self._models:
            raise ModelBookException('url %s is already assigned!' % url)

        self._models.append(model_details)

model_book = ModelBook()
        
class ModelDetailsDecorator(object):
    """
    Custom decorator for registering models with the ModelBook
    """

    def __init__(self, **kwargs):
        self._model_cls = None

    @property
    def model_cls(self):
        return self._model_cls

    def __call__(self, model_cls):
        self._model_cls = model_cls
        model_book.add_model(self)

        return model_cls

model_details = ModelDetailsDecorator
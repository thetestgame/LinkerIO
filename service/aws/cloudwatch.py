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

from flask import current_app, g
from fluentmetrics import BufferedFluentMetric

@current_app.before_request
def start_request():
	"""
	Called before every request. Starts the metric timer
	"""

	config = current_app.config
	if config.get('LOG_METRICS', False):

		# Create a new metric if one does not exist
		if not g._request_metrics:
			g._request_metrics = BufferedFluentMetric()

		g._request_metrics.with_namespace(config.get('APP_NAME', 'Flask'))
		g._request_metrics.with_timer('RequestLatency')

@current_app.after_request
def end_request(response):
	"""
	Called at the end of a request. Ends the metric timer and 
	reports the results
	"""

	def error_counter(hundred):
		if response.status_code / 100 == hundred:
			return 1
		else:
			return 0

	config = current_app.config
	if config.get('LOG_METRICS', False):
		g._request_metrics.count(MetricName='4xxError', Value=error_counter(400))
		g._request_metrics.count(MetricName='5xxError', Value=error_counter(500))
		g._request_metrics.count(MetricName='Availability', Value=(1 - error_counter(500)))
		g._request_metrics.elapsed(MetricName='RequestLatency', TimerName='RequestLatency')		
		g._request_metrics.flush()

	return response
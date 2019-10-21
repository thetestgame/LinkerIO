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
import argparse
import os
import sys

from service import create_app

# For tornado integration
try:
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    HAS_TORNADO = True
except Exception as e:
    HAS_TORNADO = False

def main():
    """
    Main entry point for the application
    """

    # CLI arguments
    parser = argparse.ArgumentParser(description='Linkify Server')
    parser.add_argument('port', metavar='Port', type=int, nargs='?', default=8080, help='port to run the application')
    parser.add_argument('--env', '-e', dest='environment', action='store', default='dev', help='type of environment')
    parser.add_argument('--tornado', '-t', dest='tornado', action='store_true', help='run the server as tornado wsgi')
    parser.add_argument('--ssl', '-s', dest='use_ssl', action='store_true', help='run server with ssl certs')
    parser.add_argument('--ssl-certfile', '-c', dest='ssl_certfile', action='store', default='server.crt', help='ssl certificate file')
    parser.add_argument('--ssl-keyfile', '-k', dest='ssl_keyfile', action='store', default='server.key', help='ssl key file')
    parser.add_argument('--upload-s3', '-s3', dest='upload_s3', action='store_true', help='deploy s3 assets to AWS')
    parser.add_argument('--create-tables', '-ct', dest='create_tables', action='store_true', help='creates dynamodb tables in AWS')
    args = parser.parse_args()

    # Configure logging
    log_level = logging.INFO if args.environment == 'prod' else logging.DEBUG
    logging.basicConfig(format='[%(levelname)s]: %(message)s', level=log_level)

    # Create the app
    logging.info('Creating application environment: %s' % args.environment)
    app = create_app(env=args.environment)

    # Start app in tornado wsgi container
    if args.tornado:

        if HAS_TORNADO:
            try:
                logging.info('Starting Tornado Server on port %d' % args.port)
                if args.use_ssl:
                    ssl_options = {
                        'certfile': os.path.join(args.ssl_certfile), 
                        'keyfile': os.path.join(args.ssl_keyfile)
                    }
                else:
                    ssl_options=None
                
                http_server = HTTPServer(WSGIContainer(app), ssl_options=ssl_options)
                http_server.listen(args.port)
                IOLoop.instance().start()
            except KeyboardInterrupt as e:
                logging.info('Stopping Tornado Server by Ctrl+C')
        else:
            logging.warning('Failed to start Tornado server. Tornado not installed')
    elif args.upload_s3:
        logging.info('Uploading to S3...')
        import flask_s3
        flask_s3.create_all(app)
        logging.info('Upload complete.')
    elif args.create_tables:
        logging.info('Creating Dynamodb Tables')
        from service.models import create_tables
        create_tables()
        logging.info('Table creation complete')
    else:
        logging.info('Starting Flask Internal (dev) Server')
        app.run(port=args.port)
        logging.info('Stopping Flask Internal (dev) Server')

    logging.info('Shutting down...')
    return 0

if __name__ == "__main__":
    sys.exit(main())

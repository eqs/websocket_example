# -*- coding: utf-8 -*-
import json
import time

import random

from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop

class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class SendWebSocket(WebSocketHandler):
    def open(self):
        print(f'Session Opened. IP: {self.request.remote_ip}')
        self.ioloop = IOLoop.instance()
        self.send_websocket()

    def on_close(self):
        print('Session closed')

    def check_origin(self, origin):
        return True

    def send_websocket(self):
        self.ioloop.add_timeout(time.time() + 0.1, self.send_websocket)
        if self.ws_connection:
            message = json.dumps({
                'data1': random.randint(0, 100),
                'data2': random.randint(0, 100)
            })
            self.write_message(message)


app = Application([(r'/', IndexHandler),
                   (r'/ws/display', SendWebSocket)],
                  template_path='.',
                  debug=True,
                  autoreload=True)


if __name__ == '__main__':
    app.listen(3000)
    IOLoop.current().start()


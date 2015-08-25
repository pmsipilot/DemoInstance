from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from demo_config import DemoConfig
from demo import Demo
from demo_exception import *
import re
import json
import os
import logging
import Cookie

COOKIE_SESSION_NAME = 'token'


class Handler(BaseHTTPRequestHandler, object):
    def __init__(self, *args, **kwargs):
        self.config = DemoConfig()
        self.demo = Demo(self.config)
        self.user = None
        self.headers_to_send = {}
        super(Handler, self).__init__(*args, **kwargs)

    def send_http_error(self, code, error_message, error_type=None):
        self.wfile.flush()
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(
            json.dumps({
                'error': error_message,
                'type': error_type
            })
        )

    def send_http_message(self, code=200, message=''):
        self.wfile.flush()
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'info': message}))

    def send_all_header(self, code=200):
        self.send_response(code)
        logging.debug('Add Header')
        for name, value in self.headers_to_send.items():
            logging.debug('name %s value %s', name, value)
            self.send_header(name, value)
        self.end_headers()

    def send_file(self, file):
        f = open('web/'+file)
        self.set_mime()
        self.send_all_header(200)
        self.wfile.write(f.read())
        f.close()
        return

    def instance_create(self, image_key, time=None):
        id = self.demo.create_instance(
            image_key,
            token=self.user.token,
            time=time
        )
        rep = {'id': id}
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(201)
        self.wfile.write(json.dumps(rep))
        self.wfile.write('\n')
        return

    def instance_info(self, instance_id):
        self.demo.check_user_own_instance(
            self.user.token,
            instance_id,
            raise_exception=True
        )
        if not self.demo.provider.instance_exist(instance_id):
            raise DemoExceptionInstanceNotFound()

        info = {'id': instance_id, 'system_up': False, 'instance_up': False}
        if self.demo.instance_is_up(instance_id):
            info['instance_up'] = True
            info['id'] = instance_id
            info['address'] = self.demo.provider.get_instance_ip(instance_id)
            info['demo_address'] = self.demo.get_soft_address(instance_id)
            info['life_time'] = self.demo.get_life_time(instance_id)
            info['dead_time'] = self.demo.get_dead_time(instance_id)
            if self.demo.check_system_up(instance_id):
                info['system_up'] = True
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(info))
        return

    def get_user(self):
        is_admin = self.demo.auth.is_admin(self.user.login)
        info = {
            'token': self.user.token,
            'login': self.user.login,
            'admin': is_admin
        }
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(info))

    def user_instances_info(self):
        if self.user is None:
            self.send_http_error(404, 'User not found')

        instances = self.demo.get_user_instance_database(self.user.token)

        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(instances))
        return

    def all_instances_info(self):
        instances = self.demo.get_all_instance_database()
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(instances))
        return

    def pool_instances_info(self):
        instances = self.demo.get_pooled_instance_database()
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(instances))
        return

    def images_info(self):
        http_images = {}
        for name in self.config.images.keys():
            image = self.config.images[name]
            time_max = None
            if 'time_max' in image:
                time_max = image['time_max']
            data = {
                'name': image['name'],
                'desc': image['desc'],
                'img': image['img'],
                'max_time': time_max,
                'default_time': image['time_default']
            }
            http_images[name] = data
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(http_images))
        return

    def image_info(self, image_key):
        if image_key not in self.config.images:
            raise DemoExceptionInstanceNotFound()
        image = self.config.images[image_key]

        time_max = None
        if 'time_max' in image:
            time_max = image['time_max']

        data = {
            'name': image['name'],
            'desc': image['desc'],
            'img': image['img'],
            'max_time': time_max,
            'default_time': image['time_default'],
            'info': image['info']
        }
        http_image = data
        self.headers_to_send['Content-type'] = 'application/json'
        self.send_all_header(200)
        self.wfile.write(json.dumps(http_image))
        return

    def connect(self, user, password):
        mail = self.demo.auth.check_auth(user, password)
        if not mail:
            raise DemoExceptionErrorAuth

        user = self.demo.create_user(mail)
        self.write_cookie(COOKIE_SESSION_NAME, user.token)
        self.send_all_header()

    def set_mime(self):
        mimetype = None
        if self.path.endswith(".html"):
            mimetype = 'text/html'
        if self.path.endswith(".js"):
            mimetype = 'application/javascript'
        if self.path.endswith(".css"):
            mimetype = 'text/css'
        if self.path.endswith(".jpg"):
            mimetype = 'image/jpg'
        if self.path.endswith(".gif"):
            mimetype = 'image/gif'
        if self.path.endswith(".png"):
            mimetype = 'image/png'
        if mimetype is not None:
            self.headers_to_send['Content-type'] = mimetype

    def do_GET(self):
        str_path = self.path.split('?')[0]
        try:
            # Public URL
            if self.path == "/":
                self.send_file('index.html')
                return

            if os.path.isfile('web/'+str_path):
                self.send_file(str_path)
                return

            if self.path == '/api/disconnect':
                self.write_cookie(COOKIE_SESSION_NAME, 'disable')
                self.send_all_header()
                return

            # Private URL
            if not self.cookie_session():
                self.send_http_error(404, 'No action')
                return

            if self.path == "/api/user":
                self.get_user()
                return

            if self.path == "/api/image":
                self.images_info()
                return

            if self.path == "/api/myinstance":
                self.user_instances_info()
                return

            match = re.match("/api/instance/(.*)", self.path)
            if match:
                self.instance_info(match.group(1))
                return

            match = re.match("/api/image/(.*)", self.path)
            if match:
                self.image_info(match.group(1))
                return

            # Admin url
            if not self.demo.auth.is_admin(self.user.login):
                self.send_http_error(404, 'No action')
                return

            if self.path == "/api/allinstance":
                self.all_instances_info()
                return

            if self.path == "/api/poolinstance":
                self.pool_instances_info()
                return

            self.send_http_error(404, 'No action')
        except DemoExceptionInstanceNotFound as e:
            self.send_http_error(404, e.message)
        except (DemoExceptionErrorAuth, DemoExceptionInvalidOwner) as e:
            if self.config.security_type == 'email':
                type = 'email'
            else:
                type = 'auth'
            self.send_http_error(401, e.message, type)
        except DemoExceptionToMuchInstanceImage as e:
            self.send_http_error(503, e.message, str(type(e)))
        except Exception as e:
            if self.config.dev:
                raise
            self.send_http_error(500, e.message, str(type(e)))
        return

    def do_PUT(self):
        try:
            length = int(self.headers.getheader('Content-Length'))
            put_vars = json.loads(self.rfile.read(length))

            # Public
            match = re.match("/api/user", self.path)
            if match:
                if 'email' in put_vars:
                    url = 'http://'+self.headers.getheader('Host')+'/'
                    email = put_vars['email']
                    user = self.demo.create_user(email)
                    self.demo.mail.send_token_mail(user.login, user.token, url)
                    self.send_all_header()
                    return
                else:
                    self.send_http_error(400, 'Email not found in request')
                    return

            # Private
            if not self.cookie_session():
                return

            match = re.match("/api/instance/(.*)", self.path)
            if match:
                time = None
                if 'time' in put_vars:
                    time = int(put_vars['time'])
                self.instance_create(match.group(1), time=time)
                return
            self.send_http_error(404, 'No action')
        except DemoExceptionInstanceNotFound as e:
            self.send_http_error(404, e.message)
        except DemoExceptionToMuchInstanceImage as e:
            self.send_http_error(400, e.message)
        except (DemoExceptionErrorAuth, DemoExceptionInvalidOwner) as e:
            if self.config.security_type == 'email':
                type = 'email'
            else:
                type = 'auth'
            self.send_http_error(401, e.message, type)
        except Exception as e:
            if self.config.dev:
                raise
            self.send_http_error(500, e.message, str(type(e)))
        return

    def do_POST(self):
        try:
            length = int(self.headers.getheader('Content-Length'))
            put_vars = json.loads(self.rfile.read(length))

            # Public
            if self.path == '/api/connect':
                if 'user' in put_vars and 'password' in put_vars and\
                        self.demo.auth:
                    self.connect(put_vars['user'], put_vars['password'])
                    return
                self.send_http_error(404, 'No action')

            # Private
            if not self.cookie_session():
                return

            match = re.match("/api/instance", self.path)
            if match:
                if 'id' in put_vars:
                    id = put_vars['id']
                    if 'add_time' in put_vars:
                        self.demo.check_user_own_instance(self.user.token, id)
                        self.demo.instance_add_time(
                            id,
                            int(put_vars['add_time'])
                        )
                        self.instance_info(id)
                        return
                    # Admin url
                    if not self.demo.auth.is_admin(self.user.login):
                        self.send_http_error(404, 'No action')
                        return
                    if 'time' in put_vars:
                        self.demo.instance_set_life_time(
                            id, int(put_vars['time'])
                        )
                        self.send_http_message(200, 'ok')
                        return
            self.send_http_error(404, 'No action')
        except DemoExceptionInstanceNotFound as e:
            self.send_http_error(404, e.message)
        except DemoExceptionNonUpdatableInstance as e:
            self.send_http_error(400, e.message)
        except (DemoExceptionErrorAuth, DemoExceptionInvalidOwner) as e:
            if self.config.security_type == 'email':
                type = 'email'
            else:
                type = 'auth'
            self.send_http_error(401, e.message, type)
        except Exception as e:
            if self.config.dev:
                raise
            self.send_http_error(500, e.message)
        return

    def do_DELETE(self):
        try:
            if not self.cookie_session():
                return

            match = re.match("/api/instance/(.*)", self.path)
            if match:
                provider_id = match.group(1)
                self.demo.check_user_own_instance(
                    self.user.token,
                    provider_id
                )
                self.demo.database_remove_server(provider_id)
                self.send_http_message(200, 'ok')
                return
            self.send_http_error(404, 'No action')
        except DemoExceptionInstanceNotFound as e:
            self.send_http_error(404, e.message)
        except (DemoExceptionErrorAuth, DemoExceptionInvalidOwner) as e:
            if self.config.security_type == 'email':
                type = 'email'
            else:
                type = 'auth'
            self.send_http_error(401, e.message, type)
        except Exception as e:
            if self.config.dev:
                raise
            self.send_http_error(500, e.message)
        return

    def cookie_session(self):
        token = self.read_cookie(COOKIE_SESSION_NAME)
        if token is not None:
            self.user = self.demo.get_user_by_token(token)
            if self.user:
                self.demo.update_user_last_connection(self.user.login)
                # Update session time
                self.write_cookie(COOKIE_SESSION_NAME, self.user.token)
                if self.user:
                    return True

        if self.config.security_type == 'open':
            self.user = self.demo.create_user()
            self.write_cookie(COOKIE_SESSION_NAME, self.user.token)
        else:
            if self.config.security_type == 'email':
                type = 'email'
            else:
                type = 'auth'
            raise DemoExceptionErrorAuth
            return False
        return True

    def write_cookie(self, name, value, age=999999999999):
        c = Cookie.SimpleCookie()
        c[name] = value
        c[name]['max-age'] = age
        c[name]['path'] = '/'
        logging.debug('New cookie : %s %s', name, value)
        self.headers_to_send['Set-Cookie'] = c.output(header='')

    def read_cookie(self, name):
        if "Cookie" in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])
            logging.debug(" Cookies : %s", self.headers["Cookie"])
            if name not in c:
                return None
            return c[name].value
        return None


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

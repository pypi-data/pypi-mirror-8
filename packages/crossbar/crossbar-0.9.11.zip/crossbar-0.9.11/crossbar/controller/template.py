###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU Affero General Public License, version 3,
##  as published by the Free Software Foundation.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
##  GNU Affero General Public License for more details.
##
##  You should have received a copy of the GNU Affero General Public License
##  along with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

__all__ = ['Templates']


import sys
import os
import shutil
import pkg_resources
import jinja2



class Templates:
   """
   Crossbar.io application templates.
   """

   SKIP_FILES = ('.pyc', '.pyo', '.exe')
   """
   File extensions of files to skip when instantiating an application template.
   """

   TEMPLATES = [
      {
         "name": "default",
         "help": "A WAMP router speaking WebSocket plus a static Web server.",
         "basedir": "templates/default",
         "params": {
         }
      },

      {
         "name": "hello:python",
         "help": "A minimal Python WAMP application hosted in a router and a HTML5 client.",
         "basedir": "templates/hello/python",
         "params": {
            "appname": "hello",
            "realm": "realm1",
         }
      },

      {
         "name": "hello:nodejs",
         "help": "A minimal NodeJS WAMP application hosted in a router and a HTML5 client.",
         "basedir": "templates/hello/nodejs",
         "params": {
            "appname": "hello",
            "realm": "realm1",
            "url": "ws://127.0.0.1:8080/ws",
            "nodejs": "/usr/bin/node"
         }
      },

      {
         "name": "hello:cpp",
         "help": "A minimal C++11/AutobahnCpp WAMP application hosted in a router and a HTML5 client.",
         "get_started_hint": "Now build the example by doing 'scons', start Crossbar using 'crossbar start' and open http://localhost:8080 in your browser.",
         "basedir": "templates/hello/cpp",
         "params": {
         },
      },

      {
         "name": "hello:csharp",
         "help": "A minimal C#/WampSharp WAMP application hosted in a router and a HTML5 client.",
         "get_started_hint": "Now build by opening 'src/Hello/Hello.sln' in Visual Studio, start Crossbar using 'crossbar start' and open http://localhost:8080 in your browser.",
         "basedir": "templates/hello/csharp",
         "params": {
         },
         "skip_jinja": []
      },

      {
         "name": "hello:erlang",
         "help": "A minimal Erlang/Erwa WAMP application hosted in a router and a HTML5 client.",
         "get_started_hint": "Now build the Erlang/Erwa client by entering 'make', start Crossbar using 'crossbar start' and open http://localhost:8080 in your browser.",
         "basedir": "templates/hello/erlang",
         "params": {
         },

         ## due to Erlang's common use of "{{" and "}}" in syntax, we reconfigure
         ## the escape characters used in Jinja templates
         "jinja": {
            "block_start_string": "@@",
            "block_end_string": "@@",
            "variable_start_string": "@=",
            "variable_end_string": "=@",
            "comment_start_string": "@#",
            "comment_end_string": "#@",
         },

         ## we need to skip binary files from being processed by Jinja
         ##
         "skip_jinja": ["relx"]
      },

      {
         "name": "hello:php",
         "help": "A minimal PHP/Thruway WAMP application hosted in a router and a HTML5 client.",
         "get_started_hint": "Now install dependencies for the PHP/Thruway client by entering 'make install', start Crossbar using 'crossbar start' and open http://localhost:8080 in your browser.",
         "basedir": "templates/hello/php",
         "params": {
         },
      },

      {
         "name": "hello:java",
         "help": "A minimal Java/jawampa WAMP application hosted in a router and a HTML5 client.",
         "get_started_hint": "Please follow the README.md to build the Java component first, then start Crossbar using 'crossbar start' and open http://localhost:8080 in your browser.",
         "basedir": "templates/hello/java",
         "params": {
         },
      },

      {
         "name": "votes:browser",
         "help": "Demo that casts live votes synchronized across HTML5 clients. Backend runs in the browser.",
         "basedir": "templates/votes/browser",
         "params": {
         },
         "skip_jinja": ['banana_small.png', 'chocolate_small.png', 'crossbar_icon_inverted.png', 'lemon_small.png', 'favicon.ico']
      },

      {
         "name": "votes:nodejs",
         "help": "Demo that casts live votes synchronized across HTML5 clients. Backend runs in NodeJS.",
         "basedir": "templates/votes/nodejs",
         "params": {
            "nodejs": "C:/Program Files (x86)/nodejs/node.exe"
         },
         "skip_jinja": ['banana_small.png', 'chocolate_small.png', 'crossbar_icon_inverted.png', 'lemon_small.png', 'favicon.ico']
      },

      {
         "name": "votes:python",
         "help": "Demo that casts live votes synchronized across HTML5 clients. Backend runs in Python.",
         "basedir": "templates/votes/python",
         "params": {
         },
         "skip_jinja": ['banana_small.png', 'chocolate_small.png', 'crossbar_icon_inverted.png', 'lemon_small.png', 'favicon.ico']
      },

      {
         "name": "demos",
         "help": "A Crossbar.io node running the crossbardemo package. Requires 'pip install crossbardemo'.",
         "basedir": "templates/demos",
         "params": {
         }
      },

      {
         "name": "pusher",
         "help": "A WAMP router with a HTTP gateway for pushing events.",
         "basedir": "templates/pusher",
         "params": {
         }
      },

      {
         "name": "longpoll",
         "help": "Demonstrates WAMP longpoll transport for old browsers.",
         "basedir": "templates/longpoll",
         "params": {
         }
      },

      {
         "name": "expressjs",
         "help": "Using Crossbar.io, Node and Express.",
         "basedir": "templates/expressjs",
         "params": {
         },
         "skip_jinja": ["index.html", "base.html", "monitor.html"]
      },

      {
         "name": "flash",
         "help": "Demonstrates using the Flash WebSocket implementation for old browsers.",
         "basedir": "templates/flash",
         "params": {
         },
         "skip_jinja": ["WebSocketMain.swf"]
      },

      {
         "name": "pg:publisher",
         "help": "Demonstrates how to publish WAMP events from within PostgreSQL.",
         "basedir": "templates/pg/publisher",
         "params": {
            "schema": "crossbar"
         },
         "get_started_hint": """
Now build the example by doing 'scons', start Crossbar using 'crossbar start'
and open http://localhost:8080 in your browser.         
         """
      },

      {
         "name": "oracle:publisher",
         "help": "Demonstrates how to publish WAMP events from within Oracle database.",
         "basedir": "templates/oracle/publisher",
         "params": {
            "cbadapter": "cbadapter",
            "cbadapter_password": "crossbar",
            "cbdb": "cbdb",
            "cbdb_password": "crossbar",
            "cbdb_tablespace": "users",
            "cbadapter": "cbadapter",
            "nchar_maxlen": 2000,
            "pipe_onpublish": "crossbar_on_publish",
            "pipe_onexport": "crossbar_on_export"
         },
         "get_started_hint": """Now install the Crossbar.io Oracle database integration by doing:

   cd database
   make create_users
   make install

Then start Crossbar.io (from the current directory):

   crossbar start

and open your browser pointing to http://localhost:8080.
         """
      },

      {
         "name": "authenticate:wampcra",
         "help": "Demonstrates authentication via WAMP-CRA from a static user database defined in the node configuration.",
         "basedir": "templates/authenticate/wampcra",
         "params": {
         }
      },

      {
         "name": "authenticate:wampcradynamic:python",
         "help": "Demonstrates authentication via WAMP-CRA from a user-defined authenticator procedure written in Python.",
         "basedir": "templates/authenticate/wampcradynamic/python",
         "params": {
         }
      },

      {
         "name": "authenticate:wampcradynamic:nodejs",
         "help": "Demonstrates authentication via WAMP-CRA from a user-defined authenticator procedure written in JavaScript.",
         "basedir": "templates/authenticate/wampcradynamic/nodejs",
         "params": {
         }
      },

      {
         "name": "authenticate:wampcradynamic:php",
         "help": "Demonstrates authentication via WAMP-CRA from a user-defined authenticator procedure written in PHP.",
         "basedir": "templates/authenticate/wampcradynamic/php",
         "params": {
         }
      },

      {
         "name": "wss:python",
         "help": "Using secure WebSocket transports (wss) with JavaScript frontend and Python backend.",
         "basedir": "templates/wss/python",
         "params": {
         },
         "get_started_hint": """Start Crossbar using 'crossbar start' and open https://localhost:8080 in your browser (note the 'https' in the URL).
For more info, please visit http://crossbar.io/docs/Secure-WebSocket-and-HTTPS/
"""
      },
   ]
   """
   Application template definitions.
   """


   def help(self):
      """
      Print CLI help.
      """
      print("\nAvailable Crossbar.io node templates:\n")
      for t in self.TEMPLATES:
         print("  {} {}".format(t['name'].ljust(16, ' '), t['help']))
      print("")



   def __contains__(self, template):
      """
      Check if template exists.

      :param template: The name of the application template to check.
      :type template: str
      """
      for t in self.TEMPLATES:
         if t['name'] == template:
            return True
      return False



   def __getitem__(self, template):
      """
      Get template by name.

      :param template: The name of the application template to get.
      :type template: str
      """
      for t in self.TEMPLATES:
         if t['name'] == template:
            return t
      raise KeyError



   def init(self, appdir, template, params = None, dryrun = False):
      """
      Ctor.


      :param appdir: The path of the directory to instantiate the application template in.
      :type appdir: str
      :param template: The name of the application template to instantiate.
      :type template: str
      :param dryrun: If `True`, only perform a dry run (don't actually do anything, only prepare).
      :type dryrun: bool
      """
      IS_WIN = sys.platform.startswith("win")

      template = self.__getitem__(template)
      basedir = pkg_resources.resource_filename("crossbar", template['basedir'])
      if IS_WIN:
         basedir = basedir.replace('\\', '/') # Jinja need forward slashes even on Windows
      print("Using template from '{}'".format(basedir))

      appdir = os.path.abspath(appdir)

      if 'jinja' in template:
         kwargs = template['jinja']
      else:
         kwargs = {}

      jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(basedir),
         keep_trailing_newline = True, **kwargs)

      _params = template['params'].copy()
      if params:
         _params.update(params)

      created = []
      try:
         for root, dirs, files in os.walk(basedir):
            for d in dirs:
               reldir = os.path.relpath(os.path.join(root, d), basedir)
               if 'appname' in _params:
                  reldir = reldir.replace('appname', _params['appname'])
               create_dir_path = os.path.join(appdir, reldir)

               print("Creating directory {}".format(create_dir_path))
               if not dryrun:
                  os.mkdir(create_dir_path)
               created.append(('dir', create_dir_path))

            for f in files:

               if not f.endswith(Templates.SKIP_FILES):

                  src_file = os.path.abspath(os.path.join(root, f))
                  src_file_rel_path = os.path.relpath(src_file, basedir)
                  reldir = os.path.relpath(root, basedir)
                  if 'appname' in _params:
                     reldir = reldir.replace('appname', _params['appname'])
                     f = f.replace('appname', _params['appname'])
                  dst_dir_path = os.path.join(appdir, reldir)
                  dst_file = os.path.abspath(os.path.join(dst_dir_path, f))

                  print("Creating file      {}".format(dst_file))
                  if not dryrun:
                     if f in template.get('skip_jinja', []):
                        shutil.copy(src_file, dst_file)
                     else:
                        with open(dst_file, 'wb') as dst_file_fd:
                           if IS_WIN:
                              # Jinja need forward slashes even on Windows
                              src_file_rel_path = src_file_rel_path.replace('\\', '/')
                           page = jinja_env.get_template(src_file_rel_path)
                           contents = page.render(**_params).encode('utf8')
                           dst_file_fd.write(contents)

                  created.append(('file', dst_file))

         # force exception to test rollback
         #a = 1/0

         return template.get('get_started_hint', None)

      except Exception as e:
         print("Error encountered ({}) - rolling back".format(e))
         for ptype, path in reversed(created):
            if ptype == 'file':
               try:
                  print("Removing file {}".format(path))
                  if not dryrun:
                     os.remove(path)
               except:
                  print("Warning: could not remove file {}".format(path))
            elif ptype == 'dir':
               try:
                  print("Removing directory {}".format(path))
                  if not dryrun:
                     os.rmdir(path)
               except:
                  print("Warning: could not remove directory {}".format(path))
            else:
               raise Exception("logic error")
         raise e

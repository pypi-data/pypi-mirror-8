djehuty
=======

post webhook manager written in Python

environment
-----------

- Python2.7 expected.

install
-------

You can use pip.

::

  $ pip install djehuty

create djehuty app on heroku
----------------------------

::

   $ pcreate -s djehuty_server YOUR_PROJECT_NAME
   $ cd YOUR_PROJECT_NAME
   $ git init
   $ heroku create

You can add existing services and commands...

add service package in requirements.txt for dependency::

  cliff==1.6.1
  pyramid==1.5.1
  cornice==0.16.2
  uWSGI==2.0.6
  djehuty==0.0.4
  # add service package.
  djehutyslack==0.0.4
  # add command package.
  djehutylgtm==0.0.1
  -e .

add pyramid.includes entry in ini-paste for pyramid extension::

  pyramid.default_locale_name = en
  pyramid.includes =
         djehuty
  # add module name that has "includeme" interface.
         djehutyslack

or implement your custom service in YOUR_PROJECT_NAME/YOUR_PROJECT_NAME/services.py.

implement custom service
------------------------

Example code with comments from djehutyslack<https://github.com/xica/djehutyslack/>.

djehutyslack/djehutyslack/slack.py

.. code:: python

  # ..snipped..

  from djehuty.service import Service


  # inherit djehuty.service.Service.
  class Slack(Service):

      # add validation(authorization token, user credential, and so on) process.
      def validate(self, request):
          token = request.params.get('token')
          if not token or token != os.environ.get('DJEHUTY_SLACK_OUTGOING_TOKEN'):
              raise HTTPUnauthorized()

      # parse web hook request and return global argument for command.Command.app_args.
      def get_service_argument(self, name, request):
          if name == 'user':
              return request.params.get('user_name')
          elif name == 'room':
              return request.params.get('channel_name')
          else:
              raise ValueError('invalid argument name "{}"'.format(name))

      # parse web hook request and return "argv" list for app.App.run.
      def make_command_line(self, request):
          m = re.match(
              r'^{}\W*(.*)$'.format(request.params.get('trigger_word', '')),
              request.params.get('text', '')
          )
          return shlex.split(m.group(1).encode('utf8')) if m is not None else []

      # convert value returned by Command.take_action into appropriate response.
      def make_response(self, result):
          return {
              'text': result,
              'link_names': 1,
              'parse': 'full',
          }

  # explicit instantiation required.
  slack = Slack()

implement service only package
--------------------------------------

If you want to publish your service, you need to implement it as a stand-alone python package and should provide "includeme" interface.

::

   $ pcreate -s djehuty_service YOUR_SERVICE_PROJECT_NAME
   $ cd YOUR_SERVICE_PROJECT_NAME
   (implement your service and publish it as git repository or PyPI package...)

"includeme" example code with comments from djehutyslack.

djehutyslack/djehutyslack/__init__.py

.. code:: python

  def includeme(config):

    config.scan('djehutyslack.slack')

implement service in server package
-----------------------------------

Or if you need not publish your service, simply implement it in your server package and use "config.scan".

.. code:: python

  from pyramid.config import Configuration

  # pyramid entry point.
  def main(global_config, **settings):
      config = Configurator(settings=settings)
      # import your service module into Pyramid by "config.scan".
      config.scan('YOUR_PROJECT_NAME.SERVICE_MODULE_NAME')
      return config.make_wsgi_app()

implement and add custom command
--------------------------------

djehuty.command.Command is almost cliff<http://cliff.readthedocs.org/en/latest/> command.After implementing your command, add command name and command class module path in setup.py entry_points.

Example code with comments from djehuty.command.yo.

.. code:: python

  from djehuty.command import Command


  # inherit djehuty.command.Command.
  class Yo(Command):
      '''echo yo'''  # add description for help.

      # add argparse style argument and return parser.
      def get_parser(self, prog_name):
          parser = Command.get_parser(self, prog_name)
          parser.add_argument('-g', '--greeting',
                              default='yo',
                              help='greeting message')
          return parser

      # return response text.
      def take_action(self, parsed_args):
          return ('@{} '.format(self.app_args.user) if self.app_args.user else '') + parsed_args.greeting

entry_points example code with comments from djehutylgtm<https://github.com/xica/djehutylgtm/>.

djehutylgtm/setup.py

.. code:: python

  # ..snipped..

  setup(
      name='djehutylgtm',
      # ..snipped..
      entry_points={
          'djehuty.commands': [
              'lgtm = djehutylgtm.commands:LGTM',
          ],
      },
  )

implement command only package
--------------------------------------

Like a service, if you want to publish your command, you need to implement it as a stand-alone python package.

::

   $ pcreate -s djehuty_command YOUR_COMMAND_PROJECT_NAME
   $ cd YOUR_COMMAND_PROJECT_NAME
   (implement your command and publish it as git repository or PyPI package...)

todo
----

- Python 3 support
- unit test

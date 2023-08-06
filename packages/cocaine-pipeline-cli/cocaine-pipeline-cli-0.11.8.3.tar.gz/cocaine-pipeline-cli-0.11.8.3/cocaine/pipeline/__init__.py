#!/usr/bin/env python
# encoding: utf-8
#
#    Copyright (c) 2013-2014+ Anton Tyurin <noxiouz@yandex.ru>
#    Copyright (c) 2013-2014 Other contributors as noted in the AUTHORS file.
#
#    This file is part of Cocaine.
#
#    Cocaine is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Cocaine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function

import json
import logging
import os
import sys

from tornado.options import define, options
from tornado import httpclient
from tornado.options import parse_command_line, parse_config_file
from tornado.ioloop import IOLoop
from tornado.httpclient import HTTPRequest

log = logging.getLogger()

AppGroup = "Application"
CocaineGroup = "Cocaine"
ActionGroup = "Actions"

POSSIBLE_ACTIONS = ('upload', 'deploy', 'start', 'stop',
                    'listing', 'undeploy', 'info', 'remove')
API_VERSION = 1.3
DEFAULT_REQUEST_TIMEOUT = 200


class Dispatcher(object):
    dispatch_tree = {}

    @classmethod
    def attach(cls, action_name):
        def wrapper(func):
            cls.dispatch_tree[action_name] = func
            return func
        return wrapper

    @classmethod
    def run(cls, action):
        return cls.dispatch_tree[action]()


def printer(data):
    print(data, end="" if data.endswith('\r') else "\n",
          file=sys.stderr)


def run_request(req):
    req.connect_timeout = 5
    req.request_timeout = options.timeout
    req.allow_ipv6 = True
    IOLoop.instance().run_sync(lambda: client.fetch(req))


def gen_url(url):
    return "http://%s:%d/%s" % (options.host, options.port, url)


def default_format_reply(body):
    printer(body)


def jail(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as err:
            log.error(err)
            exit(1)
    return wrapper


# AppGroup
define('appname', group=AppGroup,
       help='application name',
       type=str, default=None),

define('version', group=AppGroup,
       help='version',
       type=str, default=None)

define('url', group=AppGroup,
       help='repository url',
       type=str, default=None)

define('profile', group=AppGroup,
       help='profile to deploy with',
       type=str, default=None)

define('manifest', group=AppGroup,
       help='specify manifest path, which would be used',
       type=str, default="")

define('weight', group=AppGroup,
       help='application weight in group',
       type=int, default=0)

define('username', group=CocaineGroup,
       help='username',
       type=str)

define('wildcard', group=CocaineGroup,
       help='wildcard', default='*',
       type=str)

define('environment', group=CocaineGroup,
       help='specify environment', default="",
       type=str)

# CocaineGroup
define('host', group=CocaineGroup,
       help='Host of buildfarm locator',
       type=str, default="localhost")

define('port', group=CocaineGroup,
       help='Port of buildfarm locator',
       type=int, default=80)

define('timeout', group=CocaineGroup,
       help='Request timeout',
       type=int, default=DEFAULT_REQUEST_TIMEOUT)

# ActionGroup
define('action', group=ActionGroup,
       help='action name (%s)' % '|'.join(POSSIBLE_ACTIONS),
       type=str, default=None)


client = httpclient.AsyncHTTPClient()


def check_options():
    try:
        if options.action not in POSSIBLE_ACTIONS:
            log.error("Option 'action' must be one of %s",
                      ', '.join(POSSIBLE_ACTIONS))
            raise Exception()
        if options.username is None:
            log.error("Specify username by --username option")
            raise Exception()
    except Exception:
        options.print_help()
        exit(1)


def gen_task(task):
    return json.dumps({"task": task,
                       "API": API_VERSION,
                       "username": options.username})


@Dispatcher.attach("upload")
@jail
def upload():
    task = {"appname": options.appname,
            "version": options.version,
            "environment": options.environment,
            "url": options.url,
            "manifest": options.manifest}

    task = gen_task(task)
    req = HTTPRequest(gen_url("upload"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("start")
@jail
def start():
    task = {"appname": options.appname,
            "environment": options.environment,
            "version": options.version}
    if options.profile:
        task["profilename"] = options.profile

    task = gen_task(task)
    req = HTTPRequest(gen_url("start"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("stop")
@jail
def stop():
    task = {"appname": options.appname,
            "environment": options.environment,
            "version": options.version}

    task = gen_task(task)
    req = HTTPRequest(gen_url("stop"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("deploy")
@jail
def deploy():
    log.info("Application %s would be deployed with profile %s."
             " Its weight would be %d",
             options.appname,
             options.profile, options.weight)
    task = {"appname": options.appname,
            "version": options.version,
            "profilename": options.profile,
            "environment": options.environment,
            "weight": options.weight}

    task = gen_task(task)
    req = HTTPRequest(gen_url("deploy"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("undeploy")
@jail
def undeploy():
    log.info("Application %s would be undeployed with profile.",
             options.appname)
    task = {"appname": options.appname,
            "environment": options.environment,
            "version": options.version}

    task = gen_task(task)
    req = HTTPRequest(gen_url("undeploy"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("remove")
@jail
def remove():
    log.info("Application %s would be undeployed with profile.",
             options.appname)
    task = {"appname": options.appname,
            "environment": options.environment,
            "version": options.version}

    task = gen_task(task)
    req = HTTPRequest(gen_url("remove"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("listing")
@jail
def listing():
    log.info("Fetching a list of your applications according to wildcard %s",
             options.wildcard)
    task = {
        "environment": options.environment
    }
    if options.wildcard:
        task["wildcard"] = options.wildcard

    def format_reply(body):
        try:
            apps = json.loads(body)
        except Exception:
            log.info("%s", body)
            return

        if len(apps) == 0:
            print('There are no applications with your username')
            return
        for app, status in apps.iteritems():
            user, appname = app.split('_', 1)
            appname, version = appname.rsplit('_', 1)
            print(user, '\t', appname, '\t\t', version, '\t\t', status)

    task = gen_task(task)
    req = HTTPRequest(gen_url("listing"),
                      method="POST",
                      streaming_callback=format_reply,
                      body=task)
    run_request(req)


@Dispatcher.attach("info")
@jail
def info():
    log.info("Fetching a list of your applications")
    task = gen_task(None)
    req = HTTPRequest(gen_url("info"),
                      method="POST",
                      streaming_callback=default_format_reply,
                      body=task)
    run_request(req)


CONF_CANDIDATES = (os.path.expanduser("~/.cocaine.conf"),
                   ".cocaine.conf")


def main():
    try:
        for path in filter(os.path.exists, CONF_CANDIDATES):
            parse_config_file(path, final=False)
        options.add_parse_callback(check_options)
        parse_command_line()
    except Exception as err:
        print("unable to parse options: %s" % err, file=sys.stderr)
        exit(1)
    log.info("user `%s` is working with cloud at %s:%d",
             options.username, options.host, options.port)
    Dispatcher.run(options.action)


if __name__ == '__main__':
    main()

# Copyright (c) 2014 Christian Schwede <christian.schwede@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import os
import tempfile
import unittest

import six

import swiftclient
import swiftclient.shell
import swiftclient.utils

from os.path import basename, dirname

if six.PY2:
    BUILTIN_OPEN = '__builtin__.open'
else:
    BUILTIN_OPEN = 'builtins.open'

mocked_os_environ = {
    'ST_AUTH': 'http://localhost:8080/auth/v1.0',
    'ST_USER': 'test:tester',
    'ST_KEY': 'testing'
}


@mock.patch.dict(os.environ, mocked_os_environ)
class TestShell(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestShell, self).__init__(*args, **kwargs)
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        self.tmpfile = tmpfile.name

    def tearDown(self):
        try:
            os.remove(self.tmpfile)
        except OSError:
            pass

    @mock.patch('swiftclient.shell.OutputManager._print')
    @mock.patch('swiftclient.service.Connection')
    def test_stat_account(self, connection, mock_print):
        argv = ["", "stat"]
        return_headers = {
            'x-account-container-count': '1',
            'x-account-object-count': '2',
            'x-account-bytes-used': '3',
            'content-length': 0,
            'date': ''}
        connection.return_value.head_account.return_value = return_headers
        connection.return_value.url = 'http://127.0.0.1/v1/AUTH_account'
        swiftclient.shell.main(argv)
        calls = [mock.call('   Account: AUTH_account\n' +
                           'Containers: 1\n' +
                           '   Objects: 2\n' +
                           '     Bytes: 3')]
        mock_print.assert_has_calls(calls)

    @mock.patch('swiftclient.shell.OutputManager._print')
    @mock.patch('swiftclient.service.Connection')
    def test_stat_container(self, connection, mock_print):
        return_headers = {
            'x-container-object-count': '1',
            'x-container-bytes-used': '2',
            'x-container-read': 'test2:tester2',
            'x-container-write': 'test3:tester3',
            'x-container-sync-to': 'other',
            'x-container-sync-key': 'secret',
        }
        argv = ["", "stat", "container"]
        connection.return_value.head_container.return_value = return_headers
        connection.return_value.url = 'http://127.0.0.1/v1/AUTH_account'
        swiftclient.shell.main(argv)
        calls = [mock.call('  Account: AUTH_account\n' +
                           'Container: container\n' +
                           '  Objects: 1\n' +
                           '    Bytes: 2\n' +
                           ' Read ACL: test2:tester2\n' +
                           'Write ACL: test3:tester3\n' +
                           '  Sync To: other\n' +
                           ' Sync Key: secret')]
        mock_print.assert_has_calls(calls)

    @mock.patch('swiftclient.shell.OutputManager._print')
    @mock.patch('swiftclient.service.Connection')
    def test_stat_object(self, connection, mock_print):
        return_headers = {
            'x-object-manifest': 'manifest',
            'etag': 'md5',
            'last-modified': 'yesterday',
            'content-type': 'text/plain',
            'content-length': 42,
        }
        argv = ["", "stat", "container", "object"]
        connection.return_value.head_object.return_value = return_headers
        connection.return_value.url = 'http://127.0.0.1/v1/AUTH_account'
        swiftclient.shell.main(argv)
        calls = [mock.call('       Account: AUTH_account\n' +
                           '     Container: container\n' +
                           '        Object: object\n' +
                           '  Content Type: text/plain\n' +
                           'Content Length: 42\n' +
                           ' Last Modified: yesterday\n' +
                           '          ETag: md5\n' +
                           '      Manifest: manifest')]
        mock_print.assert_has_calls(calls)

    @mock.patch('swiftclient.shell.OutputManager._print')
    @mock.patch('swiftclient.service.Connection')
    def test_list_account(self, connection, mock_print):
        # Test account listing
        connection.return_value.get_account.side_effect = [
            [None, [{'name': 'container'}]],
            [None, []],
        ]

        argv = ["", "list"]
        swiftclient.shell.main(argv)
        calls = [mock.call(marker='', prefix=None),
                 mock.call(marker='container', prefix=None)]
        connection.return_value.get_account.assert_has_calls(calls)
        calls = [mock.call('container')]
        mock_print.assert_has_calls(calls)

    @mock.patch('swiftclient.shell.OutputManager._print')
    @mock.patch('swiftclient.service.Connection')
    def test_list_container(self, connection, mock_print):
        connection.return_value.get_container.side_effect = [
            [None, [{'name': 'object_a'}]],
            [None, []],
        ]
        argv = ["", "list", "container"]
        swiftclient.shell.main(argv)
        calls = [
            mock.call('container', marker='', delimiter=None, prefix=None),
            mock.call('container', marker='object_a',
                      delimiter=None, prefix=None)]
        connection.return_value.get_container.assert_has_calls(calls)
        calls = [mock.call('object_a')]
        mock_print.assert_has_calls(calls)

        # Test container listing with --long
        connection.return_value.get_container.side_effect = [
            [None, [{'name': 'object_a', 'bytes': 0,
                     'last_modified': '123T456'}]],
            [None, []],
        ]
        argv = ["", "list", "container", "--long"]
        swiftclient.shell.main(argv)
        calls = [
            mock.call('container', marker='', delimiter=None, prefix=None),
            mock.call('container', marker='object_a',
                      delimiter=None, prefix=None)]
        connection.return_value.get_container.assert_has_calls(calls)
        calls = [mock.call('object_a'),
                 mock.call('           0        123      456 object_a'),
                 mock.call('           0')]
        mock_print.assert_has_calls(calls)

    @mock.patch('swiftclient.service.makedirs')
    @mock.patch('swiftclient.service.Connection')
    def test_download(self, connection, makedirs):
        connection.return_value.get_object.return_value = [
            {'content-type': 'text/plain',
             'etag': 'd41d8cd98f00b204e9800998ecf8427e'},
            '']

        # Test downloading whole container
        connection.return_value.get_container.side_effect = [
            [None, [{'name': 'object'}]],
            [None, [{'name': 'pseudo/'}]],
            [None, []],
        ]
        connection.return_value.auth_end_time = 0
        connection.return_value.attempts = 0

        with mock.patch(BUILTIN_OPEN) as mock_open:
            argv = ["", "download", "container"]
            swiftclient.shell.main(argv)
            calls = [mock.call('container', 'object',
                               headers={}, resp_chunk_size=65536,
                               response_dict={}),
                     mock.call('container', 'pseudo/',
                               headers={}, resp_chunk_size=65536,
                               response_dict={})]
            connection.return_value.get_object.assert_has_calls(
                calls, any_order=True)
            mock_open.assert_called_once_with('object', 'wb')

        # Test downloading single object
        with mock.patch(BUILTIN_OPEN) as mock_open:
            argv = ["", "download", "container", "object"]
            swiftclient.shell.main(argv)
            connection.return_value.get_object.assert_called_with(
                'container', 'object', headers={}, resp_chunk_size=65536,
                response_dict={})
            mock_open.assert_called_with('object', 'wb')

    @mock.patch('swiftclient.shell.walk')
    @mock.patch('swiftclient.service.Connection')
    def test_upload(self, connection, walk):
        connection.return_value.head_object.return_value = {
            'content-length': '0'}
        connection.return_value.attempts = 0
        argv = ["", "upload", "container", self.tmpfile,
                "-H", "X-Storage-Policy:one"]
        swiftclient.shell.main(argv)
        connection.return_value.put_container.assert_called_with(
            'container',
            {'X-Storage-Policy': mock.ANY},
            response_dict={})

        connection.return_value.put_object.assert_called_with(
            'container',
            self.tmpfile.lstrip('/'),
            mock.ANY,
            content_length=0,
            headers={'x-object-meta-mtime': mock.ANY,
                     'X-Storage-Policy': 'one'},
            response_dict={})

        # Upload whole directory
        argv = ["", "upload", "container", "/tmp"]
        _tmpfile = self.tmpfile
        _tmpfile_dir = dirname(_tmpfile)
        _tmpfile_base = basename(_tmpfile)
        walk.return_value = [(_tmpfile_dir, [], [_tmpfile_base])]
        swiftclient.shell.main(argv)
        connection.return_value.put_object.assert_called_with(
            'container',
            self.tmpfile.lstrip('/'),
            mock.ANY,
            content_length=0,
            headers={'x-object-meta-mtime': mock.ANY},
            response_dict={})

        # Upload in segments
        connection.return_value.head_container.return_value = {
            'x-storage-policy': 'one'}
        argv = ["", "upload", "container", self.tmpfile, "-S", "10"]
        with open(self.tmpfile, "wb") as fh:
            fh.write(b'12345678901234567890')
        swiftclient.shell.main(argv)
        connection.return_value.put_container.assert_called_with(
            'container_segments',
            {'X-Storage-Policy': mock.ANY},
            response_dict={})
        connection.return_value.put_object.assert_called_with(
            'container',
            self.tmpfile.lstrip('/'),
            '',
            content_length=0,
            headers={'x-object-manifest': mock.ANY,
                     'x-object-meta-mtime': mock.ANY},
            response_dict={})

    @mock.patch('swiftclient.service.Connection')
    def test_delete_account(self, connection):
        connection.return_value.get_account.side_effect = [
            [None, [{'name': 'container'}]],
            [None, []],
        ]
        connection.return_value.get_container.side_effect = [
            [None, [{'name': 'object'}]],
            [None, []],
        ]
        connection.return_value.attempts = 0
        argv = ["", "delete", "--all"]
        connection.return_value.head_object.return_value = {}
        swiftclient.shell.main(argv)
        connection.return_value.delete_container.assert_called_with(
            'container', response_dict={})
        connection.return_value.delete_object.assert_called_with(
            'container', 'object', query_string=None, response_dict={})

    @mock.patch('swiftclient.service.Connection')
    def test_delete_container(self, connection):
        connection.return_value.get_container.side_effect = [
            [None, [{'name': 'object'}]],
            [None, []],
        ]
        connection.return_value.attempts = 0
        argv = ["", "delete", "container"]
        connection.return_value.head_object.return_value = {}
        swiftclient.shell.main(argv)
        connection.return_value.delete_container.assert_called_with(
            'container', response_dict={})
        connection.return_value.delete_object.assert_called_with(
            'container', 'object', query_string=None, response_dict={})

    @mock.patch('swiftclient.service.Connection')
    def test_delete_object(self, connection):
        argv = ["", "delete", "container", "object"]
        connection.return_value.head_object.return_value = {}
        connection.return_value.attempts = 0
        swiftclient.shell.main(argv)
        connection.return_value.delete_object.assert_called_with(
            'container', 'object', query_string=None, response_dict={})

    @mock.patch('swiftclient.service.Connection')
    def test_post_account(self, connection):
        argv = ["", "post"]
        connection.return_value.head_object.return_value = {}
        swiftclient.shell.main(argv)
        connection.return_value.post_account.assert_called_with(
            headers={}, response_dict={})

        argv = ["", "post", "container"]
        connection.return_value.head_object.return_value = {}
        swiftclient.shell.main(argv)
        connection.return_value.post_container.assert_called_with(
            'container', headers={}, response_dict={})

    @mock.patch('swiftclient.service.Connection')
    def test_post_container(self, connection):
        argv = ["", "post", "container",
                "--read-acl", "test2:tester2",
                "--write-acl", "test3:tester3 test4",
                "--sync-to", "othersite",
                "--sync-key", "secret",
                ]
        connection.return_value.head_object.return_value = {}
        swiftclient.shell.main(argv)
        connection.return_value.post_container.assert_called_with(
            'container', headers={
                'X-Container-Write': 'test3:tester3 test4',
                'X-Container-Read': 'test2:tester2',
                'X-Container-Sync-Key': 'secret',
                'X-Container-Sync-To': 'othersite'}, response_dict={})

    @mock.patch('swiftclient.service.Connection')
    def test_post_object(self, connection):
        argv = ["", "post", "container", "object",
                "--meta", "Color:Blue",
                "--header", "content-type:text/plain"
                ]
        connection.return_value.head_object.return_value = {}
        swiftclient.shell.main(argv)
        connection.return_value.post_object.assert_called_with(
            'container', 'object', headers={
                'Content-Type': 'text/plain',
                'X-Object-Meta-Color': 'Blue'}, response_dict={})

    @mock.patch('swiftclient.shell.generate_temp_url')
    def test_temp_url(self, temp_url):
        argv = ["", "tempurl", "GET", "60", "/v1/AUTH_account/c/o",
                "secret_key"
                ]
        temp_url.return_value = ""
        swiftclient.shell.main(argv)
        temp_url.assert_called_with(
            '/v1/AUTH_account/c/o', 60, 'secret_key', 'GET')

    @mock.patch('swiftclient.service.Connection')
    def test_capabilities(self, connection):
        argv = ["", "capabilities"]
        connection.return_value.get_capabilities.return_value = {'swift': None}
        swiftclient.shell.main(argv)
        connection.return_value.get_capabilities.assert_called_with(None)


class TestSubcommandHelp(unittest.TestCase):

    def test_subcommand_help(self):
        for command in swiftclient.shell.commands:
            help_var = 'st_%s_help' % command
            self.assertTrue(help_var in vars(swiftclient.shell))
            out = six.StringIO()
            with mock.patch('sys.stdout', out):
                argv = ['', command, '--help']
                self.assertRaises(SystemExit, swiftclient.shell.main, argv)
            expected = vars(swiftclient.shell)[help_var]
            self.assertEqual(out.getvalue().strip('\n'), expected)

    def test_no_help(self):
        out = six.StringIO()
        with mock.patch('sys.stdout', out):
            argv = ['', 'bad_command', '--help']
            self.assertRaises(SystemExit, swiftclient.shell.main, argv)
        expected = 'no help for bad_command'
        self.assertEqual(out.getvalue().strip('\n'), expected)


class TestParsing(unittest.TestCase):

    def setUp(self):
        super(TestParsing, self).setUp()
        self._orig_environ = os.environ.copy()
        keys = os.environ.keys()
        for k in keys:
            if k in ('ST_KEY', 'ST_USER', 'ST_AUTH'):
                del os.environ[k]

    def tearDown(self):
        os.environ = self._orig_environ

    def _make_fake_command(self, result):
        def fake_command(parser, args, thread_manager):
            result[0], result[1] = swiftclient.shell.parse_args(parser, args)
        return fake_command

    def _make_args(self, cmd, opts, os_opts, separator='-'):
        """
        Construct command line arguments for given options.
        """
        args = [""]
        for k, v in opts.items():
            arg = "--" + k.replace("_", "-")
            args = args + [arg, v]
        for k, v in os_opts.items():
            arg = "--os" + separator + k.replace("_", separator)
            args = args + [arg, v]
        args = args + [cmd]
        return args

    def _make_env(self, opts, os_opts):
        """
        Construct a dict of environment variables for given options.
        """
        env = {}
        for k, v in opts.items():
            key = 'ST_' + k.upper()
            env[key] = v
        for k, v in os_opts.items():
            key = 'OS_' + k.upper()
            env[key] = v
        return env

    def _verify_opts(self, actual_opts, opts, os_opts={}, os_opts_dict={}):
        """
        Check parsed options are correct.

        :param opts: v1 style options.
        :param os_opts: openstack style options.
        :param os_opts_dict: openstack options that should be found in the
                             os_options dict.
        """
        # check the expected opts are set
        for key, v in opts.items():
            actual = getattr(actual_opts, key)
            self.assertEqual(v, actual, 'Expected %s for key %s, found %s'
                                        % (v, key, actual))

        for key, v in os_opts.items():
            actual = getattr(actual_opts, "os_" + key)
            self.assertEqual(v, actual, 'Expected %s for key %s, found %s'
                                        % (v, key, actual))

        # check the os_options dict values are set
        self.assertTrue(hasattr(actual_opts, 'os_options'))
        actual_os_opts_dict = getattr(actual_opts, 'os_options')
        expected_os_opts_keys = ['project_name', 'region_name',
                                 'tenant_name',
                                 'user_domain_name', 'endpoint_type',
                                 'object_storage_url', 'project_domain_id',
                                 'user_id', 'user_domain_id', 'tenant_id',
                                 'service_type', 'project_id', 'auth_token',
                                 'project_domain_name']
        for key in expected_os_opts_keys:
            self.assertTrue(key in actual_os_opts_dict)
            cli_key = key
            if key == 'object_storage_url':
                # exceptions to the pattern...
                cli_key = 'storage_url'
            if cli_key in os_opts_dict:
                expect = os_opts_dict[cli_key]
            else:
                expect = None
            actual = actual_os_opts_dict[key]
            self.assertEqual(expect, actual, 'Expected %s for %s, got %s'
                             % (expect, key, actual))
        for key in actual_os_opts_dict:
            self.assertTrue(key in expected_os_opts_keys)

        # check that equivalent keys have equal values
        equivalents = [('os_username', 'user'),
                       ('os_auth_url', 'auth'),
                       ('os_password', 'key')]
        for pair in equivalents:
            self.assertEqual(getattr(actual_opts, pair[0]),
                             getattr(actual_opts, pair[1]))

    def test_minimum_required_args_v3(self):
        opts = {"auth_version": "3"}
        os_opts = {"password": "secret",
                   "username": "user",
                   "auth_url": "http://example.com:5000/v3"}

        # username with domain is sufficient in args because keystone will
        # assume user is in default domain
        args = self._make_args("stat", opts, os_opts, '-')
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, {})

        # check its ok to have user_id instead of username
        os_opts = {"password": "secret",
                   "auth_url": "http://example.com:5000/v3"}
        os_opts_dict = {"user_id": "user_ID"}
        all_os_opts = os_opts.copy()
        all_os_opts.update(os_opts_dict)

        args = self._make_args("stat", opts, all_os_opts, '-')
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, os_opts_dict)

        # check no user credentials required if token and url supplied
        os_opts = {}
        os_opts_dict = {"storage_url": "http://example.com:8080/v1",
                        "auth_token": "0123abcd"}

        args = self._make_args("stat", opts, os_opts_dict, '-')
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, os_opts_dict)

    def test_args_v3(self):
        opts = {"auth_version": "3"}
        os_opts = {"password": "secret",
                   "username": "user",
                   "auth_url": "http://example.com:5000/v3"}
        os_opts_dict = {"user_id": "user_ID",
                        "project_id": "project_ID",
                        "tenant_id": "tenant_ID",
                        "project_domain_id": "project_domain_ID",
                        "user_domain_id": "user_domain_ID",
                        "tenant_name": "tenant",
                        "project_name": "project",
                        "project_domain_name": "project_domain",
                        "user_domain_name": "user_domain",
                        "auth_token": "token",
                        "storage_url": "http://example.com:8080/v1",
                        "region_name": "region",
                        "service_type": "service",
                        "endpoint_type": "endpoint"}
        all_os_opts = os_opts.copy()
        all_os_opts.update(os_opts_dict)

        # check using hyphen separator
        args = self._make_args("stat", opts, all_os_opts, '-')
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, os_opts_dict)

        # check using underscore separator
        args = self._make_args("stat", opts, all_os_opts, '_')
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, os_opts_dict)

        # check using environment variables
        args = self._make_args("stat", {}, {})
        env = self._make_env(opts, all_os_opts)
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch.dict(os.environ, env):
            with mock.patch('swiftclient.shell.st_stat', fake_command):
                swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, os_opts_dict)

        # check again using OS_AUTH_VERSION instead of ST_AUTH_VERSION
        env = self._make_env({}, all_os_opts)
        env.update({'OS_AUTH_VERSION': '3'})
        result = [None, None]
        fake_command = self._make_fake_command(result)
        with mock.patch.dict(os.environ, env):
            with mock.patch('swiftclient.shell.st_stat', fake_command):
                swiftclient.shell.main(args)
        self._verify_opts(result[0], opts, os_opts, os_opts_dict)

    def test_command_args_v3(self):
        result = [None, None]
        fake_command = self._make_fake_command(result)
        opts = {"auth_version": "3"}
        os_opts = {"password": "secret",
                   "username": "user",
                   "auth_url": "http://example.com:5000/v3"}
        args = self._make_args("stat", opts, os_opts)
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            swiftclient.shell.main(args)
            self.assertEqual(['stat'], result[1])
        with mock.patch('swiftclient.shell.st_stat', fake_command):
            args = args + ["container_name"]
            swiftclient.shell.main(args)
            self.assertEqual(["stat", "container_name"], result[1])

    def test_insufficient_args_v3(self):
        opts = {"auth_version": "3"}
        os_opts = {"password": "secret",
                   "auth_url": "http://example.com:5000/v3"}
        args = self._make_args("stat", opts, os_opts)
        self.assertRaises(SystemExit, swiftclient.shell.main, args)

        os_opts = {"username": "user",
                   "auth_url": "http://example.com:5000/v3"}
        args = self._make_args("stat", opts, os_opts)
        self.assertRaises(SystemExit, swiftclient.shell.main, args)

        os_opts = {"username": "user",
                   "password": "secret"}
        args = self._make_args("stat", opts, os_opts)
        self.assertRaises(SystemExit, swiftclient.shell.main, args)

    def test_insufficient_env_vars_v3(self):
        args = self._make_args("stat", {}, {})
        opts = {"auth_version": "3"}
        os_opts = {"password": "secret",
                   "auth_url": "http://example.com:5000/v3"}
        env = self._make_env(opts, os_opts)
        with mock.patch.dict(os.environ, env):
            self.assertRaises(SystemExit, swiftclient.shell.main, args)

        os_opts = {"username": "user",
                   "auth_url": "http://example.com:5000/v3"}
        env = self._make_env(opts, os_opts)
        with mock.patch.dict(os.environ, env):
            self.assertRaises(SystemExit, swiftclient.shell.main, args)

        os_opts = {"username": "user",
                   "password": "secret"}
        env = self._make_env(opts, os_opts)
        with mock.patch.dict(os.environ, env):
            self.assertRaises(SystemExit, swiftclient.shell.main, args)

    def test_help(self):
        # --help returns condensed help message
        opts = {"help": ""}
        os_opts = {}
        args = self._make_args("stat", opts, os_opts)
        mock_stdout = six.StringIO()
        with mock.patch('sys.stdout', mock_stdout):
            self.assertRaises(SystemExit, swiftclient.shell.main, args)
        out = mock_stdout.getvalue()
        self.assertTrue(out.find('[--key <api_key>]') > 0)
        self.assertEqual(-1, out.find('--os-username=<auth-user-name>'))

        # --help returns condensed help message, overrides --os-help
        opts = {"help": ""}
        os_opts = {"help": ""}
                   # "password": "secret",
                   # "username": "user",
                   # "auth_url": "http://example.com:5000/v3"}
        args = self._make_args("", opts, os_opts)
        mock_stdout = six.StringIO()
        with mock.patch('sys.stdout', mock_stdout):
            self.assertRaises(SystemExit, swiftclient.shell.main, args)
        out = mock_stdout.getvalue()
        self.assertTrue(out.find('[--key <api_key>]') > 0)
        self.assertEqual(-1, out.find('--os-username=<auth-user-name>'))

        ## --os-help return os options help
        opts = {}
        args = self._make_args("", opts, os_opts)
        mock_stdout = six.StringIO()
        with mock.patch('sys.stdout', mock_stdout):
            self.assertRaises(SystemExit, swiftclient.shell.main, args)
        out = mock_stdout.getvalue()
        self.assertTrue(out.find('[--key <api_key>]') > 0)
        self.assertTrue(out.find('--os-username=<auth-user-name>') > 0)

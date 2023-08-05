# This file is part of the Juju Quickstart Plugin, which lets users set up a
# Juju environment in very few steps (https://launchpad.net/juju-quickstart).
# Copyright (C) 2013 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Test helpers for the Juju Quickstart plugin."""

from __future__ import unicode_literals

from contextlib import contextmanager
import os
import shutil
import tempfile

import mock
import yaml


@contextmanager
def assert_logs(messages, level='debug'):
    """Ensure the given messages are logged using the given log level.

    Use this function as a context manager: the code executed in the context
    block must add the expected log entries.
    """
    with mock.patch('logging.{}'.format(level.lower())) as mock_log:
        yield
    if messages:
        expected_calls = [mock.call(message) for message in messages]
        mock_log.assert_has_calls(expected_calls)
    else:
        assert not mock_log.called, 'logging unexpectedly called'


class BundleFileTestsMixin(object):
    """Shared methods for testing Juju bundle files."""

    valid_bundle = yaml.safe_dump({
        'bundle1': {'services': {'wordpress': {}, 'mysql': {}}},
        'bundle2': {'services': {'django': {}, 'nodejs': {}}},
    })

    def _write_bundle_file(self, bundle_file, contents):
        """Parse and write contents into the given bundle file object."""
        if contents is None:
            contents = self.valid_bundle
        elif isinstance(contents, dict):
            contents = yaml.safe_dump(contents)
        bundle_file.write(contents)

    def make_bundle_file(self, contents=None):
        """Create a Juju bundle file containing the given contents.

        If contents is None, use the valid bundle contents defined in
        self.valid_bundle.
        Return the bundle file path.
        """
        bundle_file = tempfile.NamedTemporaryFile(delete=False)
        self.addCleanup(os.remove, bundle_file.name)
        self._write_bundle_file(bundle_file, contents)
        bundle_file.close()
        return bundle_file.name

    def make_bundle_dir(self, contents=None):
        """Create a Juju bundle directory including a bundles.yaml file.

        The file will contain the given contents.

        If contents is None, use the valid bundle contents defined in
        self.valid_bundle.
        Return the bundle directory path.
        """
        bundle_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, bundle_dir)
        bundle_path = os.path.join(bundle_dir, 'bundles.yaml')
        with open(bundle_path, 'w') as bundle_file:
            self._write_bundle_file(bundle_file, contents)
        return bundle_dir


class CallTestsMixin(object):
    """Easily use the quickstart.utils.call function."""

    def patch_call(self, retcode, output='', error=''):
        """Patch the quickstart.utils.call function."""
        mock_call = mock.Mock(return_value=(retcode, output, error))
        return mock.patch('quickstart.utils.call', mock_call)

    def patch_multiple_calls(self, side_effect):
        """Patch multiple subsequent quickstart.utils.call calls."""
        mock_call = mock.Mock(side_effect=side_effect)
        return mock.patch('quickstart.utils.call', mock_call)


class EnvFileTestsMixin(object):
    """Shared methods for testing a Juju environments file."""

    valid_contents = yaml.safe_dump({
        'default': 'aws',
        'environments': {
            'aws': {
                'admin-secret': 'Secret!',
                'type': 'ec2',
                'default-series': 'saucy',
                'access-key': 'AccessKey',
                'secret-key': 'SeceretKey',
                'control-bucket': 'ControlBucket',
            },
        },
    })

    def make_env_file(self, contents=None):
        """Create a Juju environments file containing the given contents.

        If contents is None, use the valid environment contents defined in
        self.valid_contents.
        Return the environments file path.
        """
        if contents is None:
            contents = self.valid_contents
        env_file = tempfile.NamedTemporaryFile(delete=False)
        self.addCleanup(os.remove, env_file.name)
        env_file.write(contents)
        env_file.close()
        return env_file.name


def make_env_db(default=None, exclude_invalid=False):
    """Create and return an env_db.

    The default argument can be used to specify a default environment.
    If exclude_invalid is set to True, the resulting env_db only includes
    valid environments.
    """
    environments = {
        'ec2-west': {
            'type': 'ec2',
            'admin-secret': 'adm-307c4a53bd174c1a89e933e1e8dc8131',
            'control-bucket': 'con-aa2c6618b02d448ca7fd0f280ef66cba',
            'region': u'us-west-1',
            'access-key': 'hash',
            'secret-key': 'Secret!',
        },
        'lxc': {
            'admin-secret': 'bones',
            'default-series': 'raring',
            'storage-port': 8888,
            'type': 'local',
        },
        'test-encoding': {
            'access-key': '\xe0\xe8\xec\xf2\xf9',
            'secret-key': '\xe0\xe8\xec\xf2\xf9',
            'admin-secret': '\u2622\u2622\u2622\u2622',
            'control-bucket': '\u2746 winter-bucket \u2746',
            'juju-origin': '\u2606 the outer space \u2606',
            'type': 'toxic \u2622 type',
        },
    }
    if not exclude_invalid:
        environments.update({
            'local-with-errors': {
                'admin-secret': '',
                'storage-port': 'this-should-be-an-int',
                'type': 'local',
            },
            'private-cloud-errors': {
                'admin-secret': 'Secret!',
                'auth-url': 'https://keystone.example.com:443/v2.0/',
                'authorized-keys-path': '/home/frankban/.ssh/juju-rsa.pub',
                'control-bucket': 'e3d48007292c9abba499d96a577ceab891d320fe',
                'default-image-id': 'bb636e4f-79d7-4d6b-b13b-c7d53419fd5a',
                'default-instance-type': 'm1.medium',
                'default-series': 'no-such',
                'type': 'openstack',
            },
        })
    env_db = {'environments': environments}
    if default is not None:
        env_db['default'] = default
    return env_db


# Mock the builtin print function.
mock_print = mock.patch('__builtin__.print')


class UrlReadTestsMixin(object):
    """Expose a method to mock the quickstart.utils.urlread helper function."""

    def patch_urlread(self, contents=None, error=False):
        """Patch the quickstart.utils.urlread helper function.

        If contents is not None, urlread() will return the provided contents.
        If error is set to True, an IOError will be simulated.
        """
        mock_urlread = mock.Mock()
        if contents is not None:
            mock_urlread.return_value = contents
        if error:
            mock_urlread.side_effect = IOError('bad wolf')
        return mock.patch('quickstart.utils.urlread', mock_urlread)


class ValueErrorTestsMixin(object):
    """Set up some base methods for testing functions raising ValueErrors."""

    @contextmanager
    def assert_value_error(self, error):
        """Ensure a ValueError is raised in the context block.

        Also check that the exception includes the expected error message.
        """
        with self.assertRaises(ValueError) as context_manager:
            yield
        self.assertEqual(error, bytes(context_manager.exception))


class WatcherDataTestsMixin(object):
    """Shared methods for testing Juju mega-watcher data."""

    def make_service_data(self, data=None):
        """Create and return a data dictionary for a service.

        The passed data can be used to override default values.
        """
        default_data = {
            'CharmURL': 'cs:precise/juju-gui-47',
            'Exposed': True,
            'Life': 'alive',
            'Name': 'my-gui',
        }
        if data is not None:
            default_data.update(data)
        return default_data

    def make_service_change(self, action='change', data=None):
        """Create and return a change on a service.

        The passed data can be used to override default values.
        """
        return 'service', action, self.make_service_data(data)

    def make_unit_data(self, data=None):
        """Create and return a data dictionary for a unit.

        The passed data can be used to override default values.
        """
        default_data = {'Name': 'my-gui/47', 'Service': 'my-gui'}
        if data is not None:
            default_data.update(data)
        return default_data

    def make_unit_change(self, action='change', data=None):
        """Create and return a change on a unit.

        The passed data can be used to override default values.
        """
        return 'unit', action, self.make_unit_data(data)

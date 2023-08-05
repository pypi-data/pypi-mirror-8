# This file is part of the Juju Quickstart Plugin, which lets users set up a
# Juju environment in very few steps (https://launchpad.net/juju-quickstart).
# Copyright (C) 2013-2014 Canonical Ltd.
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

"""Juju Quickstart base application functions."""

from __future__ import (
    print_function,
    unicode_literals,
)

import json
import logging
import os
import sys
import time

import jujuclient

from quickstart import (
    juju,
    platform_support,
    settings,
    ssh,
    utils,
    watchers,
)
from quickstart.models import envs


class ProgramExit(Exception):
    """An error occurred while setting up the Juju environment.

    Raise this exception if you want the program to exit gracefully printing
    the error message to stderr.

    The error message can be either a unicode or a byte string.
    """

    def __init__(self, message):
        if isinstance(message, unicode):
            message = message.encode('utf-8')
        self.message = message

    def __str__(self):
        return b'juju-quickstart: error: {}'.format(self.message)


def ensure_dependencies(distro_only, platform, juju_command):
    """Ensure that Juju and LXC are installed.

    If the "juju" command is not found in the PATH, then install and
    setup Juju.  For Linux with apt, this includes the packages required
    to bootstrap local environments and is usually done by adding the
    Juju stable PPA and installing the juju-core and juju-local
    packages.

    If distro_only is True, the above PPA is not added to the apt sources, and
    we assume Juju packages are already available in the distro repository.
    distro_only is ignored for host other than Linux with apt.

    Return the Juju version tuple when Juju is available.

    Raise a ProgramExit if an error occurs installing packages or retrieving
    the Juju version.
    """
    try:
        installer = platform_support.get_juju_installer(platform)
    except ValueError as err:
        raise ProgramExit(bytes(err))

    required_packages = []
    # Check if juju is installed.
    try:
        juju_version = utils.get_juju_version(juju_command)
    except ValueError:
        # Juju is not installed or configured properly. To ensure everything
        # is set up correctly, also install packages required to run
        # environments using the local provider.
        required_packages.extend(settings.JUJU_PACKAGES.get(platform))
        juju_version = None
    else:
        if platform_support.supports_local(platform):
            # Check if LXC is installed.
            retcode = utils.call('/usr/bin/lxc-ls')[0]
            if retcode:
                # Some packages (e.g. lxc and mongodb-server) are required to
                # support bootstrapping environments using the local provider.
                # All those packages are installed as juju-local dependencies.
                required_packages.append('juju-local')
    if required_packages:
        try:
            installer(distro_only, required_packages)
        except OSError as error:
            raise ProgramExit(bytes(error))

    # Return the current Juju version.
    if juju_version is None:
        # Juju has been just installed, retrieve its version.
        try:
            juju_version = utils.get_juju_version(juju_command)
        except ValueError as err:
            raise ProgramExit(bytes(err))
    return juju_version


def ensure_ssh_keys():
    """Ensure that SSH keys are available.

    Allow the user to let quickstart create SSH keys, or quit by raising a
    ProgramExit if they would like to create the key themselves.
    """
    try:
        # Test to see if we have ssh-keys loaded into the ssh-agent, or if we
        # can add them to the currently running ssh-agent.
        if ssh.check_keys():
            return
        # No responsive agent was found.  Start one up.
        ssh.start_agent()
        # And now check again.
        if ssh.check_keys():
            return
    except OSError as err:
        raise ProgramExit(bytes(err))
    # At this point we have no SSH keys.
    print('Warning: no SSH keys were found in ~/.ssh\n'
          'To proceed and generate keys, quickstart can\n'
          '[a] automatically create keys for you\n'
          '[m] provide commands to manually create your keys\n\n'
          'Note: ssh-keygen will prompt you for an optional\n'
          'passphrase to generate your key for you.\n'
          'Quickstart does not store it.\n')
    try:
        answer = raw_input(
            'Automatically create keys [a], manually create the keys [m], '
            'or cancel [c]? ').lower()
    except KeyboardInterrupt:
        answer = ''
    try:
        if answer == 'a':
            ssh.create_keys()
        elif answer == 'm':
            ssh.watch_for_keys()
        else:
            sys.exit(
                b'\nIf you would like to create the keys yourself,\n'
                b'please run this command, follow its instructions,\n'
                b'and then re-run quickstart:\n'
                b'  ssh-keygen -b 4096 -t rsa')
    except OSError as err:
        raise ProgramExit(bytes(err))


def bootstrap(env_name, juju_command, requires_sudo=False, debug=False,
              upload_tools=False, upload_series=None, constraints=None):
    """Bootstrap the Juju environment with the given name.

    Do not bootstrap the environment if already bootstrapped.

    Return a tuple (already_bootstrapped, series) in which:
        - already_bootstrapped indicates whether the environment was already
          bootstrapped;
        - series is the bootstrap node Ubuntu series.

    The is_local argument indicates whether the environment is configured to
    use the local provider. If so, sudo privileges are requested in order to
    bootstrap the environment.

    If debug is True and the environment not bootstrapped, execute the
    bootstrap command passing the --debug flag.

    Raise a ProgramExit if any error occurs in the bootstrap process.
    """
    already_bootstrapped = False
    cmd = [juju_command, 'bootstrap', '-e', env_name]
    if requires_sudo:
        cmd.insert(0, 'sudo')
    if debug:
        cmd.append('--debug')
    if upload_tools:
        cmd.append('--upload-tools')
    if upload_series is not None:
        cmd.extend(['--upload-series', upload_series])
    if constraints is not None:
        cmd.extend(['--constraints', constraints])
    retcode, _, error = utils.call(*cmd)
    if retcode:
        # XXX frankban 2013-11-13 bug 1252322: the check below is weak. We are
        # relying on an error message in order to decide if the environment is
        # already bootstrapped. Other possibilities include checking if the
        # jenv file is present (in ~/.juju/environments/) and, if so, check the
        # juju status. Unfortunately this is also prone to errors, because a
        # jenv file can be there but the environment not really bootstrapped or
        # functional (e.g. sync-tools was used, or a previous bootstrap failed,
        # or the user terminated machines from the ec2 panel, etc.). Moreover
        # jenv files seems to be an internal juju-core detail. Definitely we
        # need to find a better way, but for now the "asking forgiveness"
        # approach feels like the best compromise we have. Also note that,
        # rather than comparing the expected error with the obtained one, we
        # search in the error in order to support bootstrap --debug.
        if 'environment is already bootstrapped' not in error:
            # We exit if the error is not "already bootstrapped".
            raise ProgramExit(error)
        # Juju is bootstrapped, but we don't know if it is ready yet. Fall
        # through to the next block for that check.
        already_bootstrapped = True
        print('reusing the already bootstrapped {} environment'.format(
            env_name))
    # Call "juju status" multiple times until the bootstrap node is ready.
    # Exit with an error if the agent is not ready after ten minutes.
    # Note: when using the local provider, calling "juju status" is very fast,
    # but e.g. on ec2 the first call (right after "bootstrap") can take
    # several minutes, and subsequent calls are relatively fast (seconds).
    print('retrieving the environment status')
    timeout = time.time() + (60*10)
    while time.time() < timeout:
        retcode, output, error = utils.call(
            juju_command, 'status', '-e', env_name, '--format', 'yaml')
        if retcode:
            continue
        # Ensure the state server is up and the agent is started.
        try:
            agent_state = utils.get_agent_state(output)
        except ValueError:
            continue
        if agent_state == 'started':
            series = utils.get_bootstrap_node_series(output)
            return already_bootstrapped, series
        # If the agent is in an error state, there is nothing we can do, and
        # it's not useful to keep trying.
        if agent_state == 'error':
            raise ProgramExit('state server failure:\n{}'.format(output))
    details = ''.join(filter(None, [output, error])).strip()
    raise ProgramExit('the state server is not ready:\n{}'.format(details))


def get_value_from_jenv(env_name, juju_home, key):
    """Read the key from the generated environment file.

    At bootstrap, juju (v1.16 and later) writes a generated file
    located in JUJU_HOME.  Return the value for the key.

    Raise a ValueError if:
        - the environment file is not found;
        - the environment file contents are not parsable by YAML;
        - the YAML contents are not properly structured;
        - the key is not found.
    """
    filename = '{}.jenv'.format(env_name)
    juju_env_file = os.path.expanduser(
        os.path.join(juju_home, 'environments', filename))
    jenv_db = envs.load_generated(juju_env_file)
    try:
        return jenv_db[key]
    except KeyError:
        msg = '{} not found in {}'.format(key, juju_env_file)
        raise ValueError(msg.encode('utf-8'))


def get_api_url(env_name, juju_command):
    """Return a Juju API URL for the given environment name.

    Use the Juju CLI in a subprocess in order to retrieve the API addresses.
    Return the complete URL, e.g. "wss://api.example.com:17070".
    Raise a ProgramExit if any error occurs.
    """
    retcode, output, error = utils.call(
        juju_command, 'api-endpoints', '-e', env_name, '--format', 'json')
    if retcode:
        raise ProgramExit(error)
    # Assuming there is always at least one API address, grab the first one
    # from the JSON output.
    api_address = json.loads(output)[0]
    return 'wss://{}'.format(api_address)


def connect(api_url, admin_secret):
    """Connect to the Juju API server and log in using the given credentials.

    Return a connected and authenticated Juju Environment instance.
    Raise a ProgramExit if any error occurs while establishing the WebSocket
    connection or if the API returns an error response.
    """
    try_count = 0
    while True:
        try:
            env = juju.connect(api_url)
        except Exception as err:
            try_count += 1
            msg = b'unable to connect to the Juju API server on {}: {}'.format(
                api_url.encode('utf-8'), err)
            if try_count >= 30:
                raise ProgramExit(msg)
            else:
                logging.warn('Retrying: ' + msg)
                time.sleep(1)
        else:
            break
    try:
        env.login(admin_secret)
    except jujuclient.EnvError as err:
        msg = 'unable to log in to the Juju API server on {}: {}'
        raise ProgramExit(msg.format(api_url, err.message))
    return env


def create_auth_token(env):
    """Return a new authentication token.

    If the server does not support the request, return None.  Raise any other
    error."""
    try:
        result = env.create_auth_token()
    except jujuclient.EnvError as err:
        if err.message == 'unknown object type "GUIToken"':
            # This is a legacy charm.
            return None
        else:
            raise
    return result['Token']


def check_environment(
        env, service_name, charm_url, env_type, bootstrap_node_series,
        check_preexisting):
    """Inspect the current Juju environment.

    This function is responsible for retrieving all the information required
    to deploy the Juju GUI charm to the current environment.

    Receive the following arguments:
        - env: an authenticated Juju Environment instance;
        - service_name: the name of the service to look for;
        - charm_url: a fully qualified charm URL if the user requested the
          deployment of a custom charm, or None otherwise;
        - env_type: the environment's provider type;
        - bootstrap_node_series: the bootstrap node series;
        - check_preexisting: whether to check for a pre-existing service and/or
          unit.

    If the charm URL is not provided, and the service is not already deployed,
    the function tries to retrieve it from the charmworld API. In this case a
    default charm URL is used if charmworld is not available.

    Return a tuple including the following values:
        - charm_url: the charm URL that will be used to deploy the service;
        - machine: the machine where to deploy to (e.g. "0") or None if a new
          machine must be created;
        - service_data: the service info as returned by the mega-watcher for
          services, or None if the service is not present in the environment;
        - unit_data: the unit info as returned by the mega-watcher for units,
          or None if the unit is not present in the environment.

    Raise a ProgramExit if the API server returns an error response.
    """
    print('bootstrap node series: {}'.format(bootstrap_node_series))
    service_data, unit_data, machine = None, None, None
    if check_preexisting:
        # The service and/or the unit can be already in the environment.
        try:
            status = env.get_status()
        except jujuclient.EnvError as err:
            raise ProgramExit('bad API response: {}'.format(err.message))
        service_data, unit_data = utils.get_service_info(status, service_name)
    if service_data is None:
        # The service does not exist in the environment.
        if charm_url is None:
            # The user did not provide a customized charm.
            if bootstrap_node_series in settings.JUJU_GUI_SUPPORTED_SERIES:
                series = bootstrap_node_series
            else:
                series = settings.JUJU_GUI_SUPPORTED_SERIES[-1]
            try:
                # Try to get the charm URL from charmworld.
                charm_url = utils.get_charm_url(series)
            except (IOError, ValueError) as err:
                # Fall back to the default URL for the current series.
                msg = 'unable to retrieve the {} charm URL from the API: {}'
                logging.warn(msg.format(service_name, err))
                charm_url = settings.DEFAULT_CHARM_URLS[series]
    else:
        # A deployed service already exists in the environment: ignore the
        # provided charm URL and just use the already deployed charm.
        charm_url = service_data['CharmURL']
    charm = utils.parse_gui_charm_url(charm_url)
    # Deploy on the bootstrap node if the following conditions are satisfied:
    # - we are not using the local provider (which uses localhost);
    # - we are not using the azure provider (in which availability sets prevent
    #   us from relying on the bootstrap node);
    # - the requested charm and the bootstrap node have the same series.
    if (
        (env_type not in ('local', 'azure')) and
        (charm.series == bootstrap_node_series)
    ):
        machine = '0'
    return charm_url, machine, service_data, unit_data


def deploy_gui(env, service_name, charm_url, machine, service_data, unit_data):
    """Deploy and expose the given service to the given machine.

    Only deploy the service if not already present in the environment.
    Do not add a unit to the service if the unit is already there.

    Receive the following arguments:
        - env: an authenticated Juju Environment instance;
        - service_name: the name of the service to be deployed;
        - charm_url: the fully qualified charm URL to be used to deploy the
          service;
        - machine: the machine where to deploy to (e.g. "0") or None if a new
          machine must be created;
        - service_data: the service info as returned by the mega-watcher for
          services, or None if the service is not present in the environment;
        - unit_data: the unit info as returned by the mega-watcher for units,
          or None if the unit is not present in the environment.

    Return the name of the first running unit belonging to the given service.
    Raise a ProgramExit if the API server returns an error response.
    """
    if service_data is None:
        # The service is not in the environment: deploy it without units.
        print('requesting {} deployment'.format(service_name))
        try:
            env.deploy(service_name, charm_url, num_units=0)
        except jujuclient.EnvError as err:
            raise ProgramExit('bad API response: {}'.format(err.message))
        print('{} deployment request accepted'.format(service_name))
        service_exposed = False
    else:
        # We already have the service in the environment.
        print('service {} already deployed'.format(service_name))
        service_exposed = service_data.get('Exposed', False)
    # At this point the service is surely deployed in the environment: expose
    # it if necessary and add a unit if it is missing.
    if not service_exposed:
        print('exposing service {}'.format(service_name))
        try:
            env.expose(service_name)
        except jujuclient.EnvError as err:
            raise ProgramExit('bad API response: {}'.format(err.message))
    if unit_data is None:
        # Add a unit to the service.
        print('requesting new unit deployment')
        try:
            response = env.add_unit(service_name, machine_spec=machine)
        except jujuclient.EnvError as err:
            raise ProgramExit('bad API response: {}'.format(err.message))
        unit_name = response['Units'][0]
        print('{} deployment request accepted'.format(unit_name))
    else:
        # A service unit is already present in the environment. Go ahead
        # and try to reuse that unit.
        unit_name = unit_data['Name']
        print('reusing unit {}'.format(unit_name))
    return unit_name


def watch(env, unit_name):
    """Start watching the given unit and the machine the unit belongs to.

    Output a human readable message each time a relevant change is found.

    The following changes are considered relevant for a healthy unit:
        - the machine is pending;
        - the unit is pending;
        - the machine is started;
        - the unit is reachable;
        - the unit is installed;
        - the unit is started.

    Stop watching and return the unit public address when the unit is started.
    Raise a ProgramExit if the API server returns an error response, or if
    either the service unit or the machine is removed or in error.
    """
    address = unit_status = machine_id = machine_status = ''
    collected_machine_changes = []
    watcher = env.watch_changes(watchers.unit_machine_changes)
    while True:
        try:
            unit_changes, machine_changes = watcher.next()
        except jujuclient.EnvError as err:
            raise ProgramExit(
                'bad API server response: {}'.format(err.message))
        # Process unit changes.
        for action, data in unit_changes:
            if data['Name'] == unit_name:
                try:
                    data = watchers.parse_unit_change(
                        action, data, unit_status, address)
                except ValueError as err:
                    raise ProgramExit(bytes(err))
                unit_status, address, machine_id = data
                if address and unit_status == 'started':
                    # We can exit this loop.
                    return address
                # The mega-watcher contains a single change for each specific
                # unit. For this reason, we can exit the for loop here.
                break
        if not machine_id:
            # No need to process machine changes: we don't know what machine
            # the unit belongs to. However, machine changes are collected so
            # that they can be parsed later.
            collected_machine_changes.extend(machine_changes)
            continue
        # Process machine changes. Since relevant info can also be found
        # in previously collected changes, add those to the current changes,
        # in reverse order so that more complete info comes first.
        all_machine_changes = machine_changes + list(
            reversed(collected_machine_changes))
        # At this point we can discard collected changes.
        collected_machine_changes = []
        for action, data in all_machine_changes:
            if data['Id'] == machine_id:
                try:
                    machine_status, address = watchers.parse_machine_change(
                        action, data, machine_status, address)
                except ValueError as err:
                    raise ProgramExit(bytes(err))
                if address and unit_status == 'started':
                    # We can exit this loop.
                    return address
                # The mega-watcher contains a single change for each specific
                # machine. For this reason, we can exit the for loop here.
                break


def deploy_bundle(env, bundle_yaml, bundle_name, bundle_id):
    """Deploy a bundle.

    Receive an API URL to a WebSocket server supporting bundle deployments, the
    admin_secret to use in the authentication process, the bundle YAML encoded
    contents and the bundle name to be imported.

    Raise a ProgramExit if the API server returns an error response.
    """
    try:
        env.deploy_bundle(bundle_yaml, name=bundle_name, bundle_id=bundle_id)
    except jujuclient.EnvError as err:
        raise ProgramExit('bad API server response: {}'.format(err.message))


def juju_requires_sudo(env_type, juju_version, customized):
    """Report whether the given Juju version requires "sudo".

    The env_type argument is the current environment type.
    "e.g. local, ec2, azure"

    Raise a ProgramExit if a customized version of Juju is being used and Juju
    itself requires "sudo"
    """
    # If the Juju version is less than 1.17.2 then use sudo for local envs.
    if env_type == 'local' and juju_version < (1, 17, 2):
        if customized:
            raise ProgramExit(b'cannot use a customized Juju when it '
                              'requires sudo')
        return True
    return False

# Copyright 2009-2014 INRIA Rhone-Alpes, Service Experimentation et
# Developpement
#
# This file is part of Execo.
#
# Execo is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Execo is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Execo.  If not, see <http://www.gnu.org/licenses/>

from execo.config import load_configuration, get_user_config_filename

# _STARTOF_ g5k_configuration
g5k_configuration = {
    'kadeploy3': 'kadeploy3',
    'kadeploy3_options': '-k -d',
    'default_env_name': None,
    'default_env_file': None,
    'default_timeout': 900,
    'check_deployed_command': "! (mount | grep -E '^/dev/[[:alpha:]]+2 on / ')",
    'no_ssh_for_local_frontend' : False,
    'polling_interval' : 20,
    'tiny_polling_interval' : 10,
    'default_frontend' : None,
    'api_uri': "https://api.grid5000.fr/3.0/",
    'api_username': None,
    'api_additional_args': [],
    'oar_job_key_file': None,
    'oar_mysql_ro_db': 'oar2',
    'oar_mysql_ro_user': 'oarreader',
    'oar_mysql_ro_password': 'read',
    'oar_mysql_ro_port': 3306,
    }
# _ENDOF_ g5k_configuration
"""Global Grid5000 configuration parameters.

- ``kadeploy3``: kadeploy3 command.

- ``kadeploy3_options``: a string with kadeploy3 command line options.

- ``default_env_name``: a default environment name to use for
  deployments (as registered to kadeploy3).

- ``default_env_file``: a default environment file to use for
  deployments (for kadeploy3).

- ``default_timeout``: default timeout for all calls to g5k services
  (except deployments).

- ``check_deployed_command``: default shell command used by
  `execo_g5k.kadeploy.deploy` to check that the nodes are correctly
  deployed. This command should return 0 if the node is correctly
  deployed, or another value otherwise. The default checks that the
  root is not on the second partition of the disk.

- ``no_ssh_for_local_frontend``: if True, don't use ssh to issue g5k
  commands for local site. If False, always use ssh, both for remote
  frontends and local site. Set it to True if you are sure that your
  scripts always run on the local frontend.

- ``polling_interval``: time interval between pollings for various
  operations, eg. wait oar job start.

- ``tiny_polling_interval``: small time interval between pollings for
  various operations. Used for example when waiting for a job start,
  and start date of the job is over but the job is not yet in running
  state.

- ``default_frontend``: address of default frontend.

- ``api_uri``: base uri for g5k api serverr.

- ``api_username``: username to use for requests to the Grid5000 REST
  API. If None, no credentials will be used, which is fine when
  running on a Grid5000 frontend.

- ``api_additional_args``: additional arguments to append at the end
  all requests to g5k api. May be used to request the testing branch
  (use: api_additional_args = ["branch=testing"])

- ``oar_job_key_file``: ssh key to use for oar. If defined, takes
  precedence over environment variable OAR_JOB_KEY_FILE.
"""

def make_default_oarsh_oarcp_params():
# _STARTOF_ default_oarsh_oarcp_params
    default_oarsh_oarcp_params = {
        'ssh':         'oarsh',
        'scp':         'oarcp',
        'taktuk_connector': 'oarsh',
        'pty': True,
        }
# _ENDOF_ default_oarsh_oarcp_params
    return default_oarsh_oarcp_params

default_oarsh_oarcp_params = make_default_oarsh_oarcp_params()
"""A convenient, predefined connection paramaters dict with oarsh / oarcp configuration.

See `execo.config.make_default_connection_params`
"""

def make_default_frontend_connection_params():
# _STARTOF_ default_frontend_connection_params
    default_frontend_connection_params = {
        'pty': True,
        'host_rewrite_func': lambda host: host + ".grid5000.fr"
        }
# _ENDOF_ default_frontend_connection_params
    return default_frontend_connection_params

default_frontend_connection_params = make_default_frontend_connection_params()
"""Default connection params when connecting to a Grid5000 frontend."""

load_configuration(
  get_user_config_filename(),
  ((g5k_configuration, 'g5k_configuration'),
   (default_frontend_connection_params, 'default_frontend_connection_params'),
   (default_oarsh_oarcp_params, 'default_oarsh_oarcp_params')))

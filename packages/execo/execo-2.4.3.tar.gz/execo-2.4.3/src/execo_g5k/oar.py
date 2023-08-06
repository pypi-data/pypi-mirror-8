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

from config import g5k_configuration
from execo.config import make_connection_params
from execo.exception import ProcessesFailed
from execo.host import Host
from execo.process import get_process
from execo.time_utils import get_unixts, get_seconds, str_date_to_unixts, \
    str_duration_to_seconds, format_duration, format_date, Timer, sleep
from execo.utils import comma_join
from execo_g5k.config import default_frontend_connection_params
from execo.utils import checked_min
from execo_g5k.utils import get_frontend_host
import os, re, time

def _date_in_range(date, date_range):
    """Check that a date is inside a range. If range is None, return True."""
    if date_range == None: return True
    if date_range[0] and date < date_range[0]:
        return False
    if date_range[1] and date > date_range[1]:
        return False
    return True

def format_oar_date(ts):
    """Return a string with the formatted date (year, month, day, hour, min, sec, ms) formatted for oar/oargrid.

    timezone is forced to Europe/Paris, and timezone info is discarded, for g5k oar/oargrid.

    :param tz: a date in one of the formats handled.
    """
    # forking code because modifying os.environ["TZ"] and calling
    # time.tzset() is not thread-safe
    ts = int(get_unixts(ts))
    rend, wend = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.environ["TZ"] = "Europe/Paris"
        time.tzset()
        t = time.localtime(ts)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
        os.write(wend, formatted_time)
        os._exit(0)
    else:
        os.close(wend)
        f = os.fdopen(rend)
        formatted_time = f.read()
        f.close()
        os.waitpid(pid, 0)
        return formatted_time

def format_oar_duration(duration):
    """Return a string with a formatted duration (hours, mins, secs, ms) formatted for oar/oargrid.

    :param duration: a duration in one of the formats handled.
    """
    duration = get_seconds(duration)
    s = duration
    h = (s - (s % 3600)) / 3600
    s -= h * 3600
    m = (s - (s % 60)) / 60
    s -= m * 60
    s = int(s)
    formatted_duration = ""
    if duration >= 3600:
        formatted_duration += "%i:" % h
    else:
        formatted_duration += "0:"
    if duration >= 60:
        formatted_duration += "%i:" % m
    else:
        formatted_duration += "0:"
    formatted_duration += "%i" % s
    return formatted_duration

def oar_date_to_unixts(date):
    """Convert a date in the format returned by oar/oargrid to an unix timestamp.

    Timezone of g5k oar/oargrid timestamps is Europe/Paris."""
    # forking code because modifying os.environ["TZ"] and calling
    # time.tzset() is not thread-safe
    rend, wend = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.environ["TZ"] = "Europe/Paris"
        time.tzset()
        ts = str_date_to_unixts(date)
        os.write(wend, str(ts))
        os._exit(0)
    else:
        os.close(wend)
        f = os.fdopen(rend)
        ts = float(f.read())
        f.close()
        os.waitpid(pid, 0)
        return ts

def oar_duration_to_seconds(duration):
    """Convert a duration in the format returned by oar/oargrid to a number of seconds."""
    return str_duration_to_seconds(duration)

class OarSubmission(object):
    """An oar submission.

    POD style class.

    members are:

    - resources: Set the requested resources for the job. Oar option
      -l, without the walltime.

    - walltime: Job walltime. Walltime part of oar -l option.

    - job_type: Job type, oar option -t: deploy, besteffort, cosystem,
      checkpoint, timesharing, allow_classic_ssh.

    - sql_properties: constraints to properties for the job, oar
      option -p (use single quotes for literal strings).

    - queue: the queue to submit the job to. Oar option -q.

    - reservation_date: Request that the job starts at a specified
      time. Oar option -r.

    - directory: Specify the directory where to launch the command
      (default is current directory). Oar option -d.

    - project: pecify a name of a project the job belongs to. Oar
      option --project.

    - name: Specify an arbitrary name for the job. Oar option -n.

    - additional_options: passed directly to oarsub on the command
      line.

    - command: run by oarsub (default: sleep a long time).
    """

    def __init__(self,
                 resources = None,
                 walltime = None,
                 job_type = None,
                 sql_properties = None,
                 queue = None,
                 reservation_date = None,
                 directory = None,
                 project = None,
                 name = None,
                 additional_options = None,
                 command = None):
        self.resources = resources
        self.walltime = walltime
        self.job_type = job_type
        self.sql_properties = sql_properties
        self.queue = queue
        self.reservation_date = reservation_date
        self.directory = directory
        self.project = project
        self.name = name
        self.additional_options = additional_options
        self.command = command

    def __repr__(self):
        s = ""
        if self.resources != None: s = comma_join(s, "resources=%r" % (self.resources,))
        if self.walltime != None: s = comma_join(s, "walltime=%r" % (format_duration(self.walltime),))
        if self.job_type != None: s = comma_join(s, "job_type=%r" % (self.job_type,))
        if self.sql_properties != None: s = comma_join(s, "sql_properties=%r" % (self.sql_properties,))
        if self.queue != None: s = comma_join(s, "queue=%r" % (self.queue,))
        if self.reservation_date != None: s = comma_join(s, "reservation_date=%r" % (format_date(self.reservation_date),))
        if self.directory != None: s = comma_join(s, "directory=%r" % (self.directory,))
        if self.project != None: s = comma_join(s, "project=%r" % (self.project,))
        if self.name != None: s = comma_join(s, "name=%r" % (self.name,))
        if self.additional_options != None: s = comma_join(s, "additional_options=%r" % (self.additional_options,))
        if self.command != None: s = comma_join(s, "command=%r" % (self.command,))
        return "OarSubmission(%s)" % (s,)

def get_oarsub_commandline(job_spec):
    oarsub_cmdline = 'oarsub'
    if job_spec.additional_options != None:
        oarsub_cmdline += ' %s' % (job_spec.additional_options,)
    if job_spec.resources:
        if hasattr(job_spec.resources, '__iter__'):
            resources = job_spec.resources
        else:
            resources = (job_spec.resources,)
        oarsub_cmdline += ' -l "' + "+".join(resources)
        if job_spec.walltime != None:
            oarsub_cmdline += ',walltime=%s' % (format_oar_duration(job_spec.walltime),)
        oarsub_cmdline += '"'
    elif job_spec.walltime != None:
        oarsub_cmdline += '-l "walltime=%s"' % (format_oar_duration(job_spec.walltime),)
    key = g5k_configuration.get('oar_job_key_file')
    if key == None:
        key = os.environ.get('OAR_JOB_KEY_FILE')
    if key != None:
        oarsub_cmdline += ' -k -i %s' % (key,)
    if job_spec.job_type != None:
        if hasattr(job_spec.job_type,"__iter__"):
            for t in job_spec.job_type:
                oarsub_cmdline += ' -t "%s"' % (t,)
        else:
            oarsub_cmdline += ' -t "%s"' % (job_spec.job_type,)
    if job_spec.sql_properties != None:
        oarsub_cmdline += ' -p "%s"' % (job_spec.sql_properties,)
    if job_spec.queue != None:
        oarsub_cmdline += ' -q "%s"' % (job_spec.queue,)
    if job_spec.reservation_date != None:
        oarsub_cmdline += ' -r "%s"' % (format_oar_date(job_spec.reservation_date),)
    if job_spec.directory != None:
        oarsub_cmdline += ' -d "%s"' % (job_spec.directory,)
    if job_spec.project != None:
        oarsub_cmdline += ' --project "%s"' % (job_spec.project,)
    if job_spec.name != None:
        oarsub_cmdline += ' -n "%s"' % (job_spec.name,)
    if job_spec.command != None:
        oarsub_cmdline += ' "%s"' % (job_spec.command,)
    else:
        oarsub_cmdline += ' "sleep 31536000"'
    return oarsub_cmdline

def oarsub(job_specs, frontend_connection_params = None, timeout = False, abort_on_error = False):
    """Submit jobs.

    :param job_specs: iterable of tuples (execo_g5k.oar.OarSubmission,
      frontend) with None for default frontend

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for submitting. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.

    :param abort_on_error: default False. If True, raises an exception
      on any error. If False, will returned the list of job got, even
      if incomplete (some frontends may have failed to answer).

    Returns a list of tuples (oarjob id, frontend), with frontend ==
    None for default frontend. If submission error, oarjob id ==
    None. The returned list matches, in the same order, the job_specs
    parameter.
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    processes = []
    for (spec, frontend) in job_specs:
        oarsub_cmdline = get_oarsub_commandline(spec)
        p = get_process(oarsub_cmdline,
                        host = get_frontend_host(frontend),
                        connection_params = make_connection_params(frontend_connection_params,
                                                                   default_frontend_connection_params))
        p.timeout = timeout
        p.pty = True
        p.frontend = frontend
        processes.append(p)
    oar_job_ids = []
    if len(processes) == 0:
        return oar_job_ids
    for process in processes: process.start()
    for process in processes: process.wait()
    failed_processes = []
    for process in processes:
        job_id = None
        if process.ok:
            mo = re.search("^OAR_JOB_ID=(\d+)\s*$", process.stdout, re.MULTILINE)
            if mo != None:
                job_id = int(mo.group(1))
        if job_id == None:
            failed_processes.append(process)
        oar_job_ids.append((job_id, process.frontend))
    if len(failed_processes) > 0 and abort_on_error:
        raise ProcessesFailed, failed_processes
    else:
        return oar_job_ids

def oardel(job_specs, frontend_connection_params = None, timeout = False):
    """Delete oar jobs.

    Ignores any error, so you can delete inexistant jobs, already
    deleted jobs, or jobs that you don't own. Those deletions will be
    ignored.

    :param job_specs: iterable of tuples (job_id, frontend) with None
      for default frontend

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for deleting. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    processes = []
    for (job_id, frontend) in job_specs:
        p = get_process("oardel %i" % (job_id,),
                        host = get_frontend_host(frontend),
                        connection_params = make_connection_params(frontend_connection_params,
                                                                   default_frontend_connection_params))
        p.timeout = timeout
        p.nolog_exit_code = True
        p.pty = True
        processes.append(p)
    for process in processes: process.start()
    for process in processes: process.wait()

def get_current_oar_jobs(frontends = None,
                         start_between = None,
                         end_between = None,
                         frontend_connection_params = None,
                         timeout = False,
                         abort_on_error = False):
    """Return a list of current active oar job ids.

    The list contains tuples (oarjob id, frontend).

    :param frontends: an iterable of frontends to connect to. A
      frontend with value None means default frontend. If frontends ==
      None, means get current oar jobs only for default frontend.

    :param start_between: a tuple (low, high) of endpoints. Filters
      and returns only jobs whose start date is in between these
      endpoints.

    :param end_between: a tuple (low, high) of endpoints. Filters and
      returns only jobs whose end date is in between these endpoints.

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for retrieving. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.

    :param abort_on_error: default False. If True, raises an exception
      on any error. If False, will returned the list of job got, even
      if incomplete (some frontends may have failed to answer).
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    if start_between: start_between = [ get_unixts(t) for t in start_between ]
    if end_between: end_between = [ get_unixts(t) for t in end_between ]
    processes = []
    if frontends == None:
        frontends = [ None ]
    for frontend in frontends:
        p = get_process("oarstat -u",
                        host = get_frontend_host(frontend),
                        connection_params = make_connection_params(frontend_connection_params,
                                                                   default_frontend_connection_params))
        p.timeout = timeout
        p.pty = True
        p.frontend = frontend
        processes.append(p)
    oar_job_ids = []
    if len(processes) == 0:
        return oar_job_ids
    for process in processes: process.start()
    for process in processes: process.wait()
    failed_processes = []
    for process in processes:
        if process.ok:
            jobs = re.findall("^(\d+)\s", process.stdout, re.MULTILINE)
            oar_job_ids.extend([ (int(jobid), process.frontend) for jobid in jobs ])
        else:
            failed_processes.append(process)
    if len(failed_processes) > 0 and abort_on_error:
        raise ProcessesFailed, failed_processes
    else:
        if start_between or end_between:
            filtered_job_ids = []
            for jobfrontend in oar_job_ids:
                info = get_oar_job_info(jobfrontend[0], jobfrontend[1],
                                        frontend_connection_params, timeout,
                                        nolog_exit_code = True, nolog_timeout = True,
                                        nolog_error = True)
                if (_date_in_range(info['start_date'], start_between)
                    and _date_in_range(info['start_date'] + info['walltime'], end_between)):
                    filtered_job_ids.append(jobfrontend)
            oar_job_ids = filtered_job_ids
        return oar_job_ids

def get_oar_job_info(oar_job_id = None, frontend = None,
                     frontend_connection_params = None, timeout = False,
                     nolog_exit_code = False, nolog_timeout = False, nolog_error = False):
    """Return a dict with informations about an oar job.

    :param oar_job_id: the oar job id. If None given, will try to get
      it from ``OAR_JOB_ID`` environment variable.

    :param frontend: the frontend of the oar job. If None given, use
      default frontend

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for retrieving. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.

    Hash returned may contain these keys:

    - ``start_date``: unix timestamp of job's start date

    - ``walltime``: job's walltime (seconds)

    - ``scheduled_start``: unix timestamp of job's start prediction
      (may change between invocations)

    - ``state``: job state. Possible states: 'Waiting', 'Hold',
      'toLaunch', 'toError', 'toAckReservation', 'Launching',
      'Running', 'Suspended', 'Resuming', 'Finishing', 'Terminated',
      'Error', see table jobs, column state, in oar documentation
      http://oar.imag.fr/sources/2.5/docs/documentation/OAR-DOCUMENTATION-ADMIN/#jobs

    - ``name``: job name

    But no info may be available as long as the job is not scheduled.
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    if oar_job_id == None:
        if os.environ.has_key('OAR_JOB_ID'):
            oar_job_id = os.environ['OAR_JOB_ID']
        else:
            raise ValueError, "no oar job id given and no OAR_JOB_ID environment variable found"
    process = get_process("oarstat -fj %i" % (oar_job_id,),
                          host = get_frontend_host(frontend),
                          connection_params = make_connection_params(frontend_connection_params,
                                                                     default_frontend_connection_params))
    process.timeout = timeout
    process.pty = True
    process.nolog_exit_code = nolog_exit_code
    process.nolog_timeout = nolog_timeout
    process.nolog_error = nolog_error
    process.run()
    job_info = dict()
    start_date_result = re.search("^\s*startTime = (\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)\s*$", process.stdout, re.MULTILINE)
    if start_date_result:
        start_date = oar_date_to_unixts(start_date_result.group(1))
        job_info['start_date'] = start_date
    walltime_result = re.search("^\s*walltime = (\d+:\d?\d:\d?\d)\s*$", process.stdout, re.MULTILINE)
    if walltime_result:
        walltime = oar_duration_to_seconds(walltime_result.group(1))
        job_info['walltime'] = walltime
    scheduled_start_result = re.search("^\s*scheduledStart = (\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)\s*$", process.stdout, re.MULTILINE)
    if scheduled_start_result:
        scheduled_start = oar_date_to_unixts(scheduled_start_result.group(1))
        job_info['scheduled_start'] = scheduled_start
    state_result = re.search("^\s*state = (\w*)\s*$", process.stdout, re.MULTILINE)
    if state_result:
        job_info['state'] = state_result.group(1)
    name_result = re.search("^\s*name = ([ \t\S]*)\s*$", process.stdout, re.MULTILINE)
    if name_result:
        job_info['name'] = name_result.group(1)
    return job_info

def wait_oar_job_start(oar_job_id = None, frontend = None,
                       frontend_connection_params = None,
                       timeout = None,
                       prediction_callback = None):
    """Sleep until an oar job's start time.

    As long as the job isn't scheduled, wait_oar_job_start will sleep
    / poll every
    ``execo_g5k.config.g5k_configuration['polling_interval']`` seconds
    until it is scheduled. Then, knowing its start date, it will sleep
    the amount of time necessary to wait for the job start.

    returns True if wait was successful, False otherwise (job
    cancelled, error)

    :param oar_job_id: the oar job id. If None given, will try to get
      it from ``OAR_JOB_ID`` environment variable.

    :param frontend: the frontend of the oar job. If None given, use
      default frontend.

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for retrieving. Default is None (no
      timeout).

    :param prediction_callback: function taking a unix timestamp as
      parameter. This function will be called each time oar job start
      prediction changes.
    """

    def check_prediction_changed(prediction, new_prediction):
        old_prediction = prediction
        prediction = new_prediction
        if prediction != old_prediction:
            if prediction_callback != None:
                prediction_callback(prediction)
        return prediction

    prediction = None
    countdown = Timer(timeout)
    while countdown.remaining() == None or countdown.remaining() > 0:
        infos = get_oar_job_info(oar_job_id, frontend, frontend_connection_params,
                                 countdown.remaining(), nolog_exit_code = True,
                                 nolog_timeout = True, nolog_error = True)
        now = time.time()
        if infos.has_key('start_date') or infos.has_key('scheduled_start'):
            if infos.has_key('start_date'):
                new_prediction = infos['start_date']
            elif infos.has_key('scheduled_start'):
                new_prediction = infos['scheduled_start']
            prediction = check_prediction_changed(prediction, new_prediction)
        if infos.has_key('state'):
            if infos['state'] == "Terminated" or infos['state'] == "Error":
                return False
            if infos['state'] == "Running":
                return True
        if infos.has_key('start_date') or infos.has_key('scheduled_start'):
            if now >= new_prediction:
                sleep(checked_min(g5k_configuration.get('tiny_polling_interval'), countdown.remaining()))
                continue
            elif now + g5k_configuration.get('polling_interval') > new_prediction:
                sleep(until = checked_min(new_prediction, now + countdown.remaining() if countdown.remaining() != None else None))
                continue
        sleep(checked_min(g5k_configuration.get('polling_interval'), countdown.remaining()))
    return False

def get_oar_job_nodes(oar_job_id = None, frontend = None,
                      frontend_connection_params = None, timeout = False):
    """Return an iterable of `execo.host.Host` containing the hosts of an oar job.

    This method waits for the job start (the list of nodes isn't fixed
    until the job start).

    :param oar_job_id: the oar job id. If None given, will try to get
      it from ``OAR_JOB_ID`` environment variable.

    :param frontend: the frontend of the oar job. If None given, use
      default frontend.

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for retrieving. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    if oar_job_id == None:
        if os.environ.has_key('OAR_JOB_ID'):
            oar_job_id = os.environ['OAR_JOB_ID']
        else:
            raise ValueError, "no oar job id given and no OAR_JOB_ID environment variable found"
    countdown = Timer(timeout)
    wait_oar_job_start(oar_job_id, frontend, frontend_connection_params, countdown.remaining())
    process = get_process("(oarstat -sj %(oar_job_id)i | grep 'Running\|Terminated\|Error') > /dev/null 2>&1 && oarstat -pj %(oar_job_id)i | oarprint host -f -" % {'oar_job_id': oar_job_id},
                          host = get_frontend_host(frontend),
                          connection_params = make_connection_params(frontend_connection_params,
                                                                     default_frontend_connection_params))
    process.timeout = countdown.remaining()
    process.pty = True
    process.run()
    if process.ok:
        host_addresses = re.findall("(\S+)", process.stdout, re.MULTILINE)
        return [ Host(host_address) for host_address in host_addresses ]
    else:
        raise ProcessesFailed, [process]

def get_oar_job_subnets(oar_job_id = None, frontend = None, frontend_connection_params = None, timeout = False):
    """Return a tuple containing an iterable of tuples (IP, MAC) and a dict containing the subnet parameters of the reservation (if any).

    subnet parameters dict has keys: 'ip_prefix', 'broadcast',
    'netmask', 'gateway', 'network', 'dns_hostname', 'dns_ip'.

    :param oar_job_id: the oar job id. If None given, will try to get
      it from ``OAR_JOB_ID`` environment variable.

    :param frontend: the frontend of the oar job. If None given, use
      default frontend.

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for retrieving. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    if oar_job_id == None:
        if os.environ.has_key('OAR_JOB_ID'):
            oar_job_id = os.environ['OAR_JOB_ID']
        else:
            raise ValueError, "no oar job id given and no OAR_JOB_ID environment variable found"
    countdown = Timer(timeout)
    wait_oar_job_start(oar_job_id, frontend, frontend_connection_params, countdown.remaining())
    # Get ip adresses
    process_ip = get_process(
        "(oarstat -sj %(oar_job_id)i | grep 'Running\|Terminated\|Error') > /dev/null 2>&1 && g5k-subnets -i -m -j %(oar_job_id)i" % {'oar_job_id': oar_job_id},
        host = get_frontend_host(frontend),
        connection_params = make_connection_params(
            frontend_connection_params,
            default_frontend_connection_params))
    process_ip.timeout = countdown.remaining()
    process_ip.pty = True
    process_ip.run()
    # Get network parameters
    process_net = get_process(
        "(oarstat -sj %(oar_job_id)i | grep 'Running\|Terminated\|Error') > /dev/null 2>&1 && g5k-subnets -a -j %(oar_job_id)i" % {'oar_job_id': oar_job_id},
        host = get_frontend_host(frontend),
        connection_params = make_connection_params(
            frontend_connection_params,
            default_frontend_connection_params))
    process_net.timeout = countdown.remaining()
    process_net.pty = True
    process_net.run()

    if process_net.ok and process_ip.ok:
        subnet_addresses = re.findall("(\S+)\s+(\S+)", process_ip.stdout, re.MULTILINE)
        process_net_out = process_net.stdout.rstrip().split('\t')
        network_params = dict()
        if len(process_net_out) == 7:
            network_params = {
                "ip_prefix": process_net_out[0],
                "broadcast": process_net_out[1],
                "netmask": process_net_out[2],
                "gateway": process_net_out[3],
                "network": process_net_out[4],
                "dns_hostname": process_net_out[5],
                "dns_ip": process_net_out[6]
                }
        return (subnet_addresses, network_params)
    else:
        raise ProcessesFailed, [ p for p in [process_net, process_ip] if not p.ok ]

def get_oar_job_kavlan(oar_job_id = None, frontend = None, frontend_connection_params = None, timeout = False):
    """Return the vlan id of a job (if any).

    :param oar_job_id: the oar job id. If None given, will try to get
      it from ``OAR_JOB_ID`` environment variable.

    :param frontend: the frontend of the oar job. If None given, use
      default frontend.

    :param frontend_connection_params: connection params for connecting
      to frontends if needed. Values override those in
      `execo_g5k.config.default_frontend_connection_params`.

    :param timeout: timeout for retrieving. Default is False, which
      means use
      ``execo_g5k.config.g5k_configuration['default_timeout']``. None
      means no timeout.
    """
    if isinstance(timeout, bool) and timeout == False:
        timeout = g5k_configuration.get('default_timeout')
    if oar_job_id == None:
        if os.environ.has_key('OAR_JOB_ID'):
            oar_job_id = os.environ['OAR_JOB_ID']
        else:
            raise ValueError, "no oar job id given and no OAR_JOB_ID environment variable found"
    countdown = Timer(timeout)
    wait_oar_job_start(oar_job_id, frontend, frontend_connection_params, countdown.remaining())
    process = get_process(
        'kavlan -j %s -V ' % oar_job_id,
        host = get_frontend_host(frontend),
        connection_params = make_connection_params(
            frontend_connection_params,
            default_frontend_connection_params))
    process.timeout = countdown.remaining()
    process.pty = True
    process.ignore_exit_code = True # kavlan exit code != 0 if request
    process.nolog_exit_code = True  # is for a job without a vlan
                                    # reservation
    process.run()
    if process.ok:
        try:
            return int(process.stdout.strip().rstrip())
        except:
            return None # handles cases where the job has no kavlan
                        # resource or when kavlan isn't available
    else:
        raise ProcessesFailed, [process]

def oarsubgrid(job_specs, reservation_date = None,
               walltime = None, job_type = None,
               queue = None, directory = None,
               additional_options = None,
               frontend_connection_params = None,
               timeout = False):
    """Similar to `execo_g5k.oargrid.oargridsub`, but instead of performing an oargrid reservation, it performs parallel oar submissions.

    The only difference for the user is that it returns a list of
    tuples (oarjob id, frontend) (as `execo_g5k.oar.oarsub`) instead
    of an oargrid job id. It should run faster (since oar submission
    are performed in parallel instead of sequentially, and also
    because it bypasses the oargrid layer). As with
    `execo_g5k.oargrid.oargridsub`, all parameters reservation_date,
    walltime, job_type, queue, directory, additional_options from
    job_specs are ignored and replaced by the arguments passed. As for
    oargridsub, all job submissions must succeed. If at least one job
    submission fails, all other jobs are deleted, and it returns an
    empty list.

    for parameter details, see `execo_g5k.oargrid.oargridsub`.
    """
    for job in job_specs:
        job[0].reservation_date = reservation_date
        job[0].walltime = walltime
        job[0].job_type = job_type
        job[0].queue = queue
        job[0].directory = directory
        job[0].additional_options = additional_options
    jobs = oarsub(job_specs, frontend_connection_params, timeout)
    ok = True
    for job in jobs:
        if not job[0]:
            ok = False
    if not ok:
        oardel([job for job in jobs if job[0]])
        return []
    else:
        return jobs

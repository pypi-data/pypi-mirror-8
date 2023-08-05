import glob
import time
import yaml
import json
import os
import re

from twisted.internet import fdesc
from cyclone import web

from oonib import errors as e
from oonib.report.handlers import Report
from oonib.handlers import OONIBHandler
from oonib.collector.policy import Policy

from datetime import datetime
from oonib import randomStr, otime, log
from oonib.config import config


def report_file_name(report_details):
    timestamp = otime.timestamp(datetime.fromtimestamp(report_details['start_time']))
    dst_filename = '{test_name}-{timestamp}-{probe_asn}-probe.yamloo'.format(
                timestamp=timestamp,
                **report_details)
    return dst_filename

def parseUpdateReportRequest(request):
    #db_report_id_regexp = re.compile("[a-zA-Z0-9]+$")

    # this is the regexp for the reports that include the timestamp
    report_id_regexp = re.compile("[a-zA-Z0-9_\-]+$")

    # XXX here we are actually parsing a json object that could be quite big.
    # If we want this to scale properly we only want to look at the test_id
    # field.
    # We are also keeping in memory multiple copies of the same object. A lot
    # of optimization can be done.
    parsed_request = json.loads(request)
    try:
        report_id = parsed_request['report_id']
    except KeyError:
        raise e.MissingField('report_id')

    if not re.match(report_id_regexp, report_id):
        raise e.InvalidRequestField('report_id')

    return parsed_request

def parseNewReportRequest(request):
    """
    Here we parse a new report request.
    """
    version_string = re.compile("[0-9A-Za-z_\-\.]+$")
    name = re.compile("[a-zA-Z0-9_\- ]+$")
    probe_asn = re.compile("AS[0-9]+$")
    test_helper = re.compile("[A-Za-z0-9_\-]+$")

    expected_request = {
     'software_name': name,
     'software_version': version_string,
     'test_name': name,
     'test_version': version_string,
     'probe_asn': probe_asn
    }

    parsed_request = json.loads(request)
    if 'probe_asn' not in parsed_request or not parsed_request['probe_asn']:
        parsed_request['probe_asn'] = 'AS0'

    for k, regexp in expected_request.items():
        try:
            print "Looking at %s" % k
            value_to_check = parsed_request[k]
        except KeyError:
            raise e.MissingField(k)

        print "Matching %s with %s | %s" % (regexp, value_to_check, k)
        if re.match(regexp, str(value_to_check)):
            continue
        else:
            raise e.InvalidRequestField(k)

    try:
        requested_test_helper = parsed_request['test_helper']
        if not re.match(test_helper, str(requested_test_helper)):
            raise e.InvalidRequestField('test_helper')
    except KeyError:
        pass

    return parsed_request

def validate_report_header(report_header):
    required_keys = ['probe_asn', 'probe_cc', 'probe_ip', 'software_name',
            'software_version', 'test_name', 'test_version']
    for key in required_keys:
        if key not in report_header:
            raise e.MissingReportHeaderKey(key)

    if report_header['probe_asn'] is None:
        report_header['probe_asn'] = 'AS0'

    if not re.match('AS[0-9]+$', report_header['probe_asn']):
        raise e.InvalidReportHeader('probe_asn')

    # If no country is known, set it to be ZZ (user assigned value in ISO 3166)
    if report_header['probe_cc'] is None:
        report_header['probe_cc'] = 'ZZ'

    if not re.match('[a-zA-Z]{2}$', report_header['probe_cc']):
        raise e.InvalidReportHeader('probe_cc')

    if not re.match('[a-z_\-]+$', report_header['test_name']):
        raise e.InvalidReportHeader('test_name')


    if not re.match('([0-9]+\.)+[0-9]+$', report_header['test_version']):
        raise e.InvalidReportHeader('test_version')

    return report_header

class ReportHandler(OONIBHandler):
    def initialize(self):
        self.archive_dir = config.main.archive_dir
        self.report_dir = config.main.report_dir
        self.reports = config.reports
        self.policy_file = config.main.policy_file
        self.helpers = config.helpers
        self.stale_time = config.main.stale_time if config.main.stale_time else 3600

class UpdateReportMixin(object):
    def updateReport(self, report_id, parsed_request):

        log.debug("Got this request %s" % parsed_request)
        report_filename = os.path.join(self.report_dir,
                report_id)

        self.reports[report_id].refresh()

        try:
            with open(report_filename, 'a+') as fd:
                fd.write(parsed_request['content'])
        except IOError:
            e.OONIBError(404, "Report not found")
        self.write({'status': 'success'})

class NewReportHandlerFile(ReportHandler, UpdateReportMixin):
    """
    Responsible for creating and updating reports by writing to flat file.
    """
    inputHashes = None

    def checkPolicy(self):
        policy = Policy()
        for input_hash in self.inputHashes:
            policy.validateInputHash(input_hash)
        policy.validateNettest(self.testName)

    def post(self):
        """
        Creates a new report with the input

        * Request

          {'software_name': 'XXX',
           'software_version': 'XXX',
           'test_name': 'XXX',
           'test_version': 'XXX',
           'probe_asn': 'XXX'
           'content': 'XXX'
           }

          Optional:
            'test_helper': 'XXX'
            'client_ip': 'XXX'

          (not implemented, nor in client, nor in backend)
          The idea behind these two fields is that it would be interesting to
          also collect how the request was observed from the collectors point
          of view.

          We use as a unique key the client_ip address and a time window. We
          then need to tell the test_helper that is selected the client_ip
          address and tell it to expect a connection from a probe in that time
          window.

          Once the test_helper sees a connection from that client_ip it will
          store for the testing session the data that it receives.
          When the probe completes the report (or the time window is over) the
          final report will include also the data collected from the
          collectors view point.

        * Response

          {'backend_version': 'XXX', 'report_id': 'XXX'}

        """
        # Note: the request is being validated inside of parseNewReportRequest.
        report_data = parseNewReportRequest(self.request.body)

        log.debug("Parsed this data %s" % report_data)

        software_name = str(report_data['software_name'])
        software_version = str(report_data['software_version'])

        probe_asn = str(report_data['probe_asn'])
        probe_cc = str(report_data.get('probe_cc', 'ZZ'))

        self.testName = str(report_data['test_name'])
        self.testVersion = str(report_data['test_version'])

        if self.policy_file:
            try:
                self.inputHashes = report_data['input_hashes']
            except KeyError:
                raise e.InputHashNotProvided
            self.checkPolicy()

        if 'content' in report_data:
            content = yaml.safe_load(report_data['content'])
            report_header = validate_report_header(content)

        else:
            content = {
                'software_name': software_name,
                'software_version': software_version,
                'probe_asn': probe_asn,
                'probe_cc': probe_cc,
                'test_name': self.testName,
                'test_version': self.testVersion,
                'input_hashes': self.inputHashes,
                'start_time': time.time()
            }

        content['backend_version'] = config.backend_version

        report_header = yaml.dump(content)
        content = "---\n" + report_header + '...\n'

        if not probe_asn:
            probe_asn = "AS0"

        report_id = otime.timestamp() + '_' \
                + probe_asn + '_' \
                + randomStr(50)

        # The report filename contains the timestamp of the report plus a
        # random nonce
        report_filename = os.path.join(self.report_dir, report_id)

        # The report filename contains the timestamp of the report plus a
        response = {
            'backend_version': config.backend_version,
            'report_id': report_id
        }

        requested_helper = report_data.get('test_helper')

        if requested_helper:
            try:
                response['test_helper_address'] = self.helpers[requested_helper].address
            except KeyError:
                raise e.TestHelperNotFound

        self.reports[report_id] = Report(report_id,
                                         self.stale_time,
                                         self.report_dir,
                                         self.archive_dir,
                                         self.reports)

        self.writeToReport(report_filename, content)

        self.write(response)

    def writeToReport(self, report_filename, data):
        with open(report_filename, 'w+') as fd:
            fdesc.setNonBlocking(fd.fileno())
            fdesc.writeToFD(fd.fileno(), data)

    def put(self):
        """
        Update an already existing report.

          {
           'report_id': 'XXX',
           'content': 'XXX'
          }
        """
        parsed_request = parseUpdateReportRequest(self.request.body)
        report_id = parsed_request['report_id']

        self.updateReport(report_id, parsed_request)

class UpdateReportHandlerFile(ReportHandler, UpdateReportMixin):
    def post(self, report_id):
        try:
            parsed_request = json.loads(self.request.body)
        except ValueError:
            raise e.InvalidRequest
        self.updateReport(report_id, parsed_request)

class CloseReportHandlerFile(ReportHandler):
    def get(self):
        pass

    def post(self, report_id):
        if report_id in self.reports:
            self.reports[report_id].close()
        else:
            raise e.ReportNotFound

class PCAPReportHandler(ReportHandler):
    def get(self):
        pass

    def post(self):
        pass

## Policy Handlers

class PolicyHandler(OONIBHandler):
    def initialize(self):
        self.policy = Policy()


class NetTestPolicyHandler(PolicyHandler):
    def get(self):
        """
        returns a list of accepted NetTests
        """
        self.write(self.policy.nettest)


class InputPolicyHandler(PolicyHandler):
    def get(self):
        """
        return list of input ids
        """
        self.write(self.policy.input)


### Input Handlers

class InputDescHandler(OONIBHandler):
    def get(self, inputID):
        bn = os.path.basename(inputID) + ".desc"
        try:
            f = open(os.path.join(config.main.input_dir, bn))
        except IOError:
            log.err("No Input Descriptor found for id %s" % inputID)
            raise e.InputDescriptorNotFound
        with f:
            inputDesc = yaml.safe_load(f)

        response = {'id': inputID}
        for k in ['name', 'description', 'version', 'author', 'date']:
            try:
                response[k] = inputDesc[k]
            except KeyError:
                log.err("Invalid Input Descriptor found for id %s" % inputID)
                raise e.InputDescriptorNotFound

        self.write(response)


class InputListHandler(OONIBHandler):
    def get(self):
        path = os.path.abspath(config.main.input_dir) + "/*.desc"
        inputnames = map(os.path.basename, glob.iglob(path))
        inputList = []
        for inputname in inputnames:
            with open(os.path.join(config.main.input_dir, inputname)) as f:
                d = yaml.safe_load(f)
                inputList.append({
                    'id': inputname,
                    'name': d['name'],
                    'description': d['description']
                })
        self.write(inputList)

class InputFileHandler(web.StaticFileHandler):
    def initialize(self):
        super(InputFileHandler, self).initialize(config.main.input_dir)

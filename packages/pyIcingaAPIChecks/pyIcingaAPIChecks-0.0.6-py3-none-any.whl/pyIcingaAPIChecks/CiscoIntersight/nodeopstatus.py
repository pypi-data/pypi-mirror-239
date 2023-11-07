from pyIcingaFramework.check import IcingaCheck, Measurement
from pyIcingaAPIChecks.rest import RestClient

from requests.auth import HTTPBasicAuth
import logging

from .intersight_auth import IntersightAuth

class NodeOpStatus(IcingaCheck):
    def check(self, **kwargs):

        apikey = self.extra_options.get('api-key', None)
        certfile = self.extra_options.get('api-cert-file', None)

        # set default thresholds
        self.set_threshold('80', '90', label='*')
        self.set_threshold('%Prepairing', '%Down', label='node_status')
        self.set_threshold('~%Impaired;;Operational', '%Impaired', label='op_status')

        auth = IntersightAuth(
            api_key_id=apikey,
            secret_key_filename=certfile
        )

        moid = self.filters.get('moid', None)
        logging.debug(f'Filter on Moid: {moid}')

        logging.debug(self.extra_options)
        client = RestClient(self.host, int(self.port), '/api/v1', verify=False, auth=auth)

        endpoint = client.endpoint('/appliance/NodeOpStatuses')
        resp = endpoint.get()

        logging.debug(f'API Call returned {resp.status_code}')
        logging.debug(f'JSON: {endpoint._response.json()}')

        if resp.status_code == 200:
            logging.debug('------- API RETURN Output ------')
            for r in resp.Results:
                logging.debug(f'Node State: {r.NodeState}')
                self.result.add_measurement('Node State', r.NodeState, warning=self.get_threshold('warning', 'node_status'), critical=self.get_threshold('critical', 'node_status'), is_perf=False)
                logging.debug(f'Node State: {r.OperationalStatus}')
                self.result.add_measurement('Operational Status', r.OperationalStatus, warning=self.get_threshold('warning', 'op_status'), critical=self.get_threshold('critical', 'op_status'), is_perf=False)

                logging.debug(f'cpu: {r.CpuUsage}%')
                self.result.add_measurement('load', r.CpuUsage, uom='%', warning=self.get_threshold('warning', 'load'), critical=self.get_threshold('critical', 'load'))
                logging.debug(f'mem: {r.MemUsage}%')
                self.result.add_measurement('memory_usage', r.MemUsage, uom='%', warning=self.get_threshold('warning', 'memory_usage'), critical=self.get_threshold('critical', 'memory_usage'))

        else:
            logging.info(endpoint._response.text)


        status_code = 0

        # Set stdout messages
        logging.info('checking thresholds...')
        for measurement in self.result.measurements:
            logging.debug('check measurement %s for breaches' % measurement.label)
            statusCode = measurement.status()
            if statusCode > status_code:
                status_code = int(statusCode)

        logging.info('Creating stdout msg...')
        output = []
        output.append(f'[{Measurement.status_text(status_code)}] Intersight Node Status')
        for measurement in self.result.measurements:
            if measurement.label.startswith('status_') is False:
                output.append(f'\_ [{Measurement.status_text(measurement.status())}] {measurement.label.replace("_", " ").title()}: {measurement.value} {measurement.unitOfMeasure}') # noqa

        self.result.stdout = '\n'.join(output)

        return self.result
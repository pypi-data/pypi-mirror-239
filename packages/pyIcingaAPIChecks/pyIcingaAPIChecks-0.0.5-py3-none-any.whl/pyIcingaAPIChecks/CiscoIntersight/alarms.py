from pyIcingaFramework.check import IcingaCheck, Measurement
from pyIcingaAPIChecks.rest import RestClient

from requests.auth import HTTPBasicAuth
import logging

from .intersight_auth import IntersightAuth

class Alarms(IcingaCheck):
    def check(self, **kwargs):

        apikey = self.extra_options.get('api-key', None)
        certfile = self.extra_options.get('api-cert-file', None)

        self.set_threshold('*', '1', '3')

        auth = IntersightAuth(
            api_key_id=apikey,
            secret_key_filename=certfile
        )

        logging.debug(self.extra_options)
        client = RestClient(self.host, int(self.port), '/api/v1', verify=False, auth=auth)

        endpoint = client.endpoint('/cond/Alarms?$filter=Severity ne Cleared')
        resp = endpoint.get()

        logging.debug(f'API Call returned {resp.status_code}')

        active_alarm_severities = {'none': 0, 'info': 0, 'warning': 0, 'critical': 0}

        if resp.status_code == 200:
            for alarm in resp.Results:
                active_alarm_severities[alarm.Severity.lower()] += 1
        else:
            logging.info(endpoint._response.text)


        self.result.add_measurement('info_alarms', active_alarm_severities['info'],
                                    self.get_threshold('warning', 'info_alarms'),
                                    self.get_threshold('critical', 'info_alarms'),
                                    alerts=False)
        self.result.add_measurement('warning_alarms', active_alarm_severities['warning'],
                                    self.get_threshold('warning', 'warning_alarms'),
                                    self.get_threshold('critical', 'warning_alarms'),
                                    alerts=True)
        self.result.add_measurement('critical_alarms', active_alarm_severities['critical'],
                                    self.get_threshold('warning', 'warning_alarms'),
                                    self.get_threshold('critical', 'warning_alarms'),
                                    alerts=True)

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
        output.append(f'[{Measurement.status_text(status_code)}] Intersight Alarm Status')
        for measurement in self.result.measurements:
            output.append(f'\_ [{Measurement.status_text(measurement.status())}] {measurement.label.replace("_alarms", "").title()}: {measurement.value}') # noqa

        self.result.stdout = '\n'.join(output)

        return self.result

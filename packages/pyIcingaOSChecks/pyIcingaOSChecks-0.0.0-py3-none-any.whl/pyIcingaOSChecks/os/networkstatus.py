from pyIcingaFramework.check import IcingaCheck, Measurement
from pyIcingaFramework.utils import to_bool
import re
import logging
import psutil



_METADATA = {'name':'Network Status', 'version': '1.0.0', 'status': 'preview', 'author': 'Paul Denning'}
_DESCRIPTION = '''
Module to monitor network interface stats

'''

_FITLERS = '''
| filter name | Description | required |
|---|---|---|
| interfaces | comma delimited list of interfaces to monitor | 

'''

_MEASUREMENTS = '''
'''

logger = logging.getLogger()

def to_bool(value):
    return value in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


class NetworkStatus(IcingaCheck):

    def check(self, **kwargs):


        logging.info('Building filters....')
        filters = kwargs.get('filters', None)
        filtered_intf = None

        if filters:
            if filters.get('interfaces', None):
                filtered_intf = [ x.strip() for x in filters['interfaces'].split(',')]

        logging.debug('filters applied: %s' % filters)

        logging.info('getting disk data....')

        data = psutil.net_if_stats()

        logging.debug('Interface Stats data %r' % (data,))
    
        self.set_threshold('%DOWN','%DOWN')


        #Add measurements
        for intf_name, intf_data in data.items():
            if (filtered_intf):
                logging.debug('filters: %s in %s result: %s' % (intf_name, filtered_intf, intf_name in filtered_intf))

            if (filtered_intf and intf_name in filtered_intf) or not filtered_intf:
                if intf_data.isup:
                    status = 'UP'
                else:
                    status = 'DOWN'
                self.result.add_measurement('interface_%s' % intf_name, status, warning=self.get_threshold('warning',intf_name), critical=self.get_threshold('critical',intf_name), is_perf=False)

        status_code = 0

        #Set stdout messages
        logging.info('checking thresholds...')
        for measurement in self.result.measurements:
             logging.debug('check measurement %s for breaches' % measurement.label)
             statusCode = measurement.status()
             if statusCode > status_code:
                 status_code = int(statusCode)

        logging.info('Creating stdout msg...')

        output = []
        output.append(f'[{Measurement.status_text(status_code)}] Network Interfaces')
        for measurement in self.result.measurements:
            output.append(f'\_ [{Measurement.status_text(measurement.status())}] {measurement.label.capitalize().replace("_", ": ")} - {measurement.value}')
        self.result.stdout = '\n'.join(output)
        return self.result
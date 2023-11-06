from pyIcingaFramework.check import IcingaCheck, Measurement

import re
import logging
import psutil

_METADATA = {'name': 'Load', 'version': '1.0.0', 'status': 'preview', 'author': 'Paul Denning'}
_DESCRIPTION = '''
Module to monitor the load of the local machine

'''

_FITLERS = '''
| filter name | Description | required |
|---|---|---|
| stats | which stats to return, can be a comma delimited list of measurement labels| false

'''

_MEASUREMENTS = '''
| name | Units of Measure | Description | Default Thresholds |
|------|------------------|------------|----------|
| avg | % | Percentage of avg across all cpus | warn: 80%, crit: 90% |
| cpu_<x> | % | Percentage of load on the cpu | warn: 80%, crit: 90% |



'''

def to_bool(value):
    return value in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

class Load(IcingaCheck):

    def check(self, **kwargs):

        cpu_count = psutil.cpu_count()

        data = {}

        # setup and get avg CPU Data
        stat_list = ['overall']
        self.set_threshold('80', '90', 'overall')
        data['overall'] = psutil.cpu_percent(interval=0.1)

        # setup and get CPU Data for each CPU
        percpudata = psutil.cpu_percent(interval=0.1, percpu=True)
        for num in range(0, cpu_count):
            stat_list.append('cpu_%d' % num)
            data[f'cpu_{num}'] = percpudata[num]
            self.set_threshold('101', '102', f'cpu_{num}')

        logging.debug('\nvalues %s' % data)
        logging.debug('Stats list %s' % stat_list)

        filters = self.filters

        logging.debug('filters applied: %s' % filters)

        # Add measurements
        for stat in stat_list:
            self.result.add_measurement(stat, data[stat], uom='%', warning=self.get_threshold('warning',stat), critical=self.get_threshold('critical',stat))   # noqa

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
        overall = self.result.get_measurement('overall')
        output.append(f'[{Measurement.status_text(status_code)}] CPU Load')
        output.append(f'\_ [{Measurement.status_text(overall.status())}] Overall Load: {overall.value}%')
        for m in self.result._measurements:
            if m.label != 'overall':
                output.append(f'\_ [{Measurement.status_text(m.status())}] Core {m.label.split("_")[-1]}: {m.value}')

        self.result.stdout = '\n'.join(output)

        return self.result

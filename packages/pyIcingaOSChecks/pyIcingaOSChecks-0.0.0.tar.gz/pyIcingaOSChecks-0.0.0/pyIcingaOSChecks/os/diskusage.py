from pyIcingaFramework.check import IcingaCheck, IcingaCheckResult
from pyIcingaFramework.exceptions import UnknownCheckStateError
from pyIcingaFramework.utils import convert_data

import logging
import psutil



_METADATA = {'name':'Disk Usage', 'version': '1.0.0', 'status': 'preview', 'author': 'Paul Denning'}
_DESCRIPTION = '''
Module to monitor local disk usage

'''

_FITLERS = '''
| filter name | Description | required |
|---|---|---|
| disk | disk to monitor | true

'''

_MEASUREMENTS = '''
| name | Units of Measure | Description | Default Thresholds |
|------|------------------|------------|----------|
| percent | % | Percentage of used space | warn 80% crit 10% |
| free | GB | About of free space on the disk | warn 20% of total crit: 10% of total |
| used | GB | Amount of used space | warn: 80% of total disk crit: 10% of total 


'''



def to_bool(value):
    return value in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


class DiskUsage(IcingaCheck):

    def check(self, **kwargs):

        logging.info('Building filters....')
        filter_disk = None

        if self.filters:
            if not self.filters.get('disk', None):
                raise UnknownCheckStateError(self, 'disk filter must be applied')
            else:
                logging.info('Checking for disk %s ' % self.filters.get('disk', None))
                filter_disk = self.filters.get('disk', None)

        else:
            raise UnknownCheckStateError(self, 'disk filter must be applied')
        
        logging.info('Set default thresholds')
        self._set_default_thresholds('80', '90')
        logging.debug('filters applied: %s' % self.filters)

        logging.info('getting disk data....')

        data = psutil.disk_usage(filter_disk)

        logging.debug('Disk data %r' % (data,))
        
        warnings = int(self.get_threshold('warning','percent_used'))
        criticals = int(self.get_threshold('critical','percent_used'))

        def_warn_free = round(data.total * ((100 - warnings) / 100))
        def_warn_used = round(data.total * (warnings / 100))

        def_crit_free = round(data.total * ((100 - criticals) / 100))
        def_crit_used = round(data.total * (criticals / 100))

        #Set thresholds
        warn_threshold = [str(warnings), '%s:' % def_warn_free, str(def_warn_used), None]
        crit_threshold = [str(criticals), '%s:' % def_crit_free, str(def_crit_used), None]

        logging.info('warn thresholds %r ' % warn_threshold)
        logging.info('thresholds %r ' % crit_threshold)
        # get threshold overrides


        #Add measurements


        self.result.add_measurement('percent_used', data.percent, uom='%', warning=warn_threshold[0], critical=crit_threshold[0], minimum=0, maximum=100)   #pylint: disable=no-member
        self.result.add_measurement('free', data.free, uom="B", warning=warn_threshold[1], critical=crit_threshold[1], minimum=0, maximum=data.total)   #pylint: disable=no-member 
        self.result.add_measurement('used', data.used, uom="B", warning=warn_threshold[2], critical=crit_threshold[2], minimum=0, maximum=data.total)   #pylint: disable=no-member 

        status_code = 0
        status = 'OK1'

        #Set stdout messages
        logging.info('checking thresholds...')
        for measurement in self.result.measurements:
             logging.debug('check measurement %s for breaches' % measurement.label)
             statusCode = measurement.status()
             if statusCode > status_code:
                 status_code = int(statusCode)


        logging.info(f'Creating stdout msg...statuscode {status_code}')
        if status_code == 0:
            status = 'OK'
        elif status_code == 1:
            status = 'WARNING'
        elif status_code == 2:
            status = 'CRITICAL'
        elif status_code == 3:
            status = 'UNKNOWN'

        free_space, fuom = convert_data(data.free)
        used_space, uuom = convert_data(data.used)
        output = []
        output.append(f'[{status}] Free Parition space: {status}')
        output.append(f'\_ [{status}] Parition {filter_disk}: {free_space}{fuom} free')

        self.result.stdout = '\n'.join(output)

        return self.result
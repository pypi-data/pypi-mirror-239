from pyIcingaFramework.check import IcingaCheck, Measurement
from pyIcingaFramework.utils import convertDataUOM
import logging
import psutil
from psutil._common import bytes2human



_METADATA = {'name':'Memory', 'version': '1.0.0', 'status': 'preview', 'author': 'Paul Denning'}
_DESCRIPTION = '''
Module to monitor memory stats
'''

_FITLERS = '''

'''

_MEASUREMENTS = '''
| name | Units of Measure | Description | Default Thresholds |
|------|------------------|------------|----------|
| available | MB | the amount of available memory | warn: 20% crit: 10% |
| used | MB | the amount of used memory | warn: 80% crit: 90% |
| percent | % | Percentage of memory used | warn: 80% crit: 90% |
| total | % | the total amount of memory| NIL |

'''

logger = logging.getLogger()

def to_bool(value):
    return value in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


class Memory(IcingaCheck):

    def check(self, **kwargs):

        stat_list = ['percent', 'available','used', 'total']
        stat_uom = ['%', 'B', 'B', 'B']

        #get OS Memory Data
        data = psutil.virtual_memory()
    
        #setup default threshods if not defined in command
        def_warn_used = '%s' % round((data.total) * 0.8,None)
        def_crit_used = '%s' % round((data.total) * 0.9,None)

        def_warn_free = '%s:' % round((data.total) * 0.2,None)
        def_crit_free = '%s:' % round((data.total) * 0.1,None)

        self.set_threshold('80', '90', '*')
        self.set_threshold('80', '90', 'percent')
        self.set_threshold(f'{data.total + 10}', f'{data.total + 10}', 'total')
        self.set_threshold(def_warn_free, def_crit_free, 'available')
        self.set_threshold(def_warn_used, def_crit_used, 'used')
        


        #Add measurements
        logging.debug(data)         #pylint: disable=no-member

        for stat in stat_list:
            idx = stat_list.index(stat)
            # if 'MB' in stat_uom[idx]:
            #     value = round(getattr(data, stat) / 1024 / 1024, None)
            # else:
            #     value = getattr(data,stat)
            value = getattr(data,stat)
            logging.info(f'Measurement: {stat}, value: {value}, uom: {stat_uom[idx]}')
            if stat == 'total':
                self.result.add_measurement(stat, value, uom=stat_uom[idx], warning=self.get_threshold('warning', stat), critical=self.get_threshold('critical', stat), is_perf=False, alerts=False)   #pylint: disable=no-member
            else:
                self.result.add_measurement(stat, value, uom=stat_uom[idx], warning=self.get_threshold('warning', stat), critical=self.get_threshold('critical', stat))   #pylint: disable=no-member

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
        output.append(f'[{Measurement.status_text(status_code)}] Virtual Memory Usage')
        for measurement in self.result.measurements:
            if measurement.label == 'percent':
                value = f'{measurement.value}%'
                output.append(f'\_ [{Measurement.status_text(measurement.status())}] {measurement.label.title()} Used Memory: {value}')
            else:
                value = f'{bytes2human(measurement.value)}'
                output.append(f'\_ [{Measurement.status_text(measurement.status())}] {measurement.label.title()} Memory: {value}')

        self.result.stdout = '\n'.join(output)

        return self.result
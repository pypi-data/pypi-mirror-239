
from pyIcingaFramework.check import IcingaCheck, Measurement
from pyIcingaFramework.exceptions import UnknownCheckStateError
from pyIcingaFramework.utils import convert_data_rates
from pyIcingaFramework.cache import CacheManager, CacheEntry

import re
import logging
import psutil
from psutil._common import bytes2human
import os, sys, datetime, tempfile
from collections import namedtuple

_METADATA = {'name': 'Network Stats', 'version': '1.0.0', 'status': 'preview', 'author': 'Paul Denning'}
_DESCRIPTION = '''
Module to monitor network interface counters
'''

_FITLERS = '''
| filter name | Description | required |
|---|---|---|
| interface | network interface to monitor | true |
| stats | which stats to return, can be a comma delimited list of measurement labels| false

'''

_MEASUREMENTS = '''
| name | Units of Measure | Description | Default Thresholds |
|------|------------------|------------|----------|
| bps_in | bits (b) | bits per second inbound to the interface | warn: 80% of interface speed, crit: 90% of interface speed |
| bps_out | bits (b) | bits per second outbound of the interface | warn: 80% of interface speed, crit: 90% of interface speed |
| pktsps_in | integer | packets per second inbound to the interface | warn: 80% , crit: 90% *note thresholds are set to interface theoretical max packets at 512 packet size |
| pktsps_out | integer | packets per second outbound to the interface | warn: 80% , crit: 90% *note thresholds are set to interface theoretical max packets at 512 packet size |
| drops_in_perc | % | Percent of pages dropped compared to packets in rate | warn: 30% , crit: 50%  |
| drops_out_perc | % | Percent of pages dropped compared to packets out rate | warn: 30% , crit: 50%  |

stat_list = ['bps_in','bps_out', 'pktps_in', 'pktps_out', 'drops_in_perc', 'drops_out_perc']
'''  # noqa


class NetworkStats(IcingaCheck):

    def check(self, **kwargs):
        cache_timeformat = '%Y-%m-%d %H:%M:%S'
        cacheManager = CacheManager('local_netstat_io.json')

        ###
        # stat model
        # statname: {
        #    'uom': 'uom type'
        #    'value: 'value'
        # }

        stat_list = {'bps_in': {'uom': 'b'},
                     'bps_out': {'uom': 'b'},
                     'pktps_in': {'uom': ''},
                     'pktps_out': {'uom': ''},
                     'drops_in_perc': {'uom': '%'},
                     'drops_out_perc': {'uom': '%'}}

        logging.info('Load cache.....')

        filters = self._parseFilters(required_filters='interface',
                                     stats_list=list(stat_list.keys()),
                                     required_stats=['bps_in', 'bps_out'])

        logging.info('Interface to check: %s .....' % filters['interface'])
        logging.info('getting network data....')

        ################################
        #     fetch the data           #
        ################################

        data = psutil.net_io_counters(pernic=True)
        intf_data = data.get(filters['interface'], None)

        logging.debug('Interface Data: %r ' % (intf_data,))

        if not intf_data:
            raise UnknownCheckStateError(self, 'No such interface: %s' % filters['interface'])

        logging.debug('Interface Stats data %r' % (intf_data,))

        ################################
        #     compile the the data     #
        ################################

        # build Bbps Pkts/s from cache

        bps_rate_in = 0
        bps_rate_out = 0
        pkts_rate_in = 0
        pkts_rate_out = 0

        drop_ratio_in = 0
        drop_ratio_out = 0
        err_ratio_in = 0
        err_ratio_out = 0

        if psutil.net_if_stats()[filters['interface']].speed != 0:
            intf_speed = psutil.net_if_stats()[filters['interface']].speed * 1000 * 1000
        else:
            intf_speed = 10000 * 1000 * 1000

        # cached_data = cache.get(filtered_intf, None)
        # cached_data = cacheManager.cache.get('interface_stats', {'time': datetime.datetime.now().strftime(cache_timeformat), 'data': {}})
        # cached_timestamp = datetime.datetime.strptime(cached_data.time, cache_timeformat)
        cached_data = cacheManager.getEntry(filters['interface'])
        logging.debug(f'cache data {cached_data}')
        # cached_data = cached_data.data.get(filters['interface'], None)

        if cached_data:
            cached_timestamp = datetime.datetime.strptime(cached_data.time, cache_timeformat)
            logging.debug(f'cache data for interface {cached_data}')
            delta = datetime.datetime.now() - cached_timestamp

            logging.info('Time Detla: %r' % delta)

            bps_rate_in = ((intf_data.bytes_recv * 8) - (cached_data['bytes_recv'] * 8)) / delta.seconds
            bps_rate_out = ((intf_data.bytes_sent * 8) - (cached_data['bytes_sent'] * 8)) / delta.seconds
            pkts_rate_in = (intf_data.packets_recv - cached_data['packets_recv']) / delta.seconds
            pkts_rate_out = (intf_data.packets_recv - cached_data['packets_recv']) / delta.seconds
            if pkts_rate_in > 0:
                drop_ratio_in = ((intf_data.dropin - cached_data['dropin']) / delta.seconds) / pkts_rate_in * 100

            if pkts_rate_out > 0:
                drop_ratio_out = ((intf_data.dropout - cached_data['dropout']) / delta.seconds) / pkts_rate_out * 100

        stat_list['bps_in']['value'] = bps_rate_in
        stat_list['bps_out']['value'] = bps_rate_out
        stat_list['pktps_in']['value'] = pkts_rate_in
        stat_list['pktps_out']['value'] = pkts_rate_out
        stat_list['drops_in_perc']['value'] = drop_ratio_in
        stat_list['drops_out_perc']['value'] = drop_ratio_out

        logging.debug('''Data bps_in: %d, bps_out: %d, pkt_in/s: %d, pkts_out/s: %d, drops_in_rate: %d%%,
                       drops_out_rate: %d%%''' % (bps_rate_in,
                                                  bps_rate_out,
                                                  pkts_rate_in,
                                                  pkts_rate_out,
                                                  drop_ratio_in,
                                                  drop_ratio_out))

        ################################
        #     set threshols            #
        ################################
        self.set_threshold('%DOWN', '%DOWN', 'status')
        self.set_threshold('80', '90', 'bps_in')
        self.set_threshold('80', '90', 'bps_out')
        self.set_threshold('80', '90', 'pktps_in')
        self.set_threshold('80', '90', 'pktps_out')
        self.set_threshold('5', '10', 'drops_in_perc')
        self.set_threshold('5', '10', 'drops_out_perc')

        # Add measurements
        for k, stat in stat_list.items():

            if 'drops' in stat: 
                warn = self.get_threshold('warining', k)
                crit = self.get_threshold('critical', k)
            elif intf_speed > 0 and 'drops' not in k:
                warn = str(round(intf_speed * (int(self.get_threshold('warning', k)) / 100)))
                crit = str(round(intf_speed * (int(self.get_threshold('critical', k)) / 100)))
            else:
                warn = None
                crit = None

            logging.info(f'Checking that stat: {k} is in the stats filter list {filters["stats"]}')
            if k in filters['stats']:
                self.result.add_measurement(f'{filters["interface"].lower()}::{k.lower()}',
                                            round(stat['value']),
                                            uom=stat['uom'],
                                            warning=warn,
                                            critical=crit)

        # Set stdout messages
        logging.info('checking thresholds...')
        status_code = 0
        for measurement in self.result.measurements:
            logging.debug('check measurement %s for breaches' % measurement.label)
            statusCode = measurement.status()
            if statusCode > status_code:
                status_code = int(statusCode)

        in_rate, in_uom = convert_data_rates(self.result.get_measurement(f'{filters["interface"].lower()}::bps_in').value)
        out_rate, out_uom = convert_data_rates(self.result.get_measurement(f'{filters["interface"].lower()}::bps_out').value)

        output = []
        output.append(f'[{Measurement.status_text(status_code)}] Interface Stats')
        output.append(f'''\_ [{Measurement.status_text(status_code)}] {filters["interface"].lower()} in: {in_rate} {in_uom}  out: {out_rate}{out_uom}''')  # noqa

        self.result.stdout = '\n'.join(output)

        logging.info("building new cache data...")

        # new_cache = []
        cacheData = {}

        if cached_data is None or cached_data.isExpired():
            logging.info("Cache entry is expired, creating new cache")
            timestamp = datetime.datetime.now().strftime(cache_timeformat)
            for k, value in data.items():
                logging.debug('%s,%s' % (k, value))
                if cacheData.get(k, None) is None:
                    cacheData[k] = {}

                cacheData[k]['bytes_sent'] = value.bytes_sent
                cacheData[k]['bytes_recv'] = value.bytes_recv
                cacheData[k]['packets_sent'] = value.packets_sent
                cacheData[k]['packets_recv'] = value.packets_recv
                cacheData[k]['errin'] = value.errin
                cacheData[k]['errout'] = value.errout
                cacheData[k]['dropin'] = value.dropin
                cacheData[k]['dropout'] = value.dropout

            logging.info(f'Data to cache {cacheData}')

            ce = CacheEntry('interface_stats', time=timestamp, expiry=30, data=cacheData)
            cacheManager.setCache('networkstats', ce)
            cacheManager.commitCache()
        return self.result

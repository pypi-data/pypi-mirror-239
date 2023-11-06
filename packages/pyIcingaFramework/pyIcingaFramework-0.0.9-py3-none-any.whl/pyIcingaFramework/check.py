import logging
import re
from pyIcingaFramework.utils import to_bool
from pyIcingaFramework.exceptions import CheckError, UnknownCheckStateError


class IcingaCheck(object):
    def __init__(self, host, port, filters={}, extra_options={}, warning_thresholds={}, critical_thresholds={},
                 username=None, password=None, **kwargs):

        self.filters = filters
        self.username = username
        self.password = password
        self.extra_options = extra_options
        self.host = host
        self.port = port

        self.warning_thresholds = warning_thresholds
        self.critical_thresholds = critical_thresholds

        self.result = IcingaCheckResult()

        for k, item in self.extra_options.items():
            if item.lower() in ['true', 't', 'y', 'yes']:
                self.extra_options[k] = True
            elif item.lower() in ['false', 'f', 'n', 'no']:
                self.extra_options[k] = False

    def _parseFilters(self, required_filters=None, stats_list=[], required_stats=[]):

        logging.debug(f'Building filter list stats list {stats_list}')
        logging.info('Building filters....')
        filters = {}
        filters['stats'] = []

        logging.debug('filters applied: %s' % self.filters)

        if required_filters:
            if type(required_filters) is list:
                for item in required_filters:
                    if item not in self.filters.keys():
                        raise UnknownCheckStateError(self, f'{item} needs to be set')
            elif type(required_filters) is str:
                if required_filters not in self.filters.keys():
                    raise UnknownCheckStateError(self, f'{item} needs to be set')

        for k, value in self.filters.items():
            if k == 'stats':
                filters['stats'] = value.split(',')

            elif k == '~stats':
                filters['stats'] = stats_list
                remove_statslist = value.split(',')

                for rstat in remove_statslist:
                    try:
                        filters['stats'].remove(rstat)
                    except ValueError:
                        logging.debug('Attemtped to remove stat {rstat} from stat collection but it could not found')
            else:
                filters[k] = value

        if len(filters['stats']) == 0:
            filters['stats'] = stats_list
        else:
            for stat in required_stats:
                if stat not in filters['stats']:
                    filters['stats'].append(stat)

        logging.debug(f'Filters built {filters}')
        return filters

    def _set_default_thresholds(self, warning, critical):
        self.set(warning, critical)

    def set_threshold(self, warning, critical, label='*'):
        logging.info(f'Adding threshold {label}: w:{warning}/{type(warning)} c:{critical}/{type(critical)}')
        if self.warning_thresholds.get(label) is None:
            self.warning_thresholds[label] = warning

        if self.critical_thresholds.get(label) is None:
            self.critical_thresholds[label] = critical

    def get_threshold(self, level, label):
        t = {}
        if level.lower() == 'warning':
            t = self.warning_thresholds
        elif level.lower() == 'critical':
            t = self.critical_thresholds
        else:
            raise CheckError(msg='Unknown threshold level')

        threshold = t.get(label, None)
        if threshold is None:
            logging.info('try and get default threshold')
            threshold = t.get('*', None)

        if threshold is None:
            logging.debug(f'Thresholds for {level}: {t}')
            raise CheckError('IcingaCheck', f'Unable to find a {level} threshold value')

        return threshold

    def check(self, **kwargs):
        logging.error('Check function needs to be overwritten')
        self.result.stdout("[UNKNOWN] Check function needs to be overwritten")
        return self.result


class IcingaCheckResult(object):
    def __init__(self, stdout='', value=''):
        self._stdout = stdout
        self._value = value

        self._measurements = []
        self._thresholds = []

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, value):
        self._stdout = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def measurements(self):
        return self._measurements

    def add_measurement(self, label, value, warning='', critical='', uom='', minimum='', maximum='', is_perf=True,
                        alerts=True):
        measurement = Measurement(label, value, warning, critical, uom, minimum, maximum, is_perf, alerts)
        self._measurements.append(measurement)
        return measurement

    def get_measurement(self, label):
        for measurement in self._measurements:
            if label == measurement.label:
                return measurement

        return None

    def _formatPerfData(self, label, value, uom='', warn='', crit='', min_value='', max_value=''):
        rtn = "'{}'={}{};{};{};{};{}".format(label, value, uom, warn, crit, min_value, max_value)
        return rtn

    def get_output(self):
        perfdata = []
        exitcode = 0
        output = ""

        for measurement in self.measurements:
            if measurement.isperf:
                perfdata.append(self._formatPerfData(measurement.label, measurement.value,
                                                     uom=measurement.unitOfMeasure, warn=measurement.warning,
                                                     crit=measurement.critical, min_value=measurement.minimum,
                                                     max_value=measurement.maximum))

            measurementStatus = measurement.status()
            if measurementStatus > exitcode:
                exitcode = measurementStatus

        if len(perfdata) > 0:
            perfOutput = ' '.join(perfdata)
            output = f'{self.stdout} | {perfOutput}'
        else:
            output = f'{self.stdout}'

        return (exitcode, output)


class Measurement(object):
    def __init__(self, label, value, warning, critical, uom, minimum, maximum, is_perf=True, alerts=True):
        self.label = label
        self.value = value
        self.unitOfMeasure = uom
        self.minimum = minimum
        self.maximum = maximum
        self.warning = warning
        self.critical = critical
        self.isperf = is_perf
        self.alerts = alerts

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def isperf(self):
        return self._isperf

    @isperf.setter
    def isperf(self, value):
        self._isperf = value

    @property
    def unitOfMeasure(self):
        return self._uom

    @unitOfMeasure.setter
    def unitOfMeasure(self, value):
        if isinstance(value, int):
            raise ValueError("UOM can not be an integer")
        self._uom = value

    @property
    def minimum(self):
        return self._minimum

    @minimum.setter
    def minimum(self, value):
        try:
            self._minimum = int(value)
        except ValueError:
            self._minimum = ''

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, value):
        if not value or value == '':
            self._maximum = ''

        elif isinstance(value, int):
            self._maximum = value
        else:
            try:
                self._maximum = int(value)
            except ValueError:
                raise ValueError("Maximum value must be an integer")
            finally:
                self._maximum = ''

    @property
    def warning(self):
        return self._warning

    @warning.setter
    def warning(self, value):
        self._warning = value

    @property
    def critical(self):
        return self._critical

    @critical.setter
    def critical(self, value):
        self._critical = value

    def status(self):
        '''gets the status of the measurement
           :returns: 0 = ok, 1 = Warning, 2 = Critical 3 = Unknown
        '''

        serviceStatus = 0
        isWarning = Measurement.check_threshold(self.value, self.warning)
        isCritical = Measurement.check_threshold(self.value, self.critical)

        if isWarning:
            # The service is breached the warning threshold
            serviceStatus = 1

        if isCritical:
            # The service is breached the critical threshold
            serviceStatus = 2

        logging.info(f'Status of Check is {serviceStatus}')
        return serviceStatus

    @staticmethod
    def status_text(status_code):
        statusText = 'UNKNOWN'

        if status_code == 0:
            statusText = 'OK'
        elif status_code == 1:
            statusText = 'WARNING'
        elif status_code == 2:
            statusText = 'CRITICAL'
        else:
            statusText = 'UNKNOWN'

        return statusText

    @staticmethod
    def check_threshold(value, threshold):
        ''' checks to see if a value is in breach of its threshold using the standard nagios threshold values
            :param value: value to check
            :param threshold: value to compare against
            :returns: true/false if it breachs the threshold
            :raises: ValueError
        '''
        if not threshold:
            return False

        logging.debug('Threshold:{}/{} value: {}/{}'.format(threshold, type(threshold), value, type(value)))

        re_standard_range = r'^(?P<end>\d+)$'
        re_start_value = r'^(?P<start>-?\d+)\:$'
        re_end_value = r'^~\:(?P<end>-?\d+)$'
        re_outside_range = r'^(?P<start>-?\d+)\:(?P<end>-?\d+)$'
        re_inside_range = r'^@(?P<start>-?\d+)\:(?P<end>-?\d+)$'
        re_instrings = r'^%([\w\d]+)(?:;;\s*([\w\d]+))*$'
        re_notinstrings = r'^~%([\w\d]+)(?:;;\s*([\w\d]+))*$'

        match_standard_r = re.search(re_standard_range, threshold, flags=re.M)
        match_start_r = re.search(re_start_value, threshold, flags=re.M)
        match_end_r = re.search(re_end_value, threshold, flags=re.M)
        match_outside_r = re.search(re_outside_range, threshold, flags=re.M)
        match_inside_r = re.search(re_inside_range, threshold, flags=re.M)
        match_strings = re.search(re_instrings, threshold, flags=re.M)
        match_notstrings = re.search(re_notinstrings, threshold, flags=re.M)

        # Threshold range 10
        if match_standard_r:
            end = int(match_standard_r.group('end'))
            logging.debug('check value (%s) between 0 and %s' % (value, end))
            return not int(value) in range(0, end)
        # threshold range 10:
        elif match_start_r:
            start = int(match_start_r.group('start'))
            logging.debug('check value (%s) between %s and ∞' % (value, start))
            return not int(value) > start

        # threshold range ~:10
        elif match_end_r:
            end = int(match_end_r.group('end'))
            logging.debug('check value (%s) between negative ∞ and %s' % (value, end))
            return not int(value) < end

        # threshold range 1:10
        elif match_outside_r:
            end = int(match_outside_r.group('end'))
            start = int(match_outside_r.group('start'))
            logging.debug('check value (%s) between %s and %s' % (value, start, end))
            return not int(value) in range(start, end)

        # threshold range @1:10
        elif match_inside_r:
            start = int(match_inside_r.group('start'))
            end = int(match_inside_r.group('end'))
            logging.debug('check value (%s) outside of %s and %s' % (value, start, end))

            return not int(value) not in range(start, end)

        # theshold range %string1;;string2
        elif match_strings:
            # Threshold is breached for the threshold setting is returned from the device
            matches = [x for x in match_strings.groups() if x]
            logging.debug('check value (%s) in %s result: %s' % (value, matches, value in matches))
            return value in matches

        # thresold not in list ~%string1;;string2
        elif match_notstrings:
            # Threshold is breached for the threshold setting is not returned from the device
            matches = [x for x in match_notstrings.groups() if x]
            logging.debug('check value (%s) not in %s result: %s' % (value, matches, value not in matches))
            return value not in matches

        elif threshold == '' or not threshold:
            return False

        else:
            raise ValueError()

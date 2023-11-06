
from pyIcingaFramework.check import IcingaCheck
from pyIcingaFramework.utils import to_bool
import logging

_METADATA = {'name':'Test Check', 'version': '1.0.0', 'status': 'test', 'author': 'Paul Denning'}
_DESCRIPTION = '''
Used for testing of the framework
'''

_MEASUREMENTS = '''
| name | Units of Measure | Thresholds |
|------|------------------|------------|
|test_measurement_1| MB | Amount of MB behind master| 
|test_measurement_2| MB | Amount of % behind master|
'''


class Test(IcingaCheck):

    def check(self, **kwargs):

        logging.info('**** Running Test Check *******')

        logging.info('Setting default thresholds')
        self._set_default_thresholds('10','10')

        data = {'test_measurement_1': 9, 'test_measurement_2': 20}

        logging.info(f'Got test data: {data}')

        output = []

        for k, value in data.items():
            logging.info(f'Checking messurement {k}')
            logging.info(f'')
            warnThreshold = self.get_threshold('warning', 'test_measurement_1')
            critThreshold = self.get_threshold('critical', 'test_measurement_1')

            self.result.add_measurement(k,data[k], warning=warnThreshold, critical=critThreshold, uom='b')

            output.append(f'\_ [OK] {k} is within target range')

        output.insert(0,'[OK] test check is good')
        self.result.stdout = '\n'.join(output)

        return self.result
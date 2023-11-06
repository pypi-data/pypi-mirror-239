import math


def to_bool(value, true_values=['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']):
    '''Coverts a list of typical affirmative words to true otherwise returns false
       :param value: value to convert to bool
       :param true_values: list of words that will convert to true otherwise will return false
       :returns: True or False based on string.
    '''
    return str(value).lower() in true_values


def convertDataUOM(value, uom, factor=1000):
    '''Converts data units from one Unit of measurement to another,
        :param value: value to convert
        :param uom: Unit of measurement to convert to
        :param factor: the factor to convert by, 10 for 1000, 2 for 1024
        :returns: converted unit of measurement
    '''
    convertedValue = value

    # expmap = {'PB': 5, 'TB': 4, 'GB': 3, 'MB': 2, 'KB': 1}

    if uom == 'TB':
        convertedValue = value / pow(factor, 4)
    elif uom == 'GB':
        convertedValue = value / pow(factor, 3)
    elif uom == 'MB':
        convertedValue = value / pow(factor, 2)
    elif uom == 'KB':
        convertedValue = value / pow(factor, 1)
    else:
        convertedValue = value

    return convertedValue


def convert_data(size, uom=None, unit_size=1024, unit_names=('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'EB',
                                                             'ZB', 'YB')):
    if size == 0:
        return (0, 'B')

    i = int(math.floor(math.log(size, unit_size)))

    p = math.pow(unit_size, i)
    s = round(size / p, 2)
    return (s, unit_names[i])


def convert_data_rates(size, uom=None, unit_size=1000, unit_names=('bps', 'Kbps', 'Mbps', 'Gbps', 'tbps', 'pbps',
                                                                   'ebps', 'zbps', 'ybps')):
    if size == 0:
        return (0, 'bps')

    return convert_data(size, uom, unit_size, unit_names)

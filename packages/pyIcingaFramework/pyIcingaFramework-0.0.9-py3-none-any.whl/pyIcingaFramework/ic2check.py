#!/bin/env python3
import argparse
import getpass
import logging
import logging.config
import traceback
import importlib
import sys

from pyIcingaFramework.exceptions import UnknownCheckStateError
from pyIcingaFramework.check import IcingaCheck, IcingaCheckResult


def setupLogger(level=None):
    logging.basicConfig(format='''%(asctime)s [%(levelname)s] %(name)s: %(message)s''', level=level)
    # logging.config.dictConfig({
    #     'version': 1,
    #     'disable_existing_loggers': 'False',
    #     'formatters': {
    #         'standard': {
    #             'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    #         },
    #     },
    #     'handlers': {
    #         'default': {
    #             'level': level,
    #             'class': 'logging.StreamHandler',
    #             'formatter': 'standard',
    #         },
    #     },
    #     'loggers': {
    #         'pyIcingaFramework2': {
    #             'handlers': ['default'],
    #             'level': level,
    #             'propagate': True
    #         },
    #     },

    # })


def load_module(checkname):

    logging.info('-------  loading module ---------')

    check_path = checkname.split('.')
    if len(check_path) == 2:
        logging.debug('adding standard path')
        check_path.insert(0, 'checks')
        check_path.insert(0, 'pyIcingaFramework')

    logging.info(f'Loading Check {check_path[-1]}')
    logging.info('Check to load %s' % '.'.join(check_path))

    try:
        imported_module = importlib.import_module('.'.join(check_path))
        module_class = check_path[-1].replace('_', '')
        module_list = [x for x in imported_module.__dir__()
                       if x.lower() == module_class.lower()]

        logging.debug('Module List %s' % module_list)

        if len(module_list) == 1:
            module_to_load = module_list[0]
            module = getattr(imported_module, module_to_load)

            return module

        elif len(module_list) > 1:
            logging.info('To many modules found')
            exit(3)
        else:
            logging.info('No modules found')
            exit(3)

    except ModuleNotFoundError as e:
        logging.error(f'Module {".".join(check_path)} could not be found')
        logging.error(f'{e}')
        logging.debug(traceback.format_exc())


def execute(checkname, host, port, parameters, output='icinga'):
    stdout = ""
    exitcode = 3
    logging.info('------ pre excuting check -------')

    try:
        logging.info(f'Searching for check {checkname}')
        check_module = load_module(checkname)
        if check_module:
            check_module = check_module(host, port, **parameters)
            logging.info('------ executing check -------')
            if issubclass(type(check_module), IcingaCheck):
                try:
                    checkoutput = check_module.check()
                    if isinstance(checkoutput, IcingaCheckResult):
                        exitcode, stdout = checkoutput.get_output()
                        logging.info(f'''Check returned code {exitcode} and stdout {stdout}''')
                    elif output == 'raw':
                        stdout = checkoutput
                        exitcode = 0
                    else:
                        stdout = 'EXECUTE ERROR: Invalid Result'
                        exitcode = 3

                except UnknownCheckStateError as e:
                    stdout = f'EXECUTE ERROR: {e.output}'
                    exitcode = 3
            else:
                stdout = 'EXECUTE ERROR: Unknown check output'
                exitcode = 3
    except Exception as e:
        stdout = 'EXECUTE ERROR: Unable to load the check'
        logging.error(e)
        logging.debug(traceback.format_exc())
        exitcode = 3

    return (stdout, exitcode)


def build_kwargs(options):
    kwargs = {}
    if options is not None:
        for opt in options:
            opt_split = opt.split('=')
            if len(opt_split) > 1:
                kwargs[opt_split[0]] = opt_split[1]
            else:
                kwargs['*'] = opt_split[0]
    return kwargs


def parseCliArguments(args, argtype='default'):

    verbose_level = args.v
    if verbose_level == 0:
        setupLogger(level=None)
    elif verbose_level == 1:
        setupLogger(level=logging.ERROR)
    elif verbose_level == 2:
        setupLogger(level=logging.INFO)
    elif verbose_level == 3:
        setupLogger(level=logging.DEBUG)
    else:
        setupLogger(level=logging.DEBUG)
    logging.info('----- Arg parsing -------')
    logging.info(f'Logging level set to {verbose_level}')
    host = args.host
    port = args.port
    checkname = args.check

    user = args.username

    check_parameters = {}
    check_parameters['username'] = user
    check_parameters['extra_options'] = build_kwargs(args.options)
    check_parameters['filters'] = build_kwargs(args.filter)
    check_parameters['warning_thresholds'] = build_kwargs(args.warn)
    check_parameters['critical_thresholds'] = build_kwargs(args.crit)
    if args.output == 'raw':
        check_parameters['output'] = 'raw'
    else:
        check_parameters['output'] = 'icinga'

    if argtype == 'snmp':
        check_parameters['snmp_version'] = args.snmp_version
        check_parameters['snmp_context'] = args.context

        if args.snmp_version == '1' or args.snmp_version == '2c':
            check_parameters['community'] = args.community
        elif args.snmp_version == '3':

            check_parameters['snmp_seclevel'] = args.security_level

            if args.security_level == 'authNoPriv' or args.security_level == 'authPriv':
                authPass = args.auth_password
                if args.ask_auth_pass:
                    authPass = getpass.getpass('Enter SNMPv3 Auth Password: ')

                check_parameters['snmp_authpass'] = authPass
                check_parameters['snmp_authprotocol'] = args.auth_protocol

            if args.security_level == 'authPriv':
                privPass = args.priv_password
                if args.ask_priv_pass:
                    privPass = getpass.getpass('Enter SNMPv3 Priv Password: ')

                check_parameters['snmp_privpass'] = privPass
                check_parameters['snmp_privprotocol'] = args.priv_protocol

        else:
            raise ValueError('SNMP version set to an unknown vaule')
    else:
        pwd = args.password
        if args.ask_pass:
            pwd = getpass.getpass('Password:')

        check_parameters['password'] = pwd

    return (checkname, host, port, check_parameters)


def snmpcli(**kwards):

    parser = argparse.ArgumentParser('Icinga2 CLI Check Module')
    parser.add_argument('-v', action='count', default=0)
    parser.add_argument('--check', default='pyIcingaFramework.checks.test.testcheck')
    parser.add_argument('-H', '--host')
    parser.add_argument('-p', '--port', default=443)
    parser.add_argument('-o', '--options', action='append')
    parser.add_argument('-w', '--warn', action='append')
    parser.add_argument('-c', '--crit', action='append')
    parser.add_argument('-f', '--filter', action='append')
    parser.add_argument('--output', choices=['raw', 'icinga'], default='icinga')

    snmp = parser.add_argument_group('SNMP Common Arguments')
    snmp.add_argument('--snmp-version', choices=['1', '2c', '3'], default='3')
    snmp.add_argument('--context', help='SNMP Context')

    snmpv2_parser = parser.add_argument_group("SNMPv2 Arguments")
    snmpv2_parser.add_argument('--community', help='Community string')

    snmpv3_parser = parser.add_argument_group("SNMPv3 Arguments")
    snmpv3_parser.add_argument('-u', '--username', help='SNMPv3 Username')
    snmpv3_parser.add_argument('-l', '--security-level', help='Security Level',
                               choices=['noAuthPriv', 'authNoPriv', 'authPriv'], default='authPriv')
    snmpv3_parser.add_argument('-a', '--auth-protocol', help='Auth Protocol', choices=['SHA'], default='SHA')
    snmpv3_parser.add_argument('-A', '--auth-password', help='Auth Pass')
    snmpv3_parser.add_argument('-x', '--priv-protocol', help="Priv Protocol", choices=['AES'], default='AES')
    snmpv3_parser.add_argument('-X', '--priv-password', help='Priv pass')
    snmpv3_parser.add_argument('--ask-auth-pass', action='store_true')
    snmpv3_parser.add_argument('--ask-priv-pass', action='store_true')

    args = parser.parse_args()
    main(args, argtype='snmp')


def apicli():
    parser = argparse.ArgumentParser('Icinga2 API Check Module')
    parser.add_argument('-v', action='count', default=0)
    parser.add_argument('--check', default='pyIcingaFramework.checks.test.testcheck')
    parser.add_argument('-H', '--host')
    parser.add_argument('-p', '--port', default=443)
    parser.add_argument('-u', '--username')
    parser.add_argument('--password')
    parser.add_argument('--ask-pass', action='store_true')
    parser.add_argument('-o', '--options', action='append')
    parser.add_argument('-w', '--warn', action='append')
    parser.add_argument('-c', '--crit', action='append')
    parser.add_argument('-f', '--filter', action='append')
    parser.add_argument('--output', choices=['raw', 'icinga'], default='icinga')

    args = parser.parse_args()
    main(args)


def main(args, argtype='api'):

    checkname, host, port, check_parameters = parseCliArguments(args, argtype=argtype)

    stdout, execode = execute(checkname, host, port, check_parameters, output=check_parameters['output'])
    print(stdout)
    sys.exit(execode)


if __name__ == '__main__':
    apicli()

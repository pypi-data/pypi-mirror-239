from datetime import datetime
import socket
from lib.icinga import api_post
from lib.globals import STATE_CRIT, STATE_OK, STATE_UNKNOWN, STATE_WARN
import os
from RPA.Robocorp.Vault import Vault

class icinga:

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, api_user=None, api_pass=None, icinga_fqdn=None, host_name=None, service_name=None, ignore_keywords=True, ttl=300):
        
        self.ROBOT_LIBRARY_LISTENER = self
        self.fqdn = socket.getfqdn().lower()

        self.ignore_keywords = ignore_keywords

        if api_user is None:
            VAULT = Vault()
            _vault_icinga = VAULT.get_secret("icinga")
            api_user = _vault_icinga["api_user"] 
        self.api_user = api_user

        if api_pass is None:
            api_pass = _vault_icinga["api_pass"]
        self.api_password = api_pass
        
        env_icinga_fqdn = os.getenv("ICINGA_FQDN", default=False)
        if icinga_fqdn is None and env_icinga_fqdn:
            icinga_fqdn = env_icinga_fqdn
        self.icinga = icinga_fqdn
        
        env_icinga_host_name = os.getenv("ICINGA_HOST_NAME", default=False)
        if host_name is None:
            if env_icinga_host_name:
                self.host_name = env_icinga_host_name
            else:
                self.host_name = self.fqdn

        env_icinga_service_name = os.getenv("ICINGA_SERVICE_NAME", default=False)
        if service_name is None and env_icinga_service_name:
            service_name = env_icinga_service_name
        self.service_name = service_name

        env_icinga_ttl = os.getenv("ICINGA_TTL", default=False)
        if ttl == 300 and env_icinga_ttl:
            ttl = env_icinga_ttl
        self.ttl = ttl

        current_time = datetime.now()
        self.current_ts = int(current_time.timestamp()) * 1000

        self.service_name_suite = ''
        self.icinga_status = STATE_OK
        self.icinga_message = ''
        self.icinga_perfdata = ''
        self.last_failed_keyword = ''
        self.last_failed_test = ''
        pass

    def set_service_status(self,
                    performance_data=False,
                    check_command=False,
                    check_source=False,
                    execution_start=False,
                    execution_end=False,
                    ttl=False):
        uri = "https://{}:5665/v1/actions/process-check-result".format(
            self.icinga)
        data = {
            'type': 'Service',
            'filter': 'host.name==host_name && service.name==service_name',
            'filter_vars': {
                'host_name': self.host_name,
                'service_name': self.service_name
            },
            'exit_status': self.icinga_status,
            'plugin_output': self.icinga_message
        }
        if self.icinga_perfdata:
            data['performance_data'] = self.icinga_perfdata
        data['check_command'] = self.__class__.__name__
        data['check_source'] = self.fqdn
        if execution_start:
            data['execution_start'] = execution_start
        if execution_end:
            data['execution_end'] = execution_end
        if self.ttl:
            data['ttl'] = self.ttl
        #print("Icinga: set_service_status(): ", data)
        return_code, result = api_post(
            uri=uri,
            username=self.api_user,
            password=self.api_password,
            data=data)
        if return_code:
            print("Icinga: set_service_status(): successfull")
        else:
            print("Icinga: set_service_status(): failed")
            print("Icinga: set_service_status(): ", return_code, result)
            return False
        return True

    def end_keyword(self, name, attrs):
        #print("end_keyword", name)
        #print(attrs)
        if self.ignore_keywords:
            return
        if attrs['doc'] == '':
            lable = name
        else:
            lable = attrs['doc']
        self.icinga_perfdata += " '{lable}'={value}{unit}".format(
            lable = lable,
            value = attrs['elapsedtime'],
            unit = 'ms'
        )
        if attrs['status'] != 'PASS':
            self.icinga_status = STATE_CRIT
            self.last_failed_keyword = "{} {}: {}\n".format(lable, attrs['args'], attrs['status'] )
        pass

    def end_test(self, name, attrs):
        #print("end_test", name)
        #print(attrs)
        if attrs['doc'] == '':
            lable = name
        else:
            lable = attrs['doc']
        self.icinga_perfdata += " '{lable}'={value}{unit}".format(
            lable = lable,
            value = attrs['elapsedtime'],
            unit = 'ms'
        )
        if attrs['status'] != 'PASS':
            self.icinga_status = STATE_CRIT
            self.last_failed_test = "{} {}: {}\n".format(lable, attrs['args'], attrs['status'] )
            self.icinga_message = "{}\n{}".format(self.last_failed_test, self.last_failed_keyword)
        pass

    def end_suite(self, name, attrs):
        #print("end_suite", name)
        #print(attrs)
        if attrs['doc'] == '':
            lable = name
        else:
            lable = attrs['doc']
        self.icinga_perfdata += " '{lable}'={value}{unit}".format(
            lable = lable,
            value = attrs['elapsedtime'],
            unit = 'ms'
        )
        if attrs['status'] == 'PASS':
            self.icinga_message = "Test Suite {}: {} {}".format(attrs['longname'], attrs['statistics'], attrs['status'])
        else:
            self.icinga_status = STATE_CRIT
            self.icinga_message = "Test Suite {}: {} {}\n{}\n{}".format(attrs['longname'], attrs['statistics'], attrs['status'], self.last_failed_test, self.last_failed_keyword)
        pass

    def close(self):
        self.set_service_status()
        pass
import os
import time
import json

from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import login, interface, common
from guerrilla_aaron.host import HostFactory
from guerrilla_aaron.session import SshSession
from datetime import datetime


@Given('"{host}" login to "{device}" web console from {intf} port to get jwt')
@When('"{host}" login to "{device}" web console from {intf} port')
def step_impl(context, host, device, intf):
    context.dut_jwt = {}
    web_jwt = context.hosts[host].dut_ui.web_get_jwt( 
        username=context.dut_info[device]['credential']['username'], 
        password=context.dut_info[device]['credential']['password'])
    context.dut_jwt[device] = web_jwt


@Then('"{host}" logout to "{device}" web console from {intf} port')
@When('"{host}" logout to "{device}" web console from {intf} port')
def step_impl(context, host, device, intf):
    # Session Clean Up
    res = context.hosts[host].dut_ui.web_post(
        uri="api/v1/auth/logout",
        jwt=context.dut_jwt[device])
    context.dut_jwt[device] = None
    
    res_str = str(res)
    assert 'logout success' in res_str, \
            f'response should be "logout success", but {res_str}'


@Given('"{host}" connect "{device}" to generate RSA Key')
def step_impl(context, host, device):
    if context.table and "rsakey_name" in context.table.headings:
        rsakey_name = context.table[0]["rsakey_name"]
    else:
        rsakey_name = "MoxaRsaKey"
    if context.table and "private_key_size" in context.table.headings:
        private_key_size = int(context.table[0]["private_key_size"])
    else:
        private_key_size = 1024

    assert private_key_size in [1024, 2048], \
            f'private_key_size should be 1024 or 2048 but {private_key_size}'

    res = context.hosts[host].dut_ui.web_post(
        uri="api/v1/auth/rsaKeyGen",
        data_dict={"rsakey_name": rsakey_name, "private_key": private_key_size},
        jwt=context.dut_jwt[device])

    res_str = str(res)
    assert 'RSA key generate success.' in res_str, \
            f'response should be "RSA key generate success.", but {res_str}'


@Given('"{host}" connect "{device}" to generate CSR')
def step_impl(context, host, device):
    if context.table and "private_key" in context.table.headings:
        private_key = context.table[0]["private_key"]       # private_key Naming Role: f'{rsakey_name}-{private_key}'
    else:
        private_key = "MoxaRsaKey-1024"
    
    country_name = context.table[0]["country_name"]
    locality_name = context.table[0]["locality_name"]
    org_name = context.table[0]["org_name"]
    org_unit_name =context.table[0]["org_unit_name"]
    email_addr =context.table[0]["email_addr"]
    
    res = context.hosts[host].dut_ui.web_post(
        uri="api/v1/auth/csrGen",
        data_dict={"privateKey": private_key,
                    "ct": country_name,
                    "local": locality_name,
                    "org": org_name,
                    "orgUnit": org_unit_name,
                    "cn": "192.168.127.254",  # file name
                    "ea": email_addr,
                    "subname": "192.168.127.254"},
        jwt=context.dut_jwt[device])
    
    res_str = str(res)
    assert 'CSR generate success.' in res_str, \
            f'response should be "CSR generate success.", but {res_str}'


@Given('"{host}" connect "{device}" to download CSR')
def step_impl(context, host, device):
    context.hosts[host].dut_ui.web_get(
        uri="csr/192.168.127.254.csr",
        jwt=context.dut_jwt[device],
        filename='192.168.127.254.csr')


@Given('"{host}" generate signed certificate base on CSR')
def step_impl(context, host):
    context.hosts[host].ca.prepare_env()
    context.hosts[host].ca.generate_root_ca()
    context.hosts[host].ca.sign_cert()


@Given('"{host}" connect "{device}" to import Certificate from CSR')
def step_impl(context, host, device):
    if context.table and "cert_name" in context.table.headings:
        cert_name = context.table[0]["cert_name"]
    else:
        cert_name = "Moxa"
    
    uri = 'api/v1/auth/cerMgmtUpload?'
    uri += 'cer_file=test.crt&'
    uri += 'mgmt_mode=1&'
    uri += f'cer_name={cert_name}&'
    uri += 'csr_file=192.168.127.254.csr'

    res = context.hosts[host].dut_ui.web_post_multipart(
        uri=uri,
        form_name="cer_file",           # file type
        form_filename="cert/test.crt",  # file name and path
        jwt=context.dut_jwt[device])

    res_str = str(res)
    assert 'Upload success.' in res_str, \
            f'response should be "Upload success.", but {res_str}'


@When ('"{device}" uses auto-generated default certificate')
def step_impl(context, device):
    host = "HOST"
    res = context.hosts[host].dut_ui.web_get(
        uri="api/v1/setting/data/SRV_AUTH_CERT",
        jwt=context.dut_jwt[device])
    
    res_str = str(res)
    assert '"selsslmode":0' in res_str, \
            f'DUT should use auto-generated default certificate("selsslmode":0), but {res_str}'
    


@When('"{device}" uses imported certificate from Local Certificate Database')
def step_impl(context, device):
    host = "HOST"
    if context.table and "cert_name" in context.table.headings:
        cert_name = context.table[0]["cert_name"]
    else:
        cert_name = "Moxa"    
    # private_key Naming Role: f'{rsakey_name}-{private_key}'
    if context.table and "private_key" in context.table.headings:
        private_key = context.table[0]["private_key"]
    else:
        private_key = "MoxaRsaKey-1024"

    pemkey = "/mnt/log/rsakey_file/" + private_key

    res = context.hosts[host].dut_ui.web_post(
        uri="api/v1/setting/data/?SRV=SRV_AUTH_CERT",
        data_dict={"SRV_AUTH_CERT": 
                        {"selsslmode": 1,
                         "selpem": cert_name,
                         "pemkey": pemkey, 
                         "auth_cert_reGen": 0}},
        jwt=context.dut_jwt[device])

    res_str = str(res)
    assert '"success": "true"' in res_str, \
            f'response should include "success": "true", but {res_str}'


@then(u'"{host}" {can_or_cannot} establish a secure connection to "{device}"')
@then(u'check if "{host}" {can_or_cannot} establish a secure connection to "{device}"')
def step_impl(context, host, device, can_or_cannot):
    flag = {'can': True, 'cannot': False}[can_or_cannot]
    
    if flag:
        try:
            for _ in range(10):
                ret = context.hosts[host].ca.check_secure_connection()
                if ret:
                    break
                time.sleep(10)
            assert ret , f'{host} unable to establish a secure connection to {device}.'
        finally:
            # clean up
            context.dut[device].main().reload_factory_default_no_cert()
            time.sleep(50)
            context.hosts[host].ca.rm_file()
            for host_clean in context.host_info:
                info = context.host_info[host_clean]
                username = context.host_info[host_clean]['session']['credential']['username']

                print(f'\n=======> start {host_clean} clean up\n')
                context.hosts[host_clean] = HostFactory.create_atb(info)
                context.hosts[host_clean].login()
                context.hosts[host_clean].ca.clean_up(username)
                print(f'\n<======= End of {host_clean} clean up\n')
    else:
        ret = context.hosts[host].ca.check_secure_connection()
        assert not ret , \
             f'Expect {host} cannot establish a secure connection to {device} but success.'

    
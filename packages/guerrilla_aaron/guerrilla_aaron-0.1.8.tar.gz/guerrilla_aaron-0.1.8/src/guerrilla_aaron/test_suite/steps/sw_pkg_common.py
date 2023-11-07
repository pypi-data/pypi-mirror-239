import time

from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import common, interface, login


@then(
    u'displayed pacakge version should be consistent with "{device}"s default version'
)
def step_impl(context, device):
    for _ in range(5):
        time.sleep(1)
        cur_versions = context.dut[device].main().show_package()
        cur_security_version, cur_mxsecurity_version = cur_versions[0].get('security'), cur_versions[0].get('mxsecurity')
        if all((cur_security_version, cur_mxsecurity_version)):
            break

    default_security_version = context.table[0]['security']
    default_mxsecurity_version = context.table[0]['mxsecurity']

    assert (default_security_version in cur_security_version) and (default_mxsecurity_version in cur_mxsecurity_version) , \
        f'returned version is inconsistant with default version: cur -> {cur_versions[0]} <-> defaut -> {context.table[0]}'


@when(u'upgrade security package {security_version} on "{device}"')
def step_impl(context, device, security_version):
    ret = context.dut[device].main().upgrade_package(tftp_ip='192.168.127.92',
                                                     pkg_type='security',
                                                     file_name=security_version)
    assert 'successfully' in ret[
        'data'], f'Upgrade security pacakge failed: {ret}'


@when(u'upgrade mxsecurity package {mxsecurity_version} on "{device}"')
def step_impl(context, device, mxsecurity_version):
    ret = context.dut[device].main().upgrade_package(
        tftp_ip='192.168.127.92',
        pkg_type='mxsecurity',
        file_name=mxsecurity_version)
    assert 'successfully' in ret[
        'data'], f'Upgrade mxsecurity pacakge failed: {ret}'


@then(
    u'displayed security package version should be consistent with "{device}"s {checked_security_version}'
)
def step_impl(context, device, checked_security_version):
    cur_versions = context.dut[device].main().show_package()
    cur_security_version = cur_versions[0]['security']

    assert (checked_security_version in cur_security_version), \
        f'returned version is inconsistant with default version: cur -> {cur_versions[0]} <-> defaut -> {context.table[0]}'


@then(
    u'displayed mxsecurity package version should be consistent with "{device}"s {checked_mxsecurity_version}'
)
def step_impl(context, device, checked_mxsecurity_version):
    cur_versions = context.dut[device].main().show_package()
    cur_mxsecurity_version = cur_versions[0]['mxsecurity']


    assert (checked_mxsecurity_version in cur_mxsecurity_version) , \
        f'returned version is inconsistant with default version: cur -> {cur_versions[0]} <-> defaut -> {context.table[0]}'

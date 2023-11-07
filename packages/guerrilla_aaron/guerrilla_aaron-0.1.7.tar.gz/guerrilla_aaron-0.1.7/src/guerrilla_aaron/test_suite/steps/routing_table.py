import time

from behave import *

@then('the following rule should be on "{device}"\'s routing table')
def step_impl(context, device):
    flag = False
    for _ in range(5):
        ret = context.dut[device].main().show_ip_route()
        if any(
        item['type'] == context.table[0]['Type'] and
        item['destination'] == context.table[0]['Destination'] and
        item['next_hop'] == context.table[0]['Next Hop'] and
        item['interface'] == context.table[0]['interface']
        for item in ret): 
            flag = True
            break

    assert flag, f"No match found -> expect: {context.table[0]}, actual: {ret}"
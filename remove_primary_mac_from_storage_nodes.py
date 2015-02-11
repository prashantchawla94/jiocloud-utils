import argparse
import hpilo
from ironicclient import client
from ironicclient.exc import HTTPConflict, HTTPServiceUnavailable
import os
import proliantutils.ilo.ribcl
import sys
import time

def get_ironic_client(username, password, auth_url, tenant_name):
    kwargs = {'os_username': username,
              'os_password': password,
              'os_auth_url': auth_url,
              'os_tenant_name': tenant_name }

    return client.get_client(1, **kwargs)

def main(hosts):
    parser = argparse.ArgumentParser(description='Do the stuff.')
    parser.add_argument('--os_username', type=str, default=os.environ.get('OS_USERNAME'),
                       help='Ironic username')
    parser.add_argument('--os_tenant', type=str, default=os.environ.get('OS_TENANT_NAME'),
                       help='Ironic tenant name')
    parser.add_argument('--os_password', type=str, default=os.environ.get('OS_PASSWORD'),
                       help='Ironic password')
    parser.add_argument('--os_auth_url', type=str, default=os.environ.get('OS_AUTH_URL'),
                       help='Ironic auth URL')

    args = parser.parse_args()
    if (not args.os_username
        or not args.os_tenant
        or not args.os_password
        or not args.os_auth_url):
       print('You must supply all details')
       parser.print_help()
       sys.exit(1)

    ironic = get_ironic_client(args.os_username, args.os_password,
                                args.os_auth_url, args.os_tenant)

    clients = {}

    import jiocloud.enroll
    mac_to_uuid = {}
    for _port in ironic.port.list():
        mac_to_uuid[_port.address.lower()] = _port.uuid
    
    for host in ironic.node.list():
        node_obj = ironic.node.get(host.uuid)
        if node_obj.properties['cpus'] != 24:
            continue
        iloconn = hpilo.Ilo(node_obj.driver_info['ipmi_address'], 
                            node_obj.driver_info['ipmi_username'], 
                            node_obj.driver_info['ipmi_password'])
        host_data = jiocloud.enroll.get_host_data(iloconn)
        macs = jiocloud.enroll.extract_macs(jiocloud.enroll.extract_net_info(host_data))
        mac = macs['3']
        try:
            if mac not in mac_to_uuid:
                continue
            ironic.port.delete(mac_to_uuid[mac])
        except HTTPServiceUnavailable, e:
            print e

if __name__ == '__main__':
    sys.exit(not main(sys.argv))

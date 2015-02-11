import argparse
from ironicclient import client as iclient
from novaclient.v1_1 import client as nclient
import os
import subprocess
import proliantutils.ilo.ribcl
import sys
import time

def get_ironic_client(username, password, auth_url, tenant_name):
    kwargs = {'os_username': username,
              'os_password': password,
              'os_auth_url': auth_url,
              'os_tenant_name': tenant_name }

    return iclient.get_client(1, **kwargs)

def get_nova_client(username, password, auth_url, tenant_name):
    kwargs = {'username': username,
              'api_key': password,
              'auth_url': auth_url,
              'project_id': tenant_name }

    return nclient.Client(**kwargs)

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
    nova = get_nova_client(args.os_username, args.os_password,
                                args.os_auth_url, args.os_tenant)

    clients = {}

    for host in nova.servers.list():
        node_obj = nova.servers.get(host.id)
        if node_obj.status != 'ACTIVE' or getattr(node_obj, 'OS-EXT-STS:power_state') != 1:
            continue
  
        pid = os.fork()
        if pid != 0:
            continue
        print 'Doing', host.id
        proc = subprocess.Popen('''ssh -o StrictHostKeyChecking=no ubuntu@%s 'sudo http_proxy=http://proxy:3128/ bash -c "apt-get -y install cdpr; cdpr -d em3"' ''' % (node_obj.addresses['ctlplane'][0]['addr'],), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
	lines = stdout.strip().split('\n')
        uplink_device = lines[-5].strip().split(' ')[-1]
        uplink_port = lines[-1].strip().split(' ')[-1]
        uuid = getattr(node_obj, 'OS-EXT-SRV-ATTR:hypervisor_hostname')
        print 'Setting uplink_device=%s and uplink_port=%s for node %s' % (uplink_device, uplink_port, uuid)
        ironic.node.update(uuid, 
                           [{'op': 'add', 'path': '/properties/uplink_device', 'value': uplink_device},
                            {'op': 'add', 'path': '/properties/uplink_port', 'value': uplink_port}])
        break
 


    time.sleep(5)

if __name__ == '__main__':
    sys.exit(not main(sys.argv))

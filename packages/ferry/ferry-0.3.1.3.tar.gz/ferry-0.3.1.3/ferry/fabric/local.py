# Copyright 2014 OpenCore LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from ferry.docker.docker import DockerCLI
from ferry.docker.docker import DockerInspector
from ferry.fabric.com import robust_com
from ferry.ip.client import DHCPClient
import ferry.install
import json
import logging
import os
from subprocess import Popen, PIPE
import time
import yaml

class LocalFabric(object):
    def __init__(self, bootstrap=False):
        self.name = "local"
        self.repo = 'public'
        self.cli = DockerCLI(ferry.install.DOCKER_REGISTRY)
        self.docker_user = self.cli.docker_user
        self.inspector = DockerInspector(self.cli)
        self.bootstrap = bootstrap

        # Bootstrap mode means that the DHCP network
        # isn't available yet, so we can't use the network. 
        if not bootstrap:
            self.network = DHCPClient(self._get_gateway())

    def _get_gateway(self):
        """
        Get the gateway address in CIDR notation. This defines the
        range of IP addresses available to the containers. 
        """
        cmd = "LC_MESSAGES=C ifconfig drydock0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
        gw = Popen(cmd, stdout=PIPE, shell=True).stdout.read().strip()

        cmd = "LC_MESSAGES=C ifconfig drydock0 | grep 'inet addr:' | cut -d: -f4 | awk '{ print $1}'"
        netmask = Popen(cmd, stdout=PIPE, shell=True).stdout.read().strip()
        mask = map(int, netmask.split("."))
        cidr = 1
        if mask[3] == 0:
            cidr = 8
        if mask[2] == 0:
            cidr *= 2

        return "%s/%d" % (gw, 32 - cidr)

    def _get_host(self):
        cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
        return Popen(cmd, stdout=PIPE, shell=True).stdout.read().strip()

    def get_data_dir(self):
        if 'FERRY_SCRATCH' in os.environ:
            scratch_dir = os.environ['FERRY_SCRATCH']
        else:
            scratch_dir = os.path.join(ferry.install._get_ferry_dir(server=True), 'scratch')

        if not os.path.isdir(scratch_dir):
            os.makedirs(scratch_dir)

        return scratch_dir

    def version(self):
        """
        Fetch the current docker version.
        """
        return self.cli.version()

    def get_fs_type(self):
        """
        Get the filesystem type associated with docker. 
        """
        return self.cli.get_fs_type()

    def quit(self):
        """
        Quit the local fabric. 
        """
        logging.info("quitting local fabric")

    def restart(self, cluster_uuid, service_uuid, containers):
        """
        Restart the stopped containers.
        """
        new_containers = []
        for c in containers:
            container = self.cli.start(image = c.image,
                                       container = c.container,
                                       service_type = c.service_type,
                                       keydir = c.keydir,
                                       keyname = c.keyname,
                                       privatekey = c.privatekey,
                                       volumes = c.volumes,
                                       args = c.args,
                                       inspector = self.inspector)
            container.default_user = self.docker_user
            new_containers.append(container)

        # We should wait for a second to let the ssh server start
        # on the containers (otherwise sometimes we get a connection refused)
        time.sleep(2)
        return new_containers

    def alloc(self, cluster_uuid, service_uuid, container_info, ctype):
        """
        Allocate several instances.
        """
        containers = []
        mounts = {}
        for c in container_info:
            # Get a new IP address for this container and construct
            # a default command. 
            gw = self._get_gateway().split("/")[0]

            # Check if we should use the manual LXC option. 
            if not 'netenable' in c:
                ip = self.network.assign_ip(c)
                lxc_opts = ["lxc.network.type = veth",
                            "lxc.network.ipv4 = %s/24" % ip, 
                            "lxc.network.ipv4.gateway = %s" % gw,
                            "lxc.network.link = drydock0",
                            "lxc.network.name = eth0",
                            "lxc.network.flags = up"]

                # Check if we need to forward any ports. 
                host_map = {}
                for p in c['ports']:
                    p = str(p)
                    s = p.split(":")
                    if len(s) > 1:
                        host = s[0]
                        dest = s[1]
                    else:
                        host = self.network.random_port()
                        dest = s[0]
                    host_map[dest] = [{'HostIp' : '0.0.0.0',
                                       'HostPort' : host}]
                    self.network.forward_rule('0.0.0.0/0', host, ip, dest)
                host_map_keys = host_map.keys()
            else:
                lxc_opts = None
                host_map = None
                host_map_keys = []

            # Start a container with a specific image, in daemon mode,
            # without TTY, and on a specific port
            if not 'default_cmd' in c:
                c['default_cmd'] = "/service/sbin/startnode init"
            container = self.cli.run(service_type = c['type'], 
                                     image = c['image'], 
                                     volumes = c['volumes'],
                                     keydir = c['keydir'], 
                                     keyname = c['keyname'], 
                                     privatekey = c['privatekey'], 
                                     open_ports = host_map_keys,
                                     host_map = host_map, 
                                     expose_group = c['exposed'], 
                                     hostname = c['hostname'],
                                     default_cmd = c['default_cmd'],
                                     args= c['args'],
                                     lxc_opts = lxc_opts,
                                     inspector = self.inspector,
                                     background = False)
            if container:
                container.default_user = self.docker_user
                containers.append(container)
                if not 'netenable' in c:
                    container.internal_ip = ip
                    container.external_ip = ip
                    self.network.set_owner(ip, container.container)

                if 'name' in c:
                    container.name = c['name']

                if 'volume_user' in c:
                    mounts[container] = {'user':c['volume_user'],
                                         'vols':c['volumes'].items()}

                # We should wait for a second to let the ssh server start
                # on the containers (otherwise sometimes we get a connection refused)
                time.sleep(3)

        # Check if we need to set the file permissions
        # for the mounted volumes. 
        for c, i in mounts.items():
            for _, v in i['vols']:
                self.cmd([c], 'chown -R %s %s' % (i['user'], v))

        return containers

    def stop(self, cluster_uuid, service_uuid, containers):
        """
        Forceably stop the running containers
        """
        for c in containers:
            if type(c) is dict:
                self.cli.stop(c['container'])
            else:
                self.cli.stop(c.container)

    def remove(self, cluster_uuid, service_uuid, containers):
        """
        Remove the running instances
        """
        for c in containers:
            for p in c.ports.keys():
                self.network.delete_rule(c.internal_ip, p)
            self.network.free_ip(c.internal_ip)
            self.cli.remove(c.container)

    def snapshot(self, containers, cluster_uuid, num_snapshots):
        """
        Save/commit the running instances
        """
        snapshots = []
        for c in containers:
            snapshot_name = '%s-%s-%s:SNAPSHOT-%s' % (c.image, 
                                                      cluster_uuid,
                                                      c.host_name,
                                                      num_snapshots)
            snapshots.append( {'image' : snapshot_name,
                               'base' : c.image,
                               'type' : c.service_type, 
                               'name' : c.name, 
                               'args' : c.args,
                               'ports': c.ports} )
            self.cli.commit(c, snapshot_name)
        return snapshots

    def push(self, image, registry=None):
        """
        Push an image to a remote registry.
        """        
        return self.cli.push(image, registry)

    def pull(self, image):
        """
        Pull a remote image to the local registry. 
        """        
        return self.cli.pull(image)

    def halt(self, cluster_uuid, service_uuid, containers):
        """
        Safe stop the containers. 
        """
        cmd = '/service/sbin/startnode halt'
        for c in containers:
            self.cmd_raw(c.privatekey, c.internal_ip, cmd, c.default_user)

    def copy(self, containers, from_dir, to_dir):
        """
        Copy over the contents to each container
        """
        for c in containers:
            self.copy_raw(c.privatekey, c.internal_ip, from_dir, to_dir, c.default_user)

    def copy_raw(self, key, ip, from_dir, to_dir, user):
        if key:
            opts = '-o ConnectTimeout=20 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
            scp = 'scp ' + opts + ' -i ' + key + ' -r ' + from_dir + ' ' + user + '@' + ip + ':' + to_dir
            logging.warning(scp)
            robust_com(scp)

    def cmd(self, containers, cmd):
        """
        Run a command on all the containers and collect the output. 
        """
        all_output = {}
        for c in containers:
            output = self.cmd_raw(c.privatekey, c.internal_ip, cmd, c.default_user)
            if output.strip() != "":
                all_output[c.host_name] = output.strip()
        return all_output

    def cmd_raw(self, key, ip, cmd, user):
        if key:
            ip = user + '@' + ip
            ssh = 'ssh -o ConnectTimeout=20 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ' + key + ' -t -t ' + ip + ' \'%s\'' % cmd
            logging.warning(ssh)
            out, _ = robust_com(ssh)
            return out
        else:
            return ''

    def login(self):
        """
        Login to a remote registry. Use the login credentials
        found in the user's home directory. 
        """
        config = ferry.install.read_ferry_config()
        args = config['docker']
        if all(k in args for k in ("user","password","email")):
            if 'server' in args:
                server = args['server']
            else:
                server = ''
            return self.cli.login(user = args['user'], 
                                  password = args['password'],
                                  email = args['email'],
                                  registry = server)
        logging.error("Could not open login credentials " + ferry.install.DEFAULT_LOGIN_KEY)
        return False


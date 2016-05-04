#!/usr/bin/env python
import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)
if len(sys.argv) > 1:
  OVS_DIR = sys.argv[1]
else:
  OVS_DIR = "/home/sdn-tmit/src/marci/ovs-2.5.0/utilities/"
DPDK_DIR = "/home/sdn-tmit/src/marci/dpdk-patched"
DBR = "dpdk_br"
SERVER = '192.168.56.103'


@app.route('/')
def api_root ():
  return 'Welcome'


@app.route('/ovsports')
def api_ovsports ():
  res = subprocess.check_output(["sudo", OVS_DIR + "ovs-vsctl", "show"])
  return res


@app.route('/ovsflows')
def api_ovsflows ():
  res = subprocess.check_output(
    ["sudo", OVS_DIR + "ovs-ofctl", "dump-flows", DBR])
  return res


@app.route('/running')
def api_running ():
  res = subprocess.check_output(["sudo", "docker", "ps"])
  return res


@app.route('/start', methods=['GET'])
def api_start():
  cmask=request.args['cmask']
  mem=request.args['mem']
  subprocess.call(["sudo", OVS_DIR + "ovs-vsctl", "add-port", DBR ,"vhost1" ,"--" ,"set" ,"Interface" ,"vhost1" ,"type=dpdkvhostuser"])
  subprocess.call(["sudo", OVS_DIR + "ovs-ofctl" , "add-flow", DBR, "in_port=1,actions=output:3"])
  subprocess.call(["sudo", OVS_DIR + "ovs-ofctl" , "add-flow", DBR, "in_port=3,actions=output:2"])
  pid=subprocess.Popen(["sudo", "docker" ,"run", "-d", "-v" ,"/usr/local/var/run/openvswitch/vhost1:/var/run/usvhost" ,"-v", "/dev/hugepages:/dev/hugepages", "dpdk-l2fwd", "./examples/l2fwd/build/l2fwd", "-c", cmask, "-n", "4", "-m", mem, "--no-pci", "--single-file", "--file-prefix", "fw", "--vdev=eth_cvio0,mac=00:01:02:03:04:05,path=/var/run/usvhost", "--", "-p", "0x1"]).pid
  return str(pid)

#$sudo docker run -d -v /usr/local/var/run/openvswitch/vhost1:/var/run/usvhost -v /dev/hugepages:/dev/hugepages dpdk-test
#./examples/l2fwd/build/l2fwd -c 0x4 -n 4 -m 1024 --no-pci --single-file --file-prefix fw --vdev=eth_cvio0,mac=00:01:02:03:04:05,path=/var/run/usvhost -- -p 0x1


@app.route('/stop/<cid>')
def api_stop (cid):
  ret = subprocess.check_output(["sudo", "docker", "stop", cid])
  subprocess.call(["sudo", OVS_DIR + "ovs-vsctl", "del-port", DBR, "vhost1"])
  subprocess.call(["sudo", OVS_DIR + "ovs-ofctl", "del-flows", DBR])
  return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

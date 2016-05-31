#!/usr/bin/env python
import json
import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)
if len(sys.argv) > 1:
  OVS_DIR = sys.argv[1]
else:
  #OVS_DIR = "/home/sdn-tmit/src/marci/ovs-2.5.0/utilities/"
  OVS_DIR = "/home/cart/Documents/openvswitch-2.5.1/utilities/"
DPDK_DIR = "/home/sdn-tmit/src/marci/dpdk-patched"
DBR = "dpdk_br"
SERVER = '192.168.56.103'

@app.errorhandler(500)
def error_msg(error=None):
  message={'status': 500, 'message': 'Error: ' + error}
  return json.dumps(message), 500, {'Content-Type': 'text/application/json'}


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
  flows = list(__flow_processor(res))
  return json.dumps(flows), 200, {'Content-Type': 'text/application/json'}


@app.route('/running')
def api_running ():
  res = subprocess.check_output(["sudo", "docker", "ps"])
  return res


@app.route('/start', methods=['POST'])
def api_start ():

  data=request.json
  ports=data['nf_ports']

  if len(ports) > 1:
    print "Too many ports"
    return error_msg("Too many ports")

  mem=data["mem"]
  core=(data['infra_id'].split('#'))[1]
  if int(core) < 4:							 #The bottom two ports are reserved for OVS, thus temporary shift it.
    core=str(int(core)*4)
  nf=data['nf_id'].encode() 

  params=["sudo", "docker", "run", "-d"]

  ovs_ports=dict()
  
  x=0
  for port in ports:
    ovs_port=port.encode()
    x += 1

    subprocess.call(["sudo", OVS_DIR + "ovs-vsctl", "add-port", DBR,		#Add port to the bridge.
                     ovs_port , "--", "set", "Interface",ovs_port ,
                     "type=dpdkvhostuser"])

    portnum=subprocess.check_output(["sudo", OVS_DIR + "ovs-vsctl" ,
                                     "get", "Interface", ovs_port, "ofport"])	#Get openflow portnum of the new port.

    ovs_ports[ovs_port]=portnum.rstrip()							#Store it.
    params += ["-v", "/usr/local/var/run/openvswitch/" + ovs_port + ":/var/run/usvhost" + str(x)]
    
  params += ["-v", "/dev/hugepages:/dev/hugepages","dpdk-test",
                 "./examples/l2fwd/build/l2fwd", "-c", "0x" + core ,
                 "-n", "4", "-m", str(mem) , "--no-pci",
                 "--single-file", "--file-prefix", nf]
				 
  x=0
  for port in ports:
    x += 1
    params += ["--vdev=eth_cvio" + str(x) + ",path=/var/run/usvhost" + str(x)]
	  
  params += ["--", "-p", "0x" + str(pow(2,x)-1)]
  print params	

  proc=subprocess.Popen(params, stdout=subprocess.PIPE) 
  cid=proc.stdout.readline().rstrip()
  print cid

  ret = {'cid': cid, 								# ID of the new container
         'ovs_ports': ovs_ports}						# New ports with openflow IDs
		   
  return json.dumps(ret), 200, {'Content-Type': 'text/application/json'}


@app.route('/stop/<cid>')
def api_stop (cid):
  ret = subprocess.check_output(["sudo", "docker", "stop", cid])
  subprocess.call(["sudo", OVS_DIR + "ovs-vsctl", "del-port", DBR, "vhost1"])
  subprocess.call(["sudo", OVS_DIR + "ovs-ofctl", "del-flows", DBR])
  return ret


def __flow_processor (raw):
  lines = iter(raw.strip().split('\n'))
  # Skip first header line
  lines.next()
  for line in lines:
    flow = {}
    for fragment in line.strip().split(' '):
      if fragment.startswith(('cookie', 'duration', 'table', 'n_packets',
                              'n_bytes', 'idle_age', 'hard_age', 'actions')):
        field, value = fragment.strip(', s').split('=')
        # Convert field to int/float
        if field == "actions":
          flow[field] = value
        else:
          try:
            flow[field] = int(value, 0)
          except ValueError:
            flow[field] = float(value)
      # Collect match field into one entry
      elif fragment:
        if 'match' not in flow:
          flow['match'] = [fragment]
        else:
          flow['match'].append(fragment)
    yield flow


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

#!/usr/bin/env python
import json
import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)
if len(sys.argv) > 1:
  OVS_DIR = sys.argv[1]
else:
  OVS_DIR = "/home/sdn-tmit/src/marci/ovs/utilities/"
  #OVS_DIR = "/home/cart/Documents/dpdktest/ovs/utilities/"
DPDK_DIR = "/home/sdn-tmit/src/marci/dpdk-patched"
DBR = "dpdk_br"
SERVER = '192.168.56.103'

SUPPORTED_VNFS=["simpleForwarder", "trafficGenerator"]

@app.errorhandler(500)
def error_msg(error=None):
  message={'status': 500, 'message': str(error)}
  return json.dumps(message), 500, {'Content-Type': 'text/application/json'}

@app.route('/')
def api_root ():
  return 'Welcome'

@app.route('/ovsports')
def api_ovsports ():
  res = json.loads(subprocess.check_output(["sudo", OVS_DIR + "ovs-vsctl", "-f", "json", "--", "--columns=name,ofport", "list", "Interface"]))
  portlist={}
  for port in res["data"]:
    portlist[port[0]]=port[1]
  return json.dumps(portlist), 200, {'Content-Type': 'text/application/json'}

@app.route('/ovsflows')
def api_ovsflows ():
  res = subprocess.check_output(
    ["sudo", OVS_DIR + "ovs-ofctl", "dump-flows", DBR])
  flows = list(__flow_processor(res))
  return json.dumps(flows), 200, {'Content-Type': 'text/application/json'}

@app.route('/addflow', methods=['POST'])
def api_addflow ():
  data=request.json
  match=data["match"]
  actions=data["actions"]

  flowrule="in_port=" + match["in_port"].encode()

  if 'vlan_id' in match:
    flowrule=flowrule + ",dl_vlan=" + match["vlan_id"].encode() + ",actions=pop_vlan,output:" + actions["output"].encode()
  elif 'push_vlan' in actions:
    flowrule=flowrule + ",actions=push_vlan:0x8100,mod_vlan_vid:" + actions["push_vlan"].encode() + ",output:" + actions["output"].encode()
  else:
    flowrule=flowrule + ",actions=output:" + actions["output"].encode()

  ret=subprocess.check_output([ "sudo", OVS_DIR + "ovs-ofctl", "add-flow", DBR, flowrule, "-O", "OpenFlow12"])

  if ret.rstrip() == "":
    return 'OK', 200
  else:
    return error_msg("Error in installing flow rules")

@app.route('/start', methods=['POST'])
def api_start ():

  data=request.json

  nftype=data['nf_type'].encode() 
  if nftype not in SUPPORTED_VNFS:
    return error_msg("Not implemented NF type")

  ports=data['nf_ports']

  mem=data["mem"]

  #Cores
  cores=data['infra_id']
  coreids = [int(core.split('#')[1]) for core in cores]

  #At least 1 core/port needs to be allocated
  if len(ports) > len(cores):
    return error_msg("Not enough cores")

  #Convert from PU ID to hexa portmask
  mask=0
  for core in coreids:
    mask = mask + pow(2,core)
  hexcore=hex(mask)

  nf=data['nf_id'].encode() 
  
  params=[]

  if nftype == "trafficGenerator":
    params += ["sudo", "docker", "run", "-t", "-d", "--cap-add", "SYS_ADMIN"]
  else:
    params += ["sudo", "docker", "run", "-t", "-d", "--cap-add", "SYS_ADMIN"]

  #Dict to store port name and ovs portnum mappings
  ovs_ports=dict()	 
  
  x=0
  for port in ports:
    ovs_port=port.encode()
    #Add port to the OVS bridge.
    subprocess.call(["sudo", OVS_DIR + "ovs-vsctl", "add-port", DBR,		
                     ovs_port , "--", "set", "Interface",ovs_port ,
                     "type=dpdkvhostuser"])

    #Get openflow portnum of the newly created port.
    portnum=subprocess.check_output(["sudo", OVS_DIR + "ovs-vsctl" ,
                                     "get", "Interface", ovs_port, "ofport"])

    #Store it.
    ovs_ports[ovs_port]=portnum.rstrip()					
    params += ["-v", "/usr/local/var/run/openvswitch/" +
               ovs_port + ":/var/run/usvhost" + str(x)]
    x += 1

  if nftype == "simpleForwarder": 
    params += ["-v", "/dev/hugepages:/dev/hugepages","dpdk-l2fwd",
                 "./examples/l2fwd/build/l2fwd", "-c", hexcore ,
                 "-n", "4", "-m", str(mem) , "--no-pci", "--file-prefix", nf]				 
    x=0
    for port in ports:
      params += ["--vdev=virtio_user" + str(x) + ",path=/var/run/usvhost" + str(x)]
      x += 1

    # DPDK core mask	  
    params += ["--", "-p", "0x" + str(pow(2,len(ports))-1)] 

  else:
    params += ["-v", "/dev/hugepages:/dev/hugepages","dpdk-pktgen",
                 "./app/app/x86_64-native-linuxapp-gcc/pktgen", "-c", hexcore ,
                 "-n", "4", "-m", str(mem) , "--no-pci", "--file-prefix", nf]	

    # The lowest port is reserved for display and timers
    coreids.remove(min(coreids))
    # PKTGEN port setup: each rx/tx pair handled by 1 different core
    pktgen_param= None		 
    x=0
    for port in ports:
      params += ["--vdev=virtio_user" + str(x) + ",path=/var/run/usvhost" + str(x)]
      if pktgen_param is None:
        pktgen_param = str(coreids[x]) + "." + str(x)
      else:
        pktgen_param = pktgen_param + ", " + str(coreids[x]) + "." + str(x) 
      x += 1

    # DPDK core mask
    params += ["--", "-P", "-m", pktgen_param, "-f", "./testconfig.lua"] 
        
  # Get newly initiated container ID
  proc=subprocess.Popen(params, stdout=subprocess.PIPE) 	
  cid=proc.stdout.readline().rstrip()

  ret = {'cid': cid, 		  # ID of the new container
         'ovs_ports': ovs_ports}  # New ports with openflow IDs
		   
  return json.dumps(ret), 200, {'Content-Type': 'text/application/json'}


@app.route('/stop/<cid>')
def api_stop (cid):
  ret = subprocess.check_output(["sudo", "docker", "stop", cid])
  return ret

@app.route('/delflow')
def api_delflow ():
  res = subprocess.check_output(["sudo", OVS_DIR + "ovs-ofctl", "del-flows", DBR])
  return "OK", 200

@app.route('/delport/<portname>')
def api_delport (portname):
  ret = subprocess.check_output(["sudo", OVS_DIR + "ovs-vsctl", "del-port", DBR, portname ])
  if ret.rstrip() == "":
    return 'OK', 200
  else:
    return error_msg("Error in deleting ports")


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

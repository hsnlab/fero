#!/usr/bin/env python
import json
import subprocess
import sys
import socket

from flask import Flask, request

app = Flask(__name__)
if len(sys.argv) > 1:
  OFPORT = int(sys.argv[1])
else:
  OFPORT=16633

ADDRESS = "127.0.0.1"
CPORT = OFPORT-1
DBR= "tcp:" + ADDRESS + ":" + str(OFPORT)
VHOST_DIR="/home/cart/Documents/erfs"
SOCKET=0
DPID=1
SUPPORTED_VNFS=["simpleForwarderVHOST", "trafficGeneratorVHOST", "generatorKNI", "forwarderKNI"]

portmap={}

portmap["dpdk0"]={}
portmap["dpdk0"]["erfs_port"]="KNI:1"
portmap["dpdk0"]["of_port"]=1
portmap["dpdk0"]["core"]=1

portmap["dpdk1"]={}
portmap["dpdk1"]["erfs_port"]="KNI:2"
portmap["dpdk1"]["of_port"]=2
portmap["dpdk1"]["core"]=1

@app.errorhandler(500)
def error_msg(error=None):
  message={'status': 500, 'message': str(error)}
  return json.dumps(message), 500, {'Content-Type': 'text/application/json'}

@app.route('/')
def api_root ():
  return 'Welcome'

@app.route('/ovsports')
def api_ovsports ():
  portlist={}
  for port in portmap:
    portlist[port]=portmap[port]["of_port"]
  return json.dumps(portlist), 200, {'Content-Type': 'text/application/json'}

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

  ret=subprocess.check_output([ "sudo", "ovs-ofctl", "add-flow", DBR , flowrule, "-O", "OpenFlow13"])

  if ret.rstrip() == "":
    return 'OK', 200
  else:
    return error_msg("Error in installing flow rules")

@app.route('/start', methods=['POST'])
def api_start ():

  data=request.json

  print data

  ports=data['nf_ports']
  nf=data['nf_id'].encode()
  mem=data["mem"]

  #Cores
  cores=data['infra_id']
  coreids = [int(core.split('#')[1]) for core in cores]
 
  nftype=data['nf_type'].encode() 

  #NF is not suppported
  if nftype not in SUPPORTED_VNFS:
    return error_msg("Not implemented NF type")

  #At least 1 core/port needs to be allocated
  if len(ports) > len(cores) and nftype.endswith("VHOST"):
    return error_msg("Not enough cores")

  #Convert from PU ID to hexa portmask for DPDK applications
  hexcore=get_portmask(coreids)

  params=[]

  #Dict to store port name and ovs portnum mappings
  ovs_ports=dict()	 
  
  print ports
  for port in ports:
    ovs_port=port['port_id'].encode()
    ovs_core=port['core'].encode().split('#')[1]  

    #Get the next free ofport ID directly from the switch.
    nextofport=get_next_ofport()

    #Add port to the bridge.
    if nftype.endswith("KNI"):
      pname="KNI:"+ str(nextofport)
      comm="add-port dpid={dpid} port-num={ofport} {pname} socket={sock}".format(dpid=DPID, ofport=nextofport, pname=pname, sock=SOCKET )
      ret=send_request(comm)
    else:
      comm="add-port dpid={dpid} port-num={ofport} VHOST socket={sock}".format(dpid=DPID, ofport=nextofport, sock=SOCKET)
      pname="VHOST:" + str(DPID) + "-" + str(nextofport)
      ret=send_request(comm)
      #Add symlink pointing to vhost port.
      subprocess.call(["sudo", "ln" ,"-s", VHOST_DIR + '/' + pname, VHOST_DIR + '/' + ovs_port])   
    if ret.rstrip() != "OK":
      return error_msg("Error in creating ports")

    #Store it.
    portmap[ovs_port]={}
    portmap[ovs_port]["erfs_port"]=pname
    portmap[ovs_port]["of_port"]=nextofport
    portmap[ovs_port]["core"]=int(ovs_core)
      
    ovs_ports[ovs_port]=nextofport

    #Set rxq affinity.
    ret= add_lcore(ovs_port)
    if ret != True:
      return error_msg("Error in setting rxq affinity")
					
  if nftype == "simpleForwarderVHOST":
    cid=start_simpleForwarder(ports, hexcore, mem, nf) 

  elif nftype == "trafficGeneratorVHOST":
    cid=start_trafficGenerator(ports, hexcore, mem, nf, coreids)

  elif nftype == "generatorKNI":
    cid=start_generatorKNI(ports)

  elif nftype == "forwarderKNI":
    cid=start_forwarderKNI(ports)

  ret = {'cid': cid, 		  # ID of the new container
         'ovs_ports': ovs_ports}  # New ports with openflow IDs
		   
  return json.dumps(ret), 200, {'Content-Type': 'text/application/json'}

@app.route('/stop/<cid>')
def api_stop (cid):
  ret = subprocess.check_output(["sudo", "docker", "stop", cid])
  return ret

@app.route('/delflow')
def api_delflow ():
  res = subprocess.check_output(["sudo", "ovs-ofctl", "del-flows", DBR, "-O", "OpenFlow13"])
  return "OK", 200

@app.route('/delport/<portname>')
def api_delport (portname):
  ret1=remove_lcore(portname)
  comm="remove-port " + portmap[portname]["erfs_port"]
  ret2=send_request(comm)
  if ret2.rstrip() == "OK" and ret1 == True:
    del portmap[portname]
    return 'OK', 200
  else:
    return error_msg("Error in deleting ports")


def send_request(request):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.connect((ADDRESS, CPORT))
    s.send(request + '\n')
    ans = s.recv(4096)
    s.close()
    return ans
  except socket.error:
    return "Error"

def get_next_ofport():
  ret = subprocess.check_output(["sudo", "ovs-ofctl", "show", DBR, "-O", "OpenFlow13"])
  lastnum=0
  for line in ret.splitlines():
    if line.startswith(" ") and line[1].isdigit():
      index=line.find(":")
      rule=line[1:index-1]
      rule=rule.split("(")
      lastnum=int(rule[0])
  return lastnum+1

def get_portmask(coreids):
  mask=0
  for core in coreids:
    mask = mask + pow(2,core)
  return hex(mask)

def set_rxq_aff_all():
  coremap={}
  for port in portmap:
    core=portmap[port]["core"]
    if core not in coremap:
      coremap[core]=[]
    coremap[core].append(portmap[port]["erfs_port"])

  for core in coremap:
    comm="lcore " + str(core)
    for port in coremap[core]:
      comm= comm + " " + port
    ret=send_request(comm)
    if ret.rstrip() != "OK":
      return False

  return True

def add_lcore(port):
  core=portmap[port]["core"]
  comm= "lcore " + str(core)
  for prt in portmap:
    if portmap[prt]["core"] == core:
      comm= comm + " " + portmap[prt]["erfs_port"]
  ret=send_request(comm)
  if ret.rstrip() != "OK":
    return False
  return True

def remove_lcore(port):
  core=portmap[port]["core"]
  comm= "lcore " + str(core)
  for prt in portmap:
    if prt == port:
      continue
    elif portmap[prt]["core"] == core:
      comm= comm + " " + portmap[prt]["erfs_port"]
  ret=send_request(comm)
  if ret.rstrip() != "OK":
    return False
  return True

def start_generatorKNI(nf_ports):
  params=["sudo" , "docker", "run",  "-itd", "--net='none'", "ubuntu:latest", "/bin/bash"]
  proc=subprocess.Popen(params, stdout=subprocess.PIPE) 
  cid=proc.stdout.readline().rstrip()
  ret = subprocess.check_output(["sudo", "docker", "inspect", "-f", "{{.State.Pid}}", cid])
  ret=ret.rstrip()
  for port in nf_ports:
    ovs_port=port['port_id'].encode()
    kni_port=portmap[ovs_port]["erfs_port"].replace(":","").lower()	
    subprocess.call(["sudo", "ln" ,"-s", "/proc/" + str(ret) + "/ns/net", "/var/run/netns/" + str(ret)])
    subprocess.call(["sudo", "ip" ,"link", "set", kni_port, "netns", str(ret)])
    subprocess.call(["sudo", "ip" ,"netns", "exec", str(ret), "ifconfig", kni_port,
                     "192.168.1." + str(portmap[ovs_port]["of_port"]) + "/24", "up"])    
  return cid

def start_forwarderKNI(nf_ports):
  params=["sudo" , "docker", "run",  "-itd", "--net='none'", "ubuntu:latest", "/bin/bash"]
  proc=subprocess.Popen(params, stdout=subprocess.PIPE) 
  cid=proc.stdout.readline().rstrip()
  ret = subprocess.check_output(["sudo", "docker", "inspect", "-f", "{{.State.Pid}}", cid])
  ret=ret.rstrip()
  subprocess.call(["sudo", "ln" ,"-s", "/proc/" + str(ret) + "/ns/net", "/var/run/netns/" + str(ret)])
  subprocess.call(["sudo", "ip" ,"netns", "exec", str(ret), "brctl", "addbr", "mybridge"])
  for port in nf_ports:
    ovs_port=port['port_id'].encode()
    kni_port=portmap[ovs_port]["erfs_port"].replace(":","").lower()	
    subprocess.call(["sudo", "ip" ,"link", "set", kni_port, "netns", str(ret)])
    subprocess.call(["sudo", "ip" ,"netns", "exec", str(ret), "ifconfig", kni_port, "promisc" , "up"])
    subprocess.call(["sudo", "ip" ,"netns", "exec", str(ret), "brctl", "addif", "mybridge", kni_port])
  subprocess.call(["sudo", "ip" ,"netns", "exec", str(ret), "ifconfig", "mybridge" , "up"])
  return cid

def start_simpleForwarder(nf_ports, hexcore, mem, nf):
  params=[]
  params2=[]
  params += ["sudo", "docker", "run", "-t", "-d", "--cap-add", "SYS_ADMIN"]
  x=0
  for port in nf_ports:
    ovs_port=port['port_id'].encode()
    params += ["-v", VHOST_DIR + '/' + ovs_port + ":/var/run/usvhost" + str(x)]
    params2 += ["--vdev=virtio_user" + str(x) + ",path=/var/run/usvhost" + str(x)]
    x += 1
  params += ["-v", "/dev/hugepages:/dev/hugepages","dpdk-l2fwd",
               "./examples/l2fwd/build/l2fwd", "-c", hexcore ,
               "-n", "4", "-m", str(mem) , "--no-pci", "--file-prefix", nf]
  params += params2
  params += ["--", "-p", "0x" + str(pow(2,len(nf_ports))-1)]
  proc=subprocess.Popen(params, stdout=subprocess.PIPE) 	
  cid=proc.stdout.readline().rstrip()
  return cid

def start_trafficGenerator(nf_ports, hexcore, mem, nf, nf_coreids):
  coreids=list(nf_coreids)
  params=[]
  params2=[]
  params += ["sudo", "docker", "run", "-it", "-d", "--cap-add", "SYS_ADMIN"]
  # The lowest port is reserved for display and timers
  coreids.remove(min(coreids))
  # PKTGEN port setup: each rx/tx pair handled by 1 different core
  pktgen_param= None
  x=0
  for port in nf_ports:
    ovs_port=port['port_id'].encode()
    params += ["-v", VHOST_DIR + '/' + ovs_port + ":/var/run/usvhost" + str(x)]
    params2 += ["--vdev=virtio_user" + str(x) + ",path=/var/run/usvhost" + str(x)]
    if pktgen_param is None:
      pktgen_param = str(coreids[x]) + "." + str(x)
    else:
      pktgen_param = pktgen_param + ", " + str(coreids[x]) + "." + str(x) 
    x += 1
  params += ["-v", "/dev/hugepages:/dev/hugepages","dpdk-pktgen",
             "./app/app/x86_64-native-linuxapp-gcc/pktgen", "-c", hexcore ,
             "-n", "4", "-m", str(mem) , "--no-pci", "--file-prefix", nf]
  params += params2
  params += ["--", "-P", "-m", pktgen_param]
  proc=subprocess.Popen(params, stdout=subprocess.PIPE) 	
  cid=proc.stdout.readline().rstrip()
  return cid

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

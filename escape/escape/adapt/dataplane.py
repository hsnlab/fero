# Copyright 2016 Janos Czentye <czentye@tmit.bme.hu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Domain Manager and Adapter class for dataplane project:
ESCAPEv2 used as a local orchestrator with resource information come from
CPU/hardware specialities
"""
import json
import os

from escape import CONFIG, __version__
from escape.util.domain import *
from escape.util.misc import run_cmd
from escape.nffg_lib.nffg import *


class DataplaneDomainManager(AbstractDomainManager):
  """
  Manager class to handle communication with internally emulated network.

  .. note::
    Uses :class:`InternalMininetAdapter` for managing the emulated network and
    :class:`InternalPOXAdapter` for controlling the network.
  """
  # DomainManager name
  name = "DATAPLANE"
  # Default domain name
  DEFAULT_DOMAIN_NAME = "DATAPLANE"
  # Set the local manager status
  IS_LOCAL_MANAGER = True

  def __init__ (self, domain_name=DEFAULT_DOMAIN_NAME, *args, **kwargs):
    """
    Init
    """
    log.debug("Create DataplaneDomainManager with domain name: %s" %
              domain_name)
    super(DataplaneDomainManager, self).__init__(domain_name=domain_name,
                                                 *args, **kwargs)
    # self.controlAdapter = None  # DomainAdapter for POX-InternalPOXAdapter
    self.topoAdapter = None  # DomainAdapter for Dataplane
    self.remoteAdapter = None  # REST management communication
    self.deployed_vnfs = {}

  def init (self, configurator, **kwargs):
    """
    Initialize Internal domain manager.

    :param configurator: component configurator for configuring adapters
    :type configurator: :any:`ComponentConfigurator`
    :param kwargs: optional parameters
    :type kwargs: dict
    :return: None
    """
    # Call abstract init to execute common operations
    super(DataplaneDomainManager, self).init(configurator, **kwargs)
    log.info("DomainManager for %s domain has been initialized!" %
             self.domain_name)

  def initiate_adapters (self, configurator):
    """
    Initiate adapters.

    :param configurator: component configurator for configuring adapters
    :type configurator: :any:`ComponentConfigurator`
    :return: None
    """
    # Initiate Adapters
    self.topoAdapter = configurator.load_component(
      component_name=AbstractESCAPEAdapter.TYPE_TOPOLOGY,
      parent=self._adapters_cfg)
    # Init default NETCONF adapter
    self.remoteAdapter = configurator.load_component(
      component_name=AbstractESCAPEAdapter.TYPE_REMOTE,
      parent=self._adapters_cfg)
    # Init adapter for internal controller: POX
    # self.controlAdapter = configurator.load_component(
    #   component_name=AbstractESCAPEAdapter.TYPE_CONTROLLER,
    #   parent=self._adapters_cfg)
    log.debug("Set %s as the topology Adapter for %s" %
              (self.topoAdapter.__class__.__name__, self.domain_name))

  def finit (self):
    """
    Stop polling and release dependent components.

    :return: None
    """
    self.clear_domain ()
    super(DataplaneDomainManager, self).finit()
    # self.controlAdapter.finit()
    self.topoAdapter.finit()
    self.remoteAdapter.finit()

  # @property
  # def controller_name (self):
  #   return self.controlAdapter.task_name


  def install_nffg (self, nffg_part):
    """
    Install an :any:`NFFG` related to the internal domain.

    :param nffg_part: NF-FG need to be deployed
    :type nffg_part: :any:`NFFG`
    :return: installation was success or not
    :rtype: bool
    """
    log.info(">>> Install %s domain part..." % self.domain_name)
    try:
      # Remove unnecessary and moved NFs first
      result = [
        self._delete_running_nfs(nffg=nffg_part),
        # then (re)initiate mapped NFs
        self._deploy_new_nfs(nffg_part)
      ]
      log.info("Perform traffic steering according to mapped tunnels/labels...")
      result.append(self._deploy_flowrules(nffg_part))

      return all(result)
    except:
      log.exception("Got exception during NFFG installation into: %s." %
                    self.domain_name)
      return False


  def _delete_running_nfs (self, nffg=None):
    """
    Stop and delete deployed NFs which are not existed the new mapped request.

    Detect if an NF was moved during the previous mapping and
    remove that gracefully.

    If the ``nffg`` parameter is not given, skip the NF migration detection
    and remove all non-existent NF by default.

    :param nffg: the last mapped NFFG part
    :type nffg: :any:`NFFG`
    :return: deletion was successful or not
    :rtype: bool
    """
    result = True
    topo = self.topoAdapter.get_topology_resource()
    if topo is None:
      log.warning("Missing topology description from %s domain! "
                  "Skip deleting NFs..." % self.domain_name)
      return False
    log.debug("Check for removable NFs...")
    # Skip non-execution environments
    infras = [i.id for i in topo.infras if
              i.infra_type in (NFFG.TYPE_INFRA_EE, NFFG.TYPE_INFRA_STATIC_EE)]
    for infra_id in infras:
      # Generate list of mapped NF on the infra previously
      old_running_nfs = [n.id for n in topo.running_nfs(infra_id)]
      # Detect non-moved NF if new mapping was given and skip deletion
      for nf_id in old_running_nfs:
        # If NF exist in the new mapping
        if nffg is not None and nf_id in nffg:
          new_running_nfs = [n.id for n in nffg.running_nfs(infra_id)]
          # And connected to the same infra
          if nf_id in new_running_nfs:
            # NF was not moved, Skip deletion
            log.debug('Unchanged NF: %s' % nf_id)
            continue
          # If the NF exists in the new mapping, but moved to another infra
          else:
            log.info("Found moved NF: %s")
            log.debug("NF migration is not supported! Stop and remove already "
                      "deployed NF and reinitialize later...")
        else:
          log.debug("Found removable NF: %s" % nf_id)

        log.debug("Stop deployed NF: %s" % nf_id)
        try:
          vnf_id = nf_id.split('-')[0]
          cid=self.deployed_vnfs[vnf_id]['cid']
          # Stop running container
          self.remoteAdapter.stop(cid)
          # Remove OVS ports
          for port in self.deployed_vnfs[vnf_id]['ovs_ports']:
            self.remoteAdapter.delport(port)
          # Remove NF from deployed cache
          del self.deployed_vnfs[vnf_id]
          # Get the other sub NFs
          nf_parts=[nfpart for nfpart in topo.nfs if nfpart.id.startswith(vnf_id)]
          for part in nf_parts:
            # Delete infra ports connected to the deletable NF part
            for u, v, link in topo.network.out_edges([part.id], data=True):
              topo[v].del_port(id=link.dst.id)
            # Delete NF
            topo.del_node(part.id)
        except KeyError:
          log.error("Deployed VNF data for NF: %s is not found! "
                    "Skip deletion..." % nf_id)
          result = False
          continue

    log.debug("NF deletion result: %s" % ("SUCCESS" if result else "FAILURE"))
    return result


  def _deploy_new_nfs(self, nffg_part):
    """
    Install an :any:`NFFG` related to the dataplane domain.

    :param nffg_part: NF-FG need to be deployed
    :type nffg_part: :any:`NFFG`
    :return: installation was success or not
    :rtype: bool
    """
    log.info(">>> Install %s domain part..." % self.domain_name)

    print nffg_part.dump()
    
    nffg_part.clear_links(NFFG.TYPE_LINK_REQUIREMENT)
    un_topo = self.topoAdapter.get_topology_resource()

    if un_topo is None:
      log.warning("Missing topology description from %s domain! "
                  "Skip deploying NFs..." % self.domain_name)

    # Remove special characters from infra side NF port id
    for nf in nffg_part.nfs:
      for u, v, link in nffg_part.real_out_edges_iter(nf.id):
        dyn_port = nffg_part[v].ports[link.dst.id]
        dyn_port.id=link.dst.id.translate(None, '|').replace(link.dst.node.id, '')
      
    for nf in nffg_part.nfs:

      act_nf=nf.id.split('-')
      ports=[]
      cores=[]
      mem=0

      if len(act_nf) == 1:

        if nf.id in (nf.id for nf in un_topo.nfs):
          log.debug("NF: %s has already been initiated. Continue to next NF..."
                    % nf.short_name)
          continue

        ports = [link.dst.id for u, v, link in
                   nffg_part.real_out_edges_iter(nf.id)]

        cores = [link.dst.node.id for u, v, link in
                   nffg_part.real_out_edges_iter(nf.id)]

        mem = nf.resources.mem       


      elif act_nf[0] not in self.deployed_vnfs:

        log.debug("New sub NF detected for: %s" % act_nf[0])

        nf_parts=[nfpart for nfpart in nffg_part.nfs if nfpart.id.startswith(act_nf[0])]

        log.debug("NF parts detected: %s" % [part.id for part in nf_parts])

        for n in nf_parts:
          mem=mem + n.resources.mem
          if n.id.split('-')[1].startswith("core"):
            for u, v, link in nffg_part.real_out_edges_iter(n.id):
              cores.append(link.dst.node.id)
              break
          else:
            for u, v, link in nffg_part.real_out_edges_iter(n.id):
              if len(link.dst.id.split('-')) < 3:
                ports.append(link.dst.id)
                break                        

      params = {'nf_type': nf.functional_type,
                'nf_id': act_nf[0],
                'nf_ports': [port for port in ports],
                'infra_id': [core for core in cores],
                'mem' : mem}

      if len(params['infra_id']) > 0:

        log.debug("Starting new NF with parameters: %s" % params)

        """
        self.deployed_vnfs[act_nf[0]]="aaaaa"

        """

        result = self.remoteAdapter.start(**params)

        if result is not None:
          self.deployed_vnfs[nf.id.split('-')[0]] = result

      if nf.id not in (nf.id for nf in un_topo.nfs) and nf.resources.cpu > 0:
        # Add initiated NF to topo description if not virtual NF
        log.info("Update Infrastructure layer topology description...")
        deployed_nf = nf.copy()
        deployed_nf.ports.clear()
        un_topo.add_nf(nf=deployed_nf)
        log.debug("Add deployed NF to topology: %s" % nf.id)
        # Add Link between actual NF and INFRA
        for nf_id, infra_id, link in nffg_part.real_out_edges_iter(nf.id):
          # Get Link's src ref to new NF's port
          nf_port = deployed_nf.ports.append(nf.ports[link.src.id].copy())
          # Create INFRA side Port
          infra_port = un_topo.network.node[infra_id].add_port(
            id=link.dst.id)
          log.debug("%s - detected physical %s" % (deployed_nf, infra_port))
          # Add Links to un topo
          l1, l2 = un_topo.add_undirected_link(port1=nf_port, port2=infra_port,
                                               dynamic=True, delay=link.delay,
                                               bandwidth=link.bandwidth)


        log.debug("%s topology description is updated with NF: %s" % (
            self.domain_name, deployed_nf.name))
      else:
        log.debug("Virtual NF, skipped: %s" % nf.id)

    print self.topoAdapter.get_topology_resource().dump()
    return True


  def _deploy_flowrules(self, nffg):

    self.remoteAdapter.delflow()
    
    ports = self.remoteAdapter.ovsports()
    if ports is None:
      log.warning("Missing OVS port information")
      return False

    # Add flow rules based on sg hops in the actual request

    for link in nffg.sg_hops:

      if not isinstance(link.id, int):
        continue

      vlan_match=None
      vlan_tag=None
      if link.src.node.id.startswith("dpdk"):
        src = link.src.node.id.split('-')[0]
        vlan_match=link.id
      else:
        src = link.src.node.id + str(link.src.id)

      if link.dst.node.id.startswith("dpdk"):
        dst = link.dst.node.id.split('-')[0]
        vlan_tag=link.id
        if len(link.dst.node.id.split('-')) > 1:
          vlan_tag=vlan_tag-1
      else:
        dst = link.dst.node.id + str(link.dst.id)

      flowrule = {'match': {},
                  'actions': {}
                 }

      flowrule['match']['in_port'] = str(ports[src])
      if vlan_match is not None:
        flowrule['match']['vlan_id'] = str(vlan_match)

      flowrule['actions']['output'] = str(ports[dst])
      if vlan_tag is not None:
        flowrule['actions']['push_vlan'] = str(vlan_tag)

      try:
        self.remoteAdapter.addflow(**flowrule)
      except:
        log.error("Error occured during flowrule installation")
        return False

    return True


  def clear_domain (self):
    """
    :return: cleanup result
    :rtype: bool
    """
    log.debug("Cleaning up %s domain..." % self.domain_name)
    topo = self.topoAdapter.get_topology_resource()
    if topo is None:
      log.warning("Missing topology description from %s domain! "
                  "Skip deleting NFs..." % self.domain_name)
      return False

    for nf_id in self.deployed_vnfs:
      for port in self.deployed_vnfs[nf_id]['ovs_ports']:
        self.remoteAdapter.delport(port)

      # Collecting other parts of the actual NF
      nf_parts=[nf for nf in topo.nfs if nf.id.startswith(nf_id)]

      for nf in nf_parts:
        # Delete ports
        for u, v, link in topo.network.out_edges([nf.id], data=True):
          port=link.dst.id
          topo[v].del_port(id=port)

      self.remoteAdapter.stop(self.deployed_vnfs[nf_id]['cid'])
      topo.del_node(nf_id)

    # Delete all flow rules
    self.remoteAdapter.delflow()
    # Infrastructure layer has been cleared.
    log.debug("%s domain has been cleared!" % self.domain_name)
    return True
    

class DataplaneTopologyAdapter(AbstractESCAPEAdapter):
  """
  Adapter class to handle communication with Mininet domain.

  Implement VNF managing API using direct access to the
  :class:`mininet.net.Mininet` object.
  """
  # Events raised by this class
  _eventMixin_events = {DomainChangedEvent}
  # DomainAdapter constants
  name = "DATAPLANE-COMPUTE"
  type = AbstractESCAPEAdapter.TYPE_TOPOLOGY
  # hwlock2nffg config
  HWLOC2NFFG_BIN = "hwloc2nffg/build/bin/hwloc2nffg"
  HWLOC_PARAMS = ['--merge', '--dpdk']

  def __init__ (self, params=None, **kwargs):
    """
    Init.

    :param net: set pre-defined network (optional)
    :type net: :class:`ESCAPENetworkBridge`
    """
    # Call base constructors directly to avoid super() and MRO traps
    AbstractESCAPEAdapter.__init__(self, **kwargs)
    log.debug("Init DataplaneComputeCtrlAdapter - type: %s" % self.type)
    self.cache = None
    # If initial parameters are explicitly given
    if params is not None:
      self.HWLOC_PARAMS = list(params)

  def check_domain_reachable (self):
    """
    Checker function for domain polling and first time domain detection.

    :return: the domain is detected or not
    :rtype: bool
    """
    # Direct access to IL's Mininet wrapper <-- Internal Domain
    return True

  def get_topology_resource (self):
    """
    Return with the topology description as an :any:`NFFG`.

    :return: the emulated topology description
    :rtype: :any:`NFFG`
    """
    # Return cached topo if it exists
    if self.cache:
      return self.cache
    # Assemble shell command
    cmd_hwloc2nffg = [os.path.normpath(os.path.join(
      CONFIG.get_project_root_dir(), self.HWLOC2NFFG_BIN))]
    # Add hwlock params
    cmd_hwloc2nffg.extend(self.HWLOC_PARAMS)
    log.debug("Used command: %s" % cmd_hwloc2nffg)
    # Run command
    raw_data = run_cmd(cmd_hwloc2nffg)
    # Basic validation
    if not raw_data.startswith('{'):
      if "not found" in raw_data:
        # hwloc2nffg binary not found
        raise RuntimeError(
          "hwloc2nffg binary was not found under the path: %s" % cmd_hwloc2nffg)
      elif "No such file" in raw_data:
        # Shared library not found
        raise RuntimeError(
          "dependent package of hwloc2nffg is missing: %s" % raw_data)
      else:
        # unexpected error
        raise RuntimeError(raw_data)
    # Parse raw data
    topo = NFFG.parse(raw_data)
    # Modify static topo
    self.setup_topology(topo)
    # Duplicate links for bidirectional connections
    topo.duplicate_static_links()
    # Rewrite infra domains
    self.cache = self.rewrite_domain(nffg=topo)
    # print self.cache.dump()
    return self.cache

  def setup_topology(self, nffg):
    """
    Modify the hwloc topology according to the config file.

    :return: the modified topology description
    :rtype: :any:`NFFG`
    """   
    params=CONFIG.get_un_params()
      
    saps= [sap.id for sap in nffg.saps]

    for infra in nffg.infras:

      connected_saps = [link for u, v, link in nffg.real_out_edges_iter(infra.id)
                        if link.dst.node.id in saps]

      for link in connected_saps:
        if link.dst.node.id in params["inner_saps"]:
          continue
        else:
          old_id=link.dst.node.id
          new_sap=link.dst.node
          new_sap.id=link.dst.node.id + "-" + params["domain"]
          new_sap.name=link.dst.node.name + "-" + params["domain"]
          nffg.add_sap(sap_obj=new_sap)
          nffg.del_node(old_id)
          nffg.add_link(link.src,link.dst,link=link)

      if infra.infra_type not in (
        NFFG.TYPE_INFRA_EE, NFFG.TYPE_INFRA_STATIC_EE):
        continue
      elif infra.id in params["ovs_pus"]:
        infra.supported=["ovs"]
      else:
        infra.supported=[sup for sup in params["supported_vnfs"]]
    return nffg

class DefaultDataplaneDomainAPI(object):
  """
  Define unified interface for managing Dataplane domains with REST-API.

  Follows the MixIn design pattern approach.
  """

  def ovsports (self):
    """
    """
    raise NotImplementedError("Not implemented yet!")

  def ovsflows (self):
    """
    """
    raise NotImplementedError("Not implemented yet!")

  def addflow (self, match=None, actions=None, **kwargs):
    """
    """
    raise NotImplementedError("Not implemented yet!")

  def delflow (self):
    """
    """
    raise NotImplementedError("Not implemented yet!")

  def delport (self, portname=None):
    """
    """
    raise NotImplementedError("Not implemented yet!")

  def start (self, nf_type=None, nf_id=None, nf_ports=None, infra_id=None,
             mem=None, **kwargs):
    """
    """
    raise NotImplementedError("Not implemented yet!")

  def stop (self, containerID=None):
    """
    """
    raise NotImplementedError("Not implemented yet!")


class DataplaneRESTAdapter(AbstractRESTAdapter, AbstractESCAPEAdapter,
                           DefaultDataplaneDomainAPI):
  """
  Implement the unified way to communicate with "Dataplane" domain which are
  using REST-API.
  """
  # Set custom header
  custom_headers = {
    'User-Agent': "ESCAPE/" + __version__,
    # XML-based Virtualizer format
    'Accept': "application/xml"
  }
  # Adapter name used in CONFIG and ControllerAdapter class
  name = "DATAPLANE-REST"
  # type of the Adapter class - use this name for searching Adapter config
  type = AbstractESCAPEAdapter.TYPE_MANAGEMENT

  def __init__ (self, url, prefix="", **kwargs):
    """
    Init.

    :param url: url of RESTful API
    :type url: str
    """
    AbstractRESTAdapter.__init__(self, base_url=url, prefix=prefix, **kwargs)
    AbstractESCAPEAdapter.__init__(self, **kwargs)
    log.debug("Init %s - type: %s, domain: %s, URL: %s" % (
      self.__class__.__name__, self.type, self.domain_name, url))

  def ovsflows (self):
    log.debug("Send ovsflows request to remote agent: %s" % self._base_url)
    # Get OVS ports
    data = self.send_no_error(self.POST, 'ovsflows')
    if data:
      # Got data
      log.debug("Received OVS flows from remote %s domain agent at %s" % (
        self.domain_name, self._base_url))
      return self._ovs_flows_parser(data)
    else:
      log.error("No data is received from remote agent at %s!" % self._base_url)
      return {}

  def ovsports (self):
    log.debug("Send ovsports request to remote agent: %s" % self._base_url)
    # Get OVS ports
    data = self.send_no_error(self.GET, 'ovsports')
    if data:
      # Got data
      log.debug("Received OVS ports from remote %s domain agent at %s" % (
        self.domain_name, self._base_url))
      return json.loads(data)
    else:
      log.error("No data is received from remote agent at %s!" % self._base_url)
      return {}


  def start (self, nf_type, nf_id, nf_ports, infra_id, mem=1024, **kwargs):
    logging.debug("Prepare start request for remote agent at: %s" %
                  self._base_url)
    try:
      data = {'nf_type': nf_type, 'nf_id': nf_id, 'nf_ports': nf_ports,
              'infra_id': infra_id, 'mem': mem}
      if 'headers' not in kwargs:
        kwargs['headers'] = dict()
      kwargs['headers']['Content-Type'] = "application/json"
      status = self.send_with_timeout(self.POST, 'start',
                                      body=json.dumps(data), **kwargs)

      return json.loads(status) if status else None
    except Timeout:
      logging.warning("Reached timeout(%ss) while waiting for start response!"
                      " Ignore exception..." % self.CONNECTION_TIMEOUT)

  def addflow (self, match, actions, **kwargs):
    logging.debug("Prepare install flowrule request for remote agent at: %s" %
                  self._base_url)
    try:
      data = {'match': match, 'actions': actions}
      if 'headers' not in kwargs:
        kwargs['headers'] = dict()
      kwargs['headers']['Content-Type'] = "application/json"
      status = self.send_with_timeout(self.POST, 'addflow',
                                      body=json.dumps(data), **kwargs)

      return status if status else False
    except Timeout:
      logging.warning("Reached timeout(%ss) while waiting for start response!"
                      " Ignore exception..." % self.CONNECTION_TIMEOUT)

  def stop (self, containerID):
    log.debug("Send stop container request to remote agent: %s" % self._base_url)
    response = self.send_no_error(self.GET, 'stop/' + containerID)
    if response:
      log.debug("Stopped Docker container from remote %s domain "
                "agent at %s" % (self.domain_name, self._base_url))
      return True
    else:
      log.error("No data is received from remote agent at %s!" % self._base_url)
      return False

  def delport (self, portname):
    log.debug("Send delete ports request to remote agent: %s" % self._base_url)
    response = self.send_no_error(self.GET, 'delport/' + portname)
    if response:
      log.debug("Port deleted from remote %s domain "
                "agent at %s" % (self.domain_name, self._base_url))
      return True
    else:
      log.error("No data is received from remote agent at %s!" % self._base_url)
      return False

  def delflow (self):
    log.debug("Send delete all flows request to remote agent: %s" % self._base_url)
    response = self.send_no_error(self.GET, 'delflow')
    if response:
      log.debug("Flow deleted from remote %s domain "
                "agent at %s" % (self.domain_name, self._base_url))
      return True
    else:
      log.error("No data is received from remote agent at %s!" % self._base_url)
      return False

  @staticmethod
  def _ovs_flows_parser (data):
    return json.loads(data)

  @staticmethod
  def _running_parser (data):
    # TODO
    pass

  def check_domain_reachable (self):
    """
    Checker function for domain polling. Check the remote domain agent is
    reachable.

    :return: the remote domain is detected or not
    :rtype: bool
    """
    return True

  def get_topology_resource (self):
    """
    Return with the topology description as an :any:`NFFG`.

    :return: the topology description of the remote domain
    :rtype: :any:`NFFG`
    """
    # This function should not be called by ESCAPE
    raise RuntimeError("DataplaneRESTAdapter does not support this function: "
                       "get_topology_resource()!")

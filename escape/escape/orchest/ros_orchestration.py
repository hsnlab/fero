# Copyright 2015 Janos Czentye <czentye@tmit.bme.hu>
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
Contains classes relevant to Resource Orchestration Sublayer functionality.
"""
from escape.adapt.virtualization import AbstractVirtualizer, VirtualizerManager
from escape.orchest import log as log, LAYER_NAME
from escape.orchest.nfib_mgmt import NFIBManager
from escape.orchest.ros_mapping import ResourceOrchestrationMapper
from escape.util.mapping import AbstractOrchestrator, ProcessorError
from escape.util.misc import notify_remote_visualizer, VERBOSE
from escape.nffg_lib.nffg import *


class ResourceOrchestrator(AbstractOrchestrator):
  """
  Main class for the handling of the ROS-level mapping functions.
  """
  # Default Mapper class as a fallback mapper
  DEFAULT_MAPPER = ResourceOrchestrationMapper

  def __init__ (self, layer_API):
    """
    Initialize main Resource Orchestration Layer components.

    :param layer_API: layer API instance
    :type layer_API: :any:`ResourceOrchestrationAPI`
    :return: None
    """
    super(ResourceOrchestrator, self).__init__(layer_API=layer_API)
    log.debug("Init %s" % self.__class__.__name__)
    self.nffgManager = NFFGManager()
    # Init virtualizer manager
    # Listeners must be weak references in order the layer API can garbage
    # collected
    self.virtualizerManager = VirtualizerManager()
    self.virtualizerManager.addListeners(layer_API, weak=True)
    # Init NFIB manager
    self.nfibManager = NFIBManager()
    self.nfibManager.initialize()

  def preprocess_nffg(self, nffg):

    try:
      # if there is at least ONE SGHop in the graph, we don't do SGHop retrieval.
      next(nffg.sg_hops)
    except StopIteration:
      # retrieve the SGHops from the TAG values of the flow rules, in case they
      # are cannot be found in the request graph and can only be deduced from the 
      # flows
      log.warning("No SGHops were given in the Service Graph, retrieving them"
                      " based on the flowrules...")
      sg_hops_given = False
      sg_hop_info = NFFGToolBox.retrieve_all_SGHops(nffg)
      if len(sg_hop_info) == 0:
        raise uet.BadInputException("If SGHops are not given, flowrules should be"
                                    " in the NFFG",
                                    "No SGHop could be retrieved based on the "
                                    "flowrules of the NFFG.")
      for k, v in sg_hop_info.iteritems():
        # VNF ports are given to the function
        nffg.add_sglink(v[0], v[1], flowclass=v[2], bandwidth=v[3], delay=v[4],
                           id=k[2])

    hops= [hop for hop in nffg.sg_hops]
    for hop in hops:
      if hop.src.node.id.startswith("dpdk") and hop.dst.node.id.startswith("dpdk"):
        dpdk_in=nffg.add_nf(id=hop.src.node.id.split('-')[0] + "-in" + str(hop.id))
        dpdk_in.resources.cpu=0
        dpdk_in.resources.mem=0
        dpdk_in.resources.storage=0
        dpdk_in.functional_type=hop.src.node.id.split('-')[0]
        dpdk_out=nffg.add_nf(id=hop.dst.node.id.split('-')[0] + "-out" + str(hop.id))
        dpdk_out.resources.cpu=0
        dpdk_out.resources.mem=0
        dpdk_out.resources.storage=0
        dpdk_out.functional_type=hop.dst.node.id.split('-')[0]
        link_in=nffg.add_sglink(hop.src,dpdk_in.add_port())
        link_out=nffg.add_sglink(dpdk_out.add_port(), hop.dst)
        link=hop.copy()
        link.src=dpdk_in.add_port()
        link.dst=dpdk_out.add_port()
        nffg.del_edge(hop.src,hop.dst,hop.id)
        nffg.add_sglink(link.src,link.dst,hop=link)

        for req in nffg.reqs: 
          if hop.id in req.sg_path:
            req.sg_path.insert(0,link_in.id)
            req.sg_path.insert(len(req.sg_path),link_out.id)

        
    nfs = [nf for nf in nffg.nfs]
    for nf in nfs:
      if len(nf.ports) > 1:
        in_nf = nf.copy()
        in_nf.ports.clear()
        in_nf.resources.cpu=0
        in_nf.resources.mem=0
        in_nf.id=nf.id + "-in"
        in_nf.functional_type="vhost"
        nffg.add_nf(nf=in_nf)
        out_nf = nf.copy()
        out_nf.ports.clear()
        out_nf.resources.cpu=0
        out_nf.resources.mem=0
        out_nf.functional_type="vhost"
        out_nf.id=nf.id + "-out"
        nffg.add_nf(nf=out_nf)
      else:
        in_nf = nf.copy()
        in_nf.ports.clear()
        in_nf.resources.cpu=0
        in_nf.resources.mem=0
        in_nf.id=nf.id + "-inout"
        in_nf.functional_type="vhost"
        nffg.add_nf(nf=in_nf)
        out_nf=in_nf

      in_tag=None
      out_tag=None

      dpdk_in=None
      dpdk_out=None

      hops= [hop for hop in nffg.sg_hops]
      for hop in hops:
        if hop.dst.node.id == nf.id:
          in_tag=hop.id
          try:
            in_port = nffg.network.node[in_nf.id].ports[hop.dst.id]
          except KeyError:
            in_port = nffg.network.node[in_nf.id].add_port(id=hop.dst.id)
          old_hop=hop.copy()
          old_hop.dst=in_port
          nffg.del_edge(hop.src,hop.dst,hop.id)
          if hop.src.node.id.startswith("dpdk"):
            dpdk_nf = nf.copy()
            dpdk_nf.ports.clear()
            dpdk_nf.resources.cpu=0
            dpdk_nf.resources.mem=0
            dpdk_nf.id=hop.src.node.id.split('-')[0] + "-" + nf.id
            dpdk_nf.functional_type=hop.src.node.id.split('-')[0]
            nffg.add_nf(nf=dpdk_nf)
            port1=dpdk_nf.add_port()
            old_hop.src=port1
            nffg.add_sglink(port1,in_port,hop=old_hop)
            port2=dpdk_nf.add_port()
            dpdk_in=nffg.add_sglink(hop.src,port2)
          else:
            nffg.add_sglink(hop.src,in_port,hop=old_hop)

        if hop.src.node.id == nf.id:
          out_tag=hop.id
          try:
            out_port = nffg.network.node[out_nf.id].ports[hop.src.id]
          except KeyError:
            out_port = nffg.network.node[out_nf.id].add_port(id=hop.src.id)
          old_hop=hop.copy()
          old_hop.src=out_port
          nffg.del_edge(hop.src,hop.dst,hop.id)
          if hop.dst.node.id.startswith("dpdk"):
            dpdk_nf = nf.copy()
            dpdk_nf.ports.clear()
            dpdk_nf.resources.cpu=0
            dpdk_nf.resources.mem=0
            dpdk_nf.id=hop.dst.node.id.split('-')[0] + "-" + nf.id
            dpdk_nf.functional_type=hop.dst.node.id.split('-')[0]
            nffg.add_nf(nf=dpdk_nf)
            port1=dpdk_nf.add_port()
            old_hop.dst=port1
            nffg.add_sglink(out_port,port1,hop=old_hop)
            port2=dpdk_nf.add_port()
            dpdk_out=nffg.add_sglink(port2,hop.dst)
          else:
            nffg.add_sglink(out_port,hop.dst,hop=old_hop)

      vport_in=in_nf.add_port()
      vport_out=out_nf.add_port()

      aff_reqs=[]
      prev=None

      for req in nffg.reqs: 
        for elem in req.sg_path:
          if prev == in_tag and elem == out_tag:
            aff_reqs.append(req)
          prev=elem

      cpu_req=int(nf.resources.cpu)
      if cpu_req==0:
        cpu_req=1

      for i in range(cpu_req):
        new_nf=nf.copy()
        new_nf.ports.clear()
        new_nf.resources.cpu=1.0
        new_nf.resources.mem=nf.resources.mem / cpu_req
        new_nf.id=nf.id + "-core" + str(i)
        nffg.add_nf(nf=new_nf)
        new_port1=new_nf.add_port()
        sg1=nffg.add_sglink(vport_in,new_port1) 
        new_port2=new_nf.add_port()
        sg2=nffg.add_sglink(new_port2,vport_out)
        for req in aff_reqs:
          new_req=req.copy()
          new_req.regenerate_id()
          poz=new_req.sg_path.index(in_tag)
          new_req.sg_path.insert(poz+1, sg1.id)
          new_req.sg_path.insert(poz+2, sg2.id) 
          if dpdk_in is not None:
            new_req.sg_path.insert(0, dpdk_in.id)
          if dpdk_out is not None:
            new_req.sg_path.insert(len(new_req.sg_path), dpdk_out.id) 
          nffg.add_req(req.src,req.dst,req=new_req)          
                    
      nffg.del_node(nf.id)
      for req in aff_reqs:
        nffg.del_edge(req.src,req.dst,req.id)

    print nffg.dump()
    return nffg

  def instantiate_nffg (self, nffg):
    """
    Main API function for NF-FG instantiation.

    :param nffg: NFFG instance
    :type nffg: :any:`NFFG`
    :return: mapped NFFG instance
    :rtype: :any:`NFFG`
    """

    log.debug("Invoke %s to instantiate given NF-FG" % self.__class__.__name__)
    # Store newly created NF-FG
    self.nffgManager.save(nffg)
    # Get Domain Virtualizer to acquire global domain view
    global_view = self.virtualizerManager.dov
    # Notify remote visualizer about resource view of this layer if it's needed
    notify_remote_visualizer(data=global_view.get_resource_info(),
                             id=LAYER_NAME)
    # Log verbose mapping request
    log.log(VERBOSE, "Orchestration Layer request graph:\n%s" % nffg.dump())
    # Start Orchestrator layer mapping
    print nffg.dump()
    if global_view is not None:
      if isinstance(global_view, AbstractVirtualizer):
        # If the request is a bare NFFG, it is probably an empty topo for domain
        # deletion --> skip mapping to avoid BadInputException and forward
        # topo to adaptation layer
        if nffg.is_bare():
          log.warning("No valid service request (VNFs/Flowrules/SGhops) has "
                      "been detected in SG request! Skip orchestration in "
                      "layer: %s and proceed with the bare %s..." %
                      (LAYER_NAME, nffg))
          if nffg.is_virtualized():
            if nffg.is_SBB():
              log.debug("Request is a bare SingleBiSBiS representation!")
            else:
              log.warning(
                "Detected virtualized representation with multiple BiSBiS "
                "nodes! Currently this type of virtualization is nut fully"
                "supported!")
          else:
            log.debug("Detected full view representation!")
          # Return with the original request
          return nffg
        else:
          log.info("Request check: detected valid content!")
        try:
          # Run Nf-FG mapping orchestration
          log.debug("Starting request preprocession...")
          self.preprocess_nffg(nffg)
          mapped_nffg = self.mapper.orchestrate(nffg, global_view)
          log.debug("NF-FG instantiation is finished by %s" %
                    self.__class__.__name__)
          return mapped_nffg
        except ProcessorError as e:
          log.warning("Mapping pre/post processing was unsuccessful! "
                      "Cause: %s" % e)
      else:
        log.warning("Global view is not subclass of AbstractVirtualizer!")
    else:
      log.warning("Global view is not acquired correctly!")
    log.error("Abort orchestration process!")


class NFFGManager(object):
  """
  Store, handle and organize Network Function Forwarding Graphs.
  """

  def __init__ (self):
    """
    Init.
    """
    super(NFFGManager, self).__init__()
    log.debug("Init %s" % self.__class__.__name__)
    self._nffgs = dict()

  def save (self, nffg):
    """
    Save NF-FG in a dict.

    :param nffg: Network Function Forwarding Graph
    :type nffg: :any:`NFFG`
    :return: generated ID of given NF-FG
    :rtype: int
    """
    nffg_id = self._generate_id(nffg)
    self._nffgs[nffg_id] = nffg
    log.debug("NF-FG: %s is saved by %s with id: %s" %
              (nffg, self.__class__.__name__, nffg_id))
    return nffg.id

  def _generate_id (self, nffg):
    """
    Try to generate a unique id for NFFG.

    :param nffg: NFFG
    :type nffg: :any:`NFFG`
    """
    tmp = nffg.id if nffg.id is not None else id(nffg)
    if tmp in self._nffgs:
      tmp = len(self._nffgs)
      if tmp in self._nffgs:
        for i in xrange(100):
          tmp += i
          if tmp not in self._nffgs:
            return tmp
        else:
          raise RuntimeError("Can't be able to generate a unique id!")
    return tmp

  def get (self, nffg_id):
    """
    Return NF-FG with given id.

    :param nffg_id: ID of NF-FG
    :type nffg_id: int
    :return: NF-Fg instance
    :rtype: :any:`NFFG`
    """
    return self._nffgs.get(nffg_id, default=None)

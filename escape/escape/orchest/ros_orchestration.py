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

    nfs = [nf for nf in nffg.nfs]
    for nf in nfs:
      if nf.resources.cpu > 1:
        in_nf = nf.copy()
        in_nf.ports.clear()
        in_nf.resources.cpu=0
        in_nf.id=nf.id + "-in"
        nffg.add_nf(nf=in_nf)
        out_nf = nf.copy()
        out_nf.ports.clear()
        out_nf.resources.cpu=0
        out_nf.id=nf.id + "-out"
        nffg.add_nf(nf=out_nf)

        hops= [hop for hop in nffg.sg_hops]
        for hop in hops:
          if hop.dst.node.id == nf.id:
            in_port = nffg.network.node[in_nf.id].add_port(id=hop.dst.id)
            old_hop=hop
            old_hop.dst=in_port
            nffg.del_edge(hop.src,hop.dst,hop.id)
            nffg.add_sglink(hop.src,in_port,hop=old_hop)

          if hop.src.node.id == nf.id:
            out_port = nffg.network.node[out_nf.id].add_port(id=hop.src.id)
            old_hop=hop
            old_hop.src=out_port
            nffg.del_edge(hop.src,hop.dst,hop.id)
            nffg.add_sglink(out_port,hop.dst,hop=old_hop)

        vport_in=in_nf.add_port()
        vport_out=out_nf.add_port()

        for i in range(int(nf.resources.cpu)):
          new_nf=nf.copy()
          new_nf.ports.clear()
          new_nf.resources.cpu=1
          new_nf.id=nf.id + "-core" + str(i)
          nffg.add_nf(nf=new_nf)
          new_port1=new_nf.add_port()
          nffg.add_sglink(vport_in,new_port1) 
          new_port2=new_nf.add_port()
          nffg.add_sglink(new_port2,vport_out)         

        nffg.del_node(nf.id)

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
    self.preprocess_nffg(nffg)
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

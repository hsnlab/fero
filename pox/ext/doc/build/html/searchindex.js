Search.setIndex({envversion:46,filenames:["adapt/adapt","adapt/adaptation","adapt/cas_API","adapt/domain_adapters","adaptation","escape","index","infr/il_API","infr/infr","infr/topology","infrastructure","orchest/orchest","orchest/policy_enforcement","orchest/ros_API","orchest/ros_mapping","orchest/ros_orchestration","orchest/virtualization_mgmt","orchestration","service","service/element_mgmt","service/sas_API","service/sas_mapping","service/sas_orchestration","service/service","top","unify","util/adapter","util/api","util/mapping","util/misc","util/netconf","util/nffg","util/pox_extension","util/util"],objects:{"":{adaptation:[4,0,0,"-"],escape:[5,0,0,"-"],infrastructure:[10,0,0,"-"],orchestration:[17,0,0,"-"],service:[18,0,0,"-"],unify:[25,0,0,"-"]},"escape.adapt":{adaptation:[1,0,0,"-"],cas_API:[2,0,0,"-"],domain_adapters:[3,0,0,"-"]},"escape.adapt.adaptation":{ControllerAdapter:[1,1,1,""],DomainConfigurator:[1,1,1,""],DomainResourceManager:[1,1,1,""],DomainVirtualizer:[1,1,1,""]},"escape.adapt.adaptation.ControllerAdapter":{"__init__":[1,4,1,""],"_handle_DomainChangedEvent":[1,4,1,""],"_slice_into_domains":[1,4,1,""],install_nffg:[1,4,1,""]},"escape.adapt.adaptation.DomainConfigurator":{"_DomainConfigurator__load_component":[1,4,1,""],"__init__":[1,4,1,""],"__iter__":[1,4,1,""],components:[1,2,1,""],get:[1,4,1,""],load_default_mgrs:[1,4,1,""],load_internal_mgr:[1,4,1,""],start:[1,4,1,""],stop:[1,4,1,""]},"escape.adapt.adaptation.DomainResourceManager":{"__init__":[1,4,1,""],dov:[1,2,1,""],update_resource_usage:[1,4,1,""]},"escape.adapt.adaptation.DomainVirtualizer":{"__init__":[1,4,1,""],get_resource_info:[1,4,1,""]},"escape.adapt.cas_API":{ControllerAdaptationAPI:[2,1,1,""],DeployNFFGEvent:[2,1,1,""],GlobalResInfoEvent:[2,1,1,""],InstallationFinishedEvent:[2,1,1,""]},"escape.adapt.cas_API.ControllerAdaptationAPI":{"__init__":[2,4,1,""],"_core_name":[2,2,1,""],"_handle_DeployEvent":[2,4,1,""],"_handle_DeploymentFinishedEvent":[2,4,1,""],"_handle_GetGlobalResInfoEvent":[2,4,1,""],"_handle_InstallNFFGEvent":[2,4,1,""],initialize:[2,4,1,""],shutdown:[2,4,1,""]},"escape.adapt.cas_API.DeployNFFGEvent":{"__init__":[2,4,1,""]},"escape.adapt.cas_API.GlobalResInfoEvent":{"__init__":[2,4,1,""]},"escape.adapt.cas_API.InstallationFinishedEvent":{"__init__":[2,4,1,""]},"escape.adapt.domain_adapters":{DockerDomainManager:[3,1,1,""],InternalDomainManager:[3,1,1,""],MininetDomainAdapter:[3,1,1,""],OpenStackDomainManager:[3,1,1,""],OpenStackRESTAdapter:[3,1,1,""],POXDomainAdapter:[3,1,1,""],VNFStarterAdapter:[3,1,1,""]},"escape.adapt.domain_adapters.DockerDomainManager":{"__init__":[3,4,1,""],install_nffg:[3,4,1,""],name:[3,2,1,""]},"escape.adapt.domain_adapters.InternalDomainManager":{"__init__":[3,4,1,""],controller_name:[3,2,1,""],install_nffg:[3,4,1,""],name:[3,2,1,""]},"escape.adapt.domain_adapters.MininetDomainAdapter":{"__init__":[3,4,1,""],"_eventMixin_events":[3,2,1,""],connectVNF:[3,4,1,""],disconnectVNF:[3,4,1,""],getVNFInfo:[3,4,1,""],initiateVNF:[3,4,1,""],initiate_VNFs:[3,4,1,""],name:[3,2,1,""],startVNF:[3,4,1,""],stopVNF:[3,4,1,""]},"escape.adapt.domain_adapters.OpenStackDomainManager":{"__init__":[3,4,1,""],install_nffg:[3,4,1,""],name:[3,2,1,""]},"escape.adapt.domain_adapters.OpenStackRESTAdapter":{"__init__":[3,4,1,""]},"escape.adapt.domain_adapters.POXDomainAdapter":{"__init__":[3,4,1,""],"_handle_ConnectionDown":[3,4,1,""],"_handle_ConnectionUp":[3,4,1,""],filter_connections:[3,4,1,""],install_routes:[3,4,1,""],name:[3,2,1,""]},"escape.adapt.domain_adapters.VNFStarterAdapter":{"__init__":[3,4,1,""],RPC_NAMESPACE:[3,2,1,""],connectVNF:[3,4,1,""],disconnectVNF:[3,4,1,""],getVNFInfo:[3,4,1,""],initiateVNF:[3,4,1,""],name:[3,2,1,""],startVNF:[3,4,1,""],stopVNF:[3,4,1,""]},"escape.infr":{il_API:[7,0,0,"-"],topology:[9,0,0,"-"]},"escape.infr.il_API":{DeploymentFinishedEvent:[7,1,1,""],InfrastructureLayerAPI:[7,1,1,""]},"escape.infr.il_API.DeploymentFinishedEvent":{"__init__":[7,4,1,""]},"escape.infr.il_API.InfrastructureLayerAPI":{"__init__":[7,4,1,""],"_core_name":[7,2,1,""],"_eventMixin_events":[7,2,1,""],"_handle_ComponentRegistered":[7,4,1,""],"_handle_DeployNFFGEvent":[7,4,1,""],initialize:[7,4,1,""],install_route:[7,4,1,""],shutdown:[7,4,1,""]},"escape.infr.topology":{AbstractTopology:[9,1,1,""],BackupTopology:[9,1,1,""],ESCAPENetworkBridge:[9,1,1,""],ESCAPENetworkBuilder:[9,1,1,""],InternalControllerProxy:[9,1,1,""],TopologyBuilderException:[9,6,1,""]},"escape.infr.topology.AbstractTopology":{"__init__":[9,4,1,""],default_EE_opts:[9,2,1,""],default_host_opts:[9,2,1,""],default_link_opts:[9,2,1,""],default_switch_opts:[9,2,1,""]},"escape.infr.topology.BackupTopology":{"__init__":[9,4,1,""]},"escape.infr.topology.ESCAPENetworkBridge":{"__init__":[9,4,1,""],cleanup:[9,4,1,""],network:[9,2,1,""],start_network:[9,4,1,""],stop_network:[9,4,1,""]},"escape.infr.topology.ESCAPENetworkBuilder":{"_ESCAPENetworkBuilder__init_from_AbstractTopology":[9,4,1,""],"_ESCAPENetworkBuilder__init_from_CONFIG":[9,4,1,""],"_ESCAPENetworkBuilder__init_from_NFFG":[9,4,1,""],"_ESCAPENetworkBuilder__init_from_dict":[9,4,1,""],"_ESCAPENetworkBuilder__init_from_file":[9,4,1,""],"__init__":[9,4,1,""],build:[9,4,1,""],default_opts:[9,2,1,""],topology_config_name:[9,2,1,""]},"escape.infr.topology.InternalControllerProxy":{"__init__":[9,4,1,""],checkListening:[9,4,1,""]},"escape.orchest":{policy_enforcement:[12,0,0,"-"],ros_API:[13,0,0,"-"],ros_mapping:[14,0,0,"-"],ros_orchestration:[15,0,0,"-"],virtualization_mgmt:[16,0,0,"-"]},"escape.orchest.policy_enforcement":{PolicyEnforcement:[12,1,1,""],PolicyEnforcementError:[12,6,1,""],PolicyEnforcementMetaClass:[12,1,1,""]},"escape.orchest.policy_enforcement.PolicyEnforcement":{"__init__":[12,4,1,""],post_sanity_check:[12,7,1,""],pre_sanity_check:[12,7,1,""]},"escape.orchest.policy_enforcement.PolicyEnforcementMetaClass":{"__new__":[12,3,1,""],get_wrapper:[12,7,1,""]},"escape.orchest.ros_API":{GetGlobalResInfoEvent:[13,1,1,""],InstallNFFGEvent:[13,1,1,""],InstantiationFinishedEvent:[13,1,1,""],ResourceOrchestrationAPI:[13,1,1,""],VirtResInfoEvent:[13,1,1,""]},"escape.orchest.ros_API.InstallNFFGEvent":{"__init__":[13,4,1,""]},"escape.orchest.ros_API.InstantiationFinishedEvent":{"__init__":[13,4,1,""]},"escape.orchest.ros_API.ResourceOrchestrationAPI":{"__init__":[13,4,1,""],"_core_name":[13,2,1,""],"_handle_GetVirtResInfoEvent":[13,4,1,""],"_handle_GlobalResInfoEvent":[13,4,1,""],"_handle_InstallationFinishedEvent":[13,4,1,""],"_handle_InstantiateNFFGEvent":[13,4,1,""],"_handle_MissingGlobalViewEvent":[13,4,1,""],"_handle_NFFGMappingFinishedEvent":[13,4,1,""],"_install_NFFG":[13,4,1,""],dependencies:[13,2,1,""],initialize:[13,4,1,""],shutdown:[13,4,1,""]},"escape.orchest.ros_API.VirtResInfoEvent":{"__init__":[13,4,1,""]},"escape.orchest.ros_mapping":{ESCAPEMappingStrategy:[14,1,1,""],NFFGMappingFinishedEvent:[14,1,1,""],ResourceOrchestrationMapper:[14,1,1,""]},"escape.orchest.ros_mapping.ESCAPEMappingStrategy":{"__init__":[14,4,1,""],map:[14,7,1,""]},"escape.orchest.ros_mapping.NFFGMappingFinishedEvent":{"__init__":[14,4,1,""]},"escape.orchest.ros_mapping.ResourceOrchestrationMapper":{"__init__":[14,4,1,""],"_eventMixin_events":[14,2,1,""],"_mapping_finished":[14,4,1,""],orchestrate:[14,4,1,""]},"escape.orchest.ros_orchestration":{NFFGManager:[15,1,1,""],NFIBManager:[15,1,1,""],ResourceOrchestrator:[15,1,1,""]},"escape.orchest.ros_orchestration.NFFGManager":{"__init__":[15,4,1,""],get:[15,4,1,""],save:[15,4,1,""]},"escape.orchest.ros_orchestration.NFIBManager":{"__init__":[15,4,1,""],add:[15,4,1,""],getNF:[15,4,1,""],remove:[15,4,1,""]},"escape.orchest.ros_orchestration.ResourceOrchestrator":{"__init__":[15,4,1,""],instantiate_nffg:[15,4,1,""]},"escape.orchest.virtualization_mgmt":{AbstractVirtualizer:[16,1,1,""],ESCAPEVirtualizer:[16,1,1,""],MissingGlobalViewEvent:[16,1,1,""],VirtualizerManager:[16,1,1,""]},"escape.orchest.virtualization_mgmt.AbstractVirtualizer":{"__init__":[16,4,1,""],"__metaclass__":[16,2,1,""],get_resource_info:[16,4,1,""],sanity_check:[16,4,1,""]},"escape.orchest.virtualization_mgmt.ESCAPEVirtualizer":{"__init__":[16,4,1,""],"_generate_resource_info":[16,4,1,""],get_resource_info:[16,4,1,""],sanity_check:[16,4,1,""]},"escape.orchest.virtualization_mgmt.VirtualizerManager":{"__init__":[16,4,1,""],"_eventMixin_events":[16,2,1,""],"_generate_virtual_view":[16,4,1,""],dov:[16,2,1,""],get_virtual_view:[16,4,1,""]},"escape.service":{element_mgmt:[19,0,0,"-"],sas_API:[20,0,0,"-"],sas_mapping:[21,0,0,"-"],sas_orchestration:[22,0,0,"-"]},"escape.service.element_mgmt":{AbstractElementManager:[19,1,1,""],ClickManager:[19,1,1,""]},"escape.service.element_mgmt.AbstractElementManager":{"__init__":[19,4,1,""]},"escape.service.element_mgmt.ClickManager":{"__init__":[19,4,1,""]},"escape.service.sas_API":{GetVirtResInfoEvent:[20,1,1,""],InstantiateNFFGEvent:[20,1,1,""],ServiceLayerAPI:[20,1,1,""],ServiceRequestHandler:[20,1,1,""]},"escape.service.sas_API.GetVirtResInfoEvent":{"__init__":[20,4,1,""]},"escape.service.sas_API.InstantiateNFFGEvent":{"__init__":[20,4,1,""]},"escape.service.sas_API.ServiceLayerAPI":{"__init__":[20,4,1,""],"_core_name":[20,2,1,""],"_handle_InstantiationFinishedEvent":[20,4,1,""],"_handle_MissingVirtualViewEvent":[20,4,1,""],"_handle_SGMappingFinishedEvent":[20,4,1,""],"_handle_VirtResInfoEvent":[20,4,1,""],"_initiate_gui":[20,4,1,""],"_initiate_rest_api":[20,4,1,""],"_instantiate_NFFG":[20,4,1,""],dependencies:[20,2,1,""],initialize:[20,4,1,""],request_service:[20,4,1,""],shutdown:[20,4,1,""]},"escape.service.sas_API.ServiceRequestHandler":{bounded_layer:[20,2,1,""],echo:[20,4,1,""],log:[20,2,1,""],operations:[20,4,1,""],request_perm:[20,2,1,""],sg:[20,4,1,""],version:[20,4,1,""]},"escape.service.sas_mapping":{DefaultServiceMappingStrategy:[21,1,1,""],SGMappingFinishedEvent:[21,1,1,""],ServiceGraphMapper:[21,1,1,""]},"escape.service.sas_mapping.DefaultServiceMappingStrategy":{"__init__":[21,4,1,""],map:[21,7,1,""]},"escape.service.sas_mapping.SGMappingFinishedEvent":{"__init__":[21,4,1,""]},"escape.service.sas_mapping.ServiceGraphMapper":{"__init__":[21,4,1,""],"_eventMixin_events":[21,2,1,""],"_mapping_finished":[21,4,1,""],orchestrate:[21,4,1,""]},"escape.service.sas_orchestration":{MissingVirtualViewEvent:[22,1,1,""],SGManager:[22,1,1,""],ServiceOrchestrator:[22,1,1,""],VirtualResourceManager:[22,1,1,""]},"escape.service.sas_orchestration.SGManager":{"__init__":[22,4,1,""],get:[22,4,1,""],save:[22,4,1,""]},"escape.service.sas_orchestration.ServiceOrchestrator":{"__init__":[22,4,1,""],initiate_service_graph:[22,4,1,""]},"escape.service.sas_orchestration.VirtualResourceManager":{"__init__":[22,4,1,""],"_eventMixin_events":[22,2,1,""],virtual_view:[22,2,1,""]},"escape.util":{adapter:[26,0,0,"-"],api:[27,0,0,"-"],mapping:[28,0,0,"-"],misc:[29,0,0,"-"],netconf:[30,0,0,"-"],nffg:[31,0,0,"-"],pox_extension:[32,0,0,"-"]},"escape.util.adapter":{AbstractDomainAdapter:[26,1,1,""],AbstractDomainManager:[26,1,1,""],AbstractRESTAdapter:[26,1,1,""],DeployEvent:[26,1,1,""],DomainChangedEvent:[26,1,1,""],OpenStackAPI:[26,1,1,""],VNFStarterAPI:[26,1,1,""]},"escape.util.adapter.AbstractDomainAdapter":{"__init__":[26,4,1,""],"_eventMixin_events":[26,2,1,""],name:[26,2,1,""],poll:[26,4,1,""],start_polling:[26,4,1,""],stop_polling:[26,4,1,""]},"escape.util.adapter.AbstractDomainManager":{finit:[26,4,1,""],info:[26,4,1,""],init:[26,4,1,""],install_nffg:[26,4,1,""],resume:[26,4,1,""],run:[26,4,1,""],suspend:[26,4,1,""]},"escape.util.adapter.AbstractRESTAdapter":{"__init__":[26,4,1,""],"_send_request":[26,4,1,""],custom_headers:[26,2,1,""]},"escape.util.adapter.DeployEvent":{"__init__":[26,4,1,""]},"escape.util.adapter.DomainChangedEvent":{"__init__":[26,4,1,""],type:[26,2,1,""]},"escape.util.adapter.VNFStarterAPI":{"__init__":[26,4,1,""],connectVNF:[26,4,1,""],disconnectVNF:[26,4,1,""],getVNFInfo:[26,4,1,""],initiateVNF:[26,4,1,""],startVNF:[26,4,1,""],stopVNF:[26,4,1,""]},"escape.util.api":{AbstractAPI:[27,1,1,""],AbstractRequestHandler:[27,1,1,""],RESTError:[27,6,1,""],RESTServer:[27,1,1,""]},"escape.util.api.AbstractAPI":{"__init__":[27,4,1,""],"__str__":[27,4,1,""],"_all_dependencies_met":[27,4,1,""],"_core_name":[27,2,1,""],"_read_json_from_file":[27,3,1,""],dependencies:[27,2,1,""],initialize:[27,4,1,""],shutdown:[27,4,1,""]},"escape.util.api.AbstractRequestHandler":{"_parse_json_body":[27,4,1,""],"_proceed_API_call":[27,4,1,""],"_process_url":[27,4,1,""],"_send_json_response":[27,4,1,""],bounded_layer:[27,2,1,""],do_CONNECT:[27,4,1,""],do_DELETE:[27,4,1,""],do_GET:[27,4,1,""],do_HEAD:[27,4,1,""],do_OPTIONS:[27,4,1,""],do_POST:[27,4,1,""],do_PUT:[27,4,1,""],do_TRACE:[27,4,1,""],error_content_type:[27,2,1,""],log:[27,2,1,""],log_error:[27,4,1,""],log_full_message:[27,4,1,""],log_message:[27,4,1,""],request_perm:[27,2,1,""],send_REST_headers:[27,4,1,""],send_acknowledge:[27,4,1,""],send_error:[27,4,1,""],server_version:[27,2,1,""],static_prefix:[27,2,1,""]},"escape.util.api.RESTError":{"__init__":[27,4,1,""],"__str__":[27,4,1,""],code:[27,2,1,""],msg:[27,2,1,""]},"escape.util.api.RESTServer":{"__init__":[27,4,1,""],run:[27,4,1,""],start:[27,4,1,""],stop:[27,4,1,""]},"escape.util.mapping":{AbstractMapper:[28,1,1,""],AbstractMappingStrategy:[28,1,1,""]},"escape.util.mapping.AbstractMapper":{"__init__":[28,4,1,""],"_defaults":[28,2,1,""],"_mapping_finished":[28,4,1,""],"_start_mapping":[28,4,1,""],orchestrate:[28,4,1,""]},"escape.util.mapping.AbstractMappingStrategy":{"__init__":[28,4,1,""],map:[28,7,1,""]},"escape.util.misc":{"enum":[29,5,1,""],ESCAPEConfig:[29,1,1,""],SimpleStandaloneHelper:[29,1,1,""],Singleton:[29,1,1,""],call_as_coop_task:[29,5,1,""],quit_with_error:[29,5,1,""],schedule_as_coop_task:[29,5,1,""]},"escape.util.misc.ESCAPEConfig":{"__delitem__":[29,4,1,""],"__getitem__":[29,4,1,""],"__init__":[29,4,1,""],"__metaclass__":[29,2,1,""],"__setitem__":[29,4,1,""],LAYERS:[29,2,1,""],add_cfg:[29,4,1,""],dump:[29,4,1,""],get_clean_after_shutdown:[29,4,1,""],get_default_mgrs:[29,4,1,""],get_domain_component:[29,4,1,""],get_fallback_topology:[29,4,1,""],get_strategy:[29,4,1,""],get_threaded:[29,4,1,""],is_loaded:[29,4,1,""],load_config:[29,4,1,""],set_loaded:[29,4,1,""]},"escape.util.misc.SimpleStandaloneHelper":{"__init__":[29,4,1,""],"_log_event":[29,4,1,""],"_register_listeners":[29,4,1,""]},"escape.util.misc.Singleton":{"__call__":[29,4,1,""],"_instances":[29,2,1,""]},"escape.util.netconf":{AbstractNETCONFAdapter:[30,1,1,""]},"escape.util.netconf.AbstractNETCONFAdapter":{"_AbstractNETCONFAdapter__parse_rpc_params":[30,4,1,""],"_AbstractNETCONFAdapter__parse_xml_response":[30,4,1,""],"_AbstractNETCONFAdapter__remove_namespace":[30,4,1,""],"__enter__":[30,4,1,""],"__exit__":[30,4,1,""],"__init__":[30,4,1,""],"_create_rpc_request":[30,4,1,""],"_invoke_rpc":[30,4,1,""],"_parse_rpc_response":[30,4,1,""],NETCONF_NAMESPACE:[30,2,1,""],RPC_NAMESPACE:[30,2,1,""],call_RPC:[30,4,1,""],connect:[30,4,1,""],connected:[30,2,1,""],connection_data:[30,2,1,""],disconnect:[30,4,1,""],get:[30,4,1,""],get_config:[30,4,1,""],manager:[30,2,1,""]},"escape.util.nffg":{AbstractNFFG:[31,1,1,""],NFFG:[31,1,1,""],main:[31,5,1,""]},"escape.util.nffg.AbstractNFFG":{"__abstractmethods__":[31,2,1,""],"__copy__":[31,4,1,""],"__deepcopy__":[31,4,1,""],"__init__":[31,4,1,""],"__metaclass__":[31,2,1,""],"_abc_cache":[31,2,1,""],"_abc_negative_cache":[31,2,1,""],"_abc_negative_cache_version":[31,2,1,""],"_abc_registry":[31,2,1,""],"_init_from_json":[31,4,1,""],add_edge:[31,4,1,""],add_infra:[31,4,1,""],add_link:[31,4,1,""],add_nf:[31,4,1,""],add_req:[31,4,1,""],add_sap:[31,4,1,""],add_sglink:[31,4,1,""],del_node:[31,4,1,""],load_from_file:[31,3,1,""],to_json:[31,4,1,""]},"escape.util.nffg.NFFG":{"__abstractmethods__":[31,2,1,""],"__init__":[31,4,1,""],"_abc_cache":[31,2,1,""],"_abc_negative_cache":[31,2,1,""],"_abc_negative_cache_version":[31,2,1,""],"_abc_registry":[31,2,1,""],add_infra:[31,4,1,""],add_link:[31,4,1,""],add_nf:[31,4,1,""],add_req:[31,4,1,""],add_sap:[31,4,1,""],add_sglink:[31,4,1,""],del_node:[31,4,1,""]},"escape.util.pox_extension":{ExtendedOFConnectionArbiter:[32,1,1,""],OpenFlowBridge:[32,1,1,""]},"escape.util.pox_extension.ExtendedOFConnectionArbiter":{"__init__":[32,4,1,""],"_core_name":[32,2,1,""],activate:[32,7,1,""],add_connection_listener:[32,4,1,""],getNexus:[32,4,1,""]},adaptation:{"_start_layer":[4,5,1,""],launch:[4,5,1,""]},escape:{adapt:[0,0,0,"-"],infr:[8,0,0,"-"],orchest:[11,0,0,"-"],service:[23,0,0,"-"],util:[33,0,0,"-"]},infrastructure:{"_start_layer":[10,5,1,""],launch:[10,5,1,""]},orchestration:{"_start_layer":[17,5,1,""],launch:[17,5,1,""]},service:{"_start_layer":[18,5,1,""],launch:[18,5,1,""]},unify:{"_start_components":[25,5,1,""],launch:[25,5,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","staticmethod","Python static method"],"4":["py","method","Python method"],"5":["py","function","Python function"],"6":["py","exception","Python exception"],"7":["py","classmethod","Python class method"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:staticmethod","4":"py:method","5":"py:function","6":"py:exception","7":"py:classmethod"},terms:{"0x7f2f6af3d3d0":29,"0x7f6b51cd61d0":[],"__abstractmethods__":31,"__call__":29,"__copy__":31,"__deepcopy__":31,"__delitem__":29,"__enter__":30,"__exit__":30,"__getitem__":29,"__init__":[1,2,3,7,9,12,13,14,15,16,19,20,21,22,26,27,28,29,30,31,32],"__iter__":1,"__metaclass__":[12,16,29,31],"__new__":12,"__setitem__":29,"__str__":27,"_abc_cach":31,"_abc_negative_cach":31,"_abc_negative_cache_vers":31,"_abc_registri":31,"_abstractnetconfadapter__parse_rpc_param":30,"_abstractnetconfadapter__parse_xml_respons":30,"_abstractnetconfadapter__remove_namespac":30,"_all_dependencies_met":27,"_core_nam":[2,7,13,20,27,32],"_create_rpc_request":30,"_default":[1,28],"_domainconfigurator__load_compon":1,"_escapenetworkbuilder__init_from_abstracttopolog":9,"_escapenetworkbuilder__init_from_config":9,"_escapenetworkbuilder__init_from_dict":9,"_escapenetworkbuilder__init_from_fil":9,"_escapenetworkbuilder__init_from_nffg":9,"_eventmixin_ev":[3,7,14,16,21,22,26],"_generate_resource_info":16,"_generate_virtual_view":16,"_handle_componentregist":7,"_handle_connectiondown":3,"_handle_connectionup":3,"_handle_deployev":2,"_handle_deploymentfinishedev":2,"_handle_deploynffgev":7,"_handle_domainchangedev":1,"_handle_getglobalresinfoev":2,"_handle_getvirtresinfoev":13,"_handle_globalresinfoev":13,"_handle_installationfinishedev":13,"_handle_installnffgev":2,"_handle_instantiatenffgev":13,"_handle_instantiationfinishedev":20,"_handle_missingglobalviewev":13,"_handle_missingvirtualviewev":20,"_handle_nffgmappingfinishedev":13,"_handle_sgmappingfinishedev":20,"_handle_virtresinfoev":20,"_init_from_json":31,"_initiate_gui":20,"_initiate_rest_api":20,"_install_nffg":13,"_instanc":29,"_instantiate_nffg":20,"_invoke_rpc":30,"_log_ev":29,"_mapping_finish":[14,21,28],"_networkbuilder__init_from_abstracttopolog":[],"_networkbuilder__init_from_config":[],"_networkbuilder__init_from_dict":[],"_networkbuilder__init_from_fil":[],"_networkbuilder__init_from_nffg":[],"_parse_json_bodi":27,"_parse_rpc_respons":30,"_proceed_api_cal":27,"_process_url":27,"_read_json_from_fil":27,"_register_listen":29,"_send_json_respons":27,"_send_request":26,"_slice_into_domain":1,"_start_compon":25,"_start_lay":[4,10,17,18],"_start_map":28,"_weakrefset":31,"abstract":[6,9,16,19,26,27,28,30,31],"byte":26,"case":[3,6,29],"catch":29,"class":[0,1,2,3,4],"default":[1,3,9,14,20,21,26,27,28,29,30,32],"enum":[26,29],"final":27,"function":[1,2,3,4,5,6,7,9,10,12,13,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31,32,33],"import":[3,30],"int":[3,9,15,16,20,22,26,27,30],"long":6,"new":[3,9,29,31],"return":[1,2,3,4,6,7,9,10,12,13,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31,32],"static":[12,27,29,31],"super":27,"switch":[3,9,26,30],"true":[1,3,9,25],"while":[20,27,31],abcmeta:31,about:[20,26,27],abstractapi:[2,7,13,20,27],abstractdomainadapt:[1,3,26],abstractdomainmanag:[3,26,29],abstractelementmanag:19,abstractmapp:[14,21,28],abstractmappingstrategi:[14,21,28,29],abstractnetconfadapt:[3,30],abstractnffg:31,abstractrequesthandl:[20,27],abstractrestadapt:[3,26],abstracttopolog:[9,29],abstractvirtu:[1,12,16,22,28],accept:[3,6,27],access:[1,3],accommod:6,accompani:6,accord:[22,32],achiev:32,acknowled:27,action:30,activ:32,actual:[3,12,16,22,26,27,28,31],adaptor:26,add:[6,15,31],add_cfg:29,add_connection_listen:32,add_edg:31,add_infra:31,add_link:31,add_nf:31,add_req:31,add_sap:31,add_sglink:31,addit:[3,26,30,33],addition:31,address:[3,9,20,27,30,32],advanc:6,after:12,agent:[3,26,30],algorithm:[3,6,14,21,26,28],alia:[16,26,29,31],all:[2,3,6,7,13,20,26,30,31],allow:[20,27],along:27,alreadi:32,also:[3,6,13,20,25,30],alwai:9,amount:29,analog:6,analyz:30,andra:6,ani:[3,6,9,29,30],anoth:30,api:[1,2,3,4],append:26,approach:[3,26],appropri:[4,10,17,18,25,29],apt:[6,30],arbit:[3,32],arbitrari:1,architectur:6,arg:[2,7,12,13,16,20,27,29],argument:[3,6,12,28,29,30],argv:31,assembl:30,asynchron:29,attila:6,attr:12,attribut:[3,9,12,27,31],auth:26,automat:[6,20,27,29,30],autosetmac:9,autostaticarp:9,avail:6,available_vnf:[3,26],avoid:9,back:[2,3,13,27],backuptopolog:9,balaz:6,bare:9,base:[1,2,3,6,7,9,12,13,14,15,16,19,20,21,22,26,27,28,29,30,31,32],base_url:26,basehttprequesthandl:27,basehttpserv:27,basic:[4,6,10,17,18,25,26,30,31],becaus:[27,30],been:3,befor:[3,12],behaviour:32,between:[1,3,9,20,26,27,32],bind:12,bme:[3,6],bodi:[26,27,30],bool:[1,3,4,9,10,17,18,25,27,28,29,30],both:31,bound:20,bounded_lay:[20,27],bride:32,bridg:9,build:[9,31],builder:9,built:[6,18],cach:31,call:[3,4,6,10,12,14,17,18,20,21,25,26,27,28,30],call_as_coop_task:29,call_rpc:30,calllat:[20,27],can:[2,3,6,9,13,20,26,29,30],cancel:26,candid:30,capabl:9,care:[6,20,27],carv:27,cas_api:0,caus:[9,26,27,30],central:[1,15,16,22],cfg:29,cgroup:6,chain:6,chang:[1,9,26],channel:30,check:[1,4,9,10,12,16,17,18,28],checker:16,checklisten:9,child:[27,30],classmethod:[12,14,21,28,32],clean:[9,29,30],cleanup:[9,29,30],click:[3,6,19,26],clicki:19,clickmanag:19,client_address:[20,27],close:30,code:[6,26,27],collect:[3,26,29],combin:6,command:[3,6,30],common:[27,28,29],commun:[3,26,28,30],compon:[1,3,6,7,15,16,19,22,25,26,27,29,32,33],componenet:1,component_nam:1,componentregist:7,comput:[3,22],concret:[5,27],condit:29,config:[1,5,9,28,29,30],configur:[1,5,6,26,28,29,30],connect:[3,9,26,28,30,32],connection_data:30,connectionerror:26,connectionin:32,connectionup:3,connectvnf:[3,26,30],consid:27,constructor:27,contact:[2,6,7,13,20],contain:[1,2,3,5,6,9,12,13,14,15,16,19,21,22,26,27,28,29,30,32],context:[12,20,26,27,29,30],control:[0,1,2,3,4,6,7,9,13,25,26],controller_nam:3,controlleradapt:[1,3,26],controlleradaptationapi:[1,2],conveni:9,convent:[4,10,17,18,25,27],convert:30,coocki:26,coop:[28,29],cooper:[27,29],copi:31,core:[3,4,10,17,18,20,25,27,29,32],correctli:3,correspond:[3,26],coupl:9,cover_nam:29,creat:[1,3,9,12,27,29,30,31],crud:27,csikor:[3,6],csoma:6,current:[6,22],custom:6,custom_head:26,data:[1,3,6,26,27,29,30,31],databas:1,datastructur:3,dead:27,dealloc:27,debug:[3,6,25,27,30],decor:[12,20,27,29],deep:31,deepcopi:31,def:12,defalut:30,default_ee_opt:9,default_host_opt:9,default_link_opt:9,default_opt:9,default_switch_opt:9,defaultservicemappingstrategi:[21,28],defin:[1,3,6,9,20,26,27,28,29],definit:[9,29,30],del_nod:31,delet:[3,20,27,29,31],demo:6,depend:[2,4],deploi:[3,6,26],deploy:[2,7,26],deployev:[3,26],deploymentfinishedev:[2,7],deploynffgev:[2,7],deref:1,deriv:[16,22,27,28],describ:31,descript:[3,6,22,26],design:[1,3,9,16,26,27,28,29,30,32],desir:32,destin:31,dev:[6,30],develop:6,devic:3,devot:[3,30],dict:[1,9,12,15,22,26,27,29,30,31],dictionari:[9,27,29,30],differ:[3,20,26,27],direct:[1,3],directli:[27,29],directmininetadapt:26,disabl:[27,29],disconnect:[3,26,30],disconnectvnf:[3,26],discoveri:27,discuss:26,dispatch:32,displai:9,do_connect:27,do_delet:27,do_get:27,do_head:27,do_opt:27,do_post:27,do_put:27,do_trac:27,doamin:26,doc:26,docker:3,dockerdomainmanag:3,document:3,domain:[1,2,3,16,26],domain_adapt:[0,1],domain_nam:1,domainchangedev:[1,3,26],domainconfigur:1,domainmanag:29,domainresmanag:1,domainresourcemanag:1,domainvirtu:[1,13,14,16],don:[20,27],done:29,dov:[1,16],down:3,download:[6,30],dpid:[3,32],dst:31,due:6,dump:29,dure:12,dynam:[27,31],each:27,echo:[6,20],ect:30,edg:31,edge_link:31,edge_req:31,edge_sglink:31,effect:22,either:3,elemenet:30,element:[9,12,19,30],element_mgmt:[],elementtre:30,els:26,empti:[9,27,29,30],emul:[1,2,3,6,7,9,10],encod:27,end:[2,3,13,14,21,26],enforc:12,enti:27,entir:[28,29],entiti:[26,27],entri:[2,7,13,20,29],enumer:29,environ:[6,9,28,29],eopt:9,error:[2,3,7,9,12,13,26,27,29,30],error_content_typ:27,escape_intf:27,escapeconfig:29,escapemappingstrategi:[14,28],escapenetworkbridg:9,escapenetworkbuild:9,escapev2:3,escapevirtu:[1,2,13,16,20,21],etc:[1,5,6,9,27,31],ethernet:3,etre:30,even:12,event:[1,2,3,4,7,10,13,14,16,17,18,20,21,22,25,26,27,28,29,32],eventmixin:[16,22,26,27,28,29],everi:[3,6,12,27,30],exampl:[6,12,30],exc_tb:30,exc_typ:30,exc_val:30,except:[9,12,27,30],execut:9,exist:[6,12,22,29],exit:[6,27],explicit:29,explicitli:[1,6,27,29],expos:[30,31],expr:30,express:30,extend:[9,14,32],extendedofconnectionarbit:32,extens:6,extern:[3,30],facad:27,fail:[12,27],fallback:[9,29],fals:[1,2,3,4,7,9,10,13,17,18,20,25,26,27,29,30,32],featur:26,felician:6,field:3,file:[6,9,27,29,30,31],filenam:31,filter:30,filter_connect:3,finish:[13,14,21,28],finit:26,fire:32,first:[1,6,12],fit:32,flexibl:9,flow:3,flowrul:31,follow:[1,3,4,9,10,12,16,17,18,22,25,26,27,28,30],form:[27,32],format:[3,6,9,27,30,31],forward:[2,14,15,21,27,28],found:[9,28,30],framework:6,from:[1,2,3,6,9,12,13,14,16,20,21,22,26,28,29,30,31],from_config:1,frozenset:31,fuction:26,full:[6,25],func:[12,29],further:[6,30],geenrat:21,gener:[1,2,3,9,12,13,15,16,20,26,27,28,29,30],get:[1,6,15,20,22,27,29,30],get_clean_after_shutdown:29,get_config:30,get_default_mgr:29,get_domain_compon:29,get_fallback_topolog:29,get_resource_info:[1,16],get_strategi:29,get_thread:29,get_virtual_view:16,get_wrapp:12,getglobalresinfoev:[2,13],getnexu:32,getnf:15,getter:[1,16],getvirtresinfoev:[13,20],getvnfinfo:[3,26],github:6,give:26,given:[1,3,6,9,12,13,14,15,16,21,22,26,27,28,29,30],global:[1,2,13,14,16,28],globalresinfoev:[2,13],goingdownev:27,goingupev:[4,10,17,18,25],got:30,gracefulli:3,graph:[4,6,13,14,15,17,18,20,21,22,23,25,28,31],graph_fil:27,graph_id:22,great:6,gui:[6,18,20,25],gulya:6,handl:[1,3,6,9,12,13,15,16,20,22,26,27,29,30],handler:[20,27,29],hasn:16,have:[3,6,9,12,16,27,28,29],header:27,headerdecompressor:30,help:[6,29],helper:[14,20,21,27,29,31,32],hide:[9,16,22,26,29],hierarchi:30,high:[1,9,31],higher:[1,12],holder:16,hole:29,hook:12,hopt:9,howev:3,http:[3,6,20,26,27],httperror:26,httpserver:27,hundr:6,ident:12,identifi:20,ietf:30,il_api:[],implement:[1,2,3,4,6,7,9,12,13,14,16,17,18,19,20,21,22,26,27,28,30,31],incom:[3,27,32],incorpor:6,index:6,indic:3,infer:12,info:[1,2,13,14,16,20,22,26,28,30],inform:[1,6,15,22,26,27,28,30],infr:[],infrastructur:[1,2,3,4],infrastructurelayerapi:7,inheret:26,inherit:[12,28,31,32],init:[1,2,3,9,12,13,14,15,16,19,20,21,22,26,27,28,29,31,32],initi:[1,2,3,4,5,6,7,9,10,13,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31],initialz:[2,13,20],initiate_service_graph:22,initiate_vnf:3,initiatevnf:[3,26],innamespac:9,inner:30,input:[3,6,18,25,28,30],input_graph:[14,21,28],instac:31,instal:[1,2,3,6,7,13,14,26,30],install_nffg:[1,3,26],install_rout:[3,7],installationfinishedev:2,installnffgev:[2,13],instanc:[1,3,9,12,15,16,20,22,31],instanti:[13,15,20,29],instantiate_nffg:15,instantiatenffgev:[13,20],instantiationfinishedev:13,instead:[9,28,30],intact:29,interact:[3,6],interfac:[1,9,19,26,31],intern:[1,2,3,6,7,9,26,28,31,32],internalcontrollerproxi:9,internaldomainmanag:3,internalpoxcontrol:9,invok:[1,13,20,28,29,30],irrelev:6,is_load:29,isn:22,item:29,iter:[1,30],ito:3,itself:31,json:[6,9,26,27,29,31],json_data:31,junk:9,just:[22,27],kei:[29,30],keyword:[9,30],kill:3,kind:26,kwarg:[1,2,3,7,9,12,13,16,20,26,27,29],lasr:30,last:[27,30],latest:26,launch:[4,10,17,18,25],layer:[1,2,3,4],layer_api:[1,15,22],layer_id:16,layer_nam:28,lazy_load:1,leav:29,left:9,less:9,level:[1,6,9,15,26,31],levent:6,lib:[2,7,13,14,16,20,21,22,26,27,28],librari:[30,31],libxml2:[6,30],libxslt1:[6,30],link:[3,9,31],list:[3,6,26,29,30],listen:[3,29,32],listenport:9,load:[1,29],load_config:29,load_default_mgr:1,load_from_fil:31,load_internal_mgr:1,localhost:[6,20],lock:27,log:[6,20,27,29],log_error:27,log_full_messag:27,log_messag:27,logger:[20,27,29],logic:[1,2,12,13,15,16,20,22,26,27,29],loos:9,lopt:9,lot:30,lower:[13,20,22],lxml:[6,30],magang:1,magic:[12,31],main:[1,3],maintain:[2,7,13,20],make:9,manag:[1,3,6,9,15,16,19,22,26,30,31],mandatori:[3,26,27],mani:26,manipul:[29,31],manual:[20,27],map:[1,2,4,13,14,15,20,21,22],mapped_nffg:[1,13],mapped_nffg_fil:[4,6],mapper:[14,21,28],match:12,mean:[29,31],mechan:[16,27],memo:31,messag:[6,27,29,30,32],meta:12,metaclass:29,method:[16,26,27,28],mformat:27,micro:27,microtask:[13,20,28,29],mid:9,might:9,mimic:29,minim:[6,29],minimalist:27,mininet:[2,3,6,7,9],mininetdomainadapt:3,misc:20,miscellan:29,miss:[16,22],missingglobalviewev:[13,16],missingvirtualviewev:[20,22],mixin:[3,26],mode:[6,27],model:31,modif:29,modul:0,more:[3,6],most:3,mostli:[23,26,32],msg:[27,29],much:[20,27],multigraph:31,multipl:1,multitask:[26,29],must:[1,12,27,28],name:[1,3,9,12,26,27,28,29,30,31,32],nameless:[12,29],namespac:[6,30],natur:9,ncclient:[6,30],need:[1,3,6,12,13,14,20,21,26,27,28,29,30],negoti:6,nemeth:6,net:[3,9],netconf:[1,3,26],netconf_namespac:30,netopt:9,network:[2,3,6,7,9,14,15,21,22,26,28],networkbuild:9,networkx:[6,31],nexu:32,nf_id:15,nffg:[1,2,3,13,14,15,16,20,21,22,26,28],nffg_file:[6,17],nffg_id:15,nffg_part:[2,3,26],nffgmanag:15,nffgmappingfinishedev:[13,14],nfibmanag:[15,22],no_rpc_error:30,node:[6,9,31],node_infra:31,node_nf:31,node_sap:31,nodeinfra:31,nodenf:31,nodesap:31,non:27,none:[1,2,3,4,6,7,9,10,12,13,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31],normal:[20,27],notimplementederror:[16,28],number:[6,9,20,27,29,30],obj:9,object:[1,2,3,7,9,12,13,15,16,19,20,22,26,27,28,29,30,31,32],observ:6,obvious:3,occur:[3,26],offer:9,old:9,onc:[27,29],onli:[1,3,6,26,27,29,30],open:[6,9],openflow:[3,6,32],openflowbridg:32,openflowconnectionarbit:32,openflownexu:32,openstack:[3,26],openstackapi:[3,26],openstackdomainmanag:3,openstackrestadapt:3,oper:[6,20,26,27,31],operationerror:3,opt:9,option:[3,4,6,9,10,17,18,25,26,27,28,29,30],orchest:1,orchestr:[1,11,13,14,15,16],order:[6,26,30],ordereddict:[3,26],org:26,organ:[15,16,22],orig_func:12,origin:[9,12,27,32],other:[2,3,7,13,16,20,26,27,29,30],otherwis:29,our:6,out:[20,26,27,30],over:[9,30],overrid:[16,27,28,29,32],overwritten:27,own:[30,32],page:6,pair:[3,26],paper:6,param:[6,7,12,26,27,28,30,31,32],param_nam:27,param_valu:27,paramet:[1,2,3,4,6,7,9,10,12,13,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31,32],paramiko:[6,30],parg:29,pars:[27,30,31],part:[1,7,26,30],pass:[2,13,20,30],password:30,path:[4,6,9,17,18,25,27],patteran:[3,26],pattern:[1,9,16,26,27,28,29,30,32],per:29,perform:[14,21],period:26,permiss:27,persist:26,pip:[6,26,30],place:[16,22],placehold:16,platform:[2,13,20],poc:29,point:[2,4,7,10,13,17,18,20,27],polici:[12,16],policy_enforc:11,policyenforc:[12,16],policyenforcementerror:12,policyenforcementmetaclass:[12,16],poll:26,pool:26,port:[3,9,20,26,27,30,31,32],post:[6,12,16,20,27],post_:12,post_sanity_check:12,poster:6,power:9,pox:[2,3,4,6,7,10,13,14,16,17,18,20,21,22,25,26,27,28,29,32],pox_extens:[],poxdomainadapt:[3,9],practic:3,pre:[3,9,12,26],pre_:12,pre_sanity_check:12,prefix:[12,27,30],prepar:[26,28],pretty_log:6,previou:6,previous:31,print:[27,30],privat:[16,27],privileg:6,proce:[13,20],process:[1,2,12,13,14,21,22,28,29,30,31],program:6,propag:2,proper:[9,30],properti:30,protocol:[26,30],prototyp:6,provid:[3,26,31],proxi:[12,16],purpos:[7,9,26,32],put:[20,27],python:[6,13,20,26,28,29,30,31],quit:29,quit_with_error:29,rais:[3,9,12,13,16,20,26,27,28,30],raiselat:[20,27],raw:30,rcp:[3,30],read:[6,27],realiz:[20,29],receiv:2,recoco:[20,27,29],reconnect:3,refer:[1,2,4,7,10,13,17,18,20,29],referenc:31,regist:[3,7,27,29,32],registr:27,rel:29,relat:[0,2,3,6,7,8,9,11,12,13,20,23,26],relev:[1,15,16,19,20,22,26,27],reli:[1,26,30],remot:[1,3],remotecontrol:9,remov:[3,15,30],repeat:3,replac:32,repli:[3,26,30],repres:[1,2,3,6,7,9,12,13,19,20,27,31],represent:[9,28,31],request:[2,6,13,16,20,22,26,27,30],request_data:30,request_perm:[20,27],request_servic:20,requesthandl:5,requesthandlerclass:27,requir:[6,22,26,30,31],resofedg:31,resouc:16,resourc:[1,2,6,11,13,14,15,16,17,20,21,22,25,28],resource_info:[2,13],resource_view:[14,21,28],resourceorchestr:15,resourceorchestrationapi:[13,15],resourceorchestrationmapp:14,respect:[27,29],respond:26,respons:[26,27,30],rest:3,resterror:27,restserv:27,result:[27,30],resum:26,ret_valu:12,reusabl:9,revent:[2,7,13,14,16,20,21,22,26,27,28],revers:29,rfc:[6,30],root:6,ros_api:11,ros_map:11,ros_orchestr:11,rout:[1,3],rpc:[1,3,30],rpc_name:30,rpc_namespac:[3,30],rpc_request:30,rpcerror:[3,30],rule:3,run:[4,6,9,10,17,18,25,26,27,28,29,30],run_dri:9,runtimeerror:12,safe:27,sahel:6,sahhaf:6,same:[1,26,27],sampl:6,saniti:[12,16],sanity_check:16,sap:[9,31],sas_api:[],sas_map:[],sas_orchestr:[],save:[13,15,20,22,30],scale:6,schedul:29,schedule_as_coop_task:[20,27,29],sdn:[6,26],search:[1,6,28],see:[3,26],seealso:9,self:[12,26,27,29],send:[2,3,13,20,26,27,32],send_acknowledg:27,send_error:27,send_rest_head:27,sent:3,separ:[1,9,14,21,26,28,29],sequenc:29,sequenti:29,serv:9,server:[20,27,30],server_vers:27,servic:13,servicegraphmapp:21,servicelayerapi:[20,22],serviceorchestr:22,servicerequesthandl:20,session:26,set:[3,4,6,7,9,12,14,16,20,21,22,26,27,28,29,30],set_load:29,setup:30,setuptool:[6,30],sg_file:[6,18,25],sgmanag:22,sgmappingfinishedev:[20,21],shallow:31,shell:6,should:[3,12,26,27,28,29,30],shoulder:6,show:6,shut:3,shutdown:[2,7,13,20,27],sid:20,sigcomm:6,signal:[2,7,12,13,14,16,21,22,25,26],similar:[6,9],simpl:30,simplestandalonehelp:29,simplic:30,simpliest:6,simplifi:27,singl:[21,31],singleton:29,situat:27,slice:1,socket:[3,32],socketserv:27,softwar:6,sonkoli:6,sopt:9,sourc:[6,30,31],special:[29,32],speciali:29,specif:[1,3,6,7,9,13,19,20,26,27,30],split:[3,27],src:31,ssh:30,stand:[6,12],standalon:[2,4,6,7,10,13,17,18,20,27],standard:[1,16,31],start:[1,3,6,9,26,27,29],start_network:9,start_pol:26,startup:30,startvnf:[3,26],state:[6,26,30],static_prefix:27,statu:3,stdout:30,steer:6,step:[27,28],stop:[1,3,9,26,27],stop_network:9,stop_pol:26,stopvnf:[3,26],store:[1,9,15,16,22,29],str:[1,3,4,9,12,17,18,20,25,26,27,28,29,30,31],strategi:[5,14,28,29],string:[27,31],structur:3,subclass:[1,28],sublay:[0,1,2,4],subordin:12,subpackag:[11,23],success:[2,7,13],successful:2,sudo:[6,26,30],suggest:6,supervis:12,supplementari:[14,21],support:[3,22,26,29,30],suspend:26,switch_id:[3,26],synchron:[20,27],synchronis:[20,27],system:6,tag:30,take:[6,20,27],task:[14,20,21,26,27],taverni:6,templat:26,test:[2,6,7,9,20],test_network:[],testb:6,text:[26,27],them:[3,6],therebi:20,therefor:12,thi:[1,3,6,12,16,20,26,27,28,29,30,31,32],think:[20,27],thread:[13,14,20,21,27,28,29],threadingmixin:27,three:[12,29],through:[26,30],tide:22,time:[26,27],timeout:[26,30],timer:26,tmit:[3,6],to_fil:30,to_json:31,tool:6,top:3,topmost:26,topo:[9,29],topo_class:9,topo_nam:29,topolog:[],topology_config_nam:9,topologybuilderexcept:9,toward:30,traffic:6,transfer:3,translat:3,transpar:[3,26],transporterror:3,tupl:[12,27,29,30,32],two:[12,29],type:[1,3,9,12,14,15,16,21,22,26,27,28,29,30,31,32],under:[6,29],unicod:27,unifi:[0,2,3,11,13,20],uniqu:[3,29],unlimit:[3,26],unsupport:27,unter:29,until:[27,30],uny_0:3,uny_1:3,up_and_run:3,updat:[1,9,27,29],update_resource_usag:1,upper:[2,3,13],upward:2,url:[3,26,27],urn:30,usag:[1,6,30],user:26,usernam:30,utf:27,util:[2,3,13,14,20,21,26,28,30,31,32],valid:[26,28],valu:[3,12,20,26,28,29,30],variou:[6,26,30],verb:[6,20,27],verbos:6,version:[6,20,31,32],view:[14,16,21,22],violat:12,virtresinfoev:[13,20],virtual:[1,3,6,12,13,14,16,20,21,22],virtual_view:22,virtualethernet:3,virtualization_mgmt:[1,11],virtualizermanag:16,virtualresourcemanag:22,vnf:[1,3,6,19,26,30],vnf_descript:[3,26],vnf_id:[3,26],vnf_port:[3,26],vnf_starter:[3,26],vnf_type:[3,26,30],vnfstarter:[3,26],vnfstarteradapt:3,vnfstarterapi:[3,26],vswitch:6,wai:[9,13,20,26,29],wait:[7,26,27],weakset:31,well:26,when:[4,10,13,14,17,18,20,21,25,26,27,28],where:30,whether:3,which:[1,3,4,6,9,10,12,13,14,16,17,18,20,21,26,27,28,29,30],whole:26,with_infr:[1,4,6],without:[4,6,10,17,18],work:30,worri:[20,27],wouter:6,wrap:28,wrapper:[3,9,29,30],written:29,xml:30,xml_element:30,xpath:30,yang:[3,26,31],yangcli:30,yet:[3,16,19],you:[20,27],zero:29},titles:["<em>escape.adapt</em> package","<em>adaptation.py</em> module","<em>cas_API.py</em> module","<em>domain_adapters.py</em> module","The <em>adaptation.py</em> main module","<em>escape</em> package","Welcome to ESCAPEv2&#8217;s documentation!","<em>il_API.py</em> module","<em>escape.infr</em> package","<em>topology.py</em> module","The <em>infrastructure.py</em> main module","<em>escape.orchest</em> package","<em>policy_enforcement.py</em> module","<em>ros_API.py</em> module","<em>ros_mapping.py</em> module","<em>ros_orchestration.py</em> module","<em>virtualization_mgmt.py</em> module","The <em>orchestration.py</em> main module","The <em>service.py</em> main module","<em>element_mgmt.py</em> module","<em>sas_API.py</em> module","<em>sas_mapping.py</em> module","<em>sas_orchestration.py</em> module","<em>escape.service</em> package","The <em>escape</em> package","The <em>unify.py</em> top module","<em>adapter.py</em> module","<em>api.py</em> module","<em>mapping.py</em> module","<em>misc.py</em> module","<em>netconf.py</em> module","<em>nffg.py</em> module","<em>pox_extension.py</em> module","<em>escape.util</em> package"],titleterms:{"class":6,adapt:[0,1,4,26],api:[6,27],cas_api:2,content:[1,2,3,7,9,12,13,14,15,16,19,20,21,22,26,27,28,29,30,31,32],depend:6,document:6,domain_adapt:3,element_mgmt:19,escap:[0,5,8,11,23,24,33],escapev2:6,il_api:7,indic:6,infr:8,infrastructur:10,layer:6,main:[4,6,10,17,18],map:28,misc:29,modul:[1,2,3,4,6,7,9,10,12,13,14,15,16,17,18,19,20,21,22,25,26,27,28,29,30,31,32],netconf:30,nffg:31,orchest:11,orchestr:17,overview:6,packag:[0,5,8,11,23,24,33],policy_enforc:12,pox_extens:32,readm:6,rest:6,ros_api:13,ros_map:14,ros_orchestr:15,sas_api:20,sas_map:21,sas_orchestr:22,servic:[18,23],structur:6,sublay:6,submodul:[0,5,8,11,23,25,33],tabl:6,top:25,topolog:9,unifi:25,util:33,virtualization_mgmt:16,welcom:6}})
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import xml.etree.ElementTree as ET

class ActionProvideNetworkingConceptInfo(Action):
    def name(self) -> Text:
        return "provide_concept_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the detected networking concept entity
        concept_entity = next(tracker.get_latest_entity_values("network_device"), None)

        if concept_entity:
            # Define responses for each concept
            concept_responses = {
                "router": "utter_router",
                "switch": "utter_switch",
                "firewall": "utter_firewall",
                "ip address": "utter_ip_address",
                "subnetting": "utter_subnetting",
                "dns": "utter_dns",
                "gateway": "utter_gateway",
                "ports": "utter_ports",
                "mac addresses": "utter_mac_addresses",
                "tcp/ip": "utter_tcp_ip",
            }

            # Check if the detected concept has a predefined response
            if concept_entity.lower() in concept_responses:
                response_template = concept_responses[concept_entity.lower()]
                dispatcher.utter_template(response_template, tracker)
            else:
                dispatcher.utter_message("I'm sorry, I don't have information on that networking concept.")
        else:
            dispatcher.utter_message("I couldn't detect any networking concepts in your input. Please try again.")

        return []
    


class ActionProvideSwitchConfiguration(Action):
    counter=1
    def name(self) -> Text:
        return "provide_switch_config"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the detected networking concept entity
        user_number_switch = next(tracker.get_latest_entity_values("user_number"), None)
        if user_number_switch:
            user_count=int(user_number_switch)
            if user_count >= 0:
                config=self.generate_switch_config(user_count)
                dispatcher.utter_message(config)
            else:
                dispatcher.utter_message("Non valid value! Try again!")
        else:
            dispatcher.utter_message("Non valid value! Try again!")

        return []
    def generate_switch_config(self,number):
            config="""
            enable
            configure terminal
            """
            interface_range = "interface range gigabitethernet0/1-" + str(number)
            config+=f"vlan vlan{self.counter}\n"
            config+=f"name prueba{self.counter}\n"
            config+=f"{interface_range}\n"
            config += f"switchport access vlan vlan{self.counter}\n"
            config += """
            switchport mode access
            switchport access vlan vlan1
            end
            write memory
            """
            self.counter+=1
            return config


class ActionGenerateSimpleScenario(Action):
    def name(self) -> Text:
        return "generate_example_scenario"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Define the XML content using string formatting
        intent= tracker.latest_message['intent'].get('name')
        # Create the XML file in the proyecto-integrador folder
        xml_content=''
        #Define xml content depending on intent given
        if(intent=='ask_simple_network_scenario'):
            with open('simple_lxc_ubuntu64.xml', 'r') as xml_file:
              xml_content = xml_file.read()
        else:
            with open('tutorial_lxc_ubuntu64.xml','r') as xml_file:
              xml_content=xml_file.read()
        #Change for Linux path
        file_path = "C:\\Users\\charl\\Documents\\customscenario.xml"
        with open(file_path, "w") as xml_file:
            xml_file.write(xml_content)
        dispatcher.utter_message(f"Scenario created as XML file generated and saved as {file_path}")
        return []
    
#Class to generate a simple network scenario 
class ActionGenerateSimpleNetwork(Action):
    def name(self) -> Text:
        return "generate_simple_network"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_number_network = next(tracker.get_latest_entity_values("user_number_n"), None)

    def createXMLFile(user_number):
        # Names, defaults,etc
        root = ET.Element("vnx", attrib={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                     "xsi:noNamespaceSchemaLocation": "/usr/share/xml/vnx/vnx-2.00.xsd"})
        global_elem = ET.SubElement(root, "global")
        ET.SubElement(global_elem, "version").text = "2.0"
        ET.SubElement(global_elem, "scenario_name").text = "simple_net_lxc_ubuntu"
        ET.SubElement(global_elem, "automac")
        vm_mgmt_elem = ET.SubElement(global_elem, "vm_mgmt", type="none")
        #Create virtual machine default options
        ET.SubElement(vm_mgmt_elem, "vm_defaults")
        vm_defaults = ET.SubElement(global_elem, "vm_defaults")
        ET.SubElement(vm_defaults, "console", attrib={"id": "0", "display": "no"})
        ET.SubElement(vm_defaults, "console", attrib={"id": "1", "display": "yes"})

        #Create command sequences
        cmd_seq_elem1 = ET.SubElement(global_elem, "cmd-seq", seq="ls12").text = "ls1,ls2"
        ET.SubElement(global_elem, "cmd-seq", seq="ls123").text = "ls12,ls3"
        ET.SubElement(global_elem, "cmd-seq", seq="ls1234").text = "ls123,ls4"

        # Create help elements
        help_elem = ET.SubElement(global_elem, "help")
        ET.SubElement(help_elem, "seq_help", seq='start-www').text = "Start apache2 web server"
        ET.SubElement(help_elem, "seq_help", seq='stop-www').text = "Stop apache2 web server"
        # Create network bridges 1 for host other for others
        ET.SubElement(root, "net", name=f"Net0", mode="virtual_bridge")
        ET.SubElement(root, "net", name=f"Net1", mode="virtual_bridge")

        #Create router elements
        for i in range(1, user_number+1):
          host_elem = ET.SubElement(root, "vm", name=f"h{i}", type="lxc")
          ET.SubElement(host_elem, "filesystem", type="cow").text = "/usr/share/vnx/filesystems/rootfs_lxc"
          if_elem = ET.SubElement(host_elem, "if", id="1", net="Net1")
          ET.SubElement(if_elem, "ipv4").text = f"10.1.0.{i+1}/24"
          ET.SubElement(host_elem, "route", type="ipv4", gw="10.1.0.1").text = "default"



       

        

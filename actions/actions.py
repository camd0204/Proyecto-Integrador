# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os


from typing import Any, Text, Dict, List
from lxml import etree
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import xml.etree.ElementTree as ET
import xml.dom.minidom
import subprocess

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
        return "provide_switch_config_for_cisco"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the detected networking concept entity
        user_number_switch = next(tracker.get_latest_entity_values("user_number_cisco"), None)
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
    
class ActionProvideSwitchConfigurationVNX(Action):
    counter=1
    ip_address_dict = {}
    def name(self) -> Text:
        return "provide_switch_config"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the detected networking concept entity
        user_number_switch = next(tracker.get_latest_entity_values("user_number"), None)
        if user_number_switch:
            user_count=int(user_number_switch)
            if user_count >= 0:
                self.generate_switch_config(user_count)
                description=f"Simple scenario made of one VM acting as a switch and {user_count} VMs connected to it. Shows the use of 'veth' based direct connections among LXC VMs."
                dispatcher.utter_message(f"Scenario created as XML file generated and saved as vnx_custom_network_switch_{user_count}_users.xml. Description: {description}. Machine IPS info: {self.ip_address_dict}")
                self.write_file_path_to_historic(f"user_gen_files/vnx_custom_network_switch_{user_count}_users.xml")
            else:
                dispatcher.utter_message("Non valid value! The scenario couldnt be created!")
        else:
            dispatcher.utter_message("Non valid value! Try again!")

        return []
    def generate_switch_config(self,number):
        self.ip_address_dict.clear()
        root = ET.Element("vnx", attrib={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                     "xsi:noNamespaceSchemaLocation": "/usr/share/xml/vnx/vnx-2.00.xsd"})
        global_elem = ET.SubElement(root, "global")
        ET.SubElement(global_elem, "version").text = "2.0"
        ET.SubElement(global_elem, "scenario_name").text = f"vnx_custom_network_switch_{number}_users"
        ET.SubElement(global_elem, "automac")
        ET.SubElement(global_elem,"vm_mgmt",type="none")
        vm_defaults = ET.SubElement(global_elem, "vm_defaults")
        ET.SubElement(vm_defaults, "console", attrib={"id": "0", "display": "no"})
        ET.SubElement(vm_defaults, "console", attrib={"id": "1", "display": "yes"})

        for i in range(1, number + 1):
            net_elem = ET.SubElement(root, "net", attrib={"name": f"link{i}", "mode": "veth", "type": "p2p"})

        for i in range(1, number + 1):
            vm_elem = ET.SubElement(root, "vm", attrib={"name": f"vm{i}", "type": "lxc", "exec_mode": "lxc-attach","arch":"x86_64"})
            ET.SubElement(vm_elem, "filesystem", attrib={"type": "cow"}).text = "/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64"
            if_elem_1 = ET.SubElement(vm_elem, "if", attrib={"id": "1", "net": f"link{i}"})
            ET.SubElement(if_elem_1, "ipv4").text = f"1.1.1.{i + 3}/24"
            self.ip_address_dict[f"vm{i}"] = f"1.1.1.{i + 3}"
         # Add switch element
        switch_elem = ET.SubElement(root, "vm", attrib={"name": "switch", "type": "lxc", "exec_mode": "lxc-attach","arch":"x86_64"})
        ET.SubElement(switch_elem, "filesystem", attrib={"type": "cow"}).text = "/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64"
        for i in range(1, number + 1):
            ET.SubElement(switch_elem, "if", attrib={"id": str(i), "net": f"link{i}"})
        exec_elem = ET.SubElement(switch_elem, "exec", attrib={"seq": "on_boot", "type": "verbatim", "ostype": "system"})
        exec_elem.text = '''sleep 10; 
            apt-get -y install openvswitch-switch;
            ovs-vsctl add-br switch;'''

        for i in range(1, number + 1):
            exec_elem.text += f'\novs-vsctl add-port switch eth{i};'

        exec_elem.text += f'\nip addr add 1.1.1.{number + 4}/24 dev switch'

        # Create the ElementTree object and write to file
        xml_string = ET.tostring(root, encoding='utf-8')

        # Parse the XML string
        dom = xml.dom.minidom.parseString(xml_string)

        # Prettify the XML with indentation and line breaks
        pretty_xml = dom.toprettyxml(indent="  ")

        # Write the prettified XML to a file
        with open(f"user_gen_files/vnx_custom_network_switch_{number}_users.xml", "w", encoding="utf-8") as xml_file:
            xml_file.write(pretty_xml)

    def write_file_path_to_historic(self,file_path):
        with open("historic_scripts/history.txt", "a") as txt_file:
            txt_file.write(file_path+"\n")

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
            with open('xml_files/simple_lxc_ubuntu64.xml', 'r') as xml_file:
              xml_content = xml_file.read()
        elif(intent=='ask_switch_network_scenario'):
            with open('xml_files/example_lxc_vm-as-switch.xml','r') as xml_file:
                xml_content=xml_file.read()
        elif(intent=='ask_vlan_switch_scenario'):
            with open('xml_files/tutorial_vlan_ovs.xml','r') as xml_file:
                xml_content=xml_file.read()
        else:
            with open('xml_files/tutorial_lxc_ubuntu64.xml','r') as xml_file:
              xml_content=xml_file.read()
        #Change for Linux path
        file_path =""
        description=""
        if(intent=='ask_simple_network_scenario'):
            file_path='user_gen_files/simple_lxc_ubuntu64.xml'
            description="""Just one Ubuntu virtual machine connected to a Network named Net0 with address 10.1.0.4. 
             The host has an interface in Net0 with address 10.1.0.1  
             This simple scenario is supposed to be used for testing the different 
             types of virtual machines supported by VNX. You can start several simple_*.xml
             scenarios and test the connectivity among virtual machines and the host, as all
             scenarios share the same "Net0" network."""
        elif(intent=='ask_switch_network_scenario'):
            file_path='user_gen_files/example_lxc_vm-as-switch.xml'
            description="""Simple scenario made of one VM acting as a switch and three VMs connected 
             to it. Shows the use of 'veth' based direct connections among LXC VMs."""
        elif(intent=='ask_vlan_switch_scenario'):
            file_path='user_gen_files/tutorial_vlan_ovs.xml'
            description=""" It outlines the setup for a virtual network comprising virtual machines (VMs) and virtual networks (Net0, Net1, Net2). 
            Each VM is configured with specific attributes, including its type (Linux Containers), architecture, file system, memory allocation, network interface, VLAN tagging, and IP address assignment."""
        else:
            file_path='user_gen_files/tutorial_lxc_ubuntu64.xml'
            description="""A scenario made of 6 LXC Ubuntu virtual machines (4 hosts: h1, h2, h3 and h4; 
             and 2 routers: r1 and r2) connected through three virtual networks. The host participates 
             in the scenario having a network interface in Net3."""
        with open(file_path, "w") as xml_file:
            xml_file.write(xml_content)
        self.write_file_path_to_historic(file_path)
        dispatcher.utter_message(f"Example scenario created as XML file generated and saved as {file_path}. The description for the scenario:{description}")
        return []
    

    def write_file_path_to_historic(self,file_path):
        with open("historic_scripts/history.txt", "a") as txt_file:
            txt_file.write(file_path+"\n")
    
#Class to generate a simple network scenario 
class ActionGenerateSimpleNetwork(Action):
    ip_address_dict = {}
    filecounter=1
    def name(self) -> Text:
        return "generate_simple_network"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_number_network = next(tracker.get_latest_entity_values("user_number_n"), None)
        if user_number_network:
            user_network_count=int(user_number_network)
            if(user_network_count>0):
                self.createXMLFile(user_network_count)
                description=f"""The scenario consists of a variable number of {user_network_count} LXC-based virtual machines connected to two network bridges, 
        "Net0" and "Net1." Each virtual machine has specific configurations, including filesystem settings, IP addresses, and routes. 
        Additionally, the XML file includes commands to start and stop an Apache web server and defines a router element"""
                dispatcher.utter_message(f"Scenario created as XML file generated and saved as vnx_custom_network_router_{user_network_count}_users.xml. Description: {description}. Machine IPS info: {self.ip_address_dict}")
            else:
                dispatcher.utter_message("User number not valid, file could not be created.")
        else:
            dispatcher.utter_message("User number not valid, file could not be created.")
        return []


    def createXMLFile(self,user_number):
        # Names, defaults,etc
        self.ip_address_dict.clear()
        root = ET.Element("vnx", attrib={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                     "xsi:noNamespaceSchemaLocation": "/usr/share/xml/vnx/vnx-2.00.xsd"})
        global_elem = ET.SubElement(root, "global")
        ET.SubElement(global_elem, "version").text = "2.0"
        ET.SubElement(global_elem, "scenario_name").text = f"vnx_custom_network_router_{user_number}_users"
        ET.SubElement(global_elem, "automac")
        ET.SubElement(global_elem,"vm_mgmt",type="none")
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

        #Create host elements
        for i in range(1, user_number):
          host_elem = ET.SubElement(root, "vm", name=f"h{i}", type="lxc",arch="x86_64")
          ET.SubElement(host_elem, "filesystem", type="cow").text = "/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64"
          if_elem = ET.SubElement(host_elem, "if", id="1", net="Net0")
          ET.SubElement(if_elem, "ipv4").text = f"10.1.0.{i+1}/24"
          ET.SubElement(host_elem, "route", type="ipv4", gw="10.1.0.1").text = "default"
          self.ip_address_dict[f"h{i}"] = f"10.1.0.{i+1}"
        #Create a final machine that will act as a server
        host_elem = ET.SubElement(root, "vm", name=f"h{user_number}", type="lxc",arch="x86_64")
        ET.SubElement(host_elem, "filesystem", type="cow").text = "/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64"
        if_elem = ET.SubElement(host_elem, "if", id="1", net="Net0")
        ET.SubElement(if_elem, "ipv4").text = f"10.1.0.{user_number+1}/24"
        ET.SubElement(host_elem, "route", type="ipv4", gw="10.1.0.1").text = "default"
        # Add the additional XML elements
        
        filetree_elem = ET.SubElement(host_elem, "filetree", seq="start-www", root="/var/www/")

        # Start/stop apache www server
        exec_start_www = ET.SubElement(host_elem, "exec", seq="start-www", type="verbatim", ostype="system")
        exec_start_www.text = "chmod 644 /var/www/*"

        exec_start_www = ET.SubElement(host_elem, "exec", seq="start-www", type="verbatim", ostype="system")
        exec_start_www.text = "service apache2 start"

        exec_stop_www = ET.SubElement(host_elem, "exec", seq="stop-www", type="verbatim", ostype="system")
        exec_stop_www.text = "service apache2 stop"

        
        #Create router elements
        router_elem = ET.SubElement(root, "vm", attrib={"name": "r1", "type": "lxc","arch":"x86_64"})
        ET.SubElement(router_elem, "filesystem", attrib={"type": "cow"}).text = "/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64"

        for i, net_name in enumerate(["Net0", "Net1"]):
            if_elem = ET.SubElement(router_elem, "if", attrib={"id": str(i + 1), "net": net_name})
            if i == 0:
                ET.SubElement(if_elem, "ipv4").text = "10.1.0.1/24"
            elif i == 1:
                ET.SubElement(if_elem, "ipv4").text = "10.1.3.1/24"
    
        host_elem = ET.SubElement(root, "host")
        hostif_elem = ET.SubElement(host_elem, "hostif", attrib={"net": "Net1"})
        ET.SubElement(hostif_elem, "ipv4").text = "10.1.3.2/24"
        ET.SubElement(host_elem, "route", attrib={"type": "ipv4", "gw": "10.1.3.1"}).text = "10.1.0.0/16"

        # Convert the ElementTree to a string
        xml_string = ET.tostring(root, encoding='utf-8')

        # Parse the XML string
        dom = xml.dom.minidom.parseString(xml_string)

        # Prettify the XML with indentation and line breaks
        pretty_xml = dom.toprettyxml(indent="  ")

        # Write the prettified XML to a file
        with open(f"user_gen_files/vnx_custom_network_router_{user_number}_users.xml", "w", encoding="utf-8") as xml_file:
            xml_file.write(pretty_xml)
        self.write_file_path_to_historic(f"user_gen_files/vnx_custom_network_router_{user_number}_users.xml")

    def write_file_path_to_historic(self,file_path):
        with open("historic_scripts/history.txt", "a") as txt_file:
            txt_file.write(file_path+"\n")


class ActionGenerateComplexNetwork(Action):
    perl_script_path = "scripts/create-tutorial_lxc_ubuntu-big"
    redundancy_script_path = "scripts/create-tutorial_lxc_ubuntu-big"
    def name(self) -> Text:
        return "generate_complex_network"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_number_for_router = tracker.get_slot("user_number_for_router")
        router_number = tracker.get_slot("router_number")
        redundancy= tracker.latest_message['intent'].get('name')
        if user_number_for_router and router_number:
            router_number_int=int(router_number)
            if(redundancy=='affirmative_redundancy') and router_number_int>2:
                stdout, stderr, return_code = self.run_perl_script(self.redundancy_script_path, user_number_for_router, router_number)
            else:
                stdout, stderr, return_code = self.run_perl_script(self.perl_script_path, user_number_for_router, router_number)
            self.write_script_to_XML(stdout,router_number,user_number_for_router)
            suma=int(user_number_for_router)*int(router_number)
            dispatcher.utter_message(f"Script written to: user_gen_files/{router_number}router_{suma}_user.xml. Description:A big tutorial scenario made of {suma} LXC virtual machines ({router_number} routers and {user_number_for_router} hosts).")
        else:
            dispatcher.utter_message("Network creation unable to be achieved.")
        return []

    def run_perl_script(self,script_path, *args):
        try:
            # Build the command to run the Perl script
            command = ['perl', script_path] + list(args)
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr = process.communicate()
            # Check the return code
            return_code = process.returncode

            # Return the standard output, standard error, and return code
            return stdout, stderr, return_code
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1  # Return an error code of 1
    def write_script_to_XML(self,xml_string,router_number,user_per_rout):
        # Parse the XML string
        dom = xml.dom.minidom.parseString(xml_string)

        # Prettify the XML with indentation and line breaks
        pretty_xml = dom.toprettyxml(indent="  ")

        # Write the prettified XML to a file
        mult=int(router_number)*int(user_per_rout)
        with open(f"user_gen_files/{router_number}_router_{mult}_user.xml", "w", encoding="utf-8") as xml_file:
            xml_file.write(pretty_xml)
        self.write_file_path_to_historic(f"user_gen_files/{router_number}_router_{mult}_user.xml")

    def write_file_path_to_historic(self,file_path):
        with open("historic_scripts/history.txt", "a", encoding="utf-8") as txt_file:
            txt_file.write(file_path+"\n")

class ActionRunVNXEnvironment(Action):
    def name(self) -> Text:
        return "run_script_path"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            result=self.start_vnx_pipeline()
            if isinstance (result,tuple):
                num_returns=len(result)
                if num_returns==3:
                    dispatcher.utter_message(f"Script opened on vnx as: {self.check_last_line_historic()} Results and details can be seen on the server. ")
                    print(result[0],result[1],result[2])
                else:
                    dispatcher.utter_message(f"Script opened on vnx as: {self.check_last_line_historic()} Results and details can be seen on the server. ")
                    dispatcher.utter_message(f"Script closed on vnx as: {self.check_second_to_last_line_historic()} Results and details can be seen on the server.")
                    print(result[0],result[1],result[2],result[3],result[4],result[5])

            return []
    
    def start_vnx_pipeline(self):
        last_run=self.check_second_to_last_line_historic()
        to_be_run=self.check_last_line_historic()
        file_lines=self.check_amount_lines()
        stdout,stderr,return_code,stop_stdout,stop_stderr,stop_returncode='','','','','',''
        if(file_lines>=2):
            stop_stdout,stop_stderr,stop_returncode=self.stop_vnx_script(last_run)
            stdout,stderr,return_code=self.run_vnx_script(to_be_run)
            return stdout,stderr,return_code,stop_stdout,stop_stderr,stop_returncode
        else:
            stdout,stderr,return_code=self.run_vnx_script(to_be_run)
            return stdout,stderr,return_code


    def run_vnx_script(self,script_path):
        try:
            # Build the command to run the Perl script
            command = ['sudo', 'vnx', '-f', script_path, '--create']
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr = process.communicate()
            # Check the return code
            return_code = process.returncode

            # Return the standard output, standard error, and return code
            return stdout, stderr, return_code
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1
        
    def stop_vnx_script(self,script_path):
        try:
            # Build the command to run the Perl script
            command = ['sudo', 'vnx', '-f', script_path, '--destroy']
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr = process.communicate()
            # Check the return code
            return_code = process.returncode

            # Return the standard output, standard error, and return code
            return stdout, stderr, return_code
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1
        
    def check_last_line_historic(self):
        with open("historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            last_line = lines[-1]
            return last_line.strip()
        
    def check_second_to_last_line_historic(self):
        with open("historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            last_line = lines[-2]
            return last_line.strip()
        
    def check_amount_lines(self):
        with open("historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            return len(lines)
        
class ActionConnectTwoComputers(Action):
    ip_address_dict = {}
    def name(self) -> Text:
        return "connect_two_computers_action"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            self.connect_computers()
            self.write_file_path_to_historic()
            dispatcher.utter_message(f"Script written to: user_gen_files/2_pcs_lan_connection.xml. Description: A simple LAN connection using a virtual bridge between two PCS. MAC addresses and IP address are generated automatically. Machine IPS info : {self.ip_address_dict})")
            return []
    def connect_computers(self):
        xml_content=''
        with open("xml_files/2_pcs_lan_connection.xml", "r", encoding="utf-8") as txt_file:
            xml_content=txt_file.read()
        with open("user_gen_files/2_pcs_lan_connection.xml", "w", encoding="utf-8") as xml_file:
            xml_file.write(xml_content)

    def write_file_path_to_historic(self):
        with open("historic_scripts/history.txt", "a") as txt_file:
            txt_file.write("user_gen_files/2_pcs_lan_connection.xml"+"\n")

class ActionConnectComputerWithLan(Action):
    ip_address_dict = {}
    def name(self) -> Text:
        return "provide_lan_config"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_number_lan = next(tracker.get_latest_entity_values("lan_user"), None)
        if user_number_lan:
            user_number_lan_count=int(user_number_lan)
            if(user_number_lan_count>0):
                file_path=f"user_gen_files/custom_lan_{user_number_lan_count}_users.xml"
                description=f"""The scenario consists of a variable number of {user_number_lan_count} LXC-based virtual machines connected to a network bridge, making it seem as a LAN network """
                dispatcher.utter_message(f"Scenario created as XML file generated and saved as custom_lan_{user_number_lan_count}_users.xml. Description: {description}. IPS: {self.ip_address_dict}")
                self.generate_xml(user_number_lan_count,file_path)
                self.write_file_path_to_historic(file_path)
            else:
                dispatcher.utter_message("User number not valid, file could not be created.")

        else:
            dispatcher.utter_message("User number not valid, file could not be created.")
        return []

    def write_file_path_to_historic(self,file_path):
        with open("historic_scripts/history.txt", "a", encoding="utf-8") as txt_file:
            txt_file.write(file_path+"\n")

    def generate_xml(self, num_vms, file_path):
            self.ip_address_dict.clear()
            root = ET.Element("vnx", attrib={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                            "xsi:noNamespaceSchemaLocation": "/usr/share/xml/vnx/vnx-2.00.xsd"})

            global_elem = ET.SubElement(root, "global")
            ET.SubElement(global_elem, "version").text = "2.0"
            ET.SubElement(global_elem, "scenario_name").text = f"{num_vms}_pcs_lan_connection"
            ET.SubElement(global_elem, "automac")
            vm_mgmt = ET.SubElement(global_elem, "vm_mgmt", attrib={"type": "none"})
            vm_defaults = ET.SubElement(global_elem, "vm_defaults")
            console_0 = ET.SubElement(vm_defaults, "console", attrib={"display": "no", "id": "0"})
            console_1 = ET.SubElement(vm_defaults, "console", attrib={"display": "yes", "id": "1"})

            net_elem = ET.SubElement(root, "net", attrib={"name": "Network1", "mode": "virtual_bridge", "type": "lan"})

            for i in range(1, num_vms + 1):
                vm_elem = ET.SubElement(root, "vm", attrib={"name": f"VM{i}", "type":"lxc","arch":"x86_64"})
                ET.SubElement(vm_elem, "filesystem", attrib={"type": "cow"}).text = "/usr/share/vnx/filesystems/rootfs_lxc_ubuntu64"
                if_elem = ET.SubElement(vm_elem, "if", attrib={"id": "1", "net": "Network1"})
                ET.SubElement(if_elem, "mac").text = f"fe:fd:00:00:00:{i:02d}"
                ET.SubElement(if_elem, "ipv4").text = f"192.168.1.{i}/24"
                self.ip_address_dict[f"VM{i}"] = f"192.168.1.{i}"

            tree = ET.ElementTree(root)

            # Use minidom to prettify the XML
            xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

            with open(file_path, "w", encoding="UTF-8") as f:
                f.write(xmlstr)
        
class ActionShowScenarioStatus(Action):
    def name(self) -> Text:
        return "provide_scenario_status"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            result=self.show_status()
            dispatcher.utter_message(f"Status of the scenario: {result[0]}. Possible errors: {result[1]}. Return code: {result[2]}")
            
            return []
    def show_status(self):
        try:
            last_line=self.last_run_script()
            command = ['sudo', 'vnx', '-f', last_line, '--show-status']
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr = process.communicate()
            # Check the return code
            return_code = process.returncode
            # Return the standard output, standard error, and return code
            return stdout, stderr, return_code
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1
    def last_run_script(self):
        with open("historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            last_line = lines[-1]
            return last_line.strip()

class ActionShowNetworkDiagram(Action):
    def name(self) -> Text:
        return "provide_network_diagram"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            result=self.show_network_diagram()
            dispatcher.utter_message(f"Network diagram: {result[0]}. Return code: {result[1]}")
            return []
    def show_network_diagram(self):
        try:
            last_line=self.last_run_script()
            command = ['sudo', 'vnx', '-f', last_line, '-v --show-map']
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr = process.communicate()
            # Check the return code
            return_code = process.returncode
            # Return the standard output, standard error, and return code
            return stdout, return_code
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1
    def last_run_script(self):
        with open("historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            last_line = lines[-1]
            return last_line.strip()
        
class ActionStopAll(Action):
    def name(self) -> Text:
        return "stop_all_scenarios"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            result=self.stop_all()
            dispatcher.utter_message(f"Stop all: {result[0]}. Return code: {result[1]}. Possible errors: {result[2]}  ")
            return []
    def stop_all(self):
        try:
            last_line=self.get_last_run_script()
            command = ['sudo', 'vnx','-f',last_line,'--destroy']
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr = process.communicate()
            # Check the return code
            return_code = process.returncode
            # Return the standard output, standard error, and return code
            return stdout, return_code, stderr
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1
    def get_last_run_script(self):
        with open("historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            last_line = lines[-1]
            return last_line.strip()
        
class ActionValidateXML(Action):
    def name(self) -> Text:
        return "validate_xml"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            xml_path=next(tracker.get_latest_entity_values("xml_path"), None)
            xml_path='validation_files/'+xml_path+'.xml'
            if(self.validate_path(xml_path)):
                result=self.validate_xml(xml_path)
                dispatcher.utter_message(result)
            else:
                dispatcher.utter_message(f"The file does not exist or does not have the valid extension.")
            return []
    def validate_xml(self,xml_path):
        message_to_return=""
        try:
            xsd_file_path="xsd_files/vnx-2.00.xsd"
            xml_tree=etree.parse(xml_path)
            # Load XSD file
            xsd_schema = etree.XMLSchema(etree.parse(xsd_file_path))
            xsd_schema.assertValid(xml_tree)
            message_to_return+="XML is valid according to the XSD."
        except Exception as e:
            message_to_return+="XML is invalid according to the XSD."
            for error in e.error_log:
                message_to_return+=f"Type: {error.type}, Domain: {error.domain}, Line: {error.line}, Message: {error.message}"
        return message_to_return

    def validate_path(self,path):
        return os.path.exists(path)


        






       

        

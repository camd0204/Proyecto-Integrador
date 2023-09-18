# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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


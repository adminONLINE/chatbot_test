from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random

class ActionProvideRecommendation(Action):
    def name(self) -> Text:
        return "action_provide_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        energy_usage = tracker.get_slot("energy_usage")

        if not energy_usage:
            dispatcher.utter_message(
                text="I'd be happy to provide a personalized recommendation! Could you tell me your average monthly energy usage in kWh?"
            )
            return []

        # Calculate system size (rough estimate: 5 kWh per day = 1.5 kW system)
        daily_usage = energy_usage / 30
        system_size = round(daily_usage / 5 * 1.5, 1)

        # Calculate price (rough estimate: $3/watt after tax credits)
        system_watts = system_size * 1000
        price = round(system_watts * 3 / 1000, 0)

        # Calculate bill reduction percentage
        bill_reduction = min(95, max(70, int(system_size * 8)))

        dispatcher.utter_message(
            text=f"Based on your location ({location}) and energy usage ({energy_usage} kWh/month), I recommend a {system_size}kW solar panel system. This would cost approximately ${price:,.0f} after tax credits and eliminate about {bill_reduction}% of your electricity bill! The system would pay for itself in about 7-8 years through energy savings."
        )

        dispatcher.utter_message(
            text="Would you like to know more about financing options or the installation process?"
        )

        return []

class ActionCalculateSystemSize(Action):
    def name(self) -> Text:
        return "action_calculate_system_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        energy_usage = tracker.get_slot("energy_usage")

        if not energy_usage:
            dispatcher.utter_message(
                text="To calculate the right system size, I need to know your monthly energy usage in kWh."
            )
            return []

        # Simple calculation for system sizing
        daily_usage = energy_usage / 30
        required_system_size = round(daily_usage / 5 * 1.2, 1)  # 20% buffer

        number_of_panels = int(required_system_size * 1000 / 400)  # Assuming 400W panels

        dispatcher.utter_message(
            text=f"For your {energy_usage} kWh monthly usage, you'd need approximately {required_system_size}kW system with {number_of_panels} solar panels. This would generate enough electricity to cover most of your energy needs."
        )

        return []

class ActionProvideLocationInfo(Action):
    def name(self) -> Text:
        return "action_provide_location_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")

        if not location:
            dispatcher.utter_message(
                text="Solar energy is available across the country! The best locations get 5-7 peak sun hours per day. Where are you located?"
            )
            return []

        # Provide location-specific information
        location_benefits = {
            "california": "California has excellent solar potential with 5-7 peak sun hours daily, plus great state incentives!",
            "texas": "Texas offers fantastic solar conditions with 5-6 peak sun hours and plenty of sunshine year-round!",
            "florida": "Florida is perfect for solar with 5-6 peak sun hours and excellent net metering policies!",
            "arizona": "Arizona has some of the best solar conditions in the US with 6-7 peak sun hours daily!",
            "new york": "New York offers good solar potential with strong state incentives and net metering programs!"
        }

        location_lower = location.lower()
        message = location_benefits.get(location_lower, f"{location} has good solar potential! Most areas receive 4-6 peak sun hours per day, making solar an excellent investment.")

        dispatcher.utter_message(text=message)

        return []

class ActionAskForContact(Action):
    def name(self) -> Text:
        return "action_ask_for_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent'].get('name')

        if intent == 'request_selling':
            dispatcher.utter_message(
                text="Great! I can connect you with one of our solar specialists who can provide a detailed quote and answer all your questions. Could you please provide your name and phone number, or would you prefer we email you?"
            )

        return []
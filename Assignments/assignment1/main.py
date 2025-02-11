from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
import xmltodict
import httpx


def get_enabled_events(graph_id: str, sim_id: str, auth: (str, str)):
        
        next_activities_response = httpx.get(
            "https://repository.dcrgraphs.net/api/graphs/" + graph_id +
            "/sims/" + sim_id + "/events?filter=only-enabled",
            auth=auth)

        events_xml = next_activities_response.text
        events_xml_no_quotes = events_xml[1:len(events_xml)-1]
        events_xml_clean = events_xml_no_quotes.replace('\\\"', "\"")
        events_json = xmltodict.parse(events_xml_clean)
        return events_json



def create_buttons_of_enabled_events(
    graph_id: str,
    sim_id: str,
    auth: (str, str),
    button_layout: BoxLayout):
    events_json = get_enabled_events(graph_id, sim_id,auth)
    # cleanup of previous widgets
    button_layout.clear_widgets()
    
    events = []
    # distinguish between one and multiple events
    if not isinstance(events_json['events']['event'], list):
        events = [events_json['events']['event']]
    else:
        events = events_json['events']['event']
    # add a custom button, that stores the event id
    for e in events:
        if e['@executed'] == 'false':
            s = SimulationButton(
                #the actual event id
                e['@id'],
                graph_id,
                sim_id,
                auth[0],
                auth[1],
                #the label of the event
                e['@label']
            )
            s.manipulate_box_layout = button_layout
            if e.get('@pending') == 'true':
                s.color = get_color_from_hex("#FFFF00")  # Set text color to yellow for pending events

            #add a line of code that colors pending events
            #to distinguish them from non pending events
            button_layout.add_widget(s)


class SimulationButton(Button):
    def __init__(self, event_id: int,
                graph_id: str,
                simulation_id: str,
                username: str,
                password: str,
                text: str):
        Button.__init__(self)
        self.event_id = event_id
        self.text = text
        self.graph_id = graph_id
        self.simulation_id = simulation_id
        self.username = username
        self.password = password
        self.manipulate_box_layout: BoxLayout = BoxLayout()
        self.bind(on_press=self.execute_event)

    def execute_event(self, instance):
        url = f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims/{self.simulation_id}/events/{self.event_id}"
        auth = (self.username, self.password)

        # Send a POST request to the server with basic authentication
        response = httpx.post(url, auth=auth)

        if response.is_success:
            # Handle the success case (e.g., update UI, show a message)
            print("Event executed successfully!")
        else:
            # Handle the error case (e.g., show an error message)
            print(f"Failed to execute event. Status code: {response.status_code}, Reason: {response.reason_phrase}")

        # Optionally, create buttons for new enabled events (similar to what you did in start_sim)
        create_buttons_of_enabled_events(self.graph_id, self.simulation_id, auth, self.manipulate_box_layout)
    

class MainApp(App):
    def __init__(self):
        App.__init__(self)
        self.password = TextInput(hint_text="Enter password", password=True)
        self.username = TextInput(hint_text="Enter username")
        self.layout_box = BoxLayout(orientation='vertical')
        self.graph_id = TextInput(hint_text="Enter graph id")
        self.runSim = Button(text="Create New Instance")
        self.passwordLabel = Label(text="Password")
        self.usernameLabel = Label(text="Username")
        self.graph_idLabel = Label(text="Graph ID")

    def build(self):
        #b = Button(text="Create New Instance")
        self.b_outer = BoxLayout()
        self.b_upperLeft = BoxLayout()
        self.b_lowerLeft = BoxLayout()
        self.b_upperLeftLeft = BoxLayout(orientation='vertical')
        self.b_upperLeftRight = BoxLayout(orientation='vertical')
        self.b_right = BoxLayout(orientation='vertical')
        self.b_left = BoxLayout(orientation='vertical')
        self.b_lowerLeft.add_widget(self.runSim)
        self.b_upperLeftRight.add_widget(self.username)
        self.b_upperLeftRight.add_widget(self.password)
        self.b_upperLeftRight.add_widget(self.graph_id)
        self.b_upperLeftLeft.add_widget(self.usernameLabel)
        self.b_upperLeftLeft.add_widget(self.passwordLabel)
        self.b_upperLeftLeft.add_widget(self.graph_idLabel)
        self.b_upperLeft.add_widget(self.b_upperLeftLeft)
        self.b_upperLeft.add_widget(self.b_upperLeftRight)
        self.b_left.add_widget(self.b_upperLeft)
        self.b_left.add_widget(self.b_lowerLeft)
        self.b_outer.add_widget(self.b_left)
        self.b_outer.add_widget(self.b_right)
        self.runSim.bind(on_press=self.b_press)

        return self.b_outer


    def start_sim(self, instance):
        
        newsim_response = httpx.post(
            url=f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id.text}/sims",
            auth=(self.username.text, self.password.text))
        

        if not newsim_response.is_success:
            raise Exception(f"{newsim_response.status_code}{newsim_response.reason_phrase}\n{newsim_response.text}")
         
        self.simulation_id = newsim_response.headers['simulationID']

        create_buttons_of_enabled_events(self.graph_id.text, self.simulation_id, (self.username.text, self.password.text), self.b_right)
        

    def b_press(self, instance):
        self.start_sim(instance)


if __name__ == '__main__':
    mainApp = MainApp()
    MainApp().run()
    


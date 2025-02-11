from kivy.app import App
import httpx
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import json


class MyWordApp(App):

    def __init__(self):
        App.__init__(self)
        self.label = Label(text="Nothing yet.")
        self.textbox = TextInput(text="Enter your text here...")

    def build(self):
        b = BoxLayout(orientation='vertical', padding="10pt")
        b_inner = BoxLayout(orientation='horizontal', padding="15pt")
        # You need to add code here
        # You need to add code here
        b_inner.add_widget(self.textbox)
        # You need to add code here
        b.add_widget(b_inner)
        b.add_widget(self.label)
        return b

    def press(self, instance):
        self.look_up(self.textbox.text)

    def look_up(self, word: str):
        try:
            response = "{}"
            # You need to add code here
            text_to_json = json.loads(response)
            definitions = text_to_json[0]["meanings"][0]["definitions"][0]["definition"]
            self.label.text = definitions
        except Exception:
            self.label.text = "No meaningful definition found."


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyWordApp().run()

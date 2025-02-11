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
        self.button = Button(text="Click to search")
        self.textbox = TextInput(text="")

    def build(self):
        b = BoxLayout(orientation='vertical', padding="10pt")
        b_inner = BoxLayout(orientation='horizontal', padding="15pt")
        # You need to add code here
        # You need to add code here
        b_inner.add_widget(self.textbox)
        # You need to add code here
        b.add_widget(b_inner)
        b_inner.add_widget(self.button)
        b.add_widget(self.label)
        self.button.bind(on_press=self.press)
        return b

    def press(self, instance):
        self.look_up(self.textbox.text)

    def look_up(self, word: str):
        try:
            response = httpx.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
            text_to_json = json.loads(response.content)
            definitions = text_to_json[0]["meanings"][0]["definitions"][0]["definition"]
            self.label.text = definitions
        except Exception as e:
            print(e)
            self.label.text = "No meaningful definition found."


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyWordApp().run()

    

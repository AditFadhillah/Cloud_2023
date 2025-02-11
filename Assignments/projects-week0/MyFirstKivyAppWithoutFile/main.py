from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class TutorialApp(App):
    def build(self):
        layout = BoxLayout()
        button = Button(text='Hello!',
                      background_color=(0, 0, 1, 1),  # List of
                      # rgba components
                      font_size=150)
        layout.add_widget(button)
        return layout



if __name__ == "__main__":
    TutorialApp().run()

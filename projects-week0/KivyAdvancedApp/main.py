from kivy.app import App
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput


class TutorialApp(App):
    def build(self):
        b = BoxLayout(orientation='vertical')  # The default BoxLayout, no
        # extra properties set
        t = TextInput(text='Hello World',
                      font_size=150,
                      size_hint_y=None,
                      height=200)
        f = FloatLayout()
        s = Scatter()
        l = Label(text='Hello!',
                  font_size=150)
        f.add_widget(s)
        s.add_widget(l)
        b.add_widget(t)
        b.add_widget(f)

        t.bind(text=l.setter('text'))
        return b


if __name__ == "__main__":
    TutorialApp().run()

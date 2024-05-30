
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


DEFAULT_YEAR = 1933


def update_layout(widget, value):
    widget.rect.pos = widget.pos
    widget.rect.size = widget.size


class TechnologyButton(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"

        requirement_box = BoxLayout(size_hint=(0.1, 1))
        self.requirement_label = Label(text="")
        requirement_box.add_widget(self.requirement_label)

        self.technology = Button(text="Placeholder technology", size_hint=(0.8, 1))

        blueprint_box = BoxLayout(size_hint=(0.1, 1))
        self.blueprint_label = Label(text="")
        blueprint_box.add_widget(self.blueprint_label)

        self.add_widget(requirement_box)
        self.add_widget(self.technology)
        self.add_widget(blueprint_box)

        with requirement_box.canvas.before:
            Color(0, 0, 0, 0)
            requirement_box.rect = Rectangle(size=requirement_box.size, pos=requirement_box.pos)
        requirement_box.bind(pos=update_layout, size=update_layout)
        with blueprint_box.canvas.before:
            Color(0, 0, 0, 0)
            blueprint_box.rect = Rectangle(size=blueprint_box.size, pos=blueprint_box.pos)
        blueprint_box.bind(pos=update_layout, size=update_layout)


class UpperTeamScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text="UpperTeamScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))


class TeamComparisonTable(GridLayout):
    def row_color(self, row_num):
        if row_num % 2 == 0:
            return (0.2, 0.2, 0.2, 1)
        return (0.2, 0, 0.2, 1)
    
    def update_boxlayout(self, widget, value):
        widget.rect.pos = widget.pos
        widget.rect.size = widget.size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Team", size_hint=(0.5, 0.1)))
        self.add_widget(Label(text="Time to complete", size_hint=(0.5, 0.1)))
        self.table = [BoxLayout(size_hint=(0.5, 0.1)) for _ in range(20)]
        for i, layout in enumerate(self.table):
            self.add_widget(layout)
            with layout.canvas.before:
                Color(*self.row_color(i // 2))
                layout.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(pos=update_layout, size=update_layout)
        
        self.labels = []
        for i, layout in enumerate(self.table):
            if i % 2 == 0:
                cell = Label(text="...")
            else:
                cell = Label(text="?")
            self.labels.append(cell)
            layout.add_widget(cell)


class TeamScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(UpperTeamScreen(orientation="vertical", size_hint=(1, 0.5)))
        self.add_widget(TeamComparisonTable(cols=2, size_hint=(1, 0.5)))
        


class TechCategories(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        categories = [
            "Infantry",
            "Armor & Artillery",
            "Naval",
            "Aircraft",
            "Overview",
            "Industrial",
            "Land Doctrine",
            "Secret Weapons",
            "Naval Docrine",
            "Air Doctrine"
        ]
        category_buttons = [ToggleButton(text=category) for category in categories]
        for category_button in category_buttons:
            self.add_widget(category_button)


class TechInfoPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Technology name", size_hint=(1, 0.4)))
        self.add_widget(Label(text="Tech components go here", size_hint=(1, 0.4)))
        self.add_widget(Label(text="blueprint checkbox maybe", size_hint=(1, 0.2)))
    

class RequirementPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Requirements", size_hint=(1, 0.25)))
        self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        self.add_widget(Label(text="Deactivates", size_hint=(1, 0.25)))
        self.add_widget(Label(text="...", size_hint=(1, 0.25)))


class EffectsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Effects", size_hint=(1, None), height=dp(20)))
        for i in range(20):
            self.add_widget(Label(text=f"... {i+1}", size_hint=(1, None), height=dp(20)))
        # self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        # self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        # self.add_widget(Label(text="...", size_hint=(1, 0.25)))


class ResearchButtonsPanel(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.complete_button = Button(text="Complete Tech", size_hint=(0.4, 0.4))
        self.add_widget(self.complete_button)

        # empty
        # self.add_widget(Label(text=" "))
        
        self.undo_button = Button(text="Undo Tech", size_hint=(0.4, 0.4))
        self.add_widget(self.undo_button)

        self.force_complete_button = Button(text="Force Complete Tech", size_hint=(0.4, 0.4))
        self.add_widget(self.force_complete_button)

        # empty
        # self.add_widget(Label(text=" "))

        self.clear_button = Button(text="Clear everything", size_hint=(0.4, 0.4))
        self.add_widget(self.clear_button)

class MainTechScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text="MainTechScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))


class TechInfoPanels(BoxLayout):
    BACKGROUND_COLOR2 = (0.1, 0.1, 0.1, 1)

    def update_panel(self, widget, value):
        widget.rect.pos = widget.pos
        widget.rect.size = widget.size
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.techinfopanel = TechInfoPanel(orientation="vertical", size_hint=(0.25, 1))
        self.add_widget(self.techinfopanel)
        with self.techinfopanel.canvas.before:
            Color(*self.BACKGROUND_COLOR2)
            self.techinfopanel.rect = Rectangle(size=self.techinfopanel.size, pos=self.techinfopanel.pos)
        self.techinfopanel.bind(pos=self.update_panel, size=self.update_panel)

        self.requirement_scrollview = ScrollView(size_hint=(0.25, None))
        self.requirement_panel = RequirementPanel(orientation="vertical", size_hint=(1, None))
        # self.requirement_panel.height = self.requirement_panel.minimum_height + 50
        self.requirement_panel.bind(minimum_height=self.requirement_panel.setter("height"))
        self.requirement_scrollview.add_widget(self.requirement_panel)
        # self.add_widget(RequirementPanel(orientation="vertical", size_hint=(0.25, 1)))
        self.add_widget(self.requirement_scrollview)

        self.extra_layout = BoxLayout(size_hint=(0.25, 1))
        self.effects_scrollview = ScrollView(size_hint=(1, None))
        # self.effects_scrollview = ScrollView(size_hint=(0.25, None))
        self.effects_panel = EffectsPanel(orientation="vertical", size_hint=(1, None))
        # self.effects_panel.height = self.effects_panel.minimum_height + 50
        # self.effects_panel.height = 1000
        self.effects_panel.bind(minimum_height=self.effects_panel.setter("height"))
        # self.add_widget(EffectsPanel(orientation="vertical", size_hint=(0.25, 1)))
        self.effects_scrollview.add_widget(self.effects_panel)
        # self.add_widget(self.effects_scrollview)
        self.extra_layout.add_widget(self.effects_scrollview)
        self.add_widget(self.extra_layout)

        with self.extra_layout.canvas.before:
            Color(*self.BACKGROUND_COLOR2)
            self.extra_layout.rect = Rectangle(size=self.extra_layout.size, pos=self.extra_layout.pos)
        self.extra_layout.bind(pos=self.update_panel, size=self.update_panel)

        self.add_widget(ResearchButtonsPanel(cols=2, padding=(dp(5), dp(5), dp(5), dp(5)), spacing=dp(10), size_hint=(0.25, 1)))
        # for i in range(4):
        #     self.add_widget(Button(text=f"InfoPanel {i+1}", size_hint=(0.25, 1)))


class TechScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Button(text="TechScreen"))
        # padding=(dp(10), dp(10), dp(10), dp(10))
        self.techcategories = TechCategories(cols=5, size_hint=(1, 0.05))
        self.maintechscreen = MainTechScreen(size_hint=(1, 0.80))
        self.techinfopanel = TechInfoPanels(orientation="horizontal", size_hint=(1, 0.15))
        self.add_widget(self.techcategories)
        self.add_widget(self.maintechscreen)
        self.add_widget(self.techinfopanel)


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Button(text="MainScreen", size_hint=(1, 1)))
        self.techscreen = TechScreen(orientation="vertical", size_hint=(0.8, 1))
        self.teamscreen = TeamScreen(orientation="vertical", size_hint=(0.2, 1))
        self.add_widget(self.teamscreen)
        self.add_widget(self.techscreen)


class StatusBar(BoxLayout):
    def on_checkbox_active_placeholder(self, checkbox, value):
        if value:
            print(f"Values are locked by checkbox {checkbox}")
        else:
            print(f"Values are not locked by checkbox {checkbox}")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.value_lock_checkbox = CheckBox(size_hint=(0.04, 1))
        self.value_lock_checkbox.bind(active=self.on_checkbox_active_placeholder)

        self.add_widget(Label(text="Country/Countries", size_hint=(0.15, 1)))
        self.country_input = TextInput(size_hint=(0.1, 1))
        self.add_widget(self.country_input)
        self.country_selected_text = Label(text="", size_hint=(0.2, 1))
        self.add_widget(self.country_selected_text)
        self.add_widget(Label(text="", size_hint=(0.2, 1)))

        self.add_widget(Label(text="Year", size_hint=(0.05, 1)))
        self.year_input = TextInput(text=str(DEFAULT_YEAR), size_hint=(0.05, 1))
        self.add_widget(self.year_input)

        self.add_widget(Label(text="Research Speed", size_hint=(0.1, 1)))
        self.research_speed_input = TextInput(size_hint=(0.05, 1))
        self.add_widget(self.research_speed_input)

        self.add_widget(Label(text="Lock values", size_hint=(0.1, 1)))
        self.add_widget(self.value_lock_checkbox)


class MainFullScreen(BoxLayout):
    statusbar_BACKGROUND_COLOR = (0, 0.3, 0.1, 0.7)

    def update_statusbar(self, widget, value):
        widget.rect.pos = widget.pos
        widget.rect.size = widget.size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mainscreen = MainScreen(orientation="horizontal", size_hint=(1, 0.96))
        self.statusbar = StatusBar(orientation="horizontal", size_hint=(1, 0.04))
        
        self.add_widget(self.mainscreen)
        self.add_widget(self.statusbar)

        with self.statusbar.canvas.before:
            Color(*self.statusbar_BACKGROUND_COLOR)
            self.statusbar.rect = Rectangle(size=self.statusbar.size, pos=self.statusbar.pos)
        self.statusbar.bind(pos=self.update_statusbar, size=self.update_statusbar)


# class MainWidget(Widget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.add_widget(MainFullScreen(orientation="vertical", size=(1920, 1000)))



class HoITech(App):
    def build(self):
        # return MainWidget(width=1920, height=1000)
        # return MainFullScreen(orientation="vertical", size=(1920, 1000))
        return MainFullScreen(orientation="vertical", size=Window.size)


if __name__ == '__main__':
    HoITech().run()

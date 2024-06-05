
from kivy.app import App
from kivy.core.window import Window
# from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from research import Research
from scan_hoi_files import get_country_names



DIFFICULTY_DICT = {
    "Very Easy": -2,
    "Easy": -1,
    "Normal": 0,
    "Hard": 1,
    "Very Hard": 2
}


def suggest_countries(input_text, country_names, max_num_of_suggestions):
    # suggestions = []
    matches = []
    others = []
    search_text = input_text.lower()
    for country_code, country_name in country_names.items():
        code = country_code.lower()
        name = country_name.lower()
        if code == search_text or name == search_text:
            matches.insert(0, f"{country_code} {country_name}")
        elif (search_text in code or search_text in name) and len(others) < max_num_of_suggestions:
            others.append(f"{country_code} {country_name}")
    suggestions = matches + others
    if len(suggestions) <= max_num_of_suggestions:
        return suggestions
    return suggestions[:max_num_of_suggestions]


def test_printer(*args):
    for arg in args:
        print(arg)


def update_layout(widget, value):
    widget.rect.pos = widget.pos
    widget.rect.size = widget.size


class CountryButton(BoxLayout):
    def __init__(self, country_code, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        self.country_label = Label(text=country_code, size_hint=(0.8, 1))
        self.remove_button = Button(text="X", size_hint=(0.2, 1))

        self.add_widget(self.country_label)
        self.add_widget(self.remove_button)


class TechnologyButton(BoxLayout):
    SIZE_HINT = (0.175, 0.04)
    # COLORS

    def __init__(self, tech_short_name, has_blueprint=False, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"

        requirement_box = BoxLayout(size_hint=(0.1, 1))
        self.requirement_label = Label(text="")
        requirement_box.add_widget(self.requirement_label)

        self.technology = Button(text=tech_short_name, size_hint=(0.8, 1), background_color=(0, 0.8, 0.2, 0.7))

        blueprint_box = BoxLayout(size_hint=(0.1, 1))
        self.blueprint_label = Label(text="", color=(0, 0, 1, 1))
        if has_blueprint:
            self.blueprint_label.text = "B"
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
        self.add_widget(Label(text="UpperTeamScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))


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
        # category_buttons = [ToggleButton(text=category) for category in categories]
        category_buttons = [Button(text=category) for category in categories]
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


class MainTechScreen(FloatLayout):
    def __init__(self, **kwargs):
        self.TECHNOLOGYBUTTON_SIZE = (0.175, 0.04)
        super().__init__(**kwargs)
        self.add_widget(Label(text="MainTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))

        self.add_widget(TechnologyButton("Prioritize Infantry", has_blueprint=True, size_hint=self.TECHNOLOGYBUTTON_SIZE, pos_hint={"x": 0.05, "y": 0.05}))
        self.add_widget(TechnologyButton("Prioritize Quality", size_hint=self.TECHNOLOGYBUTTON_SIZE, pos_hint={"x": 0.05, "y": 0.1}))
        self.add_widget(TechnologyButton("Int./Fighter Prototypes", size_hint=self.TECHNOLOGYBUTTON_SIZE, pos_hint={"x": 0.05, "y": 0.15}))


class MainTechScreen_BoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Label(text="MainTechScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(MainTechScreen())


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
        self.maintechscreen = MainTechScreen_BoxLayout(size_hint=(1, 0.80))
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
    def select_year(self, widget, value):
        # setattr(self.difficulty_button, "text", value)
        self.difficulty_button.text = value
        # self.year_selection_dropdown.close()

    
    def add_country(self, country_code):
        if country_code in self.country_buttons.keys():
            return
        self.country_buttons[country_code] = CountryButton(country_code)
        self.countries_selected.add_widget(self.country_buttons[country_code])
        self.country_buttons[country_code].remove_button.bind(on_release=lambda *args: self.remove_country(country_code))
        # print(f"{self.parent=}")
        self.parent.add_country(country_code)
    
    def remove_country(self, country_code):
        self.countries_selected.remove_widget(self.country_buttons[country_code])
        del self.country_buttons[country_code]
        self.parent.remove_country(country_code)


    def on_checkbox_active_placeholder(self, checkbox, value):
        if value:
            print(f"Values are locked by checkbox {checkbox}")
        else:
            print(f"Values are not locked by checkbox {checkbox}")
    

    def select_country(self, widget, value):
        if value:
            self.country_selection_dropdown.select(widget.text)
    
    def suggest_country_names(self, widget, value):
        if not self.country_input.focus:
            # print("not focused on", self.country_input)
            return
        self.country_selection_dropdown.clear_widgets()

        suggestions = suggest_countries(value, self.country_names, self.max_num_of_country_suggestions)
        for i, suggestion in enumerate(suggestions):
            suggestion_thingy = TextInput(text=suggestion, readonly=True, multiline=False, write_tab=False, size_hint_y=None, height=dp(25))
            suggestion_thingy.bind(focus=self.select_country)
            self.country_selection_dropdown.add_widget(suggestion_thingy)
        
        if self.country_selection_dropdown.parent is None and self.country_input.get_parent_window() is not None:
            self.country_selection_dropdown.open(self.country_input)

    def make_country_selection(self, widget, value):
        self.country_input.text = ""
        country_code = value[:3]
        self.add_country(country_code)

    def open_year_selection_dropdown(self, widget, text):
        if not widget.focus:
            return
        
        # print("self.year_selection_dropdown.parent is None:", self.year_selection_dropdown.parent is None)
        # print("self.get_parent_window() is not None:", self.get_parent_window() is not None)
        if self.year_selection_dropdown.parent is None and self.get_parent_window() is not None:
            self.year_selection_dropdown.open(widget)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.country_names = get_country_names()
        self.years = list(range(1933, 1953))

        # country selection
        self.add_widget(Label(text="Country/Countries", size_hint=(0.12, 1)))
        self.country_selection_dropdown = DropDown()
        self.country_input = TextInput(size_hint=(0.13, 1))
        self.add_widget(self.country_input)

        self.max_num_of_country_suggestions = 10

        self.country_selection_dropdown.bind(on_select=self.make_country_selection)
        self.country_input.bind(text=self.suggest_country_names)

        # self.country_selected_text = Label(text="", size_hint=(0.1, 1))
        self.countries_selected = BoxLayout(orientation="horizontal", size_hint=(0.1, 1))
        self.country_buttons = dict()
        self.add_widget(self.countries_selected)

        self.add_widget(Label(text="", size_hint=(0.2, 1)))

        # difficulty selection
        self.difficulty_suggestions = list(DIFFICULTY_DICT.keys())

        self.difficulty_dropdown = DropDown()
        for diff in self.difficulty_suggestions:
            btn = Button(text=diff, size_hint=(1, None), height=dp(20))
            btn.bind(on_release=lambda b: self.difficulty_dropdown.select(b.text))
            self.difficulty_dropdown.add_widget(btn)

        self.add_widget(Label(text="Difficulty", size_hint=(0.05, 1)))
        self.difficulty_button = Button(text="Normal", size_hint=(0.05, 1))
        self.difficulty_button.bind(on_release=self.difficulty_dropdown.open)
        # self.difficulty_dropdown.bind(on_select=lambda instance, value: setattr(self.difficulty_button, "text", value))
        self.difficulty_dropdown.bind(on_select=self.select_year)

        self.add_widget(self.difficulty_button)

        # year selection
        self.add_widget(Label(text="Year", size_hint=(0.05, 1)))
        self.year_selection_dropdown = DropDown()
        for year in self.years:
            # label = Label(text=str(year), size_hint=(1, None), height=dp(20))
            label = TextInput(text=str(year), readonly=True, multiline=False, write_tab=False, size_hint_y=None, height=dp(25))
            label.bind(focus=lambda w, v: self.year_selection_dropdown.select(w.text))
            # label.bind(focus=test_printer)
            self.year_selection_dropdown.add_widget(label)
        self.year_input = TextInput(text="this should not be visible", size_hint=(0.05, 1))
        # self.year_input.bind(text=lambda w, v: self.year_selection_dropdown.open(w))
        self.year_input.bind(focus=self.open_year_selection_dropdown)
        self.year_selection_dropdown.bind(on_select=lambda instance, value: setattr(self.year_input, "text", value))
        self.add_widget(self.year_input)

        # research speed selection
        self.add_widget(Label(text="Research Speed", size_hint=(0.1, 1)))
        self.research_speed_input = TextInput(size_hint=(0.05, 1))
        self.add_widget(self.research_speed_input)

        # lock values checkbox
        self.add_widget(Label(text="Lock values", size_hint=(0.1, 1)))
        self.value_lock_checkbox = CheckBox(size_hint=(0.04, 1))
        self.value_lock_checkbox.bind(active=self.on_checkbox_active_placeholder)
        self.add_widget(self.value_lock_checkbox)


class MainFullScreen(BoxLayout):
    statusbar_BACKGROUND_COLOR = (0, 0.3, 0.1, 0.7)

    def update_statusbar(self):
        self.statusbar.research_speed_input.text = str(self.research.research_speed)

    def set_year(self, year):
        self.research.year = year
        self.statusbar.year_input.text = str(self.research.year)
    
    # in case of not knowing what to do
    def reset_year(self):
        self.set_year(self.research.DEFAULT_YEAR)
    

    def set_research_speed(self, research_speed):
        self.research.research_speed = research_speed
        self.statusbar.research_speed_input.text = str(self.research.research_speed)
    
    # just in case
    def reset_research_speed(self):
        self.set_research_speed(self.research.DEFAULT_RESEARCH_SPEED)


    def add_country(self, country_code):
        self.research.add_country(country_code)
        # self.statusbar.add_country(country_code)
        self.update_statusbar()

    def remove_country(self, country_code):
        self.research.remove_country(country_code)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.research = Research()

        self.mainscreen = MainScreen(orientation="horizontal", size_hint=(1, 0.96))
        self.statusbar = StatusBar(orientation="horizontal", size_hint=(1, 0.04))

        self.statusbar.year_input.text = str(self.research.year)
        self.statusbar.research_speed_input.text = str(self.research.research_speed)
        
        self.add_widget(self.mainscreen)
        self.add_widget(self.statusbar)

        with self.statusbar.canvas.before:
            Color(*self.statusbar_BACKGROUND_COLOR)
            self.statusbar.rect = Rectangle(size=self.statusbar.size, pos=self.statusbar.pos)
        self.statusbar.bind(pos=update_layout, size=update_layout)


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

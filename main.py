
from pathlib import Path

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
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp

from research import Research
from read_hoi_files import get_country_names
from arrows import get_arrow_points, scale_arrows
from tech_positions import tech_positions
from component_types import component_types
import lines


DIFFICULTIES = (
    ("Very Easy", "VERYEASY"),
    ("Easy", "EASY"),
    ("Normal", "NORMAL"),
    ("Hard", "HARD"),
    ("Very Hard", "VERYHARD")
)

TECH_CATEGORIES = (
            ("infantry", "Infantry"),
            ("armor", "Armor & Artillery"),
            ("naval", "Naval"),
            ("aircraft", "Aircraft"),
            (None, "Post-War"),
            ("industry", "Industrial"),
            ("land_doctrines", "Land Doctrine"),
            ("secret_weapons", "Secret Weapons"),
            ("naval_doctrines", "Naval Docrine"),
            ("air_doctrines", "Air Doctrine")
)


def get_the_other_difficulty(difficulty):
    for d1, d2 in DIFFICULTIES:
        if d1 == difficulty:
            return d2
        if d2 == difficulty:
            return d1

def get_the_other_category(category):
    for c1, c2 in TECH_CATEGORIES:
        if c2 == category:
            return c1
        if c1 == category:
            return c2


the_research = Research()


def suggest_countries(input_text, country_names, max_num_of_suggestions):
    # suggestions = []
    matches = []
    starts = []
    others = []
    search_text = input_text.lower()
    for country_code, country_name in country_names.items():
        code = country_code.lower()
        name = country_name.lower()
        if code == search_text or name == search_text:
            matches.append(f"[{country_code}] {country_name}")
        elif code.startswith(search_text) or name.startswith(search_text):
            starts.append(f"[{country_code}] {country_name}")
        elif (search_text in code or search_text in name) and len(others) < max_num_of_suggestions:
            others.append(f"[{country_code}] {country_name}")
    suggestions = matches + starts + others
    # if len(suggestions) <= max_num_of_suggestions:
    #     return suggestions
    return suggestions[:max_num_of_suggestions]


def suggest_tech_teams(input_text, tech_teams, max_num_of_suggestions):
    matches = []
    starts = []
    others = []
    search_text = input_text.lower()
    for team in tech_teams:
        name = team.name.lower()
        if search_text == name:
            matches.append(team.format_name_and_country())
        elif name.startswith(search_text):
            starts.append(team.format_name_and_country())
        elif search_text in name and len(others) < max_num_of_suggestions:
            others.append(team.format_name_and_country())

    suggestions = matches + starts + others
    return suggestions[:max_num_of_suggestions]


def test_printer(*args):
    for arg in args:
        print(f"{arg=}")


def update_layout(widget, value):
    widget.rect.pos = widget.pos
    widget.rect.size = widget.size


class CountryButton(BoxLayout):
    def __init__(self, country_code, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        # country_label_box = BoxLayout(size_hint=(0.8, 1))
        self.country_label = Label(text=country_code, size_hint=(0.8, 1))
        self.country_label = Label(text=country_code)
        self.remove_button = Button(text="X", size_hint=(0.2, 1))

        with self.country_label.canvas.before:
            Color(*bg_color)
            self.country_label.rect = Rectangle(size=self.country_label.size, pos=self.country_label.pos)
        self.country_label.bind(pos=update_layout, size=update_layout)

        # country_label_box.add_widget(self.country_label)
        self.add_widget(self.country_label)
        # self.add_widget(country_label_box)
        self.add_widget(self.remove_button)


class MinisterCheckBox(BoxLayout):
    def on_checkbox_active(self, checkbox, value):
        if value:
            self.parent.choose_minister_or_idea(self.name.text)
            # print(value)
            # print(self.name.text, "is selected")
        # else:
            # print(value)
            # print(self.name.text, "is not selected")

    def __init__(self, label_text, group_name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        self.name = Label(text=label_text, size_hint=(0.8, 1))
        self.checkbox = CheckBox(group=group_name, size_hint=(0.2, 1))
        self.checkbox.bind(active=self.on_checkbox_active)

        self.add_widget(self.checkbox)
        self.add_widget(self.name)


class MinisterCheckBoxGroup(BoxLayout):
    def choose_minister_or_idea(self, name):
        if self.parent is None or self.parent.parent is None:
            return
        self.parent.parent.parent.choose_minister_or_idea(self.title.text, name)
        # print(self.title.text, name)
        # print(self.parent)
        # print(self.parent.parent)
        # print(self.parent.parent.parent)
        # print(self.parent.parent.parent.parent.attach_to)
        # print(self.parent.parent.parent.parent.parent)
    
    def change_minister(self, minister_personality_str):
        for checkbox in self.list_of_checkboxes:
            checkbox.checkbox.active = False
        if not minister_personality_str:
            self.list_of_checkboxes[-1].checkbox.active = True
            return
        for checkbox in self.list_of_checkboxes:
            if checkbox.name.text.lower() == minister_personality_str.lower():
                checkbox.checkbox.active = True
                return
        else:
            self.list_of_checkboxes[-1].checkbox.active = True
        
    def change_research_effects(self, effect_dict):
        for effect_label in self.effects:
            effect_label.text = ""
        if not effect_dict:
            return
        for effect_label, effect_type in zip(self.effects[:len(effect_dict)], effect_dict.keys()):
            effect_label.text = f"{effect_type}: +{-100 * effect_dict[effect_type]}"
    
    def __init__(self, group_name, list_of_labels, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.title = Label(text=group_name)
        self.add_widget(self.title)

        self.list_of_checkboxes = []
        for label in list_of_labels:
            checkbox = MinisterCheckBox(label, group_name)
            self.list_of_checkboxes.append(checkbox)
            self.add_widget(checkbox)
        self.list_of_checkboxes[-1].checkbox.active = True

        self.effects = [Label(text=""), Label(text="")]
        for effect in self.effects:
            self.add_widget(effect)


class TechnologyButton(BoxLayout):
    SIZE_HINT = (0.15, 0.035)
    
    # COLORS
    DEFAULT_COLOR = (0.4, 0.4, 0.4, 1)
    RANDOM_COLOR = (0.4, 0.8, 0.2, 0.7)
    COMPLETED_COLOR = (0.2, 0.7, 0.3, 1)
    ACTIVE_COLOR = (0.6, 1, 0.1, 1)
    DEACTIVATE_COLOR = (1, 0.1, 0.1, 1)

    def add_blueprint(self):
        self.blueprint_label.text = "B"
    
    def remove_blueprint(self):
        self.blueprint_label.text = ""

    def show_as_requirement(self):
        self.requirement_label.text = "R"
    
    def hide_requirement(self):
        self.requirement_label.text = ""

    def show_as_allowed_by(self):
        self.requirement_label.text = "A"
    
    def hide_is_required_in(self):
        self.requirement_label.text = ""

    def show_deactivation_warning(self):
        self.deactivation_label.text = "D"
    
    def hide_deactivation_warning(self):
        self.deactivation_label.text = ""

    def reset_color(self):
        self.technology.background_color = self.DEFAULT_COLOR
    
    def complete(self):
        self.technology.background_color = self.COMPLETED_COLOR
    
    def activate(self):
        self.technology.background_color = self.ACTIVE_COLOR
    
    def deactivate(self):
        self.technology.background_color = self.DEACTIVATE_COLOR
    
    def update_status(self, research_object):
        if self.tech_id in research_object.blueprints:
            self.add_blueprint()
        else:
            self.remove_blueprint()
        if self.tech_id in research_object.completed_techs:
            self.complete()
            return
        if self.tech_id in research_object.active_techs:
            self.activate()
            return
        if self.tech_id in research_object.deactivated_techs:
            self.deactivate()
            return
        self.reset_color()

    def __init__(self, tech_short_name, tech_id, has_blueprint=False, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"

        self.size_hint = self.SIZE_HINT

        self.tech_id = tech_id

        requirement_box = BoxLayout(size_hint=(0.05, 1))
        self.requirement_label = Label(text="", color=(1, 1, 0, 1))
        requirement_box.add_widget(self.requirement_label)

        self.technology = Button(text=tech_short_name, size_hint=(0.85, 1), background_color=self.DEFAULT_COLOR)

        blueprint_box = BoxLayout(size_hint=(0.04, 1))
        self.blueprint_label = Label(text="", color=(0, 0, 1, 1))
        if has_blueprint:
            self.blueprint_label.text = "B"
        blueprint_box.add_widget(self.blueprint_label)

        self.deactivation_label = Label(text="", size_hint=(0.06, 1), color=(1, 0, 0, 1))

        self.add_widget(requirement_box)
        self.add_widget(self.technology)
        self.add_widget(blueprint_box)
        self.add_widget(self.deactivation_label)

        with requirement_box.canvas.before:
            Color(0, 0, 0, 0)
            requirement_box.rect = Rectangle(size=requirement_box.size, pos=requirement_box.pos)
        requirement_box.bind(pos=update_layout, size=update_layout)
        with blueprint_box.canvas.before:
            Color(0, 0, 0, 0)
            blueprint_box.rect = Rectangle(size=blueprint_box.size, pos=blueprint_box.pos)
        blueprint_box.bind(pos=update_layout, size=update_layout)


class TechComparisonTable(BoxLayout):
    NUM_OF_ROWS = 10
    MAX_TECHNAME_LENGTH = 30

    def row_color(self, row_num):
        if row_num % 2 == 0:
            return (0.2, 0.2, 0.2, 1)
        return (0.2, 0, 0.2, 1)

    def button_color(self, row_num):
        if row_num % 2 == 0:
            return (0.2, 0.2, 0.2, 0)
        return (0.2, 0, 0.2, 0)
    
    def fill_comparison_table(self, tech_and_values):
        # self.title.text = f"Fastest to complete {tech.short_name}"
        # self.title.text = f"Best techs to research"
        for i, tech_and_value_n_team in enumerate(tech_and_values[:self.NUM_OF_ROWS]):
            tech, value, _ = tech_and_value_n_team
            self.labels[2*i].text = f"{tech.tech_id} {tech.name[:self.MAX_TECHNAME_LENGTH]}"
            self.labels[2*i].disabled = False
            self.labels[2*i+1].text = str(round(value, 3))
        if len(tech_and_values) < self.NUM_OF_ROWS:
            for i in range(len(tech_and_values), self.NUM_OF_ROWS):
                self.labels[2*i].text = ""
                self.labels[2*i].disabled = True
                self.labels[2*i+1].text = ""
        self.tech_in_table = [tech for tech, _, _ in tech_and_values]
    
    def select_tech_from_table(self, widget):
        button_index = self.labels.index(widget)
        # print(self.tech_in_table[button_index // 2].tech_id, self.tech_in_table[button_index // 2].name)
        # self.parent.update_team_selection(self.teams_in_table[button_index // 2])
        self.parent.select_tech(self.tech_in_table[button_index // 2])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.tech_in_table = []

        self.title = Label(text="Fastest tech to complete", size_hint=(1, 0.08))
        self.add_widget(self.title)

        header_line = BoxLayout(size_hint=(1, 0.08))
        header_line.add_widget(Label(text="Tech", size_hint=(0.8, 1)))
        self.value_label = Label(text="Days", size_hint=(0.2, 1))
        header_line.add_widget(self.value_label)
        self.add_widget(header_line)

        lines = [BoxLayout(size_hint=(1, 0.09)) for _ in range(self.NUM_OF_ROWS)]
        for line in lines:
            self.add_widget(line)

        self.table = [BoxLayout(size_hint=(0.5 + (-1)**(i) * 0.3, 1)) for i in range(2 * self.NUM_OF_ROWS)]
        for i, layout in enumerate(self.table):
            lines[i // 2].add_widget(layout)
            # print("Layout color:", self.row_color(i // 2))
            with layout.canvas.before:
                Color(*self.row_color(i // 2))
                layout.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(pos=update_layout, size=update_layout)
        
        self.labels = []
        for i, layout in enumerate(self.table):
            if i % 2 == 0:
                # cell = Label(text="...")
                cell = Button(text="", background_color=self.button_color(i // 2), on_release=self.select_tech_from_table, halign="left")
                # print("Button color:", self.row_color(i // 2))
            else:
                cell = Label(text="?")
            self.labels.append(cell)
            layout.add_widget(cell)

class FastestTechScreen(TechComparisonTable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ResearchSpeedImpactScreen(TechComparisonTable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title.text = "Tech that boost research speed the fastest"
        self.value_label.text = "Slope"


class TechteamScreen(BoxLayout):
    # TODO: parents will change
    def update_research_time(self, time_to_complete_tech = "?"):
        self.research_time_label.text = f"Finishes tech in {time_to_complete_tech} days"

    def show_default_texts(self):
        self.name_label.text = "Name: ?"
        self.nation_and_id_label.text = "Nation: ?  ID: ?"
        self.skill_label.text = "Skill: ?"
        self.years_label.text = "Years active: ? - ?"
        for speciality_label in self.speciality_labels:
            speciality_label.text = ""
        # self.research_time_label.text = "Finishes tech in ? days"
        self.update_research_time()
    
    def highlight_specialities(self, current_component_types):
        for speciality_label in self.speciality_labels:
            if speciality_label.text in current_component_types:
                speciality_label.color = (0, 1, 0, 1)
            else:
                speciality_label.color = (1, 1, 1, 1)
    
    def show_team_info(self, team, time_to_complete_tech="?", current_component_types=None):
        if team is None:
            self.show_default_texts()
            return
        self.name_label.text = team.name
        self.nation_and_id_label.text = f"{team.nation}  {team.team_id}"
        self.skill_label.text = f"Skill: {team.skill}"
        self.years_label.text = f"Years active: {team.start_year} - {team.end_year}"
        num_of_specs = len(team.specialities)
        for speciality_label, speciality in zip(self.speciality_labels[:num_of_specs], team.specialities):
            speciality_label.text = component_types[speciality]
            speciality_label.color = (1, 1, 1, 1)
            if current_component_types is not None:
                if speciality in current_component_types:
                    speciality_label.color = (0, 1, 0, 1)
        if num_of_specs < len(self.speciality_labels):
            for label in self.speciality_labels[num_of_specs:]:
                label.text = ""

        # self.research_time_label.text = f"Finishes tech in {time_to_complete_tech} days"
        self.update_research_time(time_to_complete_tech)

    def select_team(self, widget, value):
        if value:
            self.team_selection_dropdown.select(widget.text)

    def suggest_team_names(self, widget, text):
        if not self.team_input.focus:
            return
        self.team_selection_dropdown.clear_widgets()

        list_of_teams = self.parent.parent.parent.parent.research.teams
        suggestions = suggest_tech_teams(text, list_of_teams, self.max_num_of_team_suggestions)
        for i, suggestion in enumerate(suggestions):
            suggestion_thingy = TextInput(text=suggestion, readonly=True, multiline=False, write_tab=False, size_hint_y=None, height=dp(30))
            suggestion_thingy.bind(focus=self.select_team)
            self.team_selection_dropdown.add_widget(suggestion_thingy)
        
        if self.team_selection_dropdown.parent is None and self.team_input.get_parent_window() is not None:
            self.team_selection_dropdown.open(self.team_input)

    def make_team_selection(self, widget, text):
        country_code = text[1:4]
        name = text[6:]
        self.team_input.text = ""
        # team_name = text
        research = self.parent.parent.parent.parent.research
        
        tech_team = research.get_team_by_name_and_country(name, country_code)
        if tech_team is None:
            print(text, country_code, name)
        time_to_complete = None
        component_types = None
        if (tech := self.parent.parent.parent.parent.current_tech) is not None:
            time_to_complete = research.calculate_how_many_days_to_complete(tech_team, tech)
            component_types = [comp.type for comp in tech.components]
        self.show_team_info(tech_team, time_to_complete, component_types)
        self.parent.parent.parent.parent.current_team = tech_team

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Label(text="UpperTeamScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.orientation = "vertical"

        self.max_num_of_team_suggestions = 10
        self.team_selection_dropdown = DropDown()
        self.team_input = TextInput(text="", multiline=False, write_tab=False, size_hint=(1, 0.08))
        self.team_selection_dropdown.bind(on_select=self.make_team_selection)
        self.team_input.bind(text=self.suggest_team_names)
        self.add_widget(self.team_input)

        self.name_label = Label(text="name goes here", size_hint=(1, 0.1))
        # self.name_label.text_size = self.size
        self.name_label.halign = "left"
        self.add_widget(self.name_label)

        self.nation_and_id_label = Label(text="nation and id go here", size_hint=(1, 0.1), halign="left")
        self.add_widget(self.nation_and_id_label)

        self.skill_label = Label(text="Skill: ?", size_hint=(1, 0.1), halign="left")
        self.add_widget(self.skill_label)

        self.years_label = Label(text="Years active: ? - ?", size_hint=(1, 0.1), halign="left")
        self.add_widget(self.years_label)

        specialities_header_label = Label(text="Specialities:", size_hint=(1, 0.1), halign="left")
        self.add_widget(specialities_header_label)

        self.speciality_labels = [Label(text="", size_hint=(1, 0.1)) for _ in range(5)]
        for speciality in self.speciality_labels:
            self.add_widget(speciality)
        
        self.research_time_label = Label(text="Finishes tech in ? days", size_hint=(1, 0.1))
        self.add_widget(self.research_time_label)


class UpperTeamScreen(BoxLayout):
    BUTTON_TEXTS = ["Team info", "Fastest tech", "R-Speed boost"]

    def select_tech(self, tech):
        self.parent.select_tech(tech)
    
    def change_upperteamscreen_by_index(self, index_num):
        if self.screen_index == index_num:
            return
        self.clear_widgets()
        self.screen_index = index_num
        self.add_widget(self.screens[self.screen_index])

    def change_upperteamscreen(self, btn_text):
        # print(text)
        for i, text in enumerate(self.BUTTON_TEXTS):
            if btn_text == text and self.screen_index != i:
                self.clear_widgets()
                self.screen_index = i
                self.add_widget(self.screens[self.screen_index])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Label(text="UpperTeamScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))

        self.screen_index = 1
        self.screens = [TechteamScreen(), FastestTechScreen(), ResearchSpeedImpactScreen()]
        # self.techteam_screen = TechteamScreen()
        # self.fastest_tech_screen = FastestTechScreen()
        # self.research_speed_impact_screen = ResearchSpeedImpactScreen()
        self.add_widget(self.screens[self.screen_index])


# class TeamComparisonTable(GridLayout):
class TeamComparisonTable(BoxLayout):
    NUM_OF_ROWS = 10
    MAX_TEAMNAME_LENGTH = 30

    def row_color(self, row_num):
        if row_num % 2 == 0:
            return (0.2, 0.2, 0.2, 1)
        return (0.2, 0, 0.2, 1)

    def button_color(self, row_num):
        if row_num % 2 == 0:
            return (0.2, 0.2, 0.2, 0)
        return (0.2, 0, 0.2, 0)
    
    def update_boxlayout(self, widget, value):
        widget.rect.pos = widget.pos
        widget.rect.size = widget.size
    
    def fill_comparison_table(self, teams_and_times, tech):
        # self.title.text = f"Fastest to complete {tech.short_name}"
        self.title.text = f"Time to complete {tech.name}"
        for i, team_and_time in enumerate(teams_and_times[:self.NUM_OF_ROWS]):
            self.labels[2*i].text = team_and_time[0].name[:self.MAX_TEAMNAME_LENGTH]
            self.labels[2*i].disabled = False
            self.labels[2*i+1].text = str(team_and_time[1])
        if len(teams_and_times) < self.NUM_OF_ROWS:
            for i in range(len(teams_and_times), self.NUM_OF_ROWS):
                self.labels[2*i].text = ""
                self.labels[2*i].disabled = True
                self.labels[2*i+1].text = ""
        self.teams_in_table = [team for team, _ in teams_and_times]
    
    def select_team_from_table(self, widget):
        button_index = self.labels.index(widget)
        # print(self.teams_in_table[button_index // 2].name)
        self.parent.update_team_selection(self.teams_in_table[button_index // 2])
        self.parent.change_upperteamscreen_by_index(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.teams_in_table = []

        self.title = Label(text="Time to complete [tech]", size_hint=(1, 0.08))
        self.add_widget(self.title)

        header_line = BoxLayout(size_hint=(1, 0.08))
        header_line.add_widget(Label(text="Team", size_hint=(0.8, 1)))
        header_line.add_widget(Label(text="Days", size_hint=(0.2, 1)))
        self.add_widget(header_line)

        lines = [BoxLayout(size_hint=(1, 0.09)) for _ in range(self.NUM_OF_ROWS)]
        for line in lines:
            self.add_widget(line)

        self.table = [BoxLayout(size_hint=(0.5 + (-1)**(i) * 0.3, 1)) for i in range(2 * self.NUM_OF_ROWS)]
        for i, layout in enumerate(self.table):
            lines[i // 2].add_widget(layout)
            # print("Layout color:", self.row_color(i // 2))
            with layout.canvas.before:
                Color(*self.row_color(i // 2))
                layout.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(pos=update_layout, size=update_layout)
        
        self.labels = []
        for i, layout in enumerate(self.table):
            if i % 2 == 0:
                # cell = Label(text="...")
                cell = Button(text="", background_color=self.button_color(i // 2), on_release=self.select_team_from_table, halign="left")
                # print("Button color:", self.row_color(i // 2))
            else:
                cell = Label(text="?")
            self.labels.append(cell)
            layout.add_widget(cell)


class TeamScreen(BoxLayout):
    def change_upperteamscreen(self, widget):
        self.upperteamscreen.change_upperteamscreen(widget.text)

    def change_upperteamscreen_by_index(self, index_num):
        self.upperteamscreen.change_upperteamscreen_by_index(index_num)
    
    def update_team_selection(self, tech_team):
        self.parent.parent.current_team = tech_team
        research = self.parent.parent.research
        time_to_complete = None
        component_types = None
        if (tech := self.parent.parent.current_tech) is not None:
            time_to_complete = research.calculate_how_many_days_to_complete(tech_team, tech)
            component_types = [comp.type for comp in tech.components]
            self.parent.techscreen.update_tech_infopanels(tech)
        self.upperteamscreen.screens[0].show_team_info(tech_team, time_to_complete, component_types)

    def update_research_time(self, time_to_complete):
        self.upperteamscreen.screens[0].update_research_time(time_to_complete)
    
    def select_tech(self, tech):
        self.parent.select_tech(tech)

        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.upperteamscreen = UpperTeamScreen(orientation="vertical", size_hint=(1, 0.48))
        self.add_widget(self.upperteamscreen)
        with self.upperteamscreen.canvas.before:
            Color(0.15, 0.15, 0.15, 0.5)
            self.upperteamscreen.rect = Rectangle(size=self.upperteamscreen.size, pos=self.upperteamscreen.pos)
        self.upperteamscreen.bind(pos=update_layout, size=update_layout)

        buttons_row = BoxLayout(orientation="horizontal", size_hint=(1, 0.04))
        teaminfo_btn = Button(text=self.upperteamscreen.BUTTON_TEXTS[0], on_release=self.change_upperteamscreen)
        fastest_btn = Button(text=self.upperteamscreen.BUTTON_TEXTS[1], on_release=self.change_upperteamscreen)
        speedboost_btn = Button(text=self.upperteamscreen.BUTTON_TEXTS[2], on_release=self.change_upperteamscreen)
        buttons_row.add_widget(teaminfo_btn)
        buttons_row.add_widget(fastest_btn)
        buttons_row.add_widget(speedboost_btn)
        self.add_widget(buttons_row)

        # self.comparisontable = TeamComparisonTable(cols=2, size_hint=(1, 0.5))
        self.comparisontable = TeamComparisonTable(size_hint=(1, 0.48))
        self.add_widget(self.comparisontable)
        with self.comparisontable.canvas.before:
            Color(0.15, 0.15, 0.15, 0.5)
            self.comparisontable.rect = Rectangle(size=self.comparisontable.size, pos=self.comparisontable.pos)
        self.comparisontable.bind(pos=update_layout, size=update_layout)
        

class TechCategories(GridLayout):
    def select_category(self, widget):
        # print(widget.text)
        self.parent.select_category(widget.text)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # category_buttons = [ToggleButton(text=category) for category in categories]
        self.category_buttons = [Button(text=category[1]) for category in TECH_CATEGORIES]
        for category_button in self.category_buttons:
            self.add_widget(category_button)
            category_button.bind(on_release=self.select_category)


class TechInfoPanel(BoxLayout):
    def update_components(self, components):
        specialities = []
        if (team := self.parent.parent.parent.parent.current_team) is not None:
            specialities = team.specialities
        # print(specialities)
        # print(components)
        for i, component in enumerate(components):
            self.tech_components[2*i].text = component_types[component.type]
            self.tech_components[2*i + 1].text = str(component.difficulty)
            if component.type in specialities:
                self.tech_components[2*i].color = (0, 1, 0, 1)
            else:
                self.tech_components[2*i].color = (1, 1, 1, 1)
            
    def update_info(self, tech_id, tech_name, components, has_blueprint):
        self.technology_name.text = f"{tech_id} {tech_name}"
        self.update_components(components)
        self.blueprint_checkbox.active = has_blueprint
    
    def on_blueprint_checkbox_active(self, widget, value):
        try:
            tech_id = self.parent.parent.parent.parent.current_tech.tech_id
        except AttributeError:
            return
        research = self.parent.parent.research
        if value:
            research.blueprints.add(tech_id)
            if research.techs[tech_id].is_post_war:
                tech_id += 10_000
            self.parent.parent.maintechscreen.technologies[tech_id].add_blueprint()
        else:
            if tech_id in research.blueprints:
                research.blueprints.remove(tech_id)
                if research.techs[tech_id].is_post_war:
                    tech_id += 10_000
                self.parent.parent.maintechscreen.technologies[tech_id].remove_blueprint()
        # redo the calculations
        # self.parent.parent.parent.show_fastest_teams(self.parent.parent.parent.parent.current_tech)
        self.parent.parent.parent.update_tables(self.parent.parent.parent.parent.current_tech)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.technology_name = Label(text="Technology name", size_hint=(1, 0.3))
        self.add_widget(self.technology_name)

        # TODO
        components_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.5))
        self.add_widget(components_box)
        component_boxes = [BoxLayout(orientation="vertical") for _ in range(5)]
        self.tech_components = []
        for i, comp_box in enumerate(component_boxes):
            components_box.add_widget(comp_box)
            self.tech_components.append(Label(text=f"comp type {i+1}"))
            self.tech_components.append(Label(text=f"difficulty {i+1}"))
            comp_box.add_widget(self.tech_components[2*i])
            comp_box.add_widget(self.tech_components[2*i + 1])
        # self.tech_components = Label(text="Tech components go here", size_hint=(1, 0.5))
        # self.add_widget(self.tech_components)
        # for comp_box in component_boxes:
            
        checkbox_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        self.blueprint_checkbox = CheckBox(size_hint=(0.3, 1))
        checkbox_box.add_widget(Label(text="", size_hint=(0.2, 1)))
        checkbox_box.add_widget(self.blueprint_checkbox)
        checkbox_box.add_widget(Label(text="has blueprint", size_hint=(0.3, 1)))
        checkbox_box.add_widget(Label(text="", size_hint=(0.2, 1)))
        self.add_widget(checkbox_box)
        self.blueprint_checkbox.bind(active=self.on_blueprint_checkbox_active)
    

class RequirementPanel(BoxLayout):
    # requirement_header = 
    def select_technology(self, widget):
        self.parent.parent.parent.select_technology_by_id(widget.parent.tech_id)

    def create_tech_button(self, tech_id, research_object, optional=False):
        tech_btn = TechnologyButton(research_object.techs[tech_id].short_name, tech_id)
        tech_btn.update_status(research_object)
        tech_btn.size_hint = (0.8, None)
        tech_btn.pos_hint = {"center_x": 0.5}
        tech_btn.height = dp(25)
        tech_btn.technology.bind(on_release=self.select_technology)
        if optional:
            tech_btn.technology.text = f"*{tech_btn.technology.text}"
        return tech_btn

    def show_reqs_and_deacts(self, requirements, is_required_ins, deactivations, deactivated_by):
        self.clear_widgets()
        research = self.parent.parent.parent.research
        if requirements:
            self.add_widget(Label(text="Requirements:", size_hint=(1, None), height=dp(25), color=(1, 1, 0, 1)))
            for requirement in requirements:
                # self.add_widget(Label(text=requirement, size_hint=(1, None), height=dp(25)))
                tech_id = int(requirement.strip("*")) % 10_000
                tech_btn = self.create_tech_button(tech_id, research, "*" == requirement[0])
                self.add_widget(tech_btn)
        
        if is_required_ins:
            self.add_widget(Label(text="Is required in:", size_hint=(1, None), height=dp(25), color=(1, 1, 0, 1)))
            for tech_id in is_required_ins:
                tech_id = tech_id % 10_000
                # self.add_widget(Label(text=requirement, size_hint=(1, None), height=dp(25)))
                # tech_id = int(requirement.split(" ")[0].strip("*"))
                tech_btn = self.create_tech_button(tech_id, research)
                self.add_widget(tech_btn)

        if deactivations:
            self.add_widget(Label(text="Deactivates:", size_hint=(1, None), height=dp(25), color=(1, 0, 0, 1)))
            for tech_id in deactivations:
                tech_id = tech_id % 10_000
                # self.add_widget(Label(text=deactivation, size_hint=(1, None), height=dp(25)))
                # tech_id = int(deactivation.split(" ")[0].strip("*"))
                tech_btn = self.create_tech_button(tech_id, research)
                self.add_widget(tech_btn)
        
        if deactivated_by:
            self.add_widget(Label(text="Deactivated by:", size_hint=(1, None), height=dp(25), color=(1, 0, 0, 1)))
            for tech_id in deactivated_by:
                tech_id = tech_id % 10_000
                # self.add_widget(Label(text=deactivation, size_hint=(1, None), height=dp(25)))
                # tech_id = int(deactivation.split(" ")[0].strip("*"))
                tech_btn = self.create_tech_button(tech_id, research)
                self.add_widget(tech_btn)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Requirements:", size_hint=(1, 0.25), color=(1, 1, 0, 1)))
        self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        self.add_widget(Label(text="Deactivates:", size_hint=(1, 0.25), color=(1, 0, 0, 1)))
        self.add_widget(Label(text="...", size_hint=(1, 0.25)))


class EffectsPanel(BoxLayout):
    def show_effects(self, effects):
        self.clear_widgets()

        self.add_widget(Label(text="Effects:", size_hint=(1, None), height=dp(20)))
        for effect in effects:
            self.add_widget(Label(text=effect, size_hint=(1, None), height=dp(20)))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Effects:", size_hint=(1, None), height=dp(20)))
        for i in range(20):
            self.add_widget(Label(text=f"... {i+1}", size_hint=(1, None), height=dp(20)))
        # self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        # self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        # self.add_widget(Label(text="...", size_hint=(1, 0.25)))


class ResearchButtonsPanel(GridLayout):
    def complete_button_pressed(self, widget):
        self.parent.parent.complete_until_tech()

    def force_complete_button_pressed(self, widget):
        self.parent.parent.complete_tech()

    def undo_button_pressed(self, widget):
        self.parent.parent.undo_tech()

    def clear_button_pressed(self, widget):
        self.parent.parent.clear_tech()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.complete_button = Button(text="Complete Tech", on_release=self.complete_button_pressed, size_hint=(0.4, 0.4))
        self.add_widget(self.complete_button)

        # empty
        # self.add_widget(Label(text=" "))
        
        self.undo_button = Button(text="Undo Tech", on_release=self.undo_button_pressed, size_hint=(0.4, 0.4))
        self.add_widget(self.undo_button)

        self.force_complete_button = Button(text="       Force  \nComplete Tech", on_release=self.force_complete_button_pressed, size_hint=(0.4, 0.4))
        self.add_widget(self.force_complete_button)

        # empty
        # self.add_widget(Label(text=" "))

        self.clear_button = Button(text="Clear everything", on_release=self.clear_button_pressed, size_hint=(0.4, 0.4))
        self.add_widget(self.clear_button)


class MainTechScreen(FloatLayout):
    LINE_COLOR = (0.7, 0.7, 0.7, 0.8)
    DEACT_LINE_COLOR = (0.8, 0.1, 0.1, 0.9)

    def select_technology(self, widget):
        self.parent.parent.select_technology_by_id(widget.parent.tech_id)
        # print(widget.parent.tech_id)
    
    def draw_lines_from_points(self, line_points, deact_line_points):
        with self.canvas.before:
            Color(*self.LINE_COLOR)
            # print("drawing line")
            self.lines = []
            for point_tuple, draw_arrow in line_points:
                scaled_points = scale_arrows(self.size, self.pos, point_tuple)
                self.lines.append(Line(points=scaled_points, width=2))
                if draw_arrow:
                    self.lines.append(Line(points=get_arrow_points(*scaled_points), width=2))
            Color(*self.DEACT_LINE_COLOR)
            self.deact_lines = []
            for point_tuple in deact_line_points:
                scaled_points = scale_arrows(self.size, self.pos, point_tuple)
                self.deact_lines.append(Line(points=scaled_points, width=2))
    
    def draw_lines(self):
        pass

    def update_lines(self, widget, value):
        # test_printer (widget, value)
        pass

    def update_lines_from_points(self, line_points, deact_line_points):
        i = 0
        for point_tuple, draw_arrow in line_points:
            scaled_points = scale_arrows(self.size, self.pos, point_tuple)
            self.lines[i].points = scaled_points
            i += 1
            if draw_arrow:
                self.lines[i].points = get_arrow_points(*scaled_points)
                i += 1
        for line, point_tuple in zip(self.deact_lines, deact_line_points):
            line.points = scale_arrows(self.size, self.pos, point_tuple)

    def __init__(self, **kwargs):
        # self.TECHNOLOGYBUTTON_SIZE = (0.175, 0.04)
        super().__init__(**kwargs)
        # self.add_widget(Label(text="MainTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))

        self.lines = None
        self.deact_lines = None

        self.bind(size=self.update_lines, pos=self.update_lines)


class InfantryTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.infantry_lines, lines.infantry_deact_lines)

    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.infantry_lines, lines.infantry_deact_lines)    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="InfantryTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class ArmorTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.armor_lines, lines.armor_deact_lines)

    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.armor_lines, lines.armor_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="ArmorTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class NavalTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.naval_lines, [])
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.naval_lines, [])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="NavalTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class AircraftTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.aircraft_lines, lines.aircraft_deact_lines)
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.aircraft_lines, lines.aircraft_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="AircraftTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class PostWarTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.post_war_lines, lines.post_war_deact_lines)
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.post_war_lines, lines.post_war_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="OverviewTechScreen\nThis will probably remain empty", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class IndustryTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.industry_lines, lines.industry_deact_lines)
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.industry_lines, lines.industry_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="IndustryTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class LandDoctrineTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.land_doct_lines, lines.land_doct_deact_lines)
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.land_doct_lines, lines.land_doct_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="LandDoctrineTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class SecretWeaponTechScreen(MainTechScreen):
    def draw_lines(self):
        return super().draw_lines()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="SecretWeaponTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class NavalDoctrineTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.naval_doct_lines, lines.naval_doct_deact_lines)
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.naval_doct_lines, lines.naval_doct_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="NavalDoctrineTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class AirDoctrineTechScreen(MainTechScreen):
    def draw_lines(self):
        self.draw_lines_from_points(lines.air_doct_lines, lines.air_doct_deact_lines)
    
    def update_lines(self, widget, value):
        self.update_lines_from_points(lines.air_doct_lines, lines.air_doct_deact_lines)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="AirDoctrineTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class MainTechScreen_BoxLayout(BoxLayout):
    def select_technology(self, widget):
        self.parent.select_technology_by_id(widget.parent.tech_id)

    def show_requirements(self, required_tech_ids):
        for tech_id in required_tech_ids:
            tech_id = int(tech_id.strip("*"))
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.show_as_requirement()
            else:
                print(f"{tech_id} not in tech buttons")
            # self.technologies[tech_id].show_as_requirement()
        self.old_requirements = [int(tech_id.strip("*")) for tech_id in required_tech_ids]
    
    def hide_old_requirements(self):
        for tech_id in self.old_requirements:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.hide_requirement()
    
    def show_is_required_ins(self, allowed_tech_ids):
        for tech_id in allowed_tech_ids:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.show_as_allowed_by()
        self.old_is_required_ins = allowed_tech_ids
    
    def hide_old_is_required_ins(self):
        for tech_id in self.old_is_required_ins:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.hide_is_required_in()
    
    def show_deactivation_warnings(self, deactivated_tech_ids):
        for tech_id in deactivated_tech_ids:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.show_deactivation_warning()
            # self.technologies[tech_id].show_deactivation_warning()
        self.old_deactivations = deactivated_tech_ids
    
    def hide_old_deactivation_warnings(self):
        for tech_id in self.old_deactivations:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.hide_deactivation_warning()
    
    def change_layout(self, category):
        self.remove_widget(self.current_layout)
        self.current_layout = self.category_layouts[category]
        self.add_widget(self.current_layout)
    
    def add_technology_buttons(self, i, layout):
        if i == 4:
            for tech_id, tech_btn in self.technologies.items():
                if tech_id >=10_000:
                    layout.add_widget(tech_btn)
            return
        lower_id = (i + 1) * 1000 if i < 4 else i * 1000
        for tech_id, tech_btn in self.technologies.items():
            if tech_id >= lower_id and tech_id < lower_id + 1000:
                layout.add_widget(tech_btn)
    
    def update_technology_buttons(self, research_object):
        for tech_id, tech_button in self.technologies.items():
            tech_button.update_status(research_object)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Label(text="MainTechScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))

        self.old_requirements = []
        self.old_is_required_ins = []
        self.old_deactivations = []

        # self.tech_buttons = dict()

        self.technologies = dict()
        for key, value in tech_positions.items():
            tech_id = key % 10_000
            name = the_research.techs[tech_id].short_name
            self.technologies[key] = TechnologyButton(name, tech_id, pos_hint={"x": value[0], "y": value[1]})
        
        for tech_id, tech in the_research.techs.items():
            if tech.is_post_war:
                tech_id += 10_000
            if self.technologies.get(tech_id) is None:
                print(f"{tech_id} not among technology buttons")

        for tb in self.technologies.values():
            # self.add_widget(tb)
            tb.technology.bind(on_release=self.select_technology)

        self.category_layouts = {
            TECH_CATEGORIES[0][1]: InfantryTechScreen(),
            TECH_CATEGORIES[1][1]: ArmorTechScreen(),
            TECH_CATEGORIES[2][1]: NavalTechScreen(),
            TECH_CATEGORIES[3][1]: AircraftTechScreen(),
            TECH_CATEGORIES[4][1]: PostWarTechScreen(),
            TECH_CATEGORIES[5][1]: IndustryTechScreen(),
            TECH_CATEGORIES[6][1]: LandDoctrineTechScreen(),
            TECH_CATEGORIES[7][1]: SecretWeaponTechScreen(),
            TECH_CATEGORIES[8][1]: NavalDoctrineTechScreen(),
            TECH_CATEGORIES[9][1]: AirDoctrineTechScreen()
        }

        for i, layout in enumerate(self.category_layouts.values()):
            self.add_technology_buttons(i, layout)
            layout.draw_lines()

        self.current_layout = self.category_layouts["Infantry"]
        self.add_widget(self.current_layout)


class TechInfoPanels(BoxLayout):
    BACKGROUND_COLOR2 = (0.1, 0.1, 0.1, 1)

    # def update_panel(self, widget, value):
    #     widget.rect.pos = widget.pos
    #     widget.rect.size = widget.size

    def update_tech_info(self, tech, has_blueprint, requirements, is_required_ins, deactivations, deactivated_by, effects):
        self.techinfopanel.update_info(tech.tech_id, tech.name, tech.components, has_blueprint)

        self.requirement_panel.show_reqs_and_deacts(requirements, is_required_ins, deactivations, deactivated_by)

        self.effects_panel.show_effects(effects)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.techinfopanel = TechInfoPanel(orientation="vertical", size_hint=(0.34, 1))
        self.add_widget(self.techinfopanel)
        with self.techinfopanel.canvas.before:
            Color(*self.BACKGROUND_COLOR2)
            self.techinfopanel.rect = Rectangle(size=self.techinfopanel.size, pos=self.techinfopanel.pos)
        self.techinfopanel.bind(pos=update_layout, size=update_layout)

        self.requirement_scrollview = ScrollView(size_hint=(0.22, None))
        self.requirement_panel = RequirementPanel(orientation="vertical", size_hint=(1, None))
        # self.requirement_panel.height = self.requirement_panel.minimum_height + 50
        self.requirement_panel.bind(minimum_height=self.requirement_panel.setter("height"))
        self.requirement_scrollview.add_widget(self.requirement_panel)
        # self.add_widget(RequirementPanel(orientation="vertical", size_hint=(0.25, 1)))
        self.add_widget(self.requirement_scrollview)

        self.extra_layout = BoxLayout(size_hint=(0.22, 1))
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
        self.extra_layout.bind(pos=update_layout, size=update_layout)

        self.add_widget(ResearchButtonsPanel(cols=2, padding=(dp(5), dp(5), dp(5), dp(5)), spacing=dp(10), size_hint=(0.22, 1)))
        # for i in range(4):
        #     self.add_widget(Button(text=f"InfoPanel {i+1}", size_hint=(0.25, 1)))


class TechScreen(BoxLayout):

    def select_category(self, category):
        if category == self.active_category:
            return
        self.active_category = category
        self.maintechscreen.change_layout(category)
    
    def update_tech_infopanels(self, tech):
        requirements = self.research.list_requirements(tech)
        is_required_ins = self.research.list_is_required_in(tech)
        deactivations = self.research.list_deactivations(tech)
        deactivated_by = self.research.list_is_deactivated_by(tech, False)
        effects = self.research.list_effects(tech)
        has_blueprint = tech.tech_id in self.research.blueprints
        self.techinfopanel.update_tech_info(tech, has_blueprint, requirements, is_required_ins, deactivations, deactivated_by, effects)
        return [requirements, deactivations, is_required_ins]
    
    def update_panels_and_stuff(self, tech):
        # update infopanels
        requirements, deactivations, is_required_ins = self.update_tech_infopanels(tech)

        # update tech buttons
        self.maintechscreen.hide_old_requirements()
        self.maintechscreen.hide_old_is_required_ins()
        self.maintechscreen.hide_old_deactivation_warnings()

        self.maintechscreen.show_requirements(requirements)
        self.maintechscreen.show_is_required_ins(is_required_ins)
        self.maintechscreen.show_deactivation_warnings(deactivations)
        # req_ids = [int(line.split(" ")[0].strip("*")) for line in requirements]
        # deact_ids = [int(line.split(" ")[0].strip("*")) for line in deactivations]
        # allow_ids = [int(line.split(" ")[0].strip("*")) for line in is_required_ins]
        # self.maintechscreen.show_requirements(req_ids)
        # self.maintechscreen.show_is_required_ins(allow_ids)
        # self.maintechscreen.show_deactivation_warnings(deact_ids)
    
    def select_technology_by_id(self, tech_id):
        # category = get_the_other_category(self.active_category)
        tech = self.research.get_tech(tech_id)
        self.parent.parent.current_tech = tech
        # print(f"{tech.tech_id} {tech.name}")

        # sort teams based on who is fastest
        self.parent.show_fastest_teams(tech)
        # sorted_teams = self.parent.parent.research.sort_teams_for_researching_tech(tech)
        # self.parent.teamscreen.comparisontable.fill_comparison_table(sorted_teams)

        # update team info
        if (team := self.parent.parent.current_team) is not None:
            time_to_complete = self.research.calculate_how_many_days_to_complete(team, tech)
            self.parent.teamscreen.update_research_time(time_to_complete)
            self.parent.teamscreen.update_team_selection(team)

        self.update_panels_and_stuff(tech)
            
    
    def complete_until_tech(self):
        try:
            tech_id = self.parent.parent.current_tech.tech_id
        except AttributeError:
            return
        if tech_id in self.research.completed_techs:
            return
        self.research.complete_until_tech(tech_id)
        # update tables
        self.parent.update_tables(self.parent.parent.current_tech)
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.research.research_speed)
        # save status
        self.parent.parent.save_status()

    def complete_tech(self):
        try:
            tech_id = self.parent.parent.current_tech.tech_id
        except AttributeError:
            return
        if tech_id in self.research.completed_techs:
            return
        self.research.complete_tech(tech_id)
        # update tables
        self.parent.update_tables(self.parent.parent.current_tech)
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.research.research_speed)
        # save status
        self.parent.parent.save_status()
    
    def undo_tech(self):
        try:
            tech_id = self.parent.parent.current_tech.tech_id
        except AttributeError:
            return
        if tech_id not in self.research.completed_techs:
            return
        self.research.undo_completed_tech(tech_id)
        # update tables
        self.parent.update_tables(self.parent.parent.current_tech)
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.research.research_speed)
        # save status
        self.parent.parent.save_status()

    def clear_tech(self):
        if not self.research.completed_techs and not self.research.deactivated_techs and not self.research.blueprints:
            return
        self.research.clear_all_tech()
        # update tables
        self.parent.update_tables()
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.research.research_speed)
        # save status
        self.parent.parent.save_status()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.research = None

        self.active_category = TECH_CATEGORIES[0][1]

        self.techcategories = TechCategories(cols=5, size_hint=(1, 0.05))
        self.maintechscreen = MainTechScreen_BoxLayout(size_hint=(1, 0.80))
        self.techinfopanel = TechInfoPanels(orientation="horizontal", size_hint=(1, 0.15))
        self.add_widget(self.techcategories)
        self.add_widget(self.maintechscreen)
        self.add_widget(self.techinfopanel)


class MainScreen(BoxLayout):

    def show_fastest_teams(self, tech):
        if tech is None:
            return
        sorted_teams = self.parent.research.sort_teams_for_researching_tech(tech)
        self.teamscreen.comparisontable.fill_comparison_table(sorted_teams, tech)
        self.parent.change_year(self.parent.research.year)
    
    def show_fastest_tech(self):
        sorted_tech = self.parent.research.sort_active_tech_based_on_research_time()
        self.teamscreen.upperteamscreen.screens[1].fill_comparison_table(sorted_tech)
    
    def show_best_tech(self):
        sorted_tech = self.parent.research.sort_active_tech_based_on_research_time_and_research_speed()
        self.teamscreen.upperteamscreen.screens[2].fill_comparison_table(sorted_tech)

    def update_tables(self, tech=None):
        self.show_fastest_teams(tech)
        self.show_fastest_tech()
        self.show_best_tech()

    def select_tech(self, tech):
        self.parent.current_tech = tech
        self.show_fastest_teams(tech)
        # update team info
        if (team := self.parent.current_team) is not None:
            time_to_complete = self.parent.research.calculate_how_many_days_to_complete(team, tech)
            self.teamscreen.update_research_time(time_to_complete)
            self.teamscreen.update_team_selection(team)
        # update techscreen
        self.techscreen.update_panels_and_stuff(tech)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Button(text="MainScreen", size_hint=(1, 1)))
        self.techscreen = TechScreen(orientation="vertical", size_hint=(0.8, 1))
        self.teamscreen = TeamScreen(orientation="vertical", size_hint=(0.2, 1))
        self.add_widget(self.teamscreen)
        self.add_widget(self.techscreen)


class PolicyScreen(BoxLayout):
    def choose_minister_or_idea(self, position, name):
        # print(position, name)
        # print(self.parent.parent.attach_to.parent)
        if self.parent.parent.attach_to is None:
            return
        # print(self.parent)
        # print(self.parent.parent)
        # print(self.parent.parent.attach_to)
        self.parent.parent.attach_to.parent.change_policies_based_on_checkboxes(name, position)

    def change_policy_choices(self, policy_dict):
        for choice in self.choices:
            if choice.title.text.lower() in policy_dict:
                choice.change_minister(policy_dict[choice.title.text.lower()])
    
    def show_tech_effects_of_policies(self, effect_dict):
        for choice in self.choices:
            if choice.title.text.lower() in effect_dict:
                choice.change_research_effects(effect_dict[choice.title.text.lower()])
    
    def change_bankrupt_status(self, widget, value):
        self.parent.parent.attach_to.parent.change_bankrupt_status(int(value))
        # print(widget)
        # if value:
        #     print("bankrupt")
        #     return
        # print("not bankrupt")
    
    def set_bankrupt_status(self, is_bankrupt):
        self.bankrupt_checkbox.active = bool(is_bankrupt)


    def __init__(self, bg_color=(0, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.bg_color = bg_color
        # with self.canvas.before:
        #     Color(*self.bg_color)
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        # self.bind(pos=update_layout, size=update_layout)

        self.spacing = 5

        policy_part = BoxLayout(orientation="horizontal", size_hint=(1, 0.9))
        self.add_widget(policy_part)

        arm_minister_choice = BoxLayout(orientation="vertical", size_hint=(0.33, 1))
        with arm_minister_choice.canvas.before:
            Color(*bg_color)
            arm_minister_choice.rect = Rectangle(size=arm_minister_choice.size, pos=arm_minister_choice.pos)
        arm_minister_choice.bind(pos=update_layout, size=update_layout)
        intel_and_cos_choice = BoxLayout(orientation="vertical", size_hint=(0.33, 1))
        with intel_and_cos_choice.canvas.before:
            Color(*bg_color)
            intel_and_cos_choice.rect = Rectangle(size=intel_and_cos_choice.size, pos=intel_and_cos_choice.pos)
        intel_and_cos_choice.bind(pos=update_layout, size=update_layout)
        idea_choice = BoxLayout(orientation="vertical", size_hint=(0.33, 1))
        with idea_choice.canvas.before:
            Color(*bg_color)
            idea_choice.rect = Rectangle(size=idea_choice.size, pos=idea_choice.pos)
        idea_choice.bind(pos=update_layout, size=update_layout)

        labels = the_research.politics.get_policies_for_checkboxes()

        # self.choices = dict()
        self.choices = []
        for key, list_of_labels in labels.items():
            choice = MinisterCheckBoxGroup(key, list_of_labels)
            self.choices.append(choice)

        for i, choice in enumerate(self.choices):
            if i == 0:
                arm_minister_choice.add_widget(choice)
            elif i in [1, 2]:
                intel_and_cos_choice.add_widget(choice)
            else:
                idea_choice.add_widget(choice)

        # for i in range(11):
        #     checkbox = CheckBox(group="armamentminister")
        #     label = Label(text=f"minister{i+1}")
        #     arm_minister_choice.add_widget(checkbox)
        #     arm_minister_choice.add_widget(label)

        # for i in range(2):
        #     checkbox = CheckBox(group="ministerofintelligence")
        #     label = Label(text=f"minister{i+1}")
        #     intel_and_cos_choice.add_widget(checkbox)
        #     intel_and_cos_choice.add_widget(label)

        # for i in range(2):
        #     checkbox = CheckBox(group="chiefofstaff")
        #     label = Label(text=f"minister{i+1}")
        #     intel_and_cos_choice.add_widget(checkbox)
        #     intel_and_cos_choice.add_widget(label)

        # for i in range(3):
        #     checkbox = CheckBox(group="socialpolicy")
        #     label = Label(text=f"idea{i+1}")
        #     idea_choice.add_widget(checkbox)
        #     idea_choice.add_widget(label)

        # for i in range(2):
        #     checkbox = CheckBox(group="nationalculture")
        #     label = Label(text=f"idea{i+1}")
        #     idea_choice.add_widget(checkbox)
        #     idea_choice.add_widget(label)

        policy_part.add_widget(arm_minister_choice)
        policy_part.add_widget(intel_and_cos_choice)
        policy_part.add_widget(idea_choice)

        bigger_bankrupt_part = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))

        bankrupt_part = BoxLayout(orientation="horizontal", size_hint=(0.36, 1))

        with bankrupt_part.canvas.before:
            Color(*bg_color)
            bankrupt_part.rect = Rectangle(size=bankrupt_part.size, pos=bankrupt_part.pos)
        bankrupt_part.bind(pos=update_layout, size=update_layout)

        bigger_bankrupt_part.add_widget(Label(text="", size_hint=(0.32, 1)))
        self.bankrupt_checkbox = CheckBox(size_hint=(0.15, 1))
        self.bankrupt_checkbox.bind(active=self.change_bankrupt_status)
        bankrupt_part.add_widget(Label(text="", size_hint=(0.2, 1)))
        bankrupt_part.add_widget(self.bankrupt_checkbox)
        bankrupt_part.add_widget(Label(text="country is bankrupt", size_hint=(0.45, 1)))
        bankrupt_part.add_widget(Label(text="", size_hint=(0.2, 1)))
        bigger_bankrupt_part.add_widget(bankrupt_part)
        bigger_bankrupt_part.add_widget(Label(text="", size_hint=(0.32, 1)))

        self.add_widget(bigger_bankrupt_part)



class StatusBar(BoxLayout):
    save_file = Path("save.data")
    policyscreen_bg_color = (0, 0.1, 0.03, 1)

    def update_tables(self):
        self.parent.mainscreen.update_tables(self.parent.current_tech)
        # if self.parent.current_tech is not None:
        #     self.parent.mainscreen.show_fastest_teams(self.parent.current_tech)
        # self.parent.mainscreen.show_fastest_tech()
        # self.parent.mainscreen.show_best_tech()

    def save_country_difficulty_and_year(self):
        with open(self.save_file, "w") as f:
            country_line = f"country={','.join(self.country_buttons.keys())}"
            difficulty_line = f"difficulty={self.difficulty_button.text}"
            year_line = f"year={self.parent.research.year}"
            f.write(f"{country_line}\n{difficulty_line}\n{year_line}")
    
    def show_no_country_selected(self):
        self.countries_selected.clear_widgets()
        self.countries_selected.add_widget(Label(text="No country selected"))
    
    def add_only_primary_country(self):
        primary_country = self.parent.research.primary_country
        self.countries_selected.clear_widgets()
        self.country_buttons[primary_country].size_hint_y = 1
        self.country_buttons[primary_country].size_hint_x = 0.5
        self.countries_selected.add_widget(self.country_buttons[primary_country])
        self.countries_selected.add_widget(self.reload_countries_button)
    
    def add_country_ui_updates(self, country_code):
        self.country_buttons[country_code] = CountryButton(country_code, self.bg_color)
        self.country_buttons[country_code].remove_button.bind(on_release=lambda *args: self.remove_country(country_code))

        num_of_countries = len(self.country_buttons)
        btn_text = "Reload countries" if num_of_countries > 1 else "Reload country"
        self.reload_countries_button.text = btn_text

        if num_of_countries == 1:
            self.add_only_primary_country()
            return
        self.active_countries_button.text = f"{self.parent.research.primary_country} +{num_of_countries - 1}"
        if num_of_countries == 2:
            self.countries_selected.clear_widgets()
            self.countries_selected.add_widget(self.active_countries_button)
            self.countries_selected.add_widget(self.reload_countries_button)
            self.countries_selected.add_widget(self.clear_countries_button)

    def add_country(self, country_code):
        if country_code in self.country_buttons.keys():
            return
        # we need a scrollview
        # self.country_buttons[country_code] = CountryButton(country_code, size_hint=(None, 1), width=dp(100))
        
        # print(f"{self.parent=}")
        self.parent.add_country(country_code)
        if country_code == self.parent.research.primary_country:
            self.change_checkboxes_based_on_policies()
        self.update_tables()
        # self.save_country_difficulty_and_year()
        self.parent.save_status()
        self.add_country_ui_updates(country_code)
    
    def remove_country(self, country_code):
        num_of_countries = len(self.country_buttons)
        if not num_of_countries:
            return
        if num_of_countries == 1:
            self.countries_selected.remove_widget(self.country_buttons[country_code])
        elif num_of_countries > 1:
            self.active_countries_dropdown.remove_widget(self.country_buttons[country_code])
        del self.country_buttons[country_code]
        self.parent.remove_country(country_code)
        self.update_tables()
        # self.save_country_difficulty_and_year()
        self.parent.save_status()

        if not self.country_buttons:
            if self.active_countries_dropdown.parent is not None:
                self.active_countries_dropdown.dismiss()
            self.show_no_country_selected()
            return
        
        num_of_countries = len(self.country_buttons)
        btn_text = "Reload countries" if num_of_countries > 1 else "Reload country"
        self.reload_countries_button.text = btn_text
        primary_country = self.parent.research.countries[0]
        if num_of_countries == 1:
            if self.active_countries_dropdown.parent is not None:
                self.active_countries_dropdown.clear_widgets()
                self.active_countries_dropdown.dismiss()
            self.parent.add_country(primary_country)
            self.add_only_primary_country()
            return
        self.active_countries_button.text = f"{primary_country} +{num_of_countries - 1}"
        

    def clear_countries(self):
        for country_code in self.country_buttons.keys():
            self.parent.remove_country(country_code)
        self.country_buttons = dict()
        self.active_countries_dropdown.clear_widgets()
        self.show_no_country_selected()
        self.update_tables()
        # self.save_country_difficulty_and_year()
        self.parent.save_status()

    def reload_countries(self, widget):
        country_codes = list(self.country_buttons.keys())
        self.clear_countries()
        for country_code in country_codes:
            self.add_country(country_code)

    def load_country_difficulty_and_year(self):
        if not Path(self.save_file).exists():
            return
        country_codes = None
        difficulty = None
        year = None
        with open(self.save_file, "r") as f:
            lines = f.read().split("\n")
            for line in lines:
                if "country" in line:
                    # print(line.split("=")[1].strip())
                    country_codes = line.split("=")[1].strip().split(",")
                elif "difficulty" in line:
                    difficulty = line.split("=")[1].strip()
                elif "year" in line:
                    year = line.split("=")[1].strip()
        if country_codes:
            for country_code in country_codes:
                if country_code:
                    self.add_country(country_code)
        if difficulty:
            self.difficulty_button.text = difficulty
            # self.parent.research.difficulty = DIFFICULTY_DICT[difficulty]
            self.parent.research.change_difficulty(get_the_other_difficulty(difficulty))
        if year:
            try:
                self.parent.change_year(int(year))
                self.year_input.text = year
            except ValueError:
                pass

    def select_difficulty(self, widget, value):
        # setattr(self.difficulty_button, "text", value)
        self.difficulty_button.text = value
        # self.parent.research.difficulty = DIFFICULTY_DICT[value]
        self.parent.research.change_difficulty(get_the_other_difficulty(value))
        # if self.parent.current_tech is not None:
        #     self.parent.mainscreen.show_fastest_teams(self.parent.current_tech)
        self.update_tables()
        # self.save_country_difficulty_and_year()
        self.parent.save_status()

    def select_year(self, widget, value):
        # previous_year = self.year_input.select_all()
        try:
            self.parent.change_year(int(value))
            self.year_input.text = value
            # if self.parent.current_tech is not None:
            #     self.parent.mainscreen.show_fastest_teams(self.parent.current_tech)
            self.update_tables()
            # self.save_country_difficulty_and_year()
            self.parent.save_status()
        except ValueError:
            self.year_input.text = str(self.parent.research.year)
        
    def select_num_of_rocket_sites(self, widget, value):
        try:
            self.parent.research.num_of_rocket_sites = int(value)
            self.rocket_site_button.text = value
            # if self.parent.current_tech is not None:
            #     self.parent.mainscreen.show_fastest_teams(self.parent.current_tech)
            self.update_tables()
        except ValueError as e:
            print(f"Bad number of rocket sites: {value}")
            raise e
    
    def select_reactor_size(self, widget, value):
        try:
            self.parent.research.reactor_size = int(value)
            self.reactor_size_button.text = value
        except ValueError as e:
            print(f"Bad reactor size: {value}")
            raise e

    # useless method
    def on_checkbox_active_placeholder(self, checkbox, value):
        if value:
            print(f"Values are locked by checkbox {checkbox} (NOT REALLY, THIS DOES NOTHING)")
        else:
            print(f"Values are not locked by checkbox {checkbox} (THIS DOES NOTHING)")
    
    def on_active_countries_button_release(self, widget):
        if self.active_countries_dropdown.parent is not None:
            print("dismissing country dropdown")
            self.active_countries_dropdown.dismiss()
            return
        # print("should open something")
        self.active_countries_dropdown.clear_widgets()
        for country_code, country_btn in self.country_buttons.items():
            country_btn.size_hint = (1, None)
            country_btn.height = dp(25)
            self.active_countries_dropdown.add_widget(country_btn)
        self.active_countries_dropdown.open(widget)

    def on_clear_countries_button_release(self, widget):
        self.clear_countries()

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
        country_code = value.split("[")[1].split("]")[0]
        self.add_country(country_code)

    def open_year_selection_dropdown(self, widget, text):
        if not widget.focus:
            return
        
        # print("self.year_selection_dropdown.parent is None:", self.year_selection_dropdown.parent is None)
        # print("self.get_parent_window() is not None:", self.get_parent_window() is not None)
        if self.year_selection_dropdown.parent is None and self.get_parent_window() is not None:
            self.year_selection_dropdown.open(widget)

    def validate_year(self, widget, text):
        if not text:
            return
        if self.parent is None:
            return
        # previous_year = self.parent.year
        if text in self.years:
            self.year_selection_dropdown.dismiss()
            self.parent.research.change_year(int(text))
            # if self.parent.current_tech is not None:
            #     self.parent.mainscreen.show_fastest_teams(self.parent.current_tech)
            self.update_tables()
            # self.save_country_difficulty_and_year()
            self.parent.save_status()
    
    def validate_research_speed(self, widget, text):
        if not text:
            return
        if self.parent is None:
            return
        previous_research_speed = self.parent.research.research_speed
        try:
            new_research_speed = float(text)
            self.parent.research.research_speed = new_research_speed
            self.update_tables()
        except ValueError:
            widget.text = str(previous_research_speed)

    
    def change_checkboxes_based_on_policies(self, only_effects=False):
        policies_and_effects = self.parent.research.get_current_policies_and_effects_for_checkboxes()
        effects_dict = {position: value[1] for position, value in policies_and_effects.items()}
        self.policy_screen.show_tech_effects_of_policies(effects_dict)
        if only_effects:
            return
        policy__dict = {position: value[0] for position, value in policies_and_effects.items()}
        self.policy_screen.change_policy_choices(policy__dict)

    def change_policies_based_on_checkboxes(self, name, position):
        self.parent.research.change_minister_or_idea(position, name)
        # update effects
        self.change_checkboxes_based_on_policies(True)
        self.update_tables()
        self.parent.save_status()
    
    def change_bankrupt_status(self, is_bankrupt):
        self.parent.research.teams_get_paid = 1 - is_bankrupt
        self.update_tables()
        self.parent.save_status()
    
    def set_bankrupt_status(self, is_bankrupt):
        self.policy_screen.set_bankrupt_status(is_bankrupt)

    
    def update_statusbar_from_research(self):
        research = self.parent.research
        for country_code in research.countries:
            self.add_country_ui_updates(country_code)
        self.year_input.text = str(research.year)
        self.difficulty_button.text = get_the_other_difficulty(research.constants.current_difficulty_string)
        self.research_speed_input.text = str(research.research_speed)
        self.rocket_site_button.text = str(research.num_of_rocket_sites)
        # print(f"STATUSBAR UPDATED: {self.rocket_site_button.text=}")
        self.reactor_size_button.text = str(research.reactor_size)
        # print(f"STATUSBAR UPDATED: {self.reactor_size_button.text=}")
        self.change_checkboxes_based_on_policies()
        self.set_bankrupt_status(1 - research.teams_get_paid)


    def __init__(self, bg_color=(0, 0, 0, 0), **kwargs):
        super().__init__(**kwargs)

        self.bg_color = bg_color

        self.country_names = get_country_names()
        self.years = [str(year) for year in range(1933, 1953)]

        # country selection
        self.add_widget(Label(text="Country/Countries", size_hint=(0.08, 1)))
        self.country_selection_dropdown = DropDown()
        self.country_input = TextInput(size_hint=(0.13, 1), multiline=False, write_tab=False)
        self.add_widget(self.country_input)

        self.max_num_of_country_suggestions = 10

        self.country_selection_dropdown.bind(on_select=self.make_country_selection)
        self.country_input.bind(text=self.suggest_country_names)

        # self.primary_country = None

        # self.country_selected_text = Label(text="", size_hint=(0.1, 1))
        self.active_countries_dropdown = DropDown()
        # this should do nothing
        self.active_countries_dropdown.bind(on_select=test_printer)
        # country_selection_box = BoxLayout(size_hint=(0.15, 1))
        # country_selection_scrollview = ScrollView(size_hint=(None, 1), do_scroll_x=True, do_scroll_y=False)
        # self.countries_selected = BoxLayout(orientation="horizontal", size_hint=(None, 1))
        self.countries_selected = BoxLayout(orientation="horizontal", size_hint=(0.15, 1))
        self.country_buttons = dict()
        # self.active_countries_button = Button(text="", on_release=self.on_active_countries_button_release, size_hint=(0.3, 1))
        self.active_countries_button = Button(text="", on_release=self.on_active_countries_button_release, size_hint=(0.3, 1))
        self.clear_countries_button = Button(text="Clear", on_release=self.on_clear_countries_button_release, size_hint=(0.2, 1))
        self.reload_countries_button = Button(text="", on_release=self.reload_countries, size_hint=(0.5, 1))
        # self.countries_selected.bind(minimum_width=self.countries_selected.setter("width"))
        # country_selection_scrollview.add_widget(self.countries_selected)
        # country_selection_box.add_widget(country_selection_scrollview)
        # self.add_widget(country_selection_box)
        self.add_widget(self.countries_selected)

        # self.add_widget(Label(text="", size_hint=(0.01, 1)))

        self.rest_of_the_statusbar = BoxLayout(orientation="horizontal", size_hint=(0.555, 1))

        self.policy_dropdown = DropDown()
        self.policy_dropdown.attach_to = self.rest_of_the_statusbar
        # self.policy_screen = PolicyScreen(bg_color=self.bg_color, size_hint_y=None, height=dp(400))
        self.policy_screen = PolicyScreen(bg_color=self.policyscreen_bg_color, size_hint_y=None, height=dp(400))

        self.policy_dropdown.add_widget(self.policy_screen)

        

        self.rest_of_the_statusbar.add_widget(Label(text="", size_hint=(0.02, 1)))
        self.extra_bonus_button = Button(text="Ministers & Ideas", size_hint=(0.1, 1))
        self.extra_bonus_button.bind(on_release=lambda x: self.policy_dropdown.open(self.rest_of_the_statusbar))
        self.rest_of_the_statusbar.add_widget(self.extra_bonus_button)

        # difficulty selection
        self.difficulty_suggestions = tuple(d for d, _ in DIFFICULTIES)

        self.difficulty_dropdown = DropDown()
        for diff in self.difficulty_suggestions:
            btn = Button(text=diff, size_hint=(1, None), height=dp(25))
            btn.bind(on_release=lambda b: self.difficulty_dropdown.select(b.text))
            self.difficulty_dropdown.add_widget(btn)

        self.rest_of_the_statusbar.add_widget(Label(text="Difficulty", size_hint=(0.04, 1)))
        self.difficulty_button = Button(text="Easy", size_hint=(0.05, 1))
        self.difficulty_button.bind(on_release=self.difficulty_dropdown.open)
        # self.difficulty_dropdown.bind(on_select=lambda instance, value: setattr(self.difficulty_button, "text", value))
        self.difficulty_dropdown.bind(on_select=self.select_difficulty)

        self.rest_of_the_statusbar.add_widget(self.difficulty_button)

        # year selection
        self.rest_of_the_statusbar.add_widget(Label(text="Year", size_hint=(0.035, 1)))
        self.year_selection_dropdown = DropDown()
        for year in self.years:
            # label = Label(text=str(year), size_hint=(1, None), height=dp(20))
            label = TextInput(text=year, readonly=True, multiline=False, write_tab=False, size_hint_y=None, height=dp(25))
            label.bind(focus=lambda w, v: self.year_selection_dropdown.select(w.text))
            # label.bind(focus=test_printer)
            self.year_selection_dropdown.add_widget(label)
        self.year_input = TextInput(text="this should not be visible", size_hint=(0.04, 1), multiline=False, write_tab=False)
        # self.year_input.bind(text=lambda w, v: self.year_selection_dropdown.open(w))
        self.year_input.bind(focus=self.open_year_selection_dropdown)
        self.year_input.bind(text=self.validate_year)
        self.year_selection_dropdown.bind(on_select=self.select_year)
        self.rest_of_the_statusbar.add_widget(self.year_input)

        # research speed selection
        self.rest_of_the_statusbar.add_widget(Label(text="Research Speed", size_hint=(0.08, 1)))
        self.research_speed_input = TextInput(size_hint=(0.04, 1), multiline=False, write_tab=False)
        self.rest_of_the_statusbar.add_widget(self.research_speed_input)
        self.research_speed_input.bind(text=self.validate_research_speed)

        # # lock values checkbox
        # self.add_widget(Label(text="Lock values", size_hint=(0.1, 1)))
        # self.value_lock_checkbox = CheckBox(size_hint=(0.04, 1))
        # self.value_lock_checkbox.bind(active=self.on_checkbox_active_placeholder)
        # self.add_widget(self.value_lock_checkbox)

        # rocket sites
        self.rest_of_the_statusbar.add_widget(Label(text="Rocket sites", size_hint=(0.055, 1)))

        self.rocket_site_dropdown = DropDown()
        for i in range(11):
            btn = Button(text=str(i), size_hint=(1, None), height=dp(25))
            btn.bind(on_release=lambda b: self.rocket_site_dropdown.select(b.text))
            self.rocket_site_dropdown.add_widget(btn)

        self.rocket_site_button = Button(text="infty", size_hint=(0.02, 1))
        self.rocket_site_button.bind(on_release=self.rocket_site_dropdown.open)
        self.rocket_site_dropdown.bind(on_select=self.select_num_of_rocket_sites)
        self.rest_of_the_statusbar.add_widget(self.rocket_site_button)

        # nuclear reactor size
        self.rest_of_the_statusbar.add_widget(Label(text="Reactor size", size_hint=(0.055, 1)))

        self.reactor_size_dropdown = DropDown()
        for i in range(11):
            btn = Button(text=str(i), size_hint=(1, None), height=dp(25))
            btn.bind(on_release=lambda b: self.reactor_size_dropdown.select(b.text))
            self.reactor_size_dropdown.add_widget(btn)

        self.reactor_size_button = Button(text="infty", size_hint=(0.02, 1))
        self.reactor_size_button.bind(on_release=self.reactor_size_dropdown.open)
        self.reactor_size_dropdown.bind(on_select=self.select_reactor_size)
        self.rest_of_the_statusbar.add_widget(self.reactor_size_button)

        self.add_widget(self.rest_of_the_statusbar)


class MainFullScreen(BoxLayout):
    save_file = Path("save.data")
    statusbar_BACKGROUND_COLOR = (0, 0.3, 0.1, 0.9)

    def save_status(self):
        self.research.save_status_to_file(self.save_file)

    def update_statusbar(self):
        self.statusbar.research_speed_input.text = str(self.research.research_speed)

    def change_year(self, year):
        self.research.change_year(year)
        self.statusbar.year_input.text = str(self.research.year)
    
    # in case of not knowing what to do
    def reset_year(self):
        self.change_year(self.research.DEFAULT_YEAR)
    

    def set_research_speed(self, research_speed):
        self.research.research_speed = research_speed
        self.statusbar.research_speed_input.text = str(self.research.research_speed)
    
    # just in case
    def reset_research_speed(self):
        self.set_research_speed(self.research.DEFAULT_RESEARCH_SPEED)


    def add_country(self, country_code):
        update_tech = self.research.primary_country is None
        self.research.add_country(country_code)
        # self.statusbar.add_country(country_code)
        self.update_statusbar()
        if update_tech:
            self.mainscreen.techscreen.maintechscreen.update_technology_buttons(self.research)
            if (t := self.current_tech) is not None:
                self.mainscreen.techscreen.techinfopanel.techinfopanel.update_info(t.tech_id, t.name, t.components, t.tech_id in self.research.blueprints)

    def remove_country(self, country_code):
        self.research.remove_country(country_code)
    
    def load_status(self):
        try:
            self.research.load_status_from_file(self.save_file)
        except KeyError:
            pass
        # print(f"LOADED STATUS: {self.research.num_of_rocket_sites=}")
        self.statusbar.update_statusbar_from_research()
        self.mainscreen.techscreen.maintechscreen.update_technology_buttons(self.research)

    # KEYBOARD SHORTCUTS
    def _on_keyboard_down(self, keyboard, keycode, some_number, text, modifiers):
        # ctrl + c to complete
        if keycode == 99 and "ctrl" in modifiers:
            self.mainscreen.techscreen.complete_until_tech()
        # ctrl + f to force complete
        elif keycode == 102 and "ctrl" in modifiers:
            self.mainscreen.techscreen.complete_tech()
        # ctrl + u to undo
        elif keycode == 117 and "ctrl" in modifiers:
            self.mainscreen.techscreen.undo_tech()
        # ctrl + r to reload country
        elif keycode == 114 and "ctrl" in modifiers:
            self.statusbar.reload_countries(self.statusbar.reload_countries_button)
        # 1 2 3 to change the view top left
        elif keycode == 49 and "ctrl" in modifiers:
            self.mainscreen.teamscreen.change_upperteamscreen_by_index(0)
        elif keycode == 50 and "ctrl" in modifiers:
            self.mainscreen.teamscreen.change_upperteamscreen_by_index(1)
        elif keycode == 51 and "ctrl" in modifiers:
            self.mainscreen.teamscreen.change_upperteamscreen_by_index(2)
        # else:
        #     print(f"{keycode=}")
        #     print(f"{text=}")
        #     print(f"{modifiers=}")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.research = Research()
        self.research = the_research

        self.current_tech = None
        self.current_team = None

        self.mainscreen = MainScreen(orientation="horizontal", size_hint=(1, 0.96))
        self.statusbar = StatusBar(orientation="horizontal", size_hint=(1, 0.04), bg_color=self.statusbar_BACKGROUND_COLOR)

        

        # self.statusbar.year_input.text = str(self.research.year)
        # self.statusbar.research_speed_input.text = str(self.research.research_speed)
        # self.statusbar.rocket_site_button.text = str(self.research.num_of_rocket_sites)
        
        self.add_widget(self.mainscreen)
        self.add_widget(self.statusbar)

        with self.statusbar.canvas.before:
            Color(*self.statusbar_BACKGROUND_COLOR)
            self.statusbar.rect = Rectangle(size=self.statusbar.size, pos=self.statusbar.pos)
        self.statusbar.bind(pos=update_layout, size=update_layout)

        self.mainscreen.techscreen.research = self.research

        self.load_status()

        # self.statusbar.load_country_difficulty_and_year()

        Window.bind(on_key_down=self._on_keyboard_down)


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

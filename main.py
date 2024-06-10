
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
    "Very Easy": -1,
    "Easy": 0,
    "Normal": 1,
    "Hard": 2,
    "Very Hard": 3
}

TECH_CATEGORIES = (
            ("infantry", "Infantry"),
            ("armor", "Armor & Artillery"),
            ("naval", "Naval"),
            ("aircraft", "Aircraft"),
            (None, "Overview"),
            ("industry", "Industrial"),
            ("land_doctrines", "Land Doctrine"),
            ("secret_weapons", "Secret Weapons"),
            ("naval_doctrines", "Naval Docrine"),
            ("air_doctrines", "Air Doctrine")
)

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


class UpperTeamScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="UpperTeamScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))


# class TeamComparisonTable(GridLayout):
class TeamComparisonTable(BoxLayout):
    NUM_OF_ROWS = 10

    def row_color(self, row_num):
        if row_num % 2 == 0:
            return (0.2, 0.2, 0.2, 1)
        return (0.2, 0, 0.2, 1)
    
    def update_boxlayout(self, widget, value):
        widget.rect.pos = widget.pos
        widget.rect.size = widget.size
    
    def fill_comparison_table(self, teams_and_times):
        for i, team_and_time in enumerate(teams_and_times[:self.NUM_OF_ROWS]):
            self.labels[2*i].text = team_and_time[0].name
            self.labels[2*i+1].text = str(team_and_time[1])
        if len(teams_and_times) < self.NUM_OF_ROWS:
            for i in range(len(teams_and_times), self.NUM_OF_ROWS):
                self.labels[2*i].text = ""
                self.labels[2*i+1].text = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        header_line = BoxLayout(size_hint=(1, 0.09))
        header_line.add_widget(Label(text="Team", size_hint=(0.8, 1)))
        header_line.add_widget(Label(text="Days", size_hint=(0.2, 1)))
        self.add_widget(header_line)

        lines = [BoxLayout(size_hint=(1, 0.09)) for _ in range(self.NUM_OF_ROWS)]
        for line in lines:
            self.add_widget(line)

        self.table = [BoxLayout(size_hint=(0.5 + (-1)**(i) * 0.3, 1)) for i in range(2 * self.NUM_OF_ROWS)]
        for i, layout in enumerate(self.table):
            lines[i // 2].add_widget(layout)
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
        self.upperteamscreen = UpperTeamScreen(orientation="vertical", size_hint=(1, 0.5))
        self.add_widget(self.upperteamscreen)

        # self.comparisontable = TeamComparisonTable(cols=2, size_hint=(1, 0.5))
        self.comparisontable = TeamComparisonTable(size_hint=(1, 0.5))
        self.add_widget(self.comparisontable)
        


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
    def update_info(self, tech_id, tech_name, tech_components, has_blueprint):
        self.technology_name.text = f"{tech_id} {tech_name}"

        self.blueprint_checkbox.active = has_blueprint
    
    def on_blueprint_checkbox_active(self, widget, value):
        tech_id = self.parent.parent.parent.parent.current_tech.tech_id
        if value:
            self.parent.parent.parent.parent.research.blueprints.add(tech_id)
            self.parent.parent.maintechscreen.technologies[tech_id].add_blueprint()
        else:
            if tech_id in self.parent.parent.parent.parent.research.blueprints:
                self.parent.parent.parent.parent.research.blueprints.remove(tech_id)
                self.parent.parent.maintechscreen.technologies[tech_id].remove_blueprint()
        # redo the calculations
        self.parent.parent.parent.show_fastest_teams(self.parent.parent.parent.parent.current_tech)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.technology_name = Label(text="Technology name", size_hint=(1, 0.4))
        self.add_widget(self.technology_name)

        # TODO
        self.tech_components = Label(text="Tech components go here", size_hint=(1, 0.4))
        self.add_widget(self.tech_components)

        # TODO
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
    def show_reqs_and_deacts(self, requirements, deactivations):
        self.clear_widgets()
        if requirements:
            self.add_widget(Label(text="Requirements:", size_hint=(1, None), height=dp(20), color=(1, 1, 0, 1)))
            for requirement in requirements:
                self.add_widget(Label(text=requirement, size_hint=(1, None), height=dp(20)))

        if deactivations:
            self.add_widget(Label(text="Deactivates:", size_hint=(1, None), height=dp(20), color=(1, 0, 0, 1)))
            for deactivation in deactivations:
                self.add_widget(Label(text=deactivation, size_hint=(1, None), height=dp(20)))

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

        self.force_complete_button = Button(text="Force Complete Tech", on_release=self.force_complete_button_pressed, size_hint=(0.4, 0.4))
        self.add_widget(self.force_complete_button)

        # empty
        # self.add_widget(Label(text=" "))

        self.clear_button = Button(text="Clear everything", on_release=self.clear_button_pressed, size_hint=(0.4, 0.4))
        self.add_widget(self.clear_button)


class MainTechScreen(FloatLayout):
    def select_technology(self, widget):
        self.parent.parent.select_technology_by_id(widget.parent.tech_id)
        # print(widget.parent.tech_id)

    def __init__(self, **kwargs):
        # self.TECHNOLOGYBUTTON_SIZE = (0.175, 0.04)
        super().__init__(**kwargs)
        # self.add_widget(Label(text="MainTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))

        # self.add_widget(TechnologyButton("Prioritize Infantry", has_blueprint=True, pos_hint={"x": 0.05, "y": 0.05}))
        # self.add_widget(TechnologyButton("Prioritize Quality", pos_hint={"x": 0.05, "y": 0.1}))
        # self.add_widget(TechnologyButton("Int./Fighter Prototypes", pos_hint={"x": 0.05, "y": 0.15}))


class InfantryTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        # self.add_widget(Label(text="InfantryTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))

        # for tb in self.technologies.values():
        #     self.add_widget(tb)
        #     tb.technology.bind(on_release=self.select_technology)


class ArmorTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="ArmorTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class NavalTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="NavalTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class AircraftTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="AircraftTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class OverviewTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="OverviewTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class IndustryTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="IndustryTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class LandDoctrineTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="LandDoctrineTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class SecretWeaponTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="SecretWeaponTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class NavalDoctrineTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="NavalDoctrineTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class AirDoctrineTechScreen(MainTechScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder text
        self.add_widget(Label(text="AirDoctrineTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


class MainTechScreen_BoxLayout(BoxLayout):
    def select_technology(self, widget):
        self.parent.select_technology_by_id(widget.parent.tech_id)

    def show_requirements(self, required_tech_ids):
        for tech_id in required_tech_ids:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.show_as_requirement()
            # self.technologies[tech_id].show_as_requirement()
        self.old_requirements = required_tech_ids
    
    def hide_old_requirements(self):
        for tech_id in self.old_requirements:
            tech_btn = self.technologies.get(tech_id)
            if tech_btn is not None:
                tech_btn.hide_requirement()
    
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
            return
        lower_id = (i + 1) * 1000 if i < 4 else i * 1000
        for tech_id, tech_btn in self.technologies.items():
            if tech_id >= lower_id and tech_id < lower_id + 1000:
                layout.add_widget(tech_btn)
    
    def update_technology_buttons(self, research_object):
        for tech_id, tech_button in self.technologies.items():
            if tech_id in research_object.blueprints:
                tech_button.add_blueprint()
            if tech_id in research_object.completed_techs:
                tech_button.complete()
                continue
            if tech_id in research_object.active_techs:
                tech_button.activate()
                continue
            if tech_id in research_object.deactivated_techs:
                tech_button.deactivate()
                continue
            tech_button.reset_color()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Label(text="MainTechScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))

        self.old_requirements = []
        self.old_deactivations = []

        # self.tech_buttons = dict()
        sg_x = 0
        inf_x = 0.18
        third_x = 0.38
        mnt_x = 0.58
        fifth_x = 0.8
        self.technologies = {
            # small guns
            1010: TechnologyButton("Basic SMG", 1010, pos_hint={"x": sg_x, "y": 0.91}),
            1020: TechnologyButton("Improved SMG", 1020, pos_hint={"x": sg_x, "y": 0.875}),
            1030: TechnologyButton("Basic Machine Gun", 1030, pos_hint={"x": sg_x, "y": 0.84}),
            1040: TechnologyButton("Improved MG", 1040, pos_hint={"x": sg_x, "y": 0.805}),
            1050: TechnologyButton("Advanced MG", 1050, pos_hint={"x": sg_x, "y": 0.77}),
            1060: TechnologyButton("Modern MG", 1060, pos_hint={"x": sg_x, "y": 0.735}),

            # infantry
            1070: TechnologyButton("WWI Infantry", 1070, pos_hint={"x": inf_x, "y": 0.96}),
            1080: TechnologyButton("Post-WWI", 1080, pos_hint={"x": inf_x, "y": 0.925}),
            1090: TechnologyButton("Basic", 1090, pos_hint={"x": inf_x, "y": 0.885}),
            1100: TechnologyButton("Improved", 1100, pos_hint={"x": inf_x, "y": 0.845}),
            1110: TechnologyButton("Advanced", 1110, pos_hint={"x": inf_x, "y": 0.805}),
            1120: TechnologyButton("Semi-Professional", 1120, pos_hint={"x": inf_x, "y": 0.765}),
            1130: TechnologyButton("Professional", 1130, pos_hint={"x": inf_x, "y": 0.725}),
            1140: TechnologyButton("Modern", 1140, pos_hint={"x": inf_x, "y": 0.685}),

            # cavalry
            1260: TechnologyButton("Basic Cavalry", 1260, pos_hint={"x": sg_x, "y": 0.665}),
            1270: TechnologyButton("Semi-Motorized I", 1270, pos_hint={"x": sg_x + 0.01, "y": 0.63}),
            1280: TechnologyButton("Semi-Motorized II", 1280, pos_hint={"x": sg_x + 0.01, "y": 0.595}),
            1290: TechnologyButton("Semi-Mechanized I", 1290, pos_hint={"x": sg_x + 0.01, "y": 0.56}),
            1760: TechnologyButton("Semi-Mechanized II", 1760, pos_hint={"x": sg_x + 0.01, "y": 0.525}),
			
			# light vehicle
			1390: TechnologyButton("Light Vehicle", 1390, pos_hint={"x": sg_x, "y": 0.26}),

            # mechanized
            1440: TechnologyButton("Basic Mechanized", 1440, pos_hint={"x": sg_x, "y": 0.205}),
            1450: TechnologyButton("Average", 1450, pos_hint={"x": sg_x, "y": 0.17}),
            1460: TechnologyButton("Advanced", 1460, pos_hint={"x": sg_x, "y": 0.135}),
            1470: TechnologyButton("Semi-Modern", 1470, pos_hint={"x": sg_x, "y": 0.1}),

            # motorized
            1400: TechnologyButton("Basic Motorized", 1400, pos_hint={"x": inf_x, "y": 0.205}),
            1410: TechnologyButton("Average", 1410, pos_hint={"x": inf_x, "y": 0.17}),
            1420: TechnologyButton("Advanced", 1420, pos_hint={"x": inf_x, "y": 0.135}),
            1430: TechnologyButton("Semi-Modern", 1430, pos_hint={"x": inf_x, "y": 0.1}),
			
			# marines
			1300: TechnologyButton("Pre-war Marine", 1300, pos_hint={"x": inf_x, "y": 0.6}),
			1310: TechnologyButton("Basic", 1310, pos_hint={"x": inf_x, "y": 0.565}),
			1320: TechnologyButton("Average", 1410, pos_hint={"x": inf_x, "y": 0.53}),
			1330: TechnologyButton("Improved", 1410, pos_hint={"x": inf_x, "y": 0.495}),
			1340: TechnologyButton("Advanced", 1410, pos_hint={"x": inf_x, "y": 0.46}),
			
			# specialiation and equipment
			1150: TechnologyButton("Specialized Units", 1150, pos_hint={"x": third_x, "y": 0.91}),

			1160: TechnologyButton("Winter I", 1160, pos_hint={"x": third_x, "y": 0.85}),
			1170: TechnologyButton("Winter II", 1170, pos_hint={"x": third_x + 0.02, "y": 0.815}),

			1180: TechnologyButton("Desert I", 1180, pos_hint={"x": third_x, "y": 0.765}),
			1190: TechnologyButton("Desert II", 1190, pos_hint={"x": third_x + 0.02, "y": 0.73}),

			1200: TechnologyButton("Jungle I", 1200, pos_hint={"x": third_x, "y": 0.68}),
			1210: TechnologyButton("Jungle II", 1210, pos_hint={"x": third_x + 0.02, "y": 0.645}),
			
			# mountain
			1220: TechnologyButton("Mountain I", 1220, pos_hint={"x": mnt_x, "y": 0.96}),
			1230: TechnologyButton("Mountain II", 1230, pos_hint={"x": mnt_x, "y": 0.925}),
			1240: TechnologyButton("Mountain III", 1240, pos_hint={"x": mnt_x, "y": 0.89}),
			1250: TechnologyButton("Mountain IV", 1250, pos_hint={"x": mnt_x, "y": 0.855}),
			
			# paratroopers
			1350: TechnologyButton("Paratrooper studies", 1350, pos_hint={"x": mnt_x, "y": 0.8}),
			1360: TechnologyButton("Paratrooper I", 1360, pos_hint={"x": mnt_x, "y": 0.765}),
			1370: TechnologyButton("Paratrooper II", 1370, pos_hint={"x": mnt_x, "y": 0.73}),
			1380: TechnologyButton("Paratrooper III", 1380, pos_hint={"x": mnt_x, "y": 0.695}),
			
			# logistics
			1490: TechnologyButton("Supply Logistics", 1490, pos_hint={"x": third_x, "y": 0.5}),
			1500: TechnologyButton("Concentrated", 1500, pos_hint={"x": third_x, "y": 0.45}),
			1510: TechnologyButton("Logistics Planning", 1510, pos_hint={"x": third_x, "y": 0.415}),
			1520: TechnologyButton("Classification", 1520, pos_hint={"x": third_x, "y": 0.375}),
			1530: TechnologyButton("Logistical savings", 1530, pos_hint={"x": third_x, "y": 0.34}),
			
			1480: TechnologyButton("Arsenal Logistics", 1480, pos_hint={"x": mnt_x, "y": 0.5}),
			1540: TechnologyButton("Dispersed logistics", 1540, pos_hint={"x": mnt_x, "y": 0.45}),
			1550: TechnologyButton("Small warehouses", 1550, pos_hint={"x": mnt_x, "y": 0.415}),
			1560: TechnologyButton("Supply Vehicles", 1560, pos_hint={"x": mnt_x, "y": 0.375}),
			1570: TechnologyButton("Frontline Supply", 1570, pos_hint={"x": mnt_x, "y": 0.34}),
			
			1580: TechnologyButton("Management Expert", 1580, pos_hint={"x": third_x + 0.1, "y": 0.29}),

            # priorization

            1590: TechnologyButton("Prioritize Quality", 1590, pos_hint={"x": inf_x + 0.02, "y": 0.37}),
            1600: TechnologyButton("Prioritize Quantity", 1600, pos_hint={"x": inf_x + 0.02, "y": 0.33}),

            1610: TechnologyButton("Prioritize Mobility", 1610, pos_hint={"x": sg_x + 0.02, "y": 0.37}),
            1620: TechnologyButton("Prioritize Infantry", 1620, pos_hint={"x": sg_x + 0.02, "y": 0.33}),

            # commandos
            1630: TechnologyButton("Commando Units", 1630, pos_hint={"x": fifth_x, "y": 0.90}),
            1640: TechnologyButton("Basic", 1640, pos_hint={"x": fifth_x, "y": 0.86}),
            1650: TechnologyButton("Improved", 1650, pos_hint={"x": fifth_x, "y": 0.82}),
            1660: TechnologyButton("Advanced", 1660, pos_hint={"x": fifth_x, "y": 0.78}),

            # electronic warfare
            1670: TechnologyButton("Electronic Warfare", 1670, pos_hint={"x": fifth_x, "y": 0.5}),
            1680: TechnologyButton("Jamming Enemy", 1680, pos_hint={"x": fifth_x, "y": 0.45}),
            1690: TechnologyButton("Intercept Radio", 1690, pos_hint={"x": fifth_x, "y": 0.4}),
            1700: TechnologyButton("False Decoys", 1700, pos_hint={"x": fifth_x, "y": 0.35}),
            1710: TechnologyButton("Signal Detection", 1710, pos_hint={"x": fifth_x, "y": 0.3}),
            1720: TechnologyButton("High Frequency", 1720, pos_hint={"x": fifth_x, "y": 0.25}),
            1730: TechnologyButton("Detection", 1730, pos_hint={"x": fifth_x, "y": 0.2}),
            1740: TechnologyButton("Triangulation", 1740, pos_hint={"x": fifth_x, "y": 0.15}),
            1750: TechnologyButton("Advanced Jamming", 1750, pos_hint={"x": fifth_x, "y": 0.1})
		}

        for tb in self.technologies.values():
            # self.add_widget(tb)
            tb.technology.bind(on_release=self.select_technology)

        self.category_layouts = {
            TECH_CATEGORIES[0][1]: InfantryTechScreen(),
            TECH_CATEGORIES[1][1]: ArmorTechScreen(),
            TECH_CATEGORIES[2][1]: NavalTechScreen(),
            TECH_CATEGORIES[3][1]: AircraftTechScreen(),
            TECH_CATEGORIES[4][1]: OverviewTechScreen(),
            TECH_CATEGORIES[5][1]: IndustryTechScreen(),
            TECH_CATEGORIES[6][1]: LandDoctrineTechScreen(),
            TECH_CATEGORIES[7][1]: SecretWeaponTechScreen(),
            TECH_CATEGORIES[8][1]: NavalDoctrineTechScreen(),
            TECH_CATEGORIES[9][1]: AirDoctrineTechScreen()
        }

        for i, layout in enumerate(self.category_layouts.values()):
            self.add_technology_buttons(i, layout)

        self.current_layout = self.category_layouts["Infantry"]
        self.add_widget(self.current_layout)


class TechInfoPanels(BoxLayout):
    BACKGROUND_COLOR2 = (0.1, 0.1, 0.1, 1)

    # def update_panel(self, widget, value):
    #     widget.rect.pos = widget.pos
    #     widget.rect.size = widget.size

    def update_tech_info(self, tech, has_blueprint, requirements, deactivations, effects):
        self.techinfopanel.update_info(tech.tech_id, tech.name, tech.components, has_blueprint)

        self.requirement_panel.show_reqs_and_deacts(requirements, deactivations)

        self.effects_panel.show_effects(effects)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.techinfopanel = TechInfoPanel(orientation="vertical", size_hint=(0.25, 1))
        self.add_widget(self.techinfopanel)
        with self.techinfopanel.canvas.before:
            Color(*self.BACKGROUND_COLOR2)
            self.techinfopanel.rect = Rectangle(size=self.techinfopanel.size, pos=self.techinfopanel.pos)
        self.techinfopanel.bind(pos=update_layout, size=update_layout)

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
        self.extra_layout.bind(pos=update_layout, size=update_layout)

        self.add_widget(ResearchButtonsPanel(cols=2, padding=(dp(5), dp(5), dp(5), dp(5)), spacing=dp(10), size_hint=(0.25, 1)))
        # for i in range(4):
        #     self.add_widget(Button(text=f"InfoPanel {i+1}", size_hint=(0.25, 1)))


class TechScreen(BoxLayout):

    def select_category(self, category):
        if category == self.active_category:
            return
        self.active_category = category
        self.maintechscreen.change_layout(category)
    
    def select_technology_by_id(self, tech_id):
        # category = get_the_other_category(self.active_category)
        tech = self.parent.parent.research.get_tech(tech_id)
        self.parent.parent.current_tech = tech
        # print(f"{tech.tech_id} {tech.name}")

        # sort teams based on who is fastest
        self.parent.show_fastest_teams(tech)
        # sorted_teams = self.parent.parent.research.sort_teams_for_researching_tech(tech)
        # self.parent.teamscreen.comparisontable.fill_comparison_table(sorted_teams)

        # update infopanels
        requirements = self.parent.parent.research.list_requirements(tech)
        deactivations = self.parent.parent.research.list_deactivations(tech)
        effects = self.parent.parent.research.list_effects(tech)
        has_blueprint = tech.tech_id in self.parent.parent.research.blueprints
        self.techinfopanel.update_tech_info(tech, has_blueprint, requirements, deactivations, effects)

        # update tech buttons
        self.maintechscreen.hide_old_requirements()
        self.maintechscreen.hide_old_deactivation_warnings()

        req_ids = [int(line.split(" ")[0].strip("*")) for line in requirements]
        deact_ids = [int(line.split(" ")[0].strip("*")) for line in deactivations]
        self.maintechscreen.show_requirements(req_ids)
        self.maintechscreen.show_deactivation_warnings(deact_ids)
    
    def complete_until_tech(self):
        tech_id = self.parent.parent.current_tech.tech_id
        self.parent.parent.research.complete_until_tech(tech_id)
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.parent.parent.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.parent.parent.research.research_speed)

    def complete_tech(self):
        tech_id = self.parent.parent.current_tech.tech_id
        if tech_id in self.parent.parent.research.completed_techs:
            return
        self.parent.parent.research.complete_tech(tech_id)
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.parent.parent.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.parent.parent.research.research_speed)
    
    def undo_tech(self):
        tech_id = self.parent.parent.current_tech.tech_id
        if tech_id not in self.parent.parent.research.completed_techs:
            return
        self.parent.parent.research.undo_completed_tech(tech_id)
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.parent.parent.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.parent.parent.research.research_speed)

    def clear_tech(self):
        self.parent.parent.research.clear_all_tech()
        # update tech buttons
        self.maintechscreen.update_technology_buttons(self.parent.parent.research)
        # update research speed
        self.parent.parent.statusbar.research_speed_input.text = str(self.parent.parent.research.research_speed)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.active_category = TECH_CATEGORIES[0][1]

        self.techcategories = TechCategories(cols=5, size_hint=(1, 0.05))
        self.maintechscreen = MainTechScreen_BoxLayout(size_hint=(1, 0.80))
        self.techinfopanel = TechInfoPanels(orientation="horizontal", size_hint=(1, 0.15))
        self.add_widget(self.techcategories)
        self.add_widget(self.maintechscreen)
        self.add_widget(self.techinfopanel)


class MainScreen(BoxLayout):

    def show_fastest_teams(self, tech):
        sorted_teams = self.parent.research.sort_teams_for_researching_tech(tech)
        self.teamscreen.comparisontable.fill_comparison_table(sorted_teams)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Button(text="MainScreen", size_hint=(1, 1)))
        self.techscreen = TechScreen(orientation="vertical", size_hint=(0.8, 1))
        self.teamscreen = TeamScreen(orientation="vertical", size_hint=(0.2, 1))
        self.add_widget(self.teamscreen)
        self.add_widget(self.techscreen)


class StatusBar(BoxLayout):
    def select_difficulty(self, widget, value):
        # setattr(self.difficulty_button, "text", value)
        self.difficulty_button.text = value
        self.parent.research.difficulty = DIFFICULTY_DICT[value]

    def select_year(self, widget, value):
        # previous_year = self.year_input.select_all()
        try:
            self.parent.change_year(int(value))
            self.year_input.text = value
        except ValueError:
            self.year_input.text = str(self.parent.research.year)

    
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
            print(f"Values are locked by checkbox {checkbox} (NOT REALLY, THIS DOES NOTHING)")
        else:
            print(f"Values are not locked by checkbox {checkbox} (THIS DOES NOTHING)")
    

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
    
    def validate_research_speed(self, widget, text):
        if not text:
            return
        if self.parent is None:
            return
        previous_research_speed = self.parent.research.research_speed
        try:
            new_research_speed = float(text)
            self.parent.research.research_speed = new_research_speed
        except ValueError:
            widget.text = str(previous_research_speed)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.country_names = get_country_names()
        self.years = list(range(1933, 1953))

        # country selection
        self.add_widget(Label(text="Country/Countries", size_hint=(0.12, 1)))
        self.country_selection_dropdown = DropDown()
        self.country_input = TextInput(size_hint=(0.13, 1), multiline=False, write_tab=False)
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
        self.difficulty_button = Button(text="Easy", size_hint=(0.05, 1))
        self.difficulty_button.bind(on_release=self.difficulty_dropdown.open)
        # self.difficulty_dropdown.bind(on_select=lambda instance, value: setattr(self.difficulty_button, "text", value))
        self.difficulty_dropdown.bind(on_select=self.select_difficulty)

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
        self.year_input = TextInput(text="this should not be visible", size_hint=(0.05, 1), multiline=False, write_tab=False)
        # self.year_input.bind(text=lambda w, v: self.year_selection_dropdown.open(w))
        self.year_input.bind(focus=self.open_year_selection_dropdown)
        self.year_selection_dropdown.bind(on_select=self.select_year)
        self.add_widget(self.year_input)

        # research speed selection
        self.add_widget(Label(text="Research Speed", size_hint=(0.1, 1)))
        self.research_speed_input = TextInput(size_hint=(0.05, 1), multiline=False, write_tab=False)
        self.add_widget(self.research_speed_input)
        self.research_speed_input.bind(text=self.validate_research_speed)

        # lock values checkbox
        self.add_widget(Label(text="Lock values", size_hint=(0.1, 1)))
        self.value_lock_checkbox = CheckBox(size_hint=(0.04, 1))
        self.value_lock_checkbox.bind(active=self.on_checkbox_active_placeholder)
        self.add_widget(self.value_lock_checkbox)


class MainFullScreen(BoxLayout):
    statusbar_BACKGROUND_COLOR = (0, 0.3, 0.1, 0.7)

    def update_statusbar(self):
        self.statusbar.research_speed_input.text = str(self.research.research_speed)

    def change_year(self, year):
        self.research.year = year
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

    def remove_country(self, country_code):
        self.research.remove_country(country_code)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.research = Research()
        self.research = the_research

        self.current_tech = None

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

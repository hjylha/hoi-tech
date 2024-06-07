
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
    SIZE_HINT = (0.16, 0.035)
    
    # COLORS

    def add_blueprint(self):
        self.blueprint_label.text = "B"
    
    def remove_blueprint(self):
        self.blueprint_label.text = ""

    def show_as_requirement(self):
        self.requirement_label.text = "R"
    
    def hide_requirement(self):
        self.requirement_label.text = ""

    def __init__(self, tech_short_name, tech_id, has_blueprint=False, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"

        self.size_hint = self.SIZE_HINT

        self.tech_id = tech_id

        requirement_box = BoxLayout(size_hint=(0.1, 1))
        self.requirement_label = Label(text="")
        requirement_box.add_widget(self.requirement_label)

        self.technology = Button(text=tech_short_name, size_hint=(0.8, 1), background_color=(0.4, 0.8, 0.2, 0.7))

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.technology_name = Label(text="Technology name", size_hint=(1, 0.4))
        self.add_widget(self.technology_name)

        # TODO
        self.tech_components = Label(text="Tech components go here", size_hint=(1, 0.4))
        self.add_widget(self.tech_components)

        # TODO
        self.blueprint_checkbox = Label(text="blueprint checkbox maybe", size_hint=(1, 0.2))
        self.add_widget(self.blueprint_checkbox)
    

class RequirementPanel(BoxLayout):
    # requirement_header = 
    def show_reqs_and_deacts(self, requirements, deactivations):
        self.clear_widgets()

        self.add_widget(Label(text="Requirements", size_hint=(1, None), height=dp(20)))
        for requirement in requirements:
            self.add_widget(Label(text=requirement, size_hint=(1, None), height=dp(20)))

        self.add_widget(Label(text="Deactivates", size_hint=(1, None), height=dp(20)))
        for deactivation in deactivations:
            self.add_widget(Label(text=deactivation, size_hint=(1, None), height=dp(20)))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Requirements", size_hint=(1, 0.25)))
        self.add_widget(Label(text="...", size_hint=(1, 0.25)))
        self.add_widget(Label(text="Deactivates", size_hint=(1, 0.25)))
        self.add_widget(Label(text="...", size_hint=(1, 0.25)))


class EffectsPanel(BoxLayout):
    def show_effects(self, effects):
        self.clear_widgets()

        self.add_widget(Label(text="Effects", size_hint=(1, None), height=dp(20)))
        for effect in effects:
            self.add_widget(Label(text=effect, size_hint=(1, None), height=dp(20)))


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
        self.add_widget(Label(text="InfantryTechScreen", size_hint=(0.05, 0.05), pos_hint={"center_x": 0.5, "center_y": 0.5}))


        sg_x = 0
        inf_x = 0.18

        self.technologies = [
            # small guns
            TechnologyButton("Basic SMG", 1010, pos_hint={"x": sg_x, "y": 0.91}),
            TechnologyButton("Improved SMG", 1020, pos_hint={"x": sg_x, "y": 0.875}),
            TechnologyButton("Basic Machine Gun", 1030, pos_hint={"x": sg_x, "y": 0.84}),
            TechnologyButton("Improved MG", 1040, pos_hint={"x": sg_x, "y": 0.805}),
            TechnologyButton("Advanced MG", 1050, pos_hint={"x": sg_x, "y": 0.77}),
            TechnologyButton("Modern MG", 1060, pos_hint={"x": sg_x, "y": 0.735}),

            # infantry
            TechnologyButton("WWI Infantry", 1070, pos_hint={"x": inf_x, "y": 0.96}),
            TechnologyButton("Post-WWI", 1080, pos_hint={"x": inf_x, "y": 0.925}),
            TechnologyButton("Basic", 1090, pos_hint={"x": inf_x, "y": 0.885}),
            TechnologyButton("Improved", 1100, pos_hint={"x": inf_x, "y": 0.845}),
            TechnologyButton("Advanced", 1110, pos_hint={"x": inf_x, "y": 0.805}),
            TechnologyButton("Semi-Professional", 1120, pos_hint={"x": inf_x, "y": 0.765}),
            TechnologyButton("Professional", 1130, pos_hint={"x": inf_x, "y": 0.725}),
            TechnologyButton("Modern", 1140, pos_hint={"x": inf_x, "y": 0.685}),

            # cavalry
            TechnologyButton("Basic Cavalry", 1260, pos_hint={"x": sg_x, "y": 0.665}),
            TechnologyButton("Semi-Motorized I", 1270, pos_hint={"x": sg_x + 0.01, "y": 0.63}),
            TechnologyButton("Semi-Motorized II", 1280, pos_hint={"x": sg_x + 0.01, "y": 0.595}),
            TechnologyButton("Semi-Mechanized I", 1290, pos_hint={"x": sg_x + 0.01, "y": 0.56}),
            TechnologyButton("Semi-Mechanized II", 1760, pos_hint={"x": sg_x + 0.01, "y": 0.525}),

            # mechanized
            TechnologyButton("Basic Mechanized", 1440, pos_hint={"x": sg_x, "y": 0.205}),
            TechnologyButton("Average", 1450, pos_hint={"x": sg_x, "y": 0.17}),
            TechnologyButton("Advanced", 1460, pos_hint={"x": sg_x, "y": 0.135}),
            TechnologyButton("Semi-Modern", 1470, pos_hint={"x": sg_x, "y": 0.1}),

            # motorized
            TechnologyButton("Basic Motorized", 1400, pos_hint={"x": inf_x, "y": 0.205}),
            TechnologyButton("Average", 1410, pos_hint={"x": inf_x, "y": 0.17}),
            TechnologyButton("Advanced", 1420, pos_hint={"x": inf_x, "y": 0.135}),
            TechnologyButton("Semi-Modern", 1430, pos_hint={"x": inf_x, "y": 0.1}),
        ]

        for tb in self.technologies:
            self.add_widget(tb)
            tb.technology.bind(on_release=self.select_technology)


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
    def change_layout(self, category):
        self.remove_widget(self.current_layout)
        self.current_layout = self.category_layouts[category]
        self.add_widget(self.current_layout)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget(Label(text="MainTechScreen", pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.tech_buttons = dict()

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
        # print(f"{tech.tech_id} {tech.name}")

        # sort teams based on who is fastest
        sorted_teams = self.parent.parent.research.sort_teams_for_researching_tech(tech)
        self.parent.teamscreen.comparisontable.fill_comparison_table(sorted_teams)

        # update infopanels
        requirements = self.parent.parent.research.list_requirements(tech)
        deactivations = self.parent.parent.research.list_deactivations(tech)
        effects = self.parent.parent.research.list_effects(tech)
        has_blueprint = tech.tech_id in self.parent.parent.research.blueprints
        self.techinfopanel.update_tech_info(tech, has_blueprint, requirements, deactivations, effects)

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
        self.research.add_country(country_code)
        # self.statusbar.add_country(country_code)
        self.update_statusbar()

    def remove_country(self, country_code):
        self.research.remove_country(country_code)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.research = Research()
        self.research = the_research

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

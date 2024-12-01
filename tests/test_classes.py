
from pathlib import Path

import pytest

import fix_imports
from techs_for_testing import techs_for_testing
from techteams_for_testing import techteams_for_testing
import classes


class TestHoITime:
    hoi_time = classes.HoITime()

    def test_constants(self):
        assert self.hoi_time.DEFAULT_START_DAY == 30
        assert self.hoi_time.DEFAULT_START_YEAR == 1933

    @pytest.mark.parametrize(
            "new_date", [0, 64, 256, 8128, 9999999]
    )
    def test_reset_date(self, new_date):
        self.hoi_time.date = new_date
        self.hoi_time.reset_date()
        assert self.hoi_time.date == self.hoi_time.DEFAULT_START_DAY

    @pytest.mark.parametrize(
        "date, year", [
            (1, 1933),
            (370, 1934),
            (600, 1934),
            (750, 1935),
            (1000, 1935),
            (1100, 1936),
            (1441, 1937),
            (1801, 1938),
            (2161, 1939),
            (2878, 1940),
            (2890, 1941),
            (3599, 1942),
            (4321, 1945),
            (6000, 1949),
            (7000, 1952),
            (hoi_time.DEFAULT_START_DAY, hoi_time.DEFAULT_START_YEAR)
        ]
    )
    def test_get_year(self, date, year):
        self.hoi_time.date = date
        assert self.hoi_time.get_year() == year

    @pytest.mark.parametrize(
            "date, date_str", [
                (60, "1 Mar 1933"),
                (462, "13 Apr 1934"),
                (hoi_time.DEFAULT_START_DAY, "1 Feb 1933")
            ]
    )
    def test_get_date(self, date, date_str):
        self.hoi_time.date = date
        assert self.hoi_time.get_date() == date_str

    @pytest.mark.parametrize(
            "new_year, date", [
                (1940, hoi_time.DEFAULT_START_DAY + 2520),
                (1950, hoi_time.DEFAULT_START_DAY + 6120),
                (1933, hoi_time.DEFAULT_START_DAY)
            ]
    )
    def test_change_year(self, new_year, date):
        self.hoi_time.change_year(new_year)
        assert self.hoi_time.date == date
    
    @pytest.mark.parametrize(
            "new_date", [0, 64, 256, 8128, 9999999]
    )
    def test_next_day(self, new_date):
        self.hoi_time.date = new_date
        self.hoi_time.next_day()
        assert self.hoi_time.date == new_date + 1
        self.hoi_time.next_day()
        assert self.hoi_time.date == new_date + 2

    @pytest.mark.parametrize(
            "date_str, date", [
                ("0:00 December 17, 1933", 346),
                ("0:00 January 12, 1937", 1451),
                ("0:00 August 25, 1938", 2034)
            ]
    )
    def test_date_str_to_date(self, date_str, date):
        returned_date = self.hoi_time.date_str_to_date(date_str)
        assert returned_date == date



research_speed_test_result_path = Path(__file__).parent / "research_speed_testing.csv"


def format_value(column, value):
    if column == "component":
        return value.strip().lower()
    if column in ("base difficulty", "1-day progress", "extra bonus", "tech speed modifier", "blueprint bonus"):
        return float(value.strip())
    return int(value.strip())

# @pytest.fixture
def research_speed_testing_results():
    testing_results = []
    with open(research_speed_test_result_path, "r") as f:
        for i, line in enumerate(f):
            if i == 0:
                columns = [column.strip() for column in line.split(";")]
            else:
                values = line.split(";")
                result = {column: format_value(column, value) for column, value in zip(columns, values)}
                testing_results.append(result)
    return testing_results


def get_results_for_difficulty_multipliers(testing_results):
    results = []
    for result in testing_results:
        component = classes.Component(result["component"], result["tech difficulty"])
        result_tuple = (component, result["research speed"], result["game difficulty"], result["extra bonus"], result["base difficulty"])
        results.append(result_tuple)
    return results

def get_results_for_progress_estimates(testing_results):
    results = []
    for result in testing_results:
        team = techteams_for_testing[result["techteam"]]
        component = techs_for_testing[result["tech"]].components[0]
        game_constants = classes.GameConstants(result["tech speed modifier"], result["blueprint bonus"], {}, result["game difficulty"], None)
        # research_speed = 
        result_tuple = (team, component, result["research speed"], game_constants, result["extra bonus"], result["has blueprint"], result["rocket site size"], result["reactor size"], result["has_money"], result["1-day progress"])
        results.append(result_tuple)
    return results

def get_results_for_completion_estimates(testing_results):
    results = []
    for result in testing_results:
        if not result["has_money"]:
            continue
        team = techteams_for_testing[result["techteam"]]
        tech = techs_for_testing[result["tech"]]
        game_constants = classes.GameConstants(result["tech speed modifier"], result["blueprint bonus"], {}, result["game difficulty"], None)
        result_tuple = (team, tech, result["research speed"], game_constants, result["extra bonus"], result["has blueprint"], result["rocket site size"], result["reactor size"], result["days to complete game estimate"])
        results.append(result_tuple)
    return results


research_observations = research_speed_testing_results()


@pytest.mark.parametrize(
        "component, research_speed_modifier, game_difficulty, total_extra_bonus, base_difficulty", get_results_for_difficulty_multipliers(research_observations)
        # "component, research_speed_modifier, game_difficulty, total_extra_bonus, base_difficulty", [
        #     (classes.Component("small unit tactics", 2), 90, 1, 0, 1)
        # ]
)
def test_calculate_components_difficulty_multiplier(component, research_speed_modifier, game_difficulty, total_extra_bonus, base_difficulty):
    difficulty_multiplier = classes.calculate_components_difficulty_multiplier(component, research_speed_modifier, game_difficulty, total_extra_bonus)
    assert round(20 / difficulty_multiplier, 1) == base_difficulty


@pytest.mark.parametrize(
        "team, component, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, has_money, observed_1_day_progress", get_results_for_progress_estimates(research_observations)
)
def test_1_day_progression_for_component(team, component, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, has_money, observed_1_day_progress):
    one_day_progress_estimate = team.calculate_1_day_progress_for_component(component, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, has_money)
    assert round(one_day_progress_estimate, 2) == observed_1_day_progress


@pytest.mark.parametrize(
        "team, tech, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, completion_estimate", get_results_for_completion_estimates(research_observations)
)
def test_calculate_how_many_days_to_complete(team, tech, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, completion_estimate):
    days_to_complete = team.calculate_how_many_days_to_complete(tech, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size)
    assert days_to_complete == completion_estimate

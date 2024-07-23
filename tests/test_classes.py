
from pathlib import Path

import pytest

import fix_imports
from techs_for_testing import techs_for_testing
from techteams_for_testing import techteams_for_testing
import classes


research_speed_test_result_path = Path(__file__).parent / "research_speed_testing.csv"


def format_value(column, value):
    if column == "component":
        return value.strip().lower()
    if column in ("base difficulty", "1-day progress"):
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
        # research_speed = 
        result_tuple = (team, component, result["research speed"], result["game difficulty"], result["extra bonus"], result["has blueprint"], result["rocket site size"], result["reactor size"], result["1-day progress"])
        results.append(result_tuple)
    return results

def get_results_for_completion_estimates(testing_results):
    results = []
    for result in testing_results:
        team = techteams_for_testing[result["techteam"]]
        tech = techs_for_testing[result["tech"]]
        result_tuple = (team, tech, result["research speed"], result["game difficulty"], result["extra bonus"], result["has blueprint"], result["rocket site size"], result["reactor size"], result["days to complete game estimate"])
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
        "team, component, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, observed_1_day_progress", get_results_for_progress_estimates(research_observations)
)
def test_1_day_progression_for_component(team, component, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, observed_1_day_progress):
    one_day_progress_estimate = team.calculate_1_day_progress_for_component(component, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size)
    assert round(one_day_progress_estimate, 2) == observed_1_day_progress


@pytest.mark.parametrize(
        "team, tech, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, completion_estimate", get_results_for_completion_estimates(research_observations)
)
def test_calculate_how_many_days_to_complete(team, tech, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size, completion_estimate):
    days_to_complete = team.calculate_how_many_days_to_complete(tech, research_speed, game_difficulty, total_bonus, has_blueprint, num_of_rocket_sites, reactor_size)
    assert days_to_complete == completion_estimate

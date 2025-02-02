
from pathlib import Path

import pytest

import fix_imports
from techs_for_testing import techs_for_testing
from techteams_for_testing import techteams_for_testing
import classes


@pytest.fixture(scope="module")
def game_constants():
    difficulty_dict = {'VERYEASY': 10, 'EASY': 0, 'NORMAL': -10, 'HARD': -20, 'VERYHARD': -30}
    return classes.GameConstants(2.8, 1.7, difficulty_dict)


class TestGameConstants:
    # game_constants = classes.GameConstants(2.8, 1.7, {'VERYEASY': 10, 'EASY': 0, 'NORMAL': -10, 'HARD': -20, 'VERYHARD': -30})

    def test_change_difficulty(self, game_constants):
        diff_str = "HARD"
        diff_mod = -20
        game_constants.change_difficulty(diff_str)
        assert game_constants.current_difficulty_string == diff_str
        assert game_constants.current_difficulty == diff_mod
        game_constants.change_difficulty("EASY")
        assert game_constants.current_difficulty_string == "EASY"
        assert game_constants.current_difficulty == 0
    
    def test_overwrite_difficulty_modifier(self, game_constants):
        diff_mod = 50
        game_constants.overwrite_difficulty_modifier(diff_mod)
        assert game_constants.current_difficulty == diff_mod

    def test_get_research_multiplier(self, game_constants):
        assert game_constants.get_research_multiplier(1) == 0.0476
        assert game_constants.get_research_multiplier(0) == 0.028


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


@pytest.mark.parametrize(
    "difficulty_modifier, difficulty_multiplier", [
        (10, 1.1),
        (0, 1),
        (-10, 0.9),
        (-20, 0.8),
        (-30, 0.7)
    ]
)
def test_get_game_difficulty_multiplier(difficulty_modifier, difficulty_multiplier):
    assert classes.get_game_difficulty_multiplier(difficulty_modifier) == difficulty_multiplier


@pytest.mark.parametrize(
    "policy_bonus, policy_modifier", [
        (5, 0.95),
        (10, 0.9),
        (15, 0.85),
        (20, 0.8)
    ]
)
def test_get_policy_modifier(policy_bonus, policy_modifier):
    assert classes.get_policy_modifier(policy_bonus) == policy_modifier


@pytest.mark.parametrize(
    "comp_difficulty, comp_type, difficulty_modifier", [
        (2, "small_unit_tactics", 4),
        (4, "centralized_execution", 6),
        (10, "mathematics", 12),
        (18, "nuclear_engineering", 20)
    ]
)
def test_get_tech_difficulty_modifier(comp_difficulty, comp_type, difficulty_modifier):
    component = classes.Component(comp_type, comp_difficulty)
    assert classes.get_tech_difficulty_modifier(component) == difficulty_modifier


def test_get_components_difficulty_modifiers():
    component = classes.Component("mathematics", 10)
    difficulty_modifier = -20
    policy_bonus = 10
    modifiers = classes.get_components_difficulty_modifiers(component, difficulty_modifier, policy_bonus)
    assert modifiers[0] == 12
    assert modifiers[1] == 0.8
    assert modifiers[2] == 0.9


@pytest.mark.parametrize(
    "research_speed_mod, tech_difficulty_mod, game_difficulty_mod, policy_mod, difficulty_multiplier", [
        (100, 10, 1, 0.8, 12.5),
        (140, 4, 0.8, 1, 28),
        (180, 6, 0.9, 0.9, 30),
        (20, 20, 0.7, 1, 1),
        (2500, 4, 1.1, 0.8, 200)
    ]
)
def test_calculate_components_difficulty_multiplier_from_modifiers(research_speed_mod, tech_difficulty_mod, game_difficulty_mod, policy_mod, difficulty_multiplier):
    assert round(classes.calculate_components_difficulty_multiplier_from_modifiers(research_speed_mod, tech_difficulty_mod, game_difficulty_mod, policy_mod), 4) == difficulty_multiplier


@pytest.mark.parametrize(
    "skill_multiplier, difficulty_multiplier, has_blueprint, progress", [
        (1.5, 15, 0, 0.63),
        (3, 10, 1, 1.428),
        (2.6, 100, 0, 7.28)
    ]
)
def test_calculate_1_day_progress_from_multipliers(game_constants, skill_multiplier, difficulty_multiplier, has_blueprint, progress):
    assert round(classes.calculate_1_day_progress_from_multipliers(game_constants, skill_multiplier, difficulty_multiplier, has_blueprint), 4) == progress


@pytest.mark.parametrize(
    "m_type, m_value, m_option, m_extra, m_modifier_effect, result", [
        ("tech_group_mod", "industry", None, None, -0.1000, ("industry", -0.1)),
        ("diplomatic_cost_mod", "bring_to_alliance", 0, None, -0.5000, None)
    ]
)
def test_get_modifiers_tech_effects(m_type, m_value, m_option, m_extra, m_modifier_effect, result):
    modifier = classes.Modifier(m_type, m_value, m_option, m_extra, m_modifier_effect)
    assert classes.get_modifiers_tech_effects(modifier) == result

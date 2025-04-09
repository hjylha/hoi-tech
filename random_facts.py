
import sys

import scan_hoi_files as shf
from research import Research


DEFAULT_END_YEAR = 1937
DEFAULT_LEVEL = 3
DEFAULT_DIFFICULTY = "VERYHARD"
DEFAULT_RESEARCH_SPEED = 150
DEFAULT_NUM_TO_SHOW = 20


def format_string(s, length, direction="left"):
    s = s[:length]
    if direction == "left":
        return s + " " * (length - len(s))
    if direction == "right":
        return " " * (length - len(s)) + s
    raise Exception(f"Questionable direction: {direction}")


def print_row(row, lengths, directions):
    strings_to_print = []
    lengths = list(lengths)
    if extra := (len(row) - len(lengths)) > 0:
        for _ in range(extra):
            lengths.append(None)
    directions = list(directions)
    if extra := (len(row) - len(directions)) > 0:
        for _ in range(extra):
            directions.append("left")
    for i, item in enumerate(row):
        strings_to_print.append(format_string(str(item), lengths[i], directions[i]))
    printed_row = " \t ".join(strings_to_print)
    print(printed_row)


# Fcns to try to find the optimal doctrines for exploits
def get_doctrines_to_check_for_exploits(research, categories=(6, 8, 9), level=DEFAULT_LEVEL):
    doctrines = set()
    for tech_id in research.completed_techs:
        if tech_id // 1000 in categories:
            doctrines.add(tech_id)
        # if "doctrine" not in research.techs[tech_id].category:
        #     continue
    if level < 1:
        return doctrines
    old_doctrines = doctrines.copy()
    for layer in range(level):
        new_doctrines = set()
        if layer == 0:
            for tech_id in research.active_techs:
                if tech_id // 1000 in categories:
                    doctrines.add(tech_id)
                    new_doctrines.add(tech_id)
        for t_id in old_doctrines:
            for tech_id in research.techs[t_id].allows:
                if tech_id // 1000 in categories:
                    doctrines.add(tech_id)
                    new_doctrines.add(tech_id)
        old_doctrines = new_doctrines.copy()
    return doctrines
        

def get_best_exploits_for_country(research, categories=(6, 8, 9), year_range=(1933, DEFAULT_END_YEAR), level=DEFAULT_LEVEL, difficulty=DEFAULT_DIFFICULTY):
    # r = Research(countries=[country_code])
    # for country in research.countries:
    #     research.remove_country(country)
    # research.add_country(country_code)
    diff_string = difficulty
    research.change_difficulty(diff_string)
    doctrine_ids = get_doctrines_to_check_for_exploits(research, categories, level)
    results = []
    # for tech_id, tech in research.techs.items():
    for tech_id in doctrine_ids:
        # if tech_id // 1000 not in categories:
        #     continue
        # if "doctrine" not in tech.category:
        #     continue
        tech = research.techs[tech_id]
        results_for_tech = []
        research.blueprints.add(tech_id)
        rs_impact = 2 * tech.get_research_speed_change()
        min_time = 999_999
        for team in research.all_teams:
            if team.start_year > year_range[1] or team.end_year < year_range[0]:
                continue
            days_to_research = research.calculate_how_many_days_to_complete(team, tech)
            rs_slope = round(rs_impact / days_to_research, 4)
            results_for_tech.append((rs_slope, tech_id, tech.name, team.name, days_to_research, team.start_year, team.end_year))
            if days_to_research < min_time:
                min_time = days_to_research
        results_for_tech = sorted(results_for_tech, key=lambda r: r[0], reverse=True)
        for row in results_for_tech:
            if row[0] < 2 * min_time:
                results.append(row)
    return sorted(results, key=lambda r: r[0], reverse=True)


def print_exploits(exploit_list):
    lengths = (8, 32, 25, 5, 4, 4)
    directions = ("left", "left", "left", "right", "right", "right")
    for row in exploit_list:
        row_to_print = (row[0], f"{row[1]} {row[2]}", row[3], row[4], row[5], row[6])
        print_row(row_to_print, lengths, directions)


def run_exploit_test(num_to_show=DEFAULT_NUM_TO_SHOW):
    r = Research()

    cc = input("Country Code: ").upper()
    r.add_country(cc)

    end_year = input(f"End year for exploits [default={DEFAULT_END_YEAR}]: ")
    try:
        end_year = int(end_year)
    except ValueError:
        end_year = DEFAULT_END_YEAR

    level_question_text1 = "Which level of doctrines to check for exploits?\n"
    level_question_text2 = "\t (Level 0 means only those that have already been completed, 1 means completed and available.\n"
    level_question_text3 = "\t  In general, level n + 1 means include techs that are made available by researching techs at level n.)\n"
    level_question_text4 = f"[default={DEFAULT_LEVEL}]: "
    level = input(level_question_text1 + level_question_text2 + level_question_text3 + level_question_text4)
    try:
        requested_level = int(level)
    except ValueError:
        requested_level = DEFAULT_LEVEL

    # difficulty = input(f"Difficulty (VE, E, N, H, VH) [default={DEFAULT_DIFFICULTY}]: ")

    research_speed = input(f"Research speed [default={r.research_speed}]: ")
    try:
        r.research_speed = int(research_speed)
    except ValueError:
        pass


    res6 = get_best_exploits_for_country(r, categories=(6, ), year_range=(1933, end_year), level=requested_level)
    res8 = get_best_exploits_for_country(r, categories=(8, ), year_range=(1933, end_year), level=requested_level)
    res9 = get_best_exploits_for_country(r, categories=(9, ), year_range=(1933, end_year), level=requested_level)

    print(f"Best land doctrine exploits for {cc}:")
    print_exploits(res6[:num_to_show])

    print()
    print(f"Best naval doctrine exploits for {cc}:")
    print_exploits(res8[:num_to_show])

    print()
    print(f"Best air doctrine exploits for {cc}:")
    print_exploits(res9[:num_to_show])


# true random facts incoming
def get_teams_with_skill(skill, teams):
    return [team for team in teams if team.skill == skill]


def days_to_do_all_tech(team, techs, research_speed=DEFAULT_RESEARCH_SPEED, rockets=0, reactors=0):
    days = 0
    for tech in techs:
        more_days = team.calculate_how_many_days_to_complete(tech, research_speed, num_of_rocket_sites=rockets, reactor_size=reactors)
        days += more_days
    return days


def fastest_teams_to_do_all_tech(techs, teams, research_speed=DEFAULT_RESEARCH_SPEED, rockets=0, reactors=0):
    results = []
    for team in teams:
        days = days_to_do_all_tech(team, techs, research_speed, rockets, reactors)
        results.append([team, days])
    return sorted(results, key=lambda r: r[1])

def show_fastest_teams(num_of_teams=DEFAULT_NUM_TO_SHOW, research_speed=DEFAULT_RESEARCH_SPEED):
    sorted_teams = fastest_teams_to_do_all_tech(shf.scan_techs(), shf.scan_tech_teams(), research_speed)
    print(f"Fastest teams to research all tech (with research speed constantly at {research_speed}):")
    for team, days in sorted_teams[:num_of_teams]:
        print(f"{days} \t {team.name} - {team.nation}")
    return sorted_teams[:num_of_teams]


def slowest_tech(techs, teams, research_speed=DEFAULT_RESEARCH_SPEED, rockets=0, reactors=0):
    results = []
    for tech in techs:
        days_min = 1_000_000
        best_team = None
        for team in teams:
            days = team.calculate_how_many_days_to_complete(tech, research_speed, num_of_rocket_sites=rockets, reactor_size=reactors)
            if days < days_min:
                days_min = days
                best_team = team
        results.append([tech, days_min, best_team])
    return sorted(results, key=lambda r: r[1], reverse=True)


def show_slowest_tech(num_of_techs=DEFAULT_NUM_TO_SHOW, research_speed=DEFAULT_RESEARCH_SPEED):
    slowest_techs = slowest_tech(shf.scan_techs(), shf.scan_tech_teams(), research_speed)
    print(f"Slowest technologies to research (with research speed {research_speed})")
    for tech, days, team in slowest_techs[:num_of_techs]:
        print(f"{days} \t {tech.tech_id} {tech.name} \t {team.name}")
    return slowest_techs[:num_of_techs]


def least_special_tech(techs, teams):
    techs_and_specials = []
    for tech in techs:
        max_specials = 0
        top_team = None
        for team in teams:
            specials = team.get_num_of_specials(tech)
            if specials > max_specials:
                max_specials = max(max_specials, specials)
                top_team = team
        techs_and_specials.append([tech, max_specials, top_team])
    return sorted(techs_and_specials, key=lambda x: x[1])

def print_least_special_tech(techs, teams, num_of_tech=10):
    ls_tech = least_special_tech(techs, teams)
    print(f"Technologies with least specialization:")
    for line in ls_tech[:num_of_tech]:
        print(f"{line[1]} components, tech id and name: {line[0].tech_id} {line[0].name}, team: {line[2].name}")
    print()
    return ls_tech


def num_of_specilialites(techs):
    specs = dict()
    for tech in techs:
        for component in tech.components:
            if specs.get(component.type.lower()) is not None:
                specs[component.type.lower()] += 1
            else:
                specs[component.type.lower()] = 1
    return specs


def show_most_common_component_types(num_of_components=DEFAULT_NUM_TO_SHOW):
    # specs = num_of_specilialites(shf.scan_techs())
    spec0 = sorted(list(num_of_specilialites(shf.scan_techs()).items()), key=lambda x: x[1], reverse=True)
    print("Most common component types among all technologies:")
    for comp_type, num in spec0[:num_of_components]:
        print(f"{num} \t {comp_type}")
    return spec0[:num_of_components]


def sum_of_speciality_difficulties(techs, with_adjustment=1):
    num_of_specs = dict()
    for tech in techs:
        for component in tech.components:
            if num_of_specs.get(component.type.lower()) is not None:
                num_of_specs[component.type.lower()] += component.difficulty + 2 * with_adjustment
            else:
                num_of_specs[component.type.lower()] = component.difficulty + 2 * with_adjustment
    return num_of_specs

def show_sum_of_component_types(num_of_components=DEFAULT_NUM_TO_SHOW):
    spec1 = sorted(list(sum_of_speciality_difficulties(shf.scan_techs()).items()), key=lambda x: x[1], reverse=True)
    print(f"Component types with the largest sum of (adjusted) component difficulties:")
    for comp_type, num in spec1[:num_of_components]:
        print(f"{num} \t {comp_type}")
    return spec1[:num_of_components]


def sum_of_speciality_difficulties_for_team(team, sum_of_specs_overall):
    # sum_of_specs = sum_of_speciality_difficulties()
    final_sum = 0
    sums = [sum_of_specs_overall[speciality] for speciality in team.specialities]
    for num in sums:
        final_sum += num
    # return sum(*[sum_of_specs_overall[speciality] for speciality in team.specialities])
    return final_sum


def most_specialization_by_sum_of_difficulty(techs, teams, with_adjustment=1):
    sum_of_specs = sum_of_speciality_difficulties(techs, with_adjustment)
    results = dict()
    teams_by_skill = dict()
    for team in teams:
        if teams_by_skill.get(team.skill) is not None:
            teams_by_skill[team.skill].append(team)
        else:
            teams_by_skill[team.skill] = [team]
    for skill in range(1, 10):
        result = []
        for team in teams_by_skill[skill]:
            s = sum_of_speciality_difficulties_for_team(team, sum_of_specs)
            result.append([team, s])
        results[skill] = sorted(result, key=lambda x: x[1], reverse=True)
    return results


def rank_teams_by_specialization_and_skill(techs, teams, with_adjustment=1):
    sum_of_specs = sum_of_speciality_difficulties(techs, with_adjustment)
    rankings = []
    sum_of_difficulties = 0
    for num in sum_of_specs.values():
        sum_of_difficulties += num
    for team in teams:
        sum_of_specs_for_team = sum_of_speciality_difficulties_for_team(team, sum_of_specs)
        time_value = round(0.5 * sum_of_specs_for_team / (team.skill + 6), 0) + round((sum_of_difficulties - sum_of_specs_for_team) / (team.skill + 6), 0)
        rankings.append([team, time_value])
    return sorted(rankings, key=lambda x: x[1])

def show_ranked_teams(num_of_teams=DEFAULT_NUM_TO_SHOW):
    ranking = rank_teams_by_specialization_and_skill(shf.scan_techs(), shf.scan_tech_teams())
    print("Tech teams that are expected to research all tech the fastest")
    for team, time_value in ranking[:num_of_teams]:
        print(f"{time_value} \t {team.name} - {team.nation}")
    return ranking[:num_of_teams]


def choose_random_fact(random_facts):
    print("Choose a random fact:")
    for i, fact in enumerate(random_facts):
        print(f"{i + 1}. {fact}")
    choice = input()
    try:
        choice = int(choice) - 1
        if choice >= 0 and choice < len(random_facts):
            return choice
    except ValueError:
        return


def show_random_facts():
    random_facts = [
        (f"Show {DEFAULT_NUM_TO_SHOW} fastest teams to research all tech (with constant research speed {DEFAULT_RESEARCH_SPEED})", show_fastest_teams),
        (f"Show {DEFAULT_NUM_TO_SHOW} teams that should be fastest researching all tech (time ~= skill/difficulty)", show_ranked_teams),
        (f"Show {DEFAULT_NUM_TO_SHOW} technologies that are the slowest to research", show_slowest_tech),
        (f"Show {DEFAULT_NUM_TO_SHOW} most common component types", show_most_common_component_types),
        (f"Show {DEFAULT_NUM_TO_SHOW} most impactful component types (based on sum of component difficulties)", show_sum_of_component_types)
    ]
    choice = choose_random_fact([rf[0] for rf in random_facts])
    if choice is None:
        return
    random_facts[choice][1]()


if __name__ == "__main__":
    try:
        if "exp" in sys.argv[1]:
            run_exploit_test()
        elif "rand" in sys.argv[1]:
            show_random_facts()
    except IndexError:
        pass

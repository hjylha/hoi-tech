
import sys
from file_paths import get_scenarios_folder_path, get_event_text_paths, get_all_text_files_paths
from check_file_paths import AOD_PATH
from read_hoi_files import read_scenario_file_for_events, read_txt_file, get_texts_from_files, get_country_names, get_texts_from_files_w_duplicates
from classes import find_tech, find_tech_teams, find_ministers, find_ideas, find_leaders
from scan_hoi_files import get_tech_dict, FileScanner
from event import Trigger, get_actions, Event, suggest_events_based_on_search_words, get_conditions
from print_effects_and_triggers import print_event, print_tech, print_tech_team, print_minister, print_idea


def get_event_list(scenario_name, aod_path, show_empty_files=False):
    event_file_paths = read_scenario_file_for_events(scenario_name, aod_path)
    event_list = []
    for filepath in event_file_paths:
        file_content = read_txt_file(filepath)
        if isinstance(file_content, list):
            if show_empty_files:
                print(f"No events in {filepath}")
            # print(file_content)
            continue
        possible_events = file_content["event"]
        if isinstance(possible_events, list):
            for event in possible_events:
                event["path"] = filepath
                event_list.append(event)
            continue
        if isinstance(possible_events, dict):
            possible_events["path"] = filepath
            event_list.append(possible_events)
            continue
    return event_list


def get_event_dict(event_list, event_text_dict):    
    # event_text_files = get_event_text_paths(aod_path)
    # event_text_dict = get_texts_from_files(event_text_files)
    missing_texts = [[], [], []]

    id_key = "id"
    name = "name"
    desc = "desc"
    for event in event_list:
        if not event.get("trigger"):
            event["trigger"] = dict()
        name_key = event.get(name)
        if name_key is not None:
            actual_name = event_text_dict.get(name_key)
            if actual_name is not None:
                event[name] = actual_name
            else:
                missing_texts[0].append(event[id_key])
        desc_key = event.get(desc)
        if desc_key is not None:
            actual_desc = event_text_dict.get(desc_key)
            if actual_desc is not None:
                event[desc] = actual_desc
            else:
                missing_texts[1].append(event[id_key])
        letters = "abcde"
        for i, letter in enumerate(letters):
            key = f"action_{letter}"
            action = event.get(key)
            if action is not None:
                if isinstance(action, list):
                    for j, action_item in enumerate(action):
                        event[f"action_{letters[i + j]}"] = action_item
                
                if isinstance(event[key].get("command"), dict):
                    event[key]["command"] = [event[key]["command"]]
                
                name_keys = [k for k in event[key].keys() if k.lower() == name]
                action_name_key = event[key][name_keys[0]] if name_keys else event[key].get(name)
                if action_name_key is not None:
                    actual_action_name = event_text_dict.get(action_name_key)
                    if actual_action_name is not None:
                        event[key][name] = actual_action_name
                    else:
                        if event[id_key] not in missing_texts[2]:
                            missing_texts[2].append(event[id_key])

    event_dict = dict()
    for event in event_list:
        event_id = event["id"]
        if event_dict.get(event_id) is not None:
            print(f"duplicate event id: {event_id}")
            continue
        event_dict[event_id] = event
    return event_dict, missing_texts


def scan_events(scenario_name, aod_path):
    event_list = get_event_list(scenario_name, aod_path)
    event_text_dict = get_texts_from_files(get_event_text_paths(AOD_PATH))
    country_dict = get_country_names()

    event_dict = dict()
    for event in event_list:

        notes = ""

        trigger = event.get("trigger")
        if trigger is None or not trigger:
            trigger = dict()
        # TODO: Trigger class?
        name = event_text_dict.get(event["name"])
        name = "" if name is None else name

        desc_key = event.get("desc")
        desc_key = "" if desc_key is None else desc_key
        desc = event_text_dict.get(desc_key)
        desc = "" if desc is None else desc

        actions = []
        # TODO: Action class
        action_keys = []
        for key in event.keys():
            if "action" in key:
                action_keys.append(key)
        action_keys = sorted(action_keys)
        action_key = "action_key"
        if "action_a" not in action_keys:
            notes += "action_a not a key\n"
        for key in action_keys:
            action = event[key]
            if isinstance(action, list):
                notes += f"{key} is a list"
                for act in action:
                    act[action_key] = key
                    actions.append(act)
                continue
            action[action_key] = key
            actions.append(action)
        actions = get_actions(actions, event_text_dict)

        is_random_str = event.get("random")
        is_random_str = "no" if not is_random_str else is_random_str
        is_random = True if is_random_str.lower() == "yes" else False

        is_invention_str = event.get("invention")
        is_invention_str = "no" if not is_invention_str else is_invention_str
        is_invention = True if is_invention_str.lower() == "yes" else False

        is_persistent_str = event.get("persistent")
        is_persistent_str = "no" if not is_persistent_str else is_persistent_str
        is_persistent = True if is_persistent_str.lower() == "yes" else False

        country_code = event.get("country")
        country_code = "" if country_code is None else country_code.upper()

        country = country_dict.get(country_code)
        country = "" if country is None else country

        date = event.get("date")
        date = dict() if date is None else date

        offset = event.get("offset")

        death_date = event.get("deathdate")
        death_date = dict() if death_date is None else death_date

        picture = event.get("picture")
        picture = "" if picture is None else picture

        style = event.get("style")
        style = "" if style is None else style
        
        proper_event = Event(
            event["path"],
            event["id"],
            event["name"],
            name,
            actions,
            is_random,
            is_invention,
            country_code,
            country,
            Trigger(event["id"], trigger),
            desc_key, 
            desc,
            style,
            picture,
            date,
            offset,
            death_date,
            is_persistent,
            notes
        )
        event_dict[event["id"]] = proper_event
    
    for ev_id, ev in event_dict.items():
        for i, action in enumerate(ev.actions):
            for effect in action.effects:
                if effect.type and effect.type == "trigger":
                    triggered_event_id = effect.which
                    if event_dict.get(triggered_event_id) is None:
                        name_text = ev.name if ev.name else "[no name]"
                        print(f"Event {ev_id} [{ev.country_code}]: {name_text} triggers event {triggered_event_id}, which does not exist.")
                        continue
                    event_dict[triggered_event_id].triggered_by.append((ev, i))
                elif effect.type and effect.type == "sleepevent":
                    deactivated_event_id = effect.which
                    if event_dict.get(deactivated_event_id) is None:
                        name_text = ev.name if ev.name else "[no name]"
                        print(f"Event {ev_id} [{ev.country_code}]: {name_text} deactivates event {deactivated_event_id}, which does not exist.")
                        continue
                    event_dict[deactivated_event_id].deactivated_by.append((ev, i))
                    # if event_dict[triggered_event_id].triggered_by is not None:
                    #     print(f"Event {triggered_event_id} triggered also by something else than event {ev_id}")
                    # else:
                    #     event_dict[triggered_event_id].triggered_by = (ev_id, action.action_key)

    return event_dict


def suggest_events(search_text, event_dict, max_num_of_suggestions=999):
    try:
        event_id = int(search_text)
        if event_dict.get(event_id) is not None:
            return [event_dict[event_id]]
    except ValueError:
        pass
    search_text = search_text.lower()
    name_starts = []
    name_other = []
    desc_starts = []
    desc_other = []
    action_things = []
    for event_id, event in event_dict.items():
        if event["name"].lower().startswith(search_text):
            name_starts.append(event)
            continue
        if search_text in event["name"].lower():
            name_other.append(event)
            continue
        if event.get("desc") is None:
            continue
        if event["desc"].lower().startswith(search_text):
            desc_starts.append(event)
            continue
        if search_text in event["desc"].lower():
            desc_other.append(event)
            continue
        action_keys = [key for key in event.keys() if "action" in key]
        for key in action_keys:
            name = event[key].get("name")
            if name is None:
                continue
            if search_text in name.lower():
                action_things.append(event)
                break
    suggestions = name_starts + name_other + desc_starts + desc_other + action_things
    
    return suggestions[:max_num_of_suggestions]


def print_event_as_dict(event, indent_num=0):
    print(f"{event["id"]}: {event["name"]}")
    country_code = event.get("country")
    country_code = country_code.upper() if country_code else ""
    country = country_dict.get(country_code)
    if country:
        print(f"Country: {country}")
    is_invention = event.get("invention")
    is_invention = is_invention if is_invention else "no"
    if is_invention.lower() == "yes":
        print("invention event")

    is_random = event.get("random")
    is_random = is_random if is_random else "no"
    if is_random.lower() == "yes":
        print("random event")
    
    path_str = str(event["path"])[len(str(AOD_PATH)) + 1:]
    print(f"In file: {path_str}")

    if event.get("trigger") is not None:
        print("\nTrigger:")
        trigger = event["trigger"]
        if not trigger:
            print(indent_num * " ", "-")
        else:
            if isinstance(trigger, dict):
                for key, item in trigger.items():
                    if key.upper() in ["NOT", "AND", "OR"]:
                        print(indent_num * " ", key.upper())
                        indent_num += 2
                        if isinstance(item, dict):
                            for k, it in item.items():
                                print(indent_num * " ", k, "=", it)
                        elif isinstance(item, list):
                            for it in item:
                                print(indent_num * " ", it)
                        indent_num -= 2
                        continue
                    print(indent_num * " ", key, "=", item)
            elif isinstance(trigger, list):
                for item in trigger:
                    print(indent_num * " ", item)
            else:
                print(f"PROBLEM: trigger is of type {type(trigger)}")
        print()

    if event.get("date") is not None:
        print("Date:")
        print(event["date"]["day"], event["date"]["month"], event["date"]["year"])
    if event.get("offset") is not None:
        print(f"Offset: {event['offset']}")
    if event.get("deathdate") is not None:
        print("Deathdate:")
        print(event["deathdate"]["day"], event["deathdate"]["month"], event["deathdate"]["year"])
    persistence = event.get("persistent")
    if persistence is not None and persistence.lower() == "yes":
        print("persistent event")

    desc = event.get("desc")
    if desc:
        print()
        print(desc)
    
    print("\nActions:")
    action_keys = [key for key in event.keys() if "action" in key]
    for i, action in enumerate(action_keys):
        if event[action].get("name") is not None:
            num_of_effects = 0
            print(indent_num * " ", f"{i + 1}.", event[action].get("name"))
            effects = event[action].get("command")
            if effects is not None:
                print((indent_num + 2) * " ", len(effects), "effects:")
                for effect in effects:
                    print((indent_num + 2) * " ", effect)


def search_events(event_dict):
    text_input = input("Enter search term:\n")
    if not text_input:
        return False
    suggestions = suggest_events(text_input, event_dict)
    print()
    if not suggestions:
        print("No matching events found.")
    elif len(suggestions) == 1:
        indent_num = 2
        ev = suggestions[0]
        print_event_as_dict(ev, indent_num)
    else:
        for event in suggestions:
            country_code = event.get("country")
            country_code = country_code.upper() if country_code else ""
            print(f"{event["id"]} [{country_code}]: {event["name"]}")
    print("\n")
    return True


def print_too_many_to_show_message(suggestions, max_num_of_suggestions, indent_num, the_command="--all"):
    if len(suggestions) > max_num_of_suggestions:
        print(f"\n{' ' * indent_num} {max_num_of_suggestions} out of {len(suggestions)} search results shown. If you want to see them all, add {the_command} to search keywords.")

def search_events_w_class(aod_path, filescanner, max_num_of_suggestions=999, force_default=False):
    text_input = input("Enter search term(s):\n")
    if not text_input:
        return False
    no_countries = False
    if text_input.startswith("--nocc"):
        no_countries = True
        country_codes = [""]
        if text_input == "--nocc":
            text_input = ""
        else:
            text_input = text_input.replace("--nocc ", "")
    elif " --nocc" in text_input:
        no_countries = True
        country_codes = [""]
        text_input = text_input.replace(" --nocc", "")
    found_country_codes = False
    if not no_countries:
        possible_country_codes = text_input.split(" ")[0].upper().split(",")
        country_codes = []
        for possible_country_code in possible_country_codes:
            if filescanner.country_dict.get(possible_country_code) is not None:
                country_codes.append(possible_country_code)
                found_country_codes = True
            elif found_country_codes:
                print(f"{possible_country_code} is not a valid country code.")
    start_length = 0
    if found_country_codes:
        start_length = len(",".join(possible_country_codes)) + 1
    
    text_input = text_input[start_length:]
    if " --all" in text_input:
        max_num_of_suggestions = 999_999
        text_input = text_input.replace(" --all", "")
    print_all = False
    if " --printall" in text_input:
        print_all = True
        text_input = text_input.replace(" --printall", "")
    suggestions = suggest_events_based_on_search_words(text_input, filescanner.event_dict, country_codes)

    indent_add = 2
    # print(f"Search term: {text_input}, country_codes: {country_codes}")
    print()
    if country_codes and not no_countries:
        cc_texts = [f"{filescanner.country_dict[country_code]} [{country_code}]" for country_code in country_codes]
        print(f" Searching restricted to events of {', '.join(cc_texts)}\n")
    elif country_codes and no_countries:
        print(f"Searching restricted to events without a country")
    if not suggestions:
        print(" No matching events found.")
    elif len(suggestions) == 1:
        ev = suggestions[0][0]
        # ev.print_event(aod_path, 1, indent_add)
        print_event(ev, aod_path, 1, indent_add, filescanner.text_dict, filescanner.event_dict, filescanner.tech_dict, filescanner.leader_dict, filescanner.minister_dict, filescanner.techteam_dict, force_default=force_default)
    elif print_all:
        ordinal_num = 0
        for event, score in suggestions[:max_num_of_suggestions]:
            ordinal_num += 1
            print("#" * 30)
            print(f" Result {ordinal_num}: score {score}")
            print("#" * 30)
            print()
            print_event(event, aod_path, 1, indent_add, filescanner.text_dict, filescanner.event_dict, filescanner.tech_dict, filescanner.leader_dict, filescanner.minister_dict, filescanner.techteam_dict, force_default=force_default)
            print()
    else:
        for event, score in suggestions[:max_num_of_suggestions]:
            country_code = event.country_code
            country_code = country_code.upper() if country_code else ""
            if event.name:
                print(f" {event.event_id} [{country_code}]: {event.name} (score: {score})")
            else:
                print(f" {event.event_id} [{country_code}]: {event.name_key}  [name in file] (score: {score})")
        if len(suggestions) > max_num_of_suggestions:
            print(f"\n  {max_num_of_suggestions} out of {len(suggestions)} search results shown. If you want to see them all, add --all to search keyword(s).")
    print("\n")
    return True


def find_matching_text(search_term, text_dict, exact_keyword=False):
    if exact_keyword:
        suggestions = []
        for k, v_list in text_dict.items():
            if k == search_term:
                for t, p in v_list:
                    suggestions.append((k, t, p))
                continue
            for t, p in v_list:
                if t == search_term:
                    suggestions.append((k, t, p))
        return suggestions
    
    search_term = search_term.lower()
    starts = []
    others = []
    for k, v_list in text_dict.items():
        if k.lower().startswith(search_term):
            for t, p in v_list:
                starts.append((k, t, p))
            continue
        if search_term in k.lower():
            for t, p in v_list:
                others.append((k, t, p))
        for t, p in v_list:
            if t.lower().startswith(search_term):
                starts.append((k, t, p))
                continue
            if search_term in t.lower():
                others.append((k, t, p))
    suggestions = starts
    for triple in others:
        if triple not in suggestions:
            suggestions.append(triple)
    return suggestions

def print_text_suggestions(suggestions, max_num_of_suggestions=99, max_text_length=50, indent_num=2, the_command="--all"):
    print()
    if not suggestions:
        print(" " * indent_num, "Nothing found\n")
        return
    if len(suggestions) == 1:
        key, text, path = suggestions[0]
        print(" " * indent_num, key)
        print(" " * indent_num, text)
        print(" " * indent_num, f"[{path.name}]")
        print("\n")
        return
    for key, text, path in suggestions[:max_num_of_suggestions]:
        key_to_print = key[:max_text_length]
        key_to_print = key_to_print + (" " * (max_text_length- len(key_to_print)))
        text_to_print = text if len(text) <= max_text_length else text[:max_text_length] + "[...]"
        text_to_print = text_to_print + (" " * (max_text_length + 5 - len(text_to_print)))
        print(" " * indent_num, key_to_print, text_to_print, " ", f"[{path.name}]")
    if the_command:
        print_too_many_to_show_message(suggestions, max_num_of_suggestions, indent_num, the_command)
    print("\n")

def search_texts(text_dict, max_num_of_suggestions=99, max_text_length=50, the_command=""):
    exact_keyword = False
    text_input = input("Enter search term(s):\n")
    if not text_input:
        return False
    try:
        if text_input.strip()[0] == '"' and text_input.strip()[-1] == '"':
            text_input = text_input.strip()[1:-1]
            exact_keyword = True
    except IndexError:
        pass
    
    suggestions = find_matching_text(text_input, text_dict, exact_keyword)
    
    print_text_suggestions(suggestions, max_num_of_suggestions, max_text_length, indent_num=1, the_command=the_command)

    return True


def find_and_remove_text_w_space(full_text, text_to_find_and_remove):
    new_text_parts = []
    for part in full_text.split(" "):
        if part == text_to_find_and_remove:
            continue
        new_text_parts.append(part)
    return " ".join(new_text_parts)
    # if full_text == text_to_find_and_remove:
    #     return ""
    # text_at_start = f"{text_to_find_and_remove} "
    # if full_text.startswith(text_at_start):
    #     return full_text.replace(text_at_start, "")
    # text_elsewhere = f" {text_to_find_and_remove}"
    # return full_text.replace(text_elsewhere, "")


class Search:

    DEFAULT_SUBJECT = "--E"
    THE_MAX_NUM_OF_SUGGESTIONS = 999_999

    ALL_FLAG = "--all"
    PRINTALL_FLAG = "--printall"
    NO_COUNTRY_FLAG = "--nocc"
    FORCE_DEFAULT_FLAG = "--FD"

    NOT_IMPLEMENTED_TEXT = "\n  This feature has not been implemented yet.\n"

    # def change_subject(self, current_subject):
    #     self.current_subject = current_subject

    def print_too_many_to_show_message(self, suggestions, max_num_of_suggestions):
        print_too_many_to_show_message(suggestions, max_num_of_suggestions, self.indent_num, the_command=self.ALL_FLAG)

    def get_countries_at_start_of_text(self, text):
        # no_countries = False
        new_text = find_and_remove_text_w_space(text, self.NO_COUNTRY_FLAG)
        if new_text != text:
            return new_text, None

        found_country_codes = False
        # if not no_countries:
        possible_country_codes = text.split(" ")[0].upper().split(",")
        country_codes = []
        for possible_country_code in possible_country_codes:
            if self.files.country_dict.get(possible_country_code) is not None:
                country_codes.append(possible_country_code)
                found_country_codes = True
            elif found_country_codes:
                print(" " * self.indent_num, f"{possible_country_code} is not a valid country code.")
        start_length = 0
        if found_country_codes:
            start_length = len(",".join(possible_country_codes)) + 1

        text = text[start_length:]
        return text, country_codes

    def change_subject_in_search(self, text_input, current_subject):
        if not text_input:
            self.current_subject = current_subject
            print(f"\n{' ' * self.indent_num} Switching subject to {self.subjects[self.current_subject][1]}\n")
            return True
        return False

    def search_text(self, text_input, current_subject, show_all=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return
        exact_keyword = False
        try:
            if text_input.strip()[0] == '"' and text_input.strip()[-1] == '"':
                text_input = text_input.strip()[1:-1]
                exact_keyword = True
        except IndexError:
            pass

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        suggestions = find_matching_text(text_input, self.files.text_dict_w_duplicates, exact_keyword)
        print_text_suggestions(suggestions, max_num_of_suggestions, self.max_text_length, self.indent_num, the_command=self.ALL_FLAG)

    def search_events(self, text_input, current_subject, show_all=False, print_all=False, force_default=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return
        no_countries = False
        if text_input.startswith("--nocc"):
            no_countries = True
            country_codes = [""]
            if text_input == "--nocc":
                text_input = ""
            else:
                text_input = text_input.replace("--nocc ", "")
        elif " --nocc" in text_input:
            no_countries = True
            country_codes = [""]
            text_input = text_input.replace(" --nocc", "")
        found_country_codes = False
        if not no_countries:
            possible_country_codes = text_input.split(" ")[0].upper().split(",")
            country_codes = []
            for possible_country_code in possible_country_codes:
                if self.files.country_dict.get(possible_country_code) is not None:
                    country_codes.append(possible_country_code)
                    found_country_codes = True
                elif found_country_codes:
                    print(" " * self.indent_num, f"{possible_country_code} is not a valid country code.")
        start_length = 0
        if found_country_codes:
            start_length = len(",".join(possible_country_codes)) + 1
        
        text_input = text_input[start_length:]

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions
        
        suggestions = suggest_events_based_on_search_words(text_input, self.files.event_dict, country_codes)

        # indent_add = 2
        # print(f"Search term: {text_input}, country_codes: {country_codes}")
        print()
        if country_codes and not no_countries:
            cc_texts = [f"{self.files.country_dict[country_code]} [{country_code}]" for country_code in country_codes]
            print(" " * self.indent_num, f"Searching restricted to events of {', '.join(cc_texts)}\n")
        elif country_codes and no_countries:
            print(" " * self.indent_num, f"Searching restricted to events without a country")
        if not suggestions:
            print(" " * self.indent_num, "No matching events found.\n")
            return
        if len(suggestions) == 1:
            ev = suggestions[0][0]
            # ev.print_event(aod_path, 1, indent_add)
            print_event(ev, self.aod_path, self.indent_num, self.indent_add, self.files.text_dict, self.files.event_dict, self.files.tech_dict, self.files.leader_dict, self.files.minister_dict, self.files.techteam_dict, force_default=force_default)
            print()
            return
        if print_all:
            ordinal_num = 0
            for event, score in suggestions[:max_num_of_suggestions]:
                ordinal_num += 1
                print("#" * 30)
                print(" " * self.indent_num, f"Result {ordinal_num}: score {score}")
                print("#" * 30)
                print()
                print_event(event, self.aod_path, self.indent_num, self.indent_add, self.files.text_dict, self.files.event_dict, self.files.tech_dict, self.files.leader_dict, self.files.minister_dict, self.files.techteam_dict, force_default=force_default)
                print()
            return
        for event, score in suggestions[:max_num_of_suggestions]:
            country_code = event.country_code
            country_code = country_code.upper() if country_code else ""
            if event.name:
                print(" " * self.indent_num, f"{event.event_id} [{country_code}]: {event.name} (score: {score})")
            else:
                print(" " * self.indent_num, f"{event.event_id} [{country_code}]: {event.name_key}  [name in file] (score: {score})")
        
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print("\n")

    def search_tech(self, text_input, current_subject, show_all=False, force_default=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return

        suggestions = find_tech(text_input, self.files.tech_dict)

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            return

        if len(suggestions) == 1:
            # suggestions[0].print_tech_info(self.indent_num, self.indent_add)
            print_tech(suggestions[0], self.indent_num, self.indent_add, self.files.text_dict, self.files.tech_dict, force_default=force_default)
            print()
            return

        for tech in suggestions[:max_num_of_suggestions]:
            print(" " * self.indent_num, f"[{tech.tech_id}] {tech.name}")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print()

    # def get_leader_rank(self, land_naval_or_air, rank_num):
    #     letter = {0: "", 1: "N", 2: "A"}
    #     key = f"RANKNAME_{letter[land_naval_or_air]}{rank_num + 1}"
    #     return self.files.text_dict[key]

    def search_leaders(self, text_input, current_subject, show_all=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return

        text_input, country_codes = self.get_countries_at_start_of_text(text_input)
        if country_codes is None:
            print(" " * self.indent_num, f"Leaders have to have a country, {self.NO_COUNTRY_FLAG} is ignored.")

        suggestions = find_leaders(text_input, self.files.leader_dict, country_codes)

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            return

        if len(suggestions) == 1:
            suggestions[0].print_leader_info(self.indent_num, self.indent_add)
            print()
            return

        for leader in suggestions[:max_num_of_suggestions]:
            print(" " * self.indent_num, f"[{leader.leader_id}] {leader.name} [{leader.country_code}] skill: {leader.skill} ({leader.TYPES[leader.land_naval_or_air]})")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print()

    def search_ministers(self, text_input, current_subject, show_all=False, force_default=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return

        text_input, country_codes = self.get_countries_at_start_of_text(text_input)
        if country_codes is None:
            print(" " * self.indent_num, f"Ministers have to have a country, {self.NO_COUNTRY_FLAG} is ignored.")

        suggestions = find_ministers(text_input, self.files.minister_dict, country_codes)

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            return

        if len(suggestions) == 1:
            print_minister(suggestions[0], self.indent_num, self.indent_add, self.files.text_dict, force_default=force_default)
            # suggestions[0].print_minister_info(self.indent_num, self.indent_add)
            print()
            return

        for minister in suggestions[:max_num_of_suggestions]:
            personality = "-" if minister.personality is None else minister.personality.public_name
            print(" " * self.indent_num, f"[{minister.m_id}] {minister.name} [{minister.country_code}] position: {minister.position} ({personality})")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print()

    def search_ideas(self, text_input, current_subject, show_all=False, force_default=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return

        try:
            index_choice = int(text_input) - 1
            print_idea(self.old_suggestions[index_choice], self.indent_num, self.indent_add, self.files.text_dict, force_default=force_default)
            print()
            return
        except ValueError:
            pass
        except IndexError:
            pass

        suggestions = find_ideas(text_input, self.files.ideas)

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            self.old_suggestions = []
            return

        if len(suggestions) == 1:
            print_idea(suggestions[0], self.indent_num, self.indent_add, self.files.text_dict, force_default=force_default)
            # suggestions[0].print_minister_info(self.indent_num, self.indent_add)
            print()
            self.old_suggestions = []
            return

        self.old_suggestions = suggestions
        for i, idea in enumerate(suggestions[:max_num_of_suggestions]):
            print(" " * self.indent_num, f"{i + 1}. {idea.public_name} (position: {idea.position})")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print()

    def search_tech_teams(self, text_input, current_subject, show_all=False, force_default=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return

        text_input, country_codes = self.get_countries_at_start_of_text(text_input)
        if country_codes is None:
            print(" " * self.indent_num, f"Tech teams have to have a country, {self.NO_COUNTRY_FLAG} is ignored.")

        suggestions = find_tech_teams(text_input, self.files.techteam_dict, country_codes)

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            return

        if len(suggestions) == 1:
            print_tech_team(suggestions[0], self.indent_num, self.indent_add, self.files.text_dict, force_default=force_default)
            # suggestions[0].print_tech_team_info(self.indent_num, self.indent_add)
            print()
            return

        for tech_team in suggestions[:max_num_of_suggestions]:
            print(" " * self.indent_num, f"[{tech_team.team_id}] {tech_team.name} [{tech_team.country_code}] skill: {tech_team.skill}")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print()

    def search_countries(self, text_input, current_subject, show_all=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return
        exact_keyword = False
        try:
            if text_input.strip()[0] == '"' and text_input.strip()[-1] == '"':
                text_input = text_input.strip()[1:-1]
                exact_keyword = True
        except IndexError:
            pass
        text_input = text_input.lower()

        matches = []
        other_suggestions = []
        suggestions = []
        
        for country_code, country_name in self.files.country_dict.items():
            if country_code.lower() == text_input or country_name.lower() == text_input:
                if exact_keyword:
                    suggestions = [(country_code, country_name)]
                    break
                matches.append((country_code, country_name))
            elif text_input in country_code.lower() or text_input in country_name.lower():
                other_suggestions.append((country_code, country_name))
        
        if not suggestions:
            suggestions = matches + other_suggestions
        
        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            return
        for country_code, country_name in suggestions[:max_num_of_suggestions]:
            print(" " * self.indent_num, f"[{country_code}] {country_name}")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print("\n")

    def search_provinces(self, text_input, current_subject, show_all=False, **kwargs):
        if self.change_subject_in_search(text_input, current_subject):
            return
        # exact_keyword = False
        try:
            province_num = int(text_input)
            province_name = self.files.text_dict.get(f"PROV{province_num}")
            if province_name:
                print("\n", " " * self.indent_num, f"[{province_num}] {province_name}")
                return
        except ValueError:
            pass

        text_input = text_input.lower()

        suggestions = []
        for key, text in self.files.text_dict.items():
            if not key.upper().startswith("PROV"):
                continue
            if text_input in key.lower() or text_input in text.lower():
                suggestions.append((key[4:], text))

        max_num_of_suggestions = self.THE_MAX_NUM_OF_SUGGESTIONS if show_all else self.max_num_of_suggestions

        print()
        if not suggestions:
            print(" " * self.indent_num, "Nothing found\n")
            return
        for province_num, province_name in suggestions[:max_num_of_suggestions]:
            print(" " * self.indent_num, f"[{province_num}] {province_name}")
        self.print_too_many_to_show_message(suggestions, max_num_of_suggestions)
        print("\n")


    def __init__(self, aod_path, filescanner, max_num_of_suggestions=10, max_text_length=50, indent_num=1, indent_add=2, force_default=False):
        self.aod_path = aod_path
        self.files = filescanner
        self.subjects = {
            "--E": (self.search_events, "events"),
            "--t": (self.search_text, "(English) text"),
            "--T": (self.search_tech, "technologies"),
            "--TT": (self.search_tech_teams, "tech teams"), 
            "--L": (self.search_leaders, "leaders"),
            "--M": (self.search_ministers, "ministers"),
            "--I": (self.search_ideas, "policies and ideas"),
            "--C": (self.search_countries, "countries"),
            "--P": (self.search_provinces, "provinces")
        }
        self.current_subject = self.DEFAULT_SUBJECT
        self.max_num_of_suggestions = max_num_of_suggestions
        self.max_text_length = max_text_length
        self.indent_num = indent_num
        self.indent_add = indent_add
        self.force_default = force_default

        self.old_suggestions = []
    
    
    def search(self):
        print(f"\n{' ' * self.indent_num}Welcome to search!")
        print()
        print(" " * self.indent_num, f"Current scenario: {self.files.scenario_name} [{self.files.scenario_path.name}]")
        print()
        print(" " * self.indent_num, f"Subject can be changed with commands:")
        for key, value in self.subjects.items():
            text = f"{value[1]} [default]" if key == self.DEFAULT_SUBJECT else value[1]
            random_whitespace = " " * (6 - len(key))
            print(" " * (self.indent_num + self.indent_add), f"{key}{random_whitespace}{text}")
        print()
        print(" " * self.indent_num, "Empty search i.e. pressing Enter quits the program.\n")

        while True:
            text_input = input(f"Enter search term(s) [current subject: {self.subjects[self.current_subject][1]}]:\n")
            if not text_input:
                return

            show_all = False
            print_all = False
            force_default = self.force_default

            all_flag = f" {self.ALL_FLAG}"
            if all_flag in text_input:
                show_all = True
                text_input = text_input.replace(all_flag, "")

            print_all_flag = f" {self.PRINTALL_FLAG}"
            if print_all_flag in text_input:
                show_all = True
                print_all = True
                text_input = text_input.replace(print_all_flag, "")

            new_text_input = find_and_remove_text_w_space(text_input, self.FORCE_DEFAULT_FLAG)
            if new_text_input != text_input:
                text_input = new_text_input
                force_default = True

            for key, func_n_text in self.subjects.items():
                new_text_input = find_and_remove_text_w_space(text_input, key)
                if new_text_input != text_input:
                    # self.current_subject = key
                    func_n_text[0](new_text_input, current_subject=key, show_all=show_all, print_all=print_all, force_default=force_default)
                    break
            else:
                self.subjects[self.current_subject][0](text_input, current_subject=self.current_subject, show_all=show_all, print_all=print_all, force_default=force_default)


if __name__ == "__main__":
    SCENARIO_NAME = "1933.eug"
    scenario_path = get_scenarios_folder_path(AOD_PATH) / SCENARIO_NAME

    print("Gathering data from Iron Cross files...")
    # country_dict = get_country_names()
    # event_text_files = get_event_text_paths(AOD_PATH)
    # texts = get_texts_from_files(event_text_files)
    # event_list = get_event_list(SCENARIO_NAME, AOD_PATH)
    # event_dict, missing_texts = get_event_dict(event_list, texts)
    # no_name, no_desc, no_action = missing_texts
    text_dict = get_texts_from_files_w_duplicates(get_all_text_files_paths(AOD_PATH))
    text_dict_last = {key: value[-1][0] for key, value in text_dict.items()}
    
    fs = FileScanner(scenario_path)
    fs.scan(scan_everything=True)


    def get_texts():
        event_text_files = get_event_text_paths(AOD_PATH)
        return event_text_files, get_texts_from_files(event_text_files)
    
    def gel():
        return get_event_list(SCENARIO_NAME, AOD_PATH)
    
    def ged(el, texts):
        return get_event_dict(el, texts)

    # ed = scan_events(SCENARIO_NAME, AOD_PATH)
    ed = fs.event_dict

    bad_event_ids = [308008, 336154]
    double_action = [319021]
    
    def pe(event):
        event.print_event(AOD_PATH)

    ask_to_search = True
    force_default = False
    explanation = """\n    You can filter by country by typing in country code(s) (separated by ,) first, or,
    if you want to restrict your search to events without a specified country, you can
    start with '--nocc'. Additionally, you can use keywords of form 'type=value' to
    look for certain trigger conditions or effects (or dates). By default, each word is 
    searched separately, but you can search phrases using quotation marks (").
      Some example searches:
    fin,swe winter
      looks for the word winter in event names and descriptions of Finnish and Swedish events.
    chl year=1935
      looks for Chilean events that have year=1935 in their trigger conditions or dates.
    --nocc research_mod=
      looks for events that have no country specified and change research speed.
    "trade agreement" "american president"
      looks for phrases 'trade agreement' and 'american president' in names and descriptions of all events.

    Empty search i.e. pressing Enter quits the program.
    """

    


    if "d" in sys.argv:
        ask_to_search = False
        tech_dict = fs.tech_dict
        leader_dict = fs.leader_dict
        minister_dict = fs.minister_dict
        techteam_dict = fs.techteam_dict

        from print_effects_and_triggers import effect_as_str, condition_as_str, modifier_as_str
        def_effs = []
        for tech in tech_dict.values():
            for eff in tech.effects:
                eff_str = effect_as_str(eff, text_dict_last, ed, tech_dict, leader_dict, minister_dict, techteam_dict)
                if "=" in eff_str:
                    def_effs.append(eff_str)
        
        evs_w_d_effs = []
        evs_w_issues = []
        evs_w_d_conds = []
        evs_w_t_issues = []
        for ev in ed.values():
            has_error = False
            has_default = False
            for act in ev.actions:
                if has_default or has_error:
                    break
                for eff in act.effects:
                    try:
                        eff_str = effect_as_str(eff, text_dict_last, ed, tech_dict, leader_dict, minister_dict, techteam_dict)
                        if "=" in eff_str:
                            evs_w_d_effs.append(ev)
                            has_default = True
                            break
                    except KeyError:
                        has_error = True
                        evs_w_issues.append(ev)
                        break

            conditions = get_conditions(ev.trigger, [])
            conditions = [cond for cond, _ in conditions]
            has_error = False
            has_default = False
            for cond in conditions:
                if has_default or has_error:
                    break
                try:
                    cond_str = condition_as_str(cond, text_dict_last, ed, tech_dict, leader_dict, minister_dict, techteam_dict)
                    if "=" in cond_str:
                        evs_w_d_conds.append(ev)
                        has_default = True
                        break
                except KeyError:
                    has_error = True
                    evs_w_t_issues.append(ev)
                    break

        evs_w_d_effs = sorted(evs_w_d_effs, key=lambda ev: ev.event_id, reverse=True)
        evs_w_d_conds = sorted(evs_w_d_conds, key=lambda ev: ev.event_id, reverse=True)
        # evs_w_d_effs.pop().print_event(AOD_PATH)
    
        def s_ee(keyword):
            evs = []
            for ev in ed.values():
                stop_searching = False
                for a in ev.actions:
                    if stop_searching:
                        break
                    for eff in a.effects:
                        if eff.type == keyword:
                            evs.append(ev)
                            stop_searching = True
                            break
            return sorted(evs, key=lambda ev: ev.event_id, reverse=True)
        
        def s_ec(keyword):
            evs = []
            for ev in ed.values():
                # if ev.trigger.get_condition_keys([], keyword):
                #     evs.append(ev)
                conditions = get_conditions(ev.trigger, [])
                conditions = [cond for cond, _ in conditions]
                for cond in conditions:
                    if keyword in cond.keys():
                        evs.append(ev)
                        break
            return sorted(evs, key=lambda ev: ev.event_id, reverse=True)
        
        def s_c(keyword):
            conditions = []
            for ev in ed.values():
                conds = get_conditions(ev.trigger, [])
                conds = [cond for cond, _ in conds]
                for cond in conds:
                    if keyword in cond.keys():
                        conditions.append(cond)
            return conditions
        
        minister_mod_num = 0
        mod_types = set()
        def_mods = []
        mins_w_issues = []
        mins_w_ULEs = []
        mins_w_d_mods = []
        for minister in minister_dict.values():
            has_error = False
            has_ULE = False
            has_default = False
            if minister.personality is None:
                continue
            for modifier in minister.personality.modifiers:
                minister_mod_num += 1
                mod_types.add(modifier.type)
                try:
                    mod_str = modifier_as_str(modifier, text_dict_last)
                    if "=" in mod_str:
                        def_mods.append(mod_str)
                        has_default = True
                except KeyError:
                    has_error = True
                    # mins_w_issues.append(minister)
                    continue
                except UnboundLocalError:
                    has_ULE = True
                    continue
            if has_error:
                mins_w_issues.append(minister)
            if has_ULE:
                mins_w_ULEs.append(minister)
            if has_default:
                mins_w_d_mods.append(minister)
        mins_w_ULEs = sorted(mins_w_ULEs, key=lambda m: m.m_id)
        mins_w_issues = sorted(mins_w_issues, key=lambda m: m.m_id)
        mins_w_d_mods = sorted(mins_w_d_mods, key=lambda m: m.m_id)


        tech_eff_num = 0
        effect_types_in_tech = set()
        for tech in tech_dict.values():
            for eff in tech.effects:
                effect_types_in_tech.add(eff.type)
                tech_eff_num += 1
        
        print()
        print(f"Technologies: {len(tech_dict)}")
        print(f"Total number of technology effects: {tech_eff_num}")
        print(f"Total number of effect types in technologies: {len(effect_types_in_tech)}")
        print(f"Technology effects in default form: {len(def_effs)}")
        print()

        event_eff_num = 0
        effect_types_in_events = set()
        event_cond_num = 0
        condition_types_in_events = set()
        for ev in ed.values():
            for action in ev.actions:
                for eff in action.effects:
                    event_eff_num += 1
                    effect_types_in_events.add(eff.type)
            conditions = get_conditions(ev.trigger, [])
            conditions = [cond for cond, _ in conditions]
            event_cond_num += len(conditions)
            for cond in conditions:
                keys = list(cond.keys())
                if len(keys) > 1:
                    print(f"BIG PROBLEM WITH event {ev.event_id}: TOO MANY KEYS IN CONDITION {cond}")
                condition_types_in_events.add(keys[0])
        
        print(f"Events: {len(ed)}")
        print(f"Total number of event effects: {event_eff_num}")
        print(f"Total number of effect types in events: {len(effect_types_in_events)}")
        print(f"Events with KeyErrors: {len(evs_w_issues)}")
        print(f"Events with effects in default form: {len(evs_w_d_effs)}")
        print()
        print(f"Total number of event conditions: {event_cond_num}")
        print(f"Total number of condition types in events: {len(condition_types_in_events)}")
        print(f"Events with KeyErrors in conditions: {len(evs_w_t_issues)}")
        print(f"Events with conditions in default form: {len(evs_w_d_conds)}")
        print()

        all_effect_types = set()
        for eff_type in effect_types_in_events:
            all_effect_types.add(eff_type)
        for eff_type in effect_types_in_tech:
            all_effect_types.add(eff_type)
        print(f"Total number of effect types: {len(all_effect_types)}")
        print()

        print(f"Ministers: {len(minister_dict)}")
        print(f"Total number of minister modifiers: {minister_mod_num}")
        print(f"Total number of modifier types: {len(mod_types)}")
        print(f"Ministers with KeyErrors: {len(mins_w_issues)}")
        print(f"Ministers with UnboundLocalErrors: {len(mins_w_ULEs)}")
        print(f"Ministers with modifiers in default form: {len(mins_w_d_mods)}")
        print()

        all_text_duplicates = {key: value for key, value in text_dict.items() if len(value) > 1}
        real_text_duplicates = dict()
        files_w_duplicates = set()
        for key, value in all_text_duplicates.items():
            if not key:
                continue
            for text, filepath in value:
                if text != value[0][0]:
                    real_text_duplicates[key] = value
                    files_w_duplicates.add(filepath.name)
                    break
        t_dup = dict()
        for fn in files_w_duplicates:
            t_dup[fn] = {}
            for key, value in real_text_duplicates.items():
                for text, fp in value:
                    if fp.name == fn:
                        t_dup[fn][key] = value

        def show_dupl(*filenames):
            if not filenames:
                filenames = t_dup.keys()
            for filename, t_dict in t_dup.items():
                if filename not in filenames:
                    continue
                print()
                print(f"###   {filename}   ###")
                for key, duplicate_tuple in t_dict.items():
                    print()
                    print(key)
                    for text, filepath in duplicate_tuple:
                        print(f"  in {filepath.name}: ")
                        print(text)
    
    if "raw" in sys.argv:
        force_default = True
    
    if "t" in sys.argv:
        
        while ask_to_search:
            ask_to_search = search_texts(text_dict)
        ask_to_search = False

    if ask_to_search:
        TheSearch = Search(AOD_PATH, fs, max_num_of_suggestions=20, max_text_length=50, force_default=force_default)
        # print(explanation)
        TheSearch.search()
    # while ask_to_search:
    #     # ask_to_search = search_events(event_dict)
    #     ask_to_search = search_events_w_class(AOD_PATH, fs, max_num_of_suggestions=20, force_default=force_default)
    

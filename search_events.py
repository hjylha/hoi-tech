
import sys
from file_paths import AOD_PATH, get_event_text_paths, get_all_text_files_paths
from read_hoi_files import read_scenario_file_for_events, read_txt_file, get_texts_from_files, get_country_names, get_texts_from_files_w_duplicates
from event import Trigger, get_actions, Event, suggest_events_based_on_search_words
from print_effects_and_triggers import print_event


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


def search_events_w_class(event_dict, country_dict, aod_path, text_dict, max_num_of_suggestions=999):
    text_input = input("Enter search term(s):\n")
    if not text_input:
        return False
    possible_country_code = text_input.split(" ")[0].upper()
    country_code = None
    if country_dict.get(possible_country_code) is not None:
        country_code = possible_country_code
        text_input = text_input[4:]
    suggestions = suggest_events_based_on_search_words(text_input, event_dict, country_code)

    indent_add = 2
    print()
    if country_code:
        print(f" Searching restricted to events of {country_dict[country_code]} [{country_code}]\n")
    if not suggestions:
        print(" No matching events found.")
    elif len(suggestions) == 1:
        ev = suggestions[0]
        # ev.print_event(aod_path, 1, indent_add)
        print_event(ev, aod_path, 1, indent_add, text_dict)
    else:
        for event in suggestions[:max_num_of_suggestions]:
            country_code = event.country_code
            country_code = country_code.upper() if country_code else ""
            if event.name:
                print(f" {event.event_id} [{country_code}]: {event.name}")
            else:
                print(f" {event.event_id} [{country_code}]: {event.name_key}  [name in file]")
    print("\n")
    return True


def search_texts(text_dict, max_num_of_suggestions=99, max_text_length=50):
    text_input = input("Enter search term(s):\n").lower()
    if not text_input:
        return False
    starts = []
    others = []
    for k, v_list in text_dict.items():
        if k.lower().startswith(text_input):
            for t, p in v_list:
                starts.append((k, t, p))
            continue
        if text_input in k.lower():
            for t, p in v_list:
                others.append((k, t, p))
        for t, p in v_list:
            if t.lower().startswith(text_input):
                starts.append((k, t, p))
                continue
            if text_input in t.lower():
                others.append((k, t, p))
    suggestions = starts
    for triple in others:
        if triple not in suggestions:
            suggestions.append(triple)
    
    print()
    if not suggestions:
        print("Nothing found")
    if len(suggestions) == 1:
        key, text, path = suggestions[0]
        print(key)
        print(text)
        print(f"[{path.name}]")
    else:
        for key, text, path in suggestions[:max_num_of_suggestions]:
            text_to_print = text if len(text) <= max_text_length else text[:max_text_length] + "[...]"
            print(key, text_to_print, f"[{path.name}]")
    print("\n")

    return True


if __name__ == "__main__":
    SCENARIO_NAME = "1933.eug"
    country_dict = get_country_names()
    # event_text_files = get_event_text_paths(AOD_PATH)
    # texts = get_texts_from_files(event_text_files)
    # event_list = get_event_list(SCENARIO_NAME, AOD_PATH)
    # event_dict, missing_texts = get_event_dict(event_list, texts)
    # no_name, no_desc, no_action = missing_texts
    text_dict = get_texts_from_files_w_duplicates(get_all_text_files_paths())
    text_dict_last = {key: value[-1][0] for key, value in text_dict.items()}

    def get_texts():
        event_text_files = get_event_text_paths(AOD_PATH)
        return event_text_files, get_texts_from_files(event_text_files)
    
    def gel():
        return get_event_list(SCENARIO_NAME, AOD_PATH)
    
    def ged(el, texts):
        return get_event_dict(el, texts)

    ed = scan_events(SCENARIO_NAME, AOD_PATH)

    bad_event_ids = [308008, 336154]
    double_action = [319021]
    
    def pe(event):
        event.print_event(AOD_PATH)

    ask_to_search = True
    explanation = """\n    You can filter by country by typing in country code first:
    for example typing 'fin winter' looks for the word 'winter'
    in event names and descriptions of Finnish events.
    Empty search i.e. pressing Enter quits the program.
    """

    if "d" in sys.argv:
        ask_to_search = False
    
    if "t" in sys.argv:
        
        while ask_to_search:
            ask_to_search = search_texts(text_dict)
        ask_to_search = False

    if ask_to_search:
        print(explanation)
    while ask_to_search:
        # ask_to_search = search_events(event_dict)
        ask_to_search = search_events_w_class(ed, country_dict, AOD_PATH, text_dict_last)
    


from file_paths import AOD_PATH, get_event_text_paths
from read_hoi_files import read_scenario_file_for_events, read_txt_file, get_texts_from_files, get_country_names
from classes import Event


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
                action_name_key = event[key].get(name)
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
        action_keys = []
        for key in event.keys():
            if "action" in key:
                action_keys.append(key)
        action_keys = sorted(action_keys)
        if "action_a" not in action_keys:
            notes += "action_a not a key\n"
        for key in action_keys:
            action = event[key]
            if isinstance(action, list):
                notes += f"key is a list"
                for act in action:
                    actions.append(act)
                continue
            actions.append(action)

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
        country_code = "" if country_code is None else country_code

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
            trigger,
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

    return event_dict


def suggest_events(search_text, event_dict, max_num_of_suggestions=9):
    try:
        event_id = int(search_text)
        if event_dict.get(event_id) is not None:
            return [event_dict[event_id]]
    except ValueError:
        pass
    starts = []
    other = []
    for event_id, event in event_dict.items():
        if event["name"].lower().startswith(search_text.lower()):
            starts.append(event)
            continue
        if search_text.lower() in event["name"].lower():
            other.append(event)
    suggestions = starts + other
    return suggestions[:max_num_of_suggestions]


if __name__ == "__main__":
    SCENARIO_NAME = "1933.eug"
    country_dict = get_country_names()
    event_text_files = get_event_text_paths(AOD_PATH)
    texts = get_texts_from_files(event_text_files)
    event_list = get_event_list(SCENARIO_NAME, AOD_PATH)
    event_dict, missing_texts = get_event_dict(event_list, texts)
    no_name, no_desc, no_action = missing_texts

    bad_event_ids = [308008, 336154]
    double_action = [319021]

    ask_to_search = True
    while ask_to_search:
        text_input = input("Enter search term:\n")
        if not text_input:
            break
        suggestions = suggest_events(text_input, event_dict)
        print()
        if not suggestions:
            print("No matching events found.")
        elif len(suggestions) == 1:
            ev = suggestions[0]
            print(f"{ev["id"]}: {ev["name"]}")
            country_code = ev.get("country")
            country_code = country_code.upper() if country_code else ""
            country = country_dict.get(country_code)
            if country:
                print(f"Country: {country}")
            is_invention = ev.get("invention")
            is_invention = is_invention if is_invention else "no"
            if is_invention.lower() == "yes":
                print("invention event")

            is_random = ev.get("random")
            is_random = is_random if is_random else "no"
            if is_random.lower() == "yes":
                print("random event")
            
            path_str = str(ev["path"])[len(str(AOD_PATH)):]
            print(f"In file: {path_str}")

            desc = ev.get("desc")
            if desc:
                print(desc)
        else:
            for event in suggestions:
                country_code = event.get("country")
                country_code = country_code.upper() if country_code else ""
                print(f"{event["id"]} [{country_code}]: {event["name"]}")
        print()
        # continue_q = input("Do you want to search again? ")
        # if not continue_q.strip().lower().startswith("y"):
        #     ask_to_search = False
    

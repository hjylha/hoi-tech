
from file_paths import AOD_PATH, get_event_text_paths
from read_hoi_files import read_scenario_file_for_events, read_txt_file, get_texts_from_files


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


def get_event_dict(event_list, aod_path):    
    event_text_files = get_event_text_paths(aod_path)
    event_text_dict = get_texts_from_files(event_text_files)

    name = "name"
    desc = "desc"
    for event in event_list:
        name_key = event.get(name)
        if name_key is not None:
            actual_name = event_text_dict.get(name_key)
            if actual_name is not None:
                event[name] = actual_name
        desc_key = event.get(desc)
        if desc_key is not None:
            actual_desc = event_text_dict.get(desc_key)
            if actual_desc is not None:
                event[desc] = actual_desc
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


    event_dict = dict()
    for event in event_list:
        event_id = event["id"]
        if event_dict.get(event_id) is not None:
            print(f"duplicate event id: {event_id}")
            continue
        event_dict[event_id] = event
    return event_dict


if __name__ == "__main__":
    SCENARIO_NAME = "1933.eug"
    event_text_files = get_event_text_paths(AOD_PATH)
    texts = get_texts_from_files(event_text_files)
    event_list = get_event_list(SCENARIO_NAME, AOD_PATH)
    event_dict = get_event_dict(event_list, AOD_PATH)
    ed = dict()
    for event in event_list:
        event_id = event["id"]
        if ed.get(event_id) is not None:
            print(f"duplicate event id: {event_id}")
            continue
        ed[event_id] = event
    name = "name"
    desc = "desc"
    for event in event_list:
        name_key = event.get(name)
        if name_key is not None:
            actual_name = texts.get(name_key)
            if actual_name is not None:
                event[name] = actual_name
        desc_key = event.get(desc)
        if desc_key is not None:
            actual_desc = texts.get(desc_key)
            if actual_desc is not None:
                event[desc] = actual_desc

    bad_event_ids = [308008, 336154]
    double_action = [319021]
    

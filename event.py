
from classes import Effect


class Condition:
    AND_STR = "AND"
    OR_STR = "OR"
    NOT_STR = "NOT"
    AND_OR_NOT = (AND_STR, OR_STR, NOT_STR)

    def __init__(self, event_id, condition_dict, connective=None):
        self.event_id = event_id
        self.connective = connective
        self.condition = None
        self.child_conditions = []
        if len(condition_dict) == 1 and not isinstance(list(condition_dict.values())[0], list):
            if self.NOT_STR in condition_dict:
                self.child_conditions = [Condition(event_id, condition_dict[self.NOT_STR], self.NOT_STR)]
                return
            for key, value in condition_dict.items():
                if key.upper() in self.AND_OR_NOT:
                    self.child_conditions = [Condition(event_id, value, key.upper())]
                    return
            self.condition = condition_dict
            return
        # if self.connective is None:
        #     self.connective = self.AND_STR
        for key, value in condition_dict.items():
            if isinstance(value, list):
                for item in value:
                    if key.upper() in self.AND_OR_NOT:
                        self.child_conditions.append(Condition(event_id, item, key.upper()))
                    else:
                        self.child_conditions.append(Condition(event_id, {key: item}))
                continue
            if key.upper() in self.AND_OR_NOT:
                self.child_conditions.append(Condition(event_id, value, key.upper()))
                continue
            self.child_conditions.append(Condition(event_id, {key: value}))

    def get_condition_keys(self, list_of_condition_keys, keyword=""):
        if self.condition:
            new_keys = tuple([key.lower() for key in self.condition.keys()])
            for key in new_keys:
                if keyword in key:
                    break
            else:
                return list_of_condition_keys
            if new_keys not in list_of_condition_keys:
                list_of_condition_keys.append(new_keys)
            return list_of_condition_keys
        for condition in self.child_conditions:
            list_of_condition_keys = condition.get_condition_keys(list_of_condition_keys, keyword)
        return list_of_condition_keys
    
    def is_keyword_in_condition(self, condition_type, keyword, score=0, debug_thing=False):
        if self.condition:
            condition_key = list(self.condition.keys())[0].lower()
            condition_value = list(self.condition.values())[0]
            condition_value_str = str(condition_value)
            # if debug_thing:
            #     print(f" {condition_key=} \n {condition_value=} \n {condition_value_str}")
            #     print(f"{condition_type=}")
            if condition_type in condition_key and keyword in condition_value_str:
                if condition_type == condition_key:
                    # if debug_thing:
                    #     print(f"MATCH: {condition_key} = {condition_type}")
                    multiplier = 100
                elif condition_key.startswith(condition_type):
                    # if debug_thing:
                    #     print(f"NOT QUITE MATCH: {condition_key} != {condition_type}")
                    multiplier = 10
                else:
                    multiplier = 1
                if keyword == condition_value_str:
                    # if debug_thing:
                    #     print(self.condition)
                    #     print(f"MATCH: {condition_value_str} = {keyword}")
                    #     print(100 * multiplier)
                    score += 100 * multiplier
                elif condition_value_str.startswith(keyword):
                    # if debug_thing:
                    #     print(self.condition)
                    #     print(f"NOT QUITE MATCH: {condition_value_str} != {keyword}")
                    score += 10 * multiplier
                else:
                    # if debug_thing:
                    #     print(self.condition)
                    #     print(f"SOME MATCHING: {condition_value_str} != {keyword}")
                    score += 1 * multiplier
                return score
            return score
        for condition in self.child_conditions:
            score = condition.is_keyword_in_condition(condition_type, keyword, score, debug_thing)
        return score
        

    def print_condition(self, indent_num, indent_add):
        if self.condition is not None:
            if self.connective and self.connective == self.NOT_STR:
                print(indent_num * " ", f"{self.NOT_STR} (", end=" ")
            else:
                print(indent_num * " ", end=" ")
            first = True
            for key, value in self.condition.items():
                if not first:
                    print(", ", end="")
                else:
                    first = False
                print(f"{key} = {value}", end="")
            if self.connective and self.connective == self.NOT_STR:
                print(" )", end="\n")
            else:
                print()
            return
        if self.connective:
            print(indent_num * " ", self.connective)
            for condition in self.child_conditions:
                condition.print_condition(indent_num + indent_add, indent_add)
        else:
            for condition in self.child_conditions:
                condition.print_condition(indent_num, indent_add)


class Trigger(Condition):
    AND_OR_NOT = ("AND", "OR", "NOT")
    
    def __init__(self, event_id, trigger_dict):
        self.raw_conditions = trigger_dict
        if trigger_dict:
            super().__init__(event_id, trigger_dict)
        else:
            self.condition = None
            self.event_id = event_id
            self.child_conditions = []        

    def print_trigger(self, indent_num, indent_add, empty_trigger=True):
        if not self.raw_conditions and empty_trigger:
            print(indent_num * " ", "-")
            return
        if not self.raw_conditions:
            return
        self.print_condition(indent_num, 2 * indent_add)
        # if isinstance(self.raw_conditions, dict):
        #     for key, item in self.raw_conditions.items():
        #         if key.upper() in ["NOT", "AND", "OR"]:
        #             print(indent_num * " ", key.upper())
        #             indent_num += indent_add
        #             if isinstance(item, dict):
        #                 for k, it in item.items():
        #                     print(indent_num * " ", k, "=", it)
        #             elif isinstance(item, list):
        #                 for it in item:
        #                     print(indent_num * " ", it)
        #             indent_num -= indent_add
        #             continue
        #         print(indent_num * " ", key, "=", item)
        #     return
        # if isinstance(self.raw_conditions, list):
        #     for item in self.raw_conditions:
        #         print(indent_num * " ", item)
        #     return
        # print(f"PROBLEM: trigger is of type {type(self.raw_conditions)}")


def get_conditions(condition, list_of_conditions):
    if condition.condition:
        list_of_conditions.append([condition.condition, condition.event_id])
        return list_of_conditions
    for cond in condition.child_conditions:
        list_of_conditions = get_conditions(cond, list_of_conditions)
    return list_of_conditions


def get_all_conditions(event_dict):
    conditions = []
    for event in event_dict.values():
        conditions_plus = get_conditions(event.trigger, [])
        conditions += conditions_plus
    return conditions


class Action:

    def __init__(self, action_key, name_key, name="", ai_chance=None, effects=None):
        self.action_key = action_key
        self.name_key = name_key
        self.name = name

        self.ai_chance = ai_chance

        effects = [] if not effects else effects
        if isinstance(effects, dict):
            effects = [effects]
        self.effects = []
        for effect in effects:
            self.effects.append(Effect(effect.get("type"), effect.get("which"), effect.get("value"), effect.get("when"), effect.get("where")))
        
    def __str__(self):
        return f"{self.action_key}: {self.name}"
    
    def print_action(self, indent_num, indent_add):
        if self.name:
            print(indent_num * " ", f"({self.action_key})", self.name)
        elif self.name_key:
            print(indent_num * " ", f"({self.action_key})", self.name_key, " [name in file]")
        else:
            print(indent_num * " ", f"({self.action_key})", " [no name]")
        indent_num += indent_add
        if self.ai_chance is not None:
            print(indent_num * " ", f"AI chance: {self.ai_chance} %")
        
        if not self.effects:
            print(indent_num * " ", "Effects:")
            indent_num += indent_add
            print(indent_num * " ", "-")
            return
        print(indent_num * " ", f"Effects ({len(self.effects)}):")
        indent_num += indent_add
        for effect in self.effects:
            text_parts = []
            type_part = f"type = {effect.type}" if effect.type is not None else ""
            text_parts.append(type_part)
            which_part = f"which = {effect.which}" if effect.which is not None else ""
            text_parts.append(which_part)
            value_part = f"value = {effect.value}" if effect.value is not None else ""
            text_parts.append(value_part)
            when_part = f"when = {effect.when}" if effect.when is not None else ""
            text_parts.append(when_part)
            where_part = f"where = {effect.where}" if effect.where is not None else ""
            text_parts.append(where_part)
            text_parts = [t for t in text_parts if t]
            # effect_line = f"{type_part}, {which_part}, {value_part}, {when_part}, {where_part}"
            print(indent_num * " ", ", ".join(text_parts))


def get_actions(list_of_action_dicts, text_dict):
    actions = []
    key_to_action_key = "action_key"
    key_to_name_key = "name"
    key_to_ai_chance = "ai_chance"
    key_to_effects = "command"
    for action in list_of_action_dicts:
        action_key = action[key_to_action_key]
        name_key = action.get(key_to_name_key)
        name = text_dict.get(name_key)
        name = "" if name is None else name
        ai_chance = action.get(key_to_ai_chance)
        effects = action.get(key_to_effects)
        actions.append(Action(action_key, name_key, name, ai_chance, effects))
    return actions


class Event:
    EVENT_KEYS = [
        "id",
        "random",
        "invention",
        "country",
        "trigger",
        "name",
        "desc",
        "style",
        "date",
        "offset",
        "deathdate",
        "persistent",
        "picture",
        "action_a",
        "action_b",
        "action_c",
        "action_d",
        "action_e"
    ]

    def __init__(
        self,
        filepath,
        event_id,
        name_key,
        name,
        actions,
        is_random=False,
        is_invention=False,
        country_code=None,
        country=None,
        trigger=None,
        desc_key=None,
        description="",
        style=0,
        picture="",
        date=None,
        offset=None,
        deathdate=None,
        is_persistent=False,
        notes="",
        triggered_by=None,
        deactivated_by=None
    ):
        self.event_id = event_id
        self.filepath = filepath
        self.name_key = name_key
        self.name = name
        self.desc_key = desc_key
        self.description = description

        self.country_code = country_code
        self.country = country

        self.is_random = is_random
        self.is_invention = is_invention
        self.is_persistent = is_persistent

        self.trigger = trigger
        self.triggered_by = [] if triggered_by is None else triggered_by

        self.deactivated_by = [] if deactivated_by is None else deactivated_by

        self.date = date
        self.offset = offset
        self.deathdate = deathdate

        self.actions = actions

        self.notes = notes

        self.style = style
        self.picture = picture
    
    # def set_triggered_by(self, trigger_event_id, trigger_action_key):
    #     self.triggered_by = (trigger_event_id, trigger_action_key)
    
    def __str__(self):
        return f"{self.event_id} [{self.country_code}]: {self.name}"
    
    def is_keyword_in_condition(self, condition_type, keyword, score=0, debug_thing=False):
        # if debug_thing and self.event_id == 348:
        #     print(f"DEBUGGING")
        #     return self.trigger.is_keyword_in_condition(condition_type, keyword, score, debug_thing)
        return self.trigger.is_keyword_in_condition(condition_type, keyword, score)

    def print_event(self, aod_path, indent_num=0, indent_add=2):
        if self.name:
            print(f"{indent_num * ' '} {self.event_id}: {self.name}")
        else:
            print(f"{indent_num * ' '} {self.event_id}: {self.name_key}  [name in file]")
        if self.country:
            print(f"{indent_num * ' '} Country: {self.country}")
        if self.is_invention:
            print(f"{indent_num * ' '} Invention event")
        if self.is_random:
            print(f"{indent_num * ' '} Random event")
        
        path_str = str(self.filepath)[len(str(aod_path)) + 1:]
        print(f"{indent_num * ' '} In file: {path_str}")

        print()
        print(indent_num * ' ', "Trigger:")
        trigger_empty = True
        if self.triggered_by:
            trigger_empty = False
            print((indent_num + indent_add) * " ", "Triggered by:")
            for trigger_event, action_index in self.triggered_by:
                text_about_event = f"event {trigger_event.event_id} [{trigger_event.country}]: {trigger_event.name}"
                text_about_action = f"action '{trigger_event.actions[action_index].name}' [{trigger_event.actions[action_index].action_key}]"
                print((indent_num + 2 * indent_add) * " ", f"{text_about_event}, {text_about_action}")
        self.trigger.print_trigger(indent_num + indent_add, indent_add, empty_trigger=trigger_empty)
        print()

        if self.date:
            print(indent_num * ' ', "Date:")
            print(indent_num * ' ', self.date["day"], self.date["month"], self.date["year"])
        if self.offset is not None:
            print(f"{indent_num * ' '} Offset: {self.offset}")
        if self.deathdate:
            print(indent_num * ' ', "Deathdate:")
            print(indent_num * ' ', self.deathdate["day"], self.deathdate["month"], self.deathdate["year"])
        
        if self.is_persistent:
            print(indent_num * ' ', "Persistent event")

        print()
        print(f"{indent_num * ' '} Description:")
        if self.description:
            print(indent_num * ' ', self.description)
        else:
            print(indent_num * ' ', "-")

        print()
        print(indent_num * ' ', "Possible Actions:")
        for action in self.actions:
            action.print_action(indent_num + indent_add, indent_add)

def get_event_from_raw_event(raw_event_dict, filepath, event_text_dict):    
    notes = ""

    trigger = raw_event_dict.get("trigger")
    if trigger is None or not trigger:
        trigger = dict()
    # TODO: Trigger class?
    name = event_text_dict.get(raw_event_dict["name"])
    name = "" if name is None else name

    desc_key = raw_event_dict.get("desc")
    desc_key = "" if desc_key is None else desc_key
    desc = event_text_dict.get(desc_key)
    desc = "" if desc is None else desc

    actions = []
    # TODO: Action class
    action_keys = []
    for key in raw_event_dict.keys():
        if "action" in key:
            action_keys.append(key)
    action_keys = sorted(action_keys)
    action_key = "action_key"
    if "action_a" not in action_keys:
        notes += "action_a not a key\n"
    for key in action_keys:
        action = raw_event_dict[key]
        if isinstance(action, list):
            notes += f"{key} is a list"
            for act in action:
                act[action_key] = key
                actions.append(act)
            continue
        action[action_key] = key
        actions.append(action)
    actions = get_actions(actions, event_text_dict)

    is_random_str = raw_event_dict.get("random")
    is_random_str = "no" if not is_random_str else is_random_str
    is_random = True if is_random_str.lower() == "yes" else False

    is_invention_str = raw_event_dict.get("invention")
    is_invention_str = "no" if not is_invention_str else is_invention_str
    is_invention = True if is_invention_str.lower() == "yes" else False

    is_persistent_str = raw_event_dict.get("persistent")
    is_persistent_str = "no" if not is_persistent_str else is_persistent_str
    is_persistent = True if is_persistent_str.lower() == "yes" else False

    country_code = raw_event_dict.get("country")
    country_code = "" if country_code is None else country_code.upper()

    country = event_text_dict.get(country_code)
    country = "" if country is None else country

    date = raw_event_dict.get("date")
    date = dict() if date is None else date

    offset = raw_event_dict.get("offset")

    death_date = raw_event_dict.get("deathdate")
    death_date = dict() if death_date is None else death_date

    picture = raw_event_dict.get("picture")
    picture = "" if picture is None else picture

    style = raw_event_dict.get("style")
    style = "" if style is None else style
    
    proper_event = Event(
        raw_event_dict["path"],
        raw_event_dict["id"],
        raw_event_dict["name"],
        name,
        actions,
        is_random,
        is_invention,
        country_code,
        country,
        Trigger(raw_event_dict["id"], trigger),
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
    return proper_event


def suggest_events_based_on_search_words(search_text, event_dict, country_codes=None):
    # exact_keyword = False
    print(f"{search_text=} {country_codes=}")
    try:
        event_id = int(search_text)
        if event_dict.get(event_id) is not None:
            return [[event_dict[event_id], 1]]
    except ValueError:
        pass
    keywords = []
    type_value_pairs = dict()
    search_text = search_text.strip()
    if not search_text:
        keywords = [""]
    while search_text:
        if search_text.startswith('"') and '"' in search_text[1:]:
            end_index = search_text[1:].index('"') + 1
            keywords.append(search_text[1:end_index].lower())
            search_text = search_text[end_index + 1:].strip()
            continue
        possible_keyword = search_text.split(" ")[0].strip()
        if "=" in possible_keyword[1:]:
            type_str = possible_keyword.split("=")[0].lower()
            value_str = possible_keyword[len(type_str) + 1:].lower()
            type_value_pairs[type_str] = value_str
            search_text = search_text[len(possible_keyword):].strip()
            continue
        keywords.append(possible_keyword.lower())
        search_text = search_text[len(possible_keyword):].strip()
    # try:
    #     if search_text.strip()[0] == '"' and search_text.strip()[-1] == '"':
    #         search_text = search_text.strip()[1:-1]
    #         exact_keyword = True
    # except IndexError:
    #     pass
    # if exact_keyword:
    #     suggestions = []
    #     for event_id, event in event_dict.items():
    #         if country_codes and event.country_code not in country_codes:
    #             continue
    #         if event.name == search_text:
    #             suggestions.append(event)
    #             continue
    #         if event.description == search_text:
    #             suggestions.append(event)
    #             continue
    #         for action in event.actions:
    #             if not action.name:
    #                 continue
    #             if action.name == search_text:
    #                 suggestions.append(event)
    #                 break
    #     return suggestions
    # search_text = search_text.lower()
    suggestions = []
    scores = dict()
    for event_id, event in event_dict.items():
        if country_codes and event.country_code not in country_codes:
            continue
        score = 0
        all_keywords_found = False
        for keyword in keywords:
            keyword_score = 0
            event_name = event.name.lower()
            if keyword == event_name:
                keyword_score +=10_000
            elif event_name.startswith(keyword):
                keyword_score += 500
            elif keyword in event_name:
                keyword_score += 10

            try:
                event_description = event.description.lower()
                if keyword == event_description:
                    keyword_score += 1000
                if event_description.startswith(keyword):
                    keyword_score += 100
                if keyword in event_description:
                    keyword_score += 1
            except AttributeError:
                pass

            for action in event.actions:
                if not action.name:
                    continue
                action_name = action.name.lower()
                if keyword == action_name:
                    keyword_score += 1000
                if action_name.startswith(keyword):
                    keyword_score += 100
                if keyword in action_name:
                    keyword_score += 5
            if keyword_score > 0:
                score += keyword_score
                continue
            break
        else:
            all_keywords_found = True
        if not all_keywords_found:
            continue
        # all_type_value_pairs_found = False
        for type_str, value_str in type_value_pairs.items():
            t_v_score = 0
            trigger_score = event.is_keyword_in_condition(type_str, value_str, 0, debug_thing=True)
            t_v_score += trigger_score

            if date_value := event.date.get(type_str):
                date_value_str = str(date_value).lower()
                if value_str == date_value_str:
                    t_v_score += 1000
                elif date_value_str.startswith(value_str):
                    t_v_score += 100
                elif value_str in date_value_str:
                    t_v_score += 5
            
            # found_in_effects = False
            for action in event.actions:
                for effect in action.effects:
                    effect_type_str = effect.type.lower()
                    if type_str in effect_type_str:
                        if type_str == effect_type_str:
                            multiplier = 100
                        elif effect_type_str.startswith(type_str):
                            multiplier = 10
                        else:
                            multiplier = 1
                        for item in effect:
                            if item and value_str in str(item).lower():
                                item_str = str(item).lower()
                                # TODO: should this check for highest score?
                                if value_str == item_str:
                                    t_v_score += 100 * multiplier
                                if item_str.startswith(value_str):
                                    t_v_score += 10 * multiplier
                                t_v_score += 1 * multiplier
            if t_v_score > 0:
                score += t_v_score
                continue
            break
        else:
            # all_type_value_pairs_found = True
            suggestions.append(event)
            scores[event_id] = score
            continue

    # suggestions = name_starts + name_other + desc_starts + desc_other + action_things
    # if cond_or_effect_type:
    #     suggestions += trigger_things + effect_things + date_things
    suggestions_and_scores = [[ev, scores[ev.event_id]] for ev in suggestions]
    return sorted(suggestions_and_scores, key=lambda pair: pair[1], reverse=True)
    # return sorted(suggestions, key=lambda ev: scores[ev.event_id], reverse=True)

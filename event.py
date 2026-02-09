
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
    
    def is_keyword_in_condition(self, condition_type, keyword):
        if self.condition:
            if condition_type.lower() in list(self.condition.keys())[0].lower() and keyword.lower() in str(self.condition).lower():
                return True
            return False
        for condition in self.child_conditions:
            is_keyword_in = condition.is_keyword_in_condition(condition_type, keyword)
            if is_keyword_in:
                return True
        return False
        

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


def suggest_events_based_on_search_words(search_text, event_dict, country_code=None, cond_or_effect_type="", cond_or_effect_keyword=""):
    exact_keyword = False
    try:
        event_id = int(search_text)
        if event_dict.get(event_id) is not None:
            return [event_dict[event_id]]
    except ValueError:
        pass
    try:
        if search_text.strip()[0] == '"' and search_text.strip()[-1] == '"':
            search_text = search_text.strip()[1:-1]
            exact_keyword = True
    except IndexError:
        pass
    if exact_keyword:
        suggestions = []
        for event_id, event in event_dict.items():
            if country_code and event.country_code != country_code:
                continue
            if event.name == search_text:
                suggestions.append(event)
                continue
            if event.description == search_text:
                suggestions.append(event)
                continue
            for action in event.actions:
                if not action.name:
                    continue
                if action.name == search_text:
                    suggestions.append(event)
                    break
        return suggestions
    search_text = search_text.lower()
    name_starts = []
    name_other = []
    desc_starts = []
    desc_other = []
    action_things = []
    if cond_or_effect_type:
        trigger_things = []
        effect_things = []
    for event_id, event in event_dict.items():
        if cond_or_effect_type and event.trigger.is_keyword_in_condition(cond_or_effect_type, cond_or_effect_keyword):
            trigger_things.append(event)
        if country_code and event.country_code != country_code:
            continue
        if event.name.lower().startswith(search_text):
            name_starts.append(event)
            continue
        if search_text in event.name.lower():
            name_other.append(event)
            continue
        if event.description is None:
            continue
        if event.description.lower().startswith(search_text):
            desc_starts.append(event)
            continue
        if search_text in event.description.lower():
            desc_other.append(event)
            continue
        for action in event.actions:
            if not action.name:
                continue
            if search_text in action.name.lower():
                action_things.append(event)
                break
            if cond_or_effect_type:
                found_cond_or_effect = False
                for effect in action.effects:
                    if cond_or_effect_type.lower() in effect.type.lower():
                        for item in effect:
                            if item and cond_or_effect_keyword.lower() in str(item).lower():
                                effect_things.append(event)
                                found_cond_or_effect = True
                                break
                if found_cond_or_effect:
                    break

    suggestions = name_starts + name_other + desc_starts + desc_other + action_things
    if cond_or_effect_type:
        suggestions += trigger_things + effect_things

    return suggestions

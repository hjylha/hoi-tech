
from classes import Effect


class Condition:
    AND_STR = "AND"
    OR_STR = "OR"
    NOT_STR = "NOT"
    AND_OR_NOT = (AND_STR, OR_STR, NOT_STR)

    def __init__(self, condition_dict, connective=None):
        self.connective = connective
        self.condition = None
        self.child_conditions = []
        if len(condition_dict) == 1 and not isinstance(list(condition_dict.values())[0], list):
            if self.NOT_STR in condition_dict:
                self.connective = self.NOT_STR
                self.condition = condition_dict[self.NOT_STR]
                return
            for key, value in condition_dict.items():
                if key.upper() in self.AND_OR_NOT:
                    self.child_conditions = [Condition(value, key.upper())]
                    return
            self.condition = condition_dict
            return
        # if self.connective is None:
        #     self.connective = self.AND_STR
        for key, value in condition_dict.items():
            if isinstance(value, list):
                for item in value:
                    if key.upper() in self.AND_OR_NOT:
                        self.child_conditions.append(Condition(item, key.upper()))
                    else:
                        self.child_conditions.append(Condition({key: item}))
                continue
            if key.upper() in self.AND_OR_NOT:
                self.child_conditions.append(Condition(value, key.upper()))
                continue
            self.child_conditions.append(Condition({key: value}))
        

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
    
    def __init__(self, trigger_dict):
        self.raw_conditions = trigger_dict
        if trigger_dict:
            super().__init__(trigger_dict)
        else:
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
        triggered_by=None
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


def suggest_events_based_on_search_words(search_text, event_dict, country_code=None):
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
    suggestions = name_starts + name_other + desc_starts + desc_other + action_things
    
    return suggestions

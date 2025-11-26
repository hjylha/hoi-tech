
import csv


def change_type_if_necessary(text):
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text.strip('" ')

def get_first_item_from_text(text):
    if text[0] in "{}=":
        return (text[0], text[1:].strip())
    if text[0] == '"':
        item = text[1:].split('"')[0]
        return (item, text[len(item) + 2:].strip())
    if text[0] == "'":
        item = text[1:].split("'")[0]
        return (item, text[len(item) + 2:].strip())
    
    item = text
    for symbol in "{}=":
        if symbol in text:
            item = text.split(symbol)[0].strip()
    item = item.split(" ")[0].strip().split("\t")[0].strip()
    
    return (change_type_if_necessary(item), text[len(item):].strip())


def read_csv_file(filepath, encoding, check_filetype=False, delimiter=";"):
        if check_filetype and filepath.suffix != ".csv":
            print(f"{filepath} is not a csv file.")
            return
        csv_content_list = None
        with open(filepath, "r", encoding = encoding) as f:
            csv_reader = csv.reader(f, delimiter=delimiter)
            csv_content_list = []
            for line in csv_reader:
                csv_content_list.append([change_type_if_necessary(item) for item in line[:-1]])
            # csv_content_list = [line[:-1] for line in csv_reader]
        return csv_content_list


def read_inside_brackets(opened_file, current_line):
    # while not current_line:
    #     raw_line = opened_file.readline()
    #     if not raw_line:
    #         raise Exception("File has curly brackets mismatch.")
    #     current_line = raw_line.split("#")[0].strip()
    current_list_or_dict = []
    # if current_line[0] == "}":
    #     return [current_list_or_dict, current_line[1:]]
    
    previous_object = None
    previous_key = None
    key_value_counts = dict()
    previous_item = None
    while True:
        while not current_line:
            raw_line = opened_file.readline()
            if not raw_line:
                return [current_list_or_dict, raw_line]
            current_line = raw_line.split("#")[0].strip()
        item, current_line = get_first_item_from_text(current_line)
        if item == "}":
            if not current_list_or_dict:
                if previous_item is not None:
                    return [[previous_item], current_line]
                return [[], current_line]
            # if previous_item == "}" or previous_key is not None:
            return [current_list_or_dict, current_line]

        if item == "{":
            new_object, current_line = read_inside_brackets(opened_file, current_line)
            # if previous_text is None:
            #     current_list_or_dict.append(new_object)
            previous_item = "}"
            if previous_key is None:
                if new_object is not None:
                    current_list_or_dict.append(new_object)
                continue
            
            num_of_values_for_key = key_value_counts.get(previous_key)
            if num_of_values_for_key is None:
                key_value_counts[previous_key] = 1
                current_list_or_dict[previous_key] = new_object
                continue
            if num_of_values_for_key == 1:
                key_value_counts[previous_key] += 1
                current_list_or_dict[previous_key] = [current_list_or_dict[previous_key], new_object]
                continue
            current_list_or_dict[previous_key].append(new_object)
            continue
                
        if item == "=":
            previous_key = previous_item
            previous_item = "="
            if not isinstance(current_list_or_dict, dict):
                current_list_or_dict = dict()
            continue
        if previous_item == "=":
            num_of_values_for_key = key_value_counts.get(previous_key)
            if num_of_values_for_key is None:
                key_value_counts[previous_key] = 1
                current_list_or_dict[previous_key] = item
            elif num_of_values_for_key == 1:
                key_value_counts[previous_key] += 1
                current_list_or_dict[previous_key] = [current_list_or_dict[previous_key], item]
            else:
                current_list_or_dict[previous_key].append(item)
            previous_item = "}"
            continue
        if isinstance(current_list_or_dict, list) and current_list_or_dict:
            current_list_or_dict.append(item)
            previous_item = item
            continue
        if previous_item is None:
            previous_item = item
            continue
        if not isinstance(previous_item, str) or len(previous_item) > 1 or previous_item not in "{}=":
            current_list_or_dict.append(previous_item)
            current_list_or_dict.append(item)
            previous_item = item
            continue
        previous_item = item
        
    # if "}" in current_line:

    # while "}" not in current_line:
    return [current_list_or_dict, current_line[1:].strip()]


# def read_txt_file0(filepath, check_filetype=False):
def read_txt_file(filepath, encoding, check_filetype=False):
    if check_filetype and filepath.suffix != ".txt":
        print(f"{filepath} is not a txt file.")
        return
    
    with open(filepath, "r", encoding = encoding) as f:
        content, _ = read_inside_brackets(f, "")
    if isinstance(content, list) and len(content) == 1:
        content = content[0]
    return content


# def read_txt_file(filepath, check_filetype=False):
#     if check_filetype and filepath.suffix != ".txt":
#         print(f"{filepath} is not a txt file.")
#         return
#     content = dict()
    
#     with open(filepath, "r", encoding = the_encoding) as f:
#         nested_keys = []
#         nested_values = []
#         previous_text = None
#         for line in f:
#             clean_line = line.split("#")[0].strip()
#             if not clean_line:
#                 continue
#             while clean_line:
#                 item = clean_line.split(" ")[0].strip().split("\t")[0].strip()
#                 # previous_text = item
#                 # clean_line = clean_line[len(item):].strip()
#                 if item[0] == "{":
#                     item = "{"
#                     # if previous_text == "{":
#                     #     nested_keys.append(None)
#                     #     nested_values.append([])
#                     if previous_text != "=":
#                         # TODO: handle pure list
#                         print(line)
#                         raise Exception(f"{previous_text} {item} can not be handled (at least not yet...)")
#                     # 
#                     # print("{", previous_text, item)
#                     clean_line = clean_line[1:].strip()
#                     # previous_text = item
#                     previous_text = item
#                     continue
#                 if item[0] == "=":
#                     item = "="
#                     if previous_text in ["{", "=", "}"]:
#                         raise Exception(f"{previous_text} {item} can not be handled")
#                     nested_keys.append(change_type_if_necessary(previous_text))
#                     if previous_text is None:
#                         print(line)
#                     nested_values.append(None)
#                     # 
#                     # print("=", previous_text, item)
#                     clean_line = clean_line[1:].strip()
#                     previous_text = item
#                     continue
#                 if item[0] == "}":
#                     item = "}"
#                     # 
#                     key = nested_keys.pop()
#                     value = nested_values.pop()

#                     # print()
#                     # print(nested_keys)
#                     # for v in nested_values:
#                     #     print(v)
#                     # print(len(nested_values), "values")

#                     if value is None:
#                         value = [change_type_if_necessary(previous_text)]
#                     # if isinstance(value, list):
#                     #     value.append(change_type_if_necessary(previous_text))
#                     if not nested_keys:
#                         if content.get(key) is None:
#                             content[key] = value
#                         elif isinstance(content[key], list):
#                             content[key].append(value)
#                         else:
#                             content[key] = [content[key], value]
#                     elif nested_values[-1] is None:
#                         nested_values[-1] = {key: value}
#                     elif key in nested_values[-1].keys():
#                         if isinstance(nested_values[-1][key], list):
#                             nested_values[-1][key].append(value)
#                         else:
#                             nested_values[-1][key] = [nested_values[-1][key], value]
#                     else:
#                         nested_values[-1][key] = value

#                     # print("}", previous_text, item)
#                     clean_line = clean_line[1:].strip()
#                     # previous_text = item
#                     previous_text = None
#                     continue
#                 if "=" in item:
#                     item = item.split("=")[0].strip()
#                 if "}" in item:
#                     item = item.split("}")[0].strip()
#                 if item[0] == '"':
#                     quoted_text = clean_line[1:].split('"')[0]
#                     item = f'"{quoted_text}"'
#                 if previous_text == "=":
#                     key = nested_keys.pop()
#                     value = nested_values.pop()
#                     if value is not None:
#                         raise Exception(f"{value} should be None")
#                     value = change_type_if_necessary(item)
#                     if not nested_keys:
#                         if content.get(key) is None:
#                             content[key] = value
#                         elif isinstance(content[key], list):
#                             content[key].append(value)
#                         else:
#                             content[key] = [content[key], value]
#                     elif nested_values[-1] is None:
#                         nested_values[-1] = {key: value}
#                     elif key in nested_values[-1].keys():
#                         if isinstance(nested_values[-1][key], list):
#                             nested_values[-1][key].append(value)
#                         else:
#                             nested_values[-1][key] = [nested_values[-1][key], value]
#                     else:
#                         nested_values[-1][key] = value
#                     # nested_values[-1] = change_type_if_necessary(item)
#                     # print(previous_text, item)
#                     previous_text = None
#                     clean_line = clean_line[len(item):].strip()
#                     continue
#                 if previous_text is not None and previous_text != "{":
#                     if nested_values[-1] is None:
#                         nested_values[-1] = [change_type_if_necessary(previous_text), change_type_if_necessary(item)]
#                     elif isinstance(nested_values[-1], list):
#                         nested_values[-1].append(change_type_if_necessary(item))
#                     else:
#                         raise Exception(f"{item} and {previous_text} do not seem to go to {nested_values[-1]}")
#                     # print(previous_text, item)
#                     previous_text = item
#                     clean_line = clean_line[len(item):].strip()
#                     continue

#                 # previous_text = item
#                 # print("no conditions", previous_text, item)
#                 previous_text = item
#                 clean_line = clean_line[len(item):].strip()


#                 # stuff
                
#             # if "}" in clean_line:
#     return content
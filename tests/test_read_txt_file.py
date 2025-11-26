
from pathlib import Path

import pytest

import fix_imports
import read_hoi_files as rhf


@pytest.fixture
def txt_file_content0():
    return {"key1": "normal value", "key2": 2, "key3": 3.14}

@pytest.fixture
def txt_file_content1():
    content = dict()
    content["layer0"] = {
        "key1": "normal",
        "key2": 2,
        "key3": 3.14
    }
    return content

@pytest.fixture
def txt_file_content2():
    content = dict()
    content["layer0"] = {
        "key1": "normal",
        "key2": 2,
        "key3": 3.14
    }
    layer1 = {
        "key1": [3, 5],
        "key2": ["a", "b", "c"],
        "key3": []
    }
    content["layer0"]["layer1"] = layer1
    return content

@pytest.fixture
def txt_file_content3():
    content = dict()
    content["layer0"] = {
        "key1": "normal",
        "key2": 2,
        "key3": 3.14
    }
    layer2 = {"key1": [0, 1]}
    layer1 = {
        "key1": [3, 5],
        "key2": ["a", "b", "c"],
        "layer2": layer2
    }
    content["layer0"]["layer1"] = layer1
    return content


@pytest.fixture
def txt_file_content_list0():
    return []

@pytest.fixture
def txt_file_content_list1():
    return [[1, 2, 3, 4], [5, 6, 7, 8]]

@pytest.fixture
def txt_file_content_list2():
    dict1 = {
        "key1": "normal value",
        "key2": 2,
        "key3": 3.14
    }
    dict2 = {
        "key1": "not normal",
        "key2": 1,
        "key3": 3.14
    }
    return [dict1, dict2]


@pytest.mark.parametrize(
        "text, result", [
            ("0", 0),
            ("314", 314),
            ("-5", -5),
            ("2.71", 2.71),
            ("0.500", 0.5),
            ("-3.140", -3.14),
            ("testing", "testing"),
            ('"quoted"', 'quoted'),
            ("  testing  ", "testing")
        ]
)
def test_change_type_if_necessary(text, result):
    assert rhf.change_type_if_necessary(text) == result


@pytest.mark.parametrize(
    "text, first_item, the_rest", [
        ("value = 3", "value", "= 3"),
        ("{abcdefg}", "{", "abcdefg}"),
        ("=123abc {}", "=", "123abc {}"),
        ("'big if true'={123}", "big if true", "={123}"),
        ('"same with other quotation marks"= 123', "same with other quotation marks", "= 123"),
        ("1 is one", 1, "is one"),
        ("}123abc={", "}", "123abc={"),
        ("3.14 = pi", 3.14, "= pi"),
        ("-2.7 -1 1.608", -2.7, "-1 1.608")
    ]
)
def test_get_first_item_from_text(text, first_item, the_rest):
    assert rhf.get_first_item_from_text(text) == (first_item, the_rest)

def test_get_first_item_from_text_iterative():
    full_line = "{1 2 3 4}"
    item0, line0 = rhf.get_first_item_from_text(full_line)
    assert item0 == "{"
    assert line0 == "1 2 3 4}"
    item1, line1 = rhf.get_first_item_from_text(line0)
    assert item1 == 1
    assert line1 == "2 3 4}"
    item2, line2 = rhf.get_first_item_from_text(line1)
    assert item2 == 2
    assert line2 == "3 4}"
    item3, line3 = rhf.get_first_item_from_text(line2)
    assert item3 == 3
    assert line3 == "4}"
    item4, line4 = rhf.get_first_item_from_text(line3)
    assert item4 == 4
    assert line4 == "}"

def test_get_first_item_from_text_iterative2():
    full_line = "key1 = 0 key1 = 1"
    item0, line0 = rhf.get_first_item_from_text(full_line)
    assert item0 == "key1"
    assert line0 == "= 0 key1 = 1"
    item1, line1 = rhf.get_first_item_from_text(line0)
    assert item1 == "="
    assert line1 == "0 key1 = 1"
    item2, line2 = rhf.get_first_item_from_text(line1)
    assert item2 == 0
    assert line2 == "key1 = 1"
    item3, line3 = rhf.get_first_item_from_text(line2)
    assert item3 == "key1"
    assert line3 == "= 1"
    item4, line4 = rhf.get_first_item_from_text(line3)
    assert item4 == "="
    assert line4 == "1"
    item5, line5 = rhf.get_first_item_from_text(line4)
    assert item5 == 1
    assert line5 == ""


# def test_read_txt_file00(txt_file_content0):
#     test_txt_file_path = Path(__file__).parent / "txt_file_for_testing0.txt"
#     assert test_txt_file_path.exists()
#     content = rhf.read_txt_file0(test_txt_file_path)
#     assert isinstance(content, dict)
#     assert content == txt_file_content0

# def test_read_txt_file01(txt_file_content1):
#     test_txt_file_path = Path(__file__).parent / "txt_file_for_testing1.txt"
#     assert test_txt_file_path.exists()
#     content = rhf.read_txt_file0(test_txt_file_path)
#     assert isinstance(content, dict)
#     assert content == txt_file_content1

# def test_read_txt_file02(txt_file_content2):
#     test_txt_file_path = Path(__file__).parent / "txt_file_for_testing2.txt"
#     assert test_txt_file_path.exists()
#     content = rhf.read_txt_file0(test_txt_file_path)
#     assert isinstance(content, dict)
#     assert content == txt_file_content2

# def test_read_txt_file03(txt_file_content3):
#     test_txt_file_path = Path(__file__).parent / "txt_file_for_testing3.txt"
#     assert test_txt_file_path.exists()
#     content = rhf.read_txt_file0(test_txt_file_path)
#     assert isinstance(content, dict)
#     assert content == txt_file_content3

# def test_read_txt_file0_list0(txt_file_content_list0):
#     test_txt_file_path = Path(__file__).parent / "txt_file_for_testing_list0.txt"
#     assert test_txt_file_path.exists()
#     content = rhf.read_txt_file0(test_txt_file_path)
#     assert isinstance(content, list)
#     assert content == txt_file_content_list0

# def test_read_txt_file0_list1(txt_file_content_list1):
#     test_txt_file_path = Path(__file__).parent / "txt_file_for_testing_list1.txt"
#     assert test_txt_file_path.exists()
#     content = rhf.read_txt_file0(test_txt_file_path)
#     assert isinstance(content, list)
#     assert content == txt_file_content_list1


def test_read_txt_file0(txt_file_content0):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing0.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content0


def test_read_txt_file1(txt_file_content1):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing1.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content1

def test_read_txt_file2(txt_file_content2):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing2.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content2

def test_read_txt_file3(txt_file_content3):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing3.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, dict)
    assert content == txt_file_content3

def test_read_txt_file_list0(txt_file_content_list0):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing_list0.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, list)
    assert content == txt_file_content_list0

def test_read_txt_file_list1(txt_file_content_list1):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing_list1.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, list)
    assert content == txt_file_content_list1

def test_read_txt_file_list2(txt_file_content_list2):
    test_txt_file_path = Path(__file__).parent / "txt_file_for_testing_list2.txt"
    assert test_txt_file_path.exists()
    content = rhf.read_txt_file(test_txt_file_path)
    assert isinstance(content, list)
    assert content == txt_file_content_list2

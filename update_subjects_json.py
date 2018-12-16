import json

SUB_JSON_FILE = "subjects.json"


def update_sub_list(sub_code, sub_name):
    """
    updates the subjects.json for missing subject entry

    :param sub_code:
        code of the subject to be appended
    :param sub_name:
        name of the subject
    :return: None

    """
    with open(SUB_JSON_FILE) as data_file:
        subjects = json.load(data_file)

    subjects[sub_code] = str(sub_name)

    with open(SUB_JSON_FILE, "w") as data_file:
        json.dump(subjects, data_file, indent=4, sort_keys=True)



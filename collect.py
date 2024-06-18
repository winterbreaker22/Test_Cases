
import csv
import os
import json

class TestCase:
    def __init__(self, id, test_data, title, preconditions, steps_to_replicate, expected_result, actual_result="", status="Not Executed"):
        self.id = id
        self.test_data = test_data
        self.title = title
        self.preconditions = preconditions
        self.steps_to_replicate = steps_to_replicate
        self.expected_result = expected_result
        self.actual_result = actual_result
        self.status = status

    def to_dict(self):
        return {
            "ID": self.id,
            "Test Data": self.test_data,
            "Title": self.title,
            "Preconditions": self.preconditions,
            "Steps to Replicate": self.steps_to_replicate,
            "Expected Result": self.expected_result,
            "Actual Result": self.actual_result,
            "Status": self.status
        }


def save_test_case(test_case, filename='test_cases.csv'):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ["ID", "Title", "Test Data", "Preconditions", "Steps to Replicate", "Expected Result", "Actual Result", "Status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(test_case.to_dict())


def load_test_cases(filename='test_cases.csv'):
    test_cases = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_case = TestCase(
                id=row["ID"],
                test_data=row["Test Data"],
                title=row["Title"],
                preconditions=row["Preconditions"],
                steps_to_replicate=row["Steps to Replicate"],
                expected_result=row["Expected Result"],
                actual_result=row.get("Actual Result", ""),
                status=row.get("Status", "Not Executed")
            )
            test_cases.append(test_case)
    return test_cases


def update_test_case_status(test_case_id, actual_result, status, filename='test_cases.csv'):
    test_cases = load_test_cases(filename)
    updated = False

    for test_case in test_cases:
        if test_case.id == test_case_id:
            test_case.actual_result = actual_result
            test_case.status = status
            updated = True
            break

    if updated:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ["ID", "Title", "Test Data", "Preconditions", "Steps to Replicate", "Expected Result", "Actual Result", "Status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for test_case in test_cases:
                writer.writerow(test_case.to_dict())
    return updated


# load test_case.json file
with open('test_case.json', encoding="utf8") as json_file:
    load_cases = json.load(json_file)

for load_case in load_cases:
    case_item = TestCase(
        id = load_case['ID'],
        title = load_case['Title'],
        test_data = load_case['Test Data'],
        preconditions = load_case['Preconditions'],
        steps_to_replicate = load_case['Steps to Replicate'],
        expected_result = load_case['Expected Result']
    )
    save_test_case(case_item)


# Load all test cases
test_cases = load_test_cases()
for tc in test_cases:
    print(tc.to_dict())


# Update a test case status
update_test_case_status("TC001", "The user is redirected to the dashboard.", "Pass")


# Load and print the updated test cases
updated_test_cases = load_test_cases()
for tc in updated_test_cases:
    print(tc.to_dict())

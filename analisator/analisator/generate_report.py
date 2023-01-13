import pickle
import codecs
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import csv
from typing import AnyStr, Union, List


def parse_row_from_csv_to_numbers(
    raw_row: List[AnyStr],
) -> List[Union[int, float]]:
    new_row = []
    for element in raw_row[1:]:
        if "." in element:
            new_row.append(float(element))
        else:
            new_row.append(int(element))

    return new_row


def open_ml_model_file(model):
    return pickle.load(model)


def generate_test_and_predicted_results(csvfile, net):
    test_results = []
    predicted_results = []

    test_file_reader = csv.reader(
        codecs.iterdecode(csvfile, "utf-8"), delimiter=",", quotechar="|"
    )

    for index, row in enumerate(test_file_reader):
        if index == 0:
            labels = row
        else:
            parsed_row = parse_row_from_csv_to_numbers(row)

            test_results.append(parsed_row[-1])
            predicted_results.append(int(net.predict([parsed_row[:-1]])))

    return test_results, predicted_results


def generate_report(model_file, test_file):
    net = open_ml_model_file(model_file)
    test_results, predicted_results = generate_test_and_predicted_results(
        test_file, net
    )
    confusion_m = confusion_matrix(test_results, predicted_results)

    report = classification_report(test_results, predicted_results, output_dict=True)

    for key in report:
        if isinstance(report[key], dict):
            report[key]["f1score"] = report[key].pop("f1-score")

    return confusion_m.tolist(), report

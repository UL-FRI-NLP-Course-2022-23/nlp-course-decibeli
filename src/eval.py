from utils import (
    Book,
    parse_gt_relationships,
    parse_predicted_relationships,
    RELATIONSHIP,
    read_json,
    substring_in_array,
    gt_relationships,
)
import json
import re


def partial_matches(dict, key):
    matches_num = 0
    for k in dict.keys():
        if key in k:
            matches_num += 1
    return matches_num


def closest_match(dict, key):
    num_matches = partial_matches(dict, key)
    if num_matches > 1:
        return None

    if key in dict.keys():
        return key

    for k in dict.keys():
        if key in k:
            return k


def eval_relationship_extraction(gt_haracter_data, predicted_character_data):
    matches = 0
    all = 0
    tp = 0
    fp = 0
    skips = 0

    for predicted_char, rel_name, rel_to in predicted_character_data:
        predicted_char = re.sub(r"'s\b", "", predicted_char)
        rel_to = re.sub(r"'s\b", "", rel_to)

        if (
            partial_matches(gt_haracter_data, predicted_char) == 0
            or partial_matches(gt_haracter_data, predicted_char) > 1
        ) and (
            partial_matches(gt_haracter_data, rel_to) == 0
            or partial_matches(gt_haracter_data, rel_to) > 1
        ):
            # print(f"skipping: {predicted_char};{rel_name};{rel_to}")
            skips += 1
            continue

        # if predicted_char != "jon snow":
        #     continue

        # print(f"{predicted_char};{rel_name};{rel_to}")
        # if predicted_char == "robert" and rel_to == "catelyn":
        #     print(f"{predicted_char};{rel_name};{rel_to}")
        #     continue

        if rel_name == "spouse" or rel_name == "parents":
            all += 1
            char_key = closest_match(gt_haracter_data, predicted_char)

            if rel_name == "spouse" and char_key is not None:
                if "spouse" in gt_haracter_data[char_key]:
                    if substring_in_array(rel_to, gt_haracter_data[char_key]["spouse"]):
                        matches += 1
                        tp += 1

            elif rel_name == "parents" and char_key is not None:
                if "father" in gt_haracter_data[char_key]:
                    if substring_in_array(rel_to, gt_haracter_data[char_key]["father"]):
                        matches += 1
                        tp += 1
                elif "mother" in gt_haracter_data[char_key]:
                    if substring_in_array(rel_to, gt_haracter_data[char_key]["mother"]):
                        matches += 1
                        tp += 1

        if rel_name == "siblings":
            all += 1
            char_key = closest_match(gt_haracter_data, predicted_char)
            if char_key is not None and char_key in gt_haracter_data:
                if "sibling" in gt_haracter_data[char_key]:
                    if substring_in_array(
                        rel_to, gt_haracter_data[char_key]["sibling"]
                    ):
                        matches += 1
                        tp += 1

        if rel_name == "children":
            all += 1
            char_key = closest_match(gt_haracter_data, predicted_char)
            if char_key is not None and char_key in gt_haracter_data:
                if "children" in gt_haracter_data[char_key]:
                    if substring_in_array(
                        rel_to, gt_haracter_data[char_key]["children"]
                    ):
                        matches += 1
                        tp += 1

    fp = all - tp
    fn = ground_truth_relations_num(gt_haracter_data) - tp
    print(f"SKIPS:{skips}")

    return tp, fp, fn


def precision(tp, fp):
    return tp / (tp + fp)


def recall(tp, fn):
    return tp / (tp + fn)


def f1(tp, fp, fn):
    return 2 * tp / (2 * tp + fp + fn)


def ground_truth_relations_num(gt):
    rels_num = 0
    for character in gt:
        if "spouse" in gt[character]:
            rels_num += len(gt[character]["spouse"])
        if "father" in gt[character]:
            rels_num += len(gt[character]["father"])
        if "mother" in gt[character]:
            rels_num += len(gt[character]["mother"])
        if "sibling" in gt[character]:
            rels_num += len(gt[character]["sibling"])
        if "children" in gt[character]:
            rels_num += len(gt[character]["children"])

    return rels_num


if __name__ == "__main__":
    # ONLY CHANGE THIS
    PREDICTIONS_FILENAME = "data/triplets/z_narek/family_triplets_coreNLP_all.csv"
    # ----------------

    gt = read_json("data/gt_relationships_top25.json")
    predicted = parse_predicted_relationships(PREDICTIONS_FILENAME)

    tp, fp, fn = eval_relationship_extraction(gt, predicted)
    print(f"TP: {tp}, FP: {fp}, FN: {fn}\n------------------")

    print(f"Precision: {precision(tp, fp)}")
    print(f"Recall: {recall(tp, fn)}")
    print(f"F1: {f1(tp, fp, fn)}")

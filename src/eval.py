from utils import (
    Book,
    parse_predicted_relationships,
    RELATIONSHIP,
    substring_in_array,
    gt_relationships,
)
import json


def eval_relationship(gt_haracter_data, predicted_character_data):
    matches = 0
    all = 0
    tp = 0
    fp = 0

    # compute tp and fp
    for predicted_char, rel_name, rel_to in predicted_character_data:
        # relationship name
        # rel_name = list(predicted_character_data[predicted_char].keys())[0]
        # # related character
        # rel_to = predicted_character_data[predicted_char][rel_name]

        if rel_name == "spouse" or rel_name == "parents":
            all += 1
            old_tp = tp
            for gt_char in gt_haracter_data:
                if rel_name == "spouse" and predicted_char in gt_char:
                    if RELATIONSHIP.SPOUSE in gt_haracter_data[gt_char]:
                        if substring_in_array(
                            rel_to, gt_haracter_data[gt_char][RELATIONSHIP.SPOUSE]
                        ):
                            matches += 1
                            tp += 1

                elif rel_name == "parents" and predicted_char in gt_char:
                    if RELATIONSHIP.FATHER in gt_haracter_data[gt_char]:
                        if substring_in_array(
                            rel_to, gt_haracter_data[gt_char][RELATIONSHIP.FATHER]
                        ):
                            matches += 1
                            tp += 1
                    elif RELATIONSHIP.MOTHER in gt_haracter_data[gt_char]:
                        if substring_in_array(
                            rel_to, gt_haracter_data[gt_char][RELATIONSHIP.MOTHER]
                        ):
                            matches += 1
                            tp += 1
            if old_tp == tp:
                fp += 1

        if rel_name == "siblings":
            all += 1
            old_tp = tp
            for gt_char in gt_haracter_data:
                if predicted_char in gt_char:
                    if RELATIONSHIP.SIBLING in gt_haracter_data[gt_char]:
                        if substring_in_array(
                            rel_to, gt_haracter_data[gt_char][RELATIONSHIP.SIBLING]
                        ):
                            matches += 1
                            tp += 1
            if old_tp == tp:
                fp += 1

        if rel_name == "children":
            all += 1
            old_tp = tp
            for gt_char in gt_haracter_data:
                if predicted_char in gt_char:
                    if RELATIONSHIP.CHILDREN in gt_haracter_data[gt_char]:
                        if substring_in_array(
                            rel_to, gt_haracter_data[gt_char][RELATIONSHIP.CHILDREN]
                        ):
                            matches += 1
                            tp += 1
            if old_tp == tp:
                fp += 1

    # compute fn
    fn = 0
    for gt_char in gt_haracter_data:
        if RELATIONSHIP.SPOUSE in gt_haracter_data[gt_char]:
            rels_count = len(gt_haracter_data[gt_char][RELATIONSHIP.SPOUSE])
            for rel_to in gt_haracter_data[gt_char][RELATIONSHIP.SPOUSE]:
                for predicted_char in predicted_character_data:
                    if gt_char in predicted_char:
                        rels_count -= 1
                        break
            fn += rels_count
        if (
            RELATIONSHIP.MOTHER in gt_haracter_data[gt_char]
            and RELATIONSHIP.FATHER in gt_haracter_data[gt_char]
        ):
            parent_rels = (
                gt_haracter_data[gt_char][RELATIONSHIP.MOTHER]
                + gt_haracter_data[gt_char][RELATIONSHIP.FATHER]
            )
            rels_count = len(parent_rels)
            for rel_to in parent_rels:
                for predicted_char in predicted_character_data:
                    if gt_char in predicted_char:
                        rels_count -= 1
            fn += rels_count
        elif (
            RELATIONSHIP.MOTHER in gt_haracter_data[gt_char]
            and RELATIONSHIP.FATHER not in gt_haracter_data[gt_char]
        ):
            parent_rels = gt_haracter_data[gt_char][RELATIONSHIP.MOTHER]
            rels_count = len(parent_rels)
            for rel_to in parent_rels:
                for predicted_char in predicted_character_data:
                    if gt_char in predicted_char:
                        rels_count -= 1
            fn += rels_count
        elif (
            RELATIONSHIP.MOTHER not in gt_haracter_data[gt_char]
            and RELATIONSHIP.FATHER in gt_haracter_data[gt_char]
        ):
            parent_rels = gt_haracter_data[gt_char][RELATIONSHIP.FATHER]
            rels_count = len(parent_rels)
            for rel_to in parent_rels:
                for predicted_char in predicted_character_data:
                    if gt_char in predicted_char:
                        rels_count -= 1
            fn += rels_count

    return tp, fp, fn


def precision(tp, fp):
    return tp / (tp + fp)


def recall(tp, fn):
    return tp / (tp + fn)


def f1(tp, fp, fn):
    return 2 * tp / (2 * tp + fp + fn)


if __name__ == "__main__":
    gt = gt_relationships(Book.A_GAME_OF_THRONES.value["title"])
    # gt = parse_gt_relationships()
    predicted = parse_predicted_relationships()

    tp, fp, fn = eval_relationship(gt, predicted)
    print(f"TP: {tp}, FP: {fp}, FN: {fn}\n------------------")

    print(f"Precision: {precision(tp, fp)}")
    print(f"Recall: {recall(tp, fn)}")
    print(f"F1: {f1(tp, fp, fn)}")

import csv
import ast

d = {}

def fill_in_retrieval():

    with open("rationale_dataset_1128_lite_harry_annotated_100.csv") as f:
        for row in csv.DictReader(f):
            goal_step = (row["goal"], row["branching_step"])
            if row["r1"].split(','):
                if row["r1"].split(',') != ['']:
                    r1_annotations = ', '.join([x for x in row["r1"].split(',') if int(x) in [0,1,2,3,5,7]])
                else:
                    r1_annotations = ''
            if row["r2"].split(','):
                if row["r2"].split(',') != ['']:
                    r2_annotations = ', '.join([x for x in row["r2"].split(',') if int(x) in [0,1,2,3,5,7]])
                else:
                    r2_annotations = ''
            r1 = '[' + r1_annotations + ']'
            r2 = '[' + r2_annotations + ']'
            d[goal_step] = (r1,r2)

    with open("retrieval.csv") as f, open("retrieval_annotated.csv", 'w') as fw:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(fw, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            goal_step = (row["goal"], row["branching_step"])
            if goal_step in d:
                r1 = d[goal_step][0]
                r2 = d[goal_step][1]
            else:
                r1 = ''
                r2 = ''
            writer.writerow({"goal": row["goal"], "steps": row["steps"], "branching_step": row["branching_step"], "options": row["options"], "op1_ra_human": r1, "op2_ra_human": r2})

def fill_in_classification():
    with open("retrieval_harry_annotated.csv") as f:
        for row in csv.DictReader(f):
            goal = row["goal"]
            step = row["branching_step"]
            ra1s = ast.literal_eval(row["op1_ra_human"])
            ra2s = ast.literal_eval(row["op2_ra_human"])
            for ra1 in ra1s:
                d[(goal, step, ra1)] = '1'
            for ra2 in ra2s:
                d[(goal, step, ra2)] = '2'

    #print(d)   

    with open("classification.csv") as f, open("classification_annotated.csv", 'w') as fw:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(fw, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            labels = []
            for rat in ast.literal_eval(row["rationales"]):
                if (row["goal"], row["branching_step"], rat) in d:
                    choice = d[(row["goal"], row["branching_step"], rat)]
                else:
                    choice = ''
                labels.append(str(rat) + ': ' + choice)
            choice = '\n'.join(labels)
            writer.writerow({"goal": row["goal"], "steps": row["steps"], "branching_step": row["branching_step"], "options": row["options"], "rationales": row["rationales"], "label_to_be_annotated": choice})

fill_in_classification()
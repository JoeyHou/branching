import csv
import ast

with open("classification.csv") as f, open("classification_cleaned.csv", 'w') as fw:
    writer = csv.writer(fw)
    for i,row in enumerate(csv.reader(f)):
        if i == 0:
            writer.writerow(row[:6])
        else:
            op1 = ast.literal_eval(row[4])
            op1 = [x for x in op1 if x in [0,1,2,3,5,7]]
            op2 = ast.literal_eval(row[5])
            op2 = [x for x in op2 if x in [0,1,2,3,5,7]]
            writer.writerow(row[:4] + [str(op1), str(op2)])
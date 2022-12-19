import argparse
import openai
import csv
import random
random.seed(29)
from solver import solve
import backoff
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--model', default='code-davinci-002', type=str, help='Model ID from OpenAI.')
parser.add_argument('--key', default='harry', type=str, help='The name of the OpenAI API key file.')

args = parser.parse_args()
openai.api_key = open(f'../../_private/{args.key}.key').read()

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def run_llm(prompt, temperature=0):
    ret = openai.Completion.create(
        engine=args.model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Final answer: "]
    )

    gen_text = ret["choices"][0]["text"].strip()
    return gen_text

def build_prompt(story, query_0, query_1):
    s = ""
    s += "# Context: " + story + '\n'
    s += f"# Question: How is [{query_0}] related to [{query_1}]?" + '\n'
    s += "# To answer this question, we write a program to answer the following subquestions:" + '\n'
    s += f"# 1. How is [{query_0}] related to"
    return s

prompt_file_name = "prompts/code_cot.py" if args.model != "text-davinci-001" else "prompts/code_cot_3.py"
with open(prompt_file_name) as f:
    written_prompt = f.read()
with open("ignore.pkl", 'rb') as f:
    ignored_ids = pickle.load(f)

total_scores = []

for fname in reversed(['1.2_test.csv', '1.3_test.csv', '1.4_test.csv', '1.5_test.csv', '1.6_test.csv', '1.7_test.csv', '1.8_test.csv', '1.9_test.csv', '1.10_test.csv']):
    print(fname)
    output_folder = "output" if args.model == "code-davinci-002" else f"output/{args.model}"
    with open('data/' + fname) as f, open(f"{output_folder}/{fname}", 'w') as fw:
        scores = []
        writer = csv.DictWriter(fw, fieldnames=["id", "question", "is_correct", "gold_answer", "pred_answer", "gold_chain", "pred_chain"])
        writer.writeheader()
        for i, row in enumerate(csv.DictReader(f)):
            if row['id'] in ignored_ids:
                continue
            print(i)
            story = row["story"]
            query_0 = row["query"].strip("('").strip("')").split("', '")[1]
            query_1 = row["query"].strip("('").strip("')").split("', '")[0]
            gold_answer = row["target"]
            built_prompt = build_prompt(story, query_0, query_1)
            prompt = written_prompt + built_prompt
            gen_text = run_llm(prompt)
            try:
                pred_answer = solve(gen_text)
            except KeyError as e:
                pred_answer = "unknown"
            scores.append(1 if pred_answer == gold_answer else 0)
            total_scores.append(1 if pred_answer == gold_answer else 0)
            writer.writerow({"id": row["id"], "question": story + '\n' + f"How is [{query_0}] related to [{query_1}]?", "is_correct": "TRUE" if pred_answer == gold_answer else "FALSE", "gold_answer": gold_answer, "pred_answer": pred_answer, "gold_chain": row["f_comb"], "pred_chain": gen_text})

        print(sum(scores) / len(scores))
        fw.write(f"Accuracy: {sum(scores)}/{len(scores)}" + '\n' + str(sum(scores) / len(scores)))

print("Total accurcy")
print(sum(total_scores) / len(total_scores))
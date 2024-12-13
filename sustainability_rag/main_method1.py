from tqdm import tqdm
from search import search
from parse_pdf import parse_pdf
from parse_conclusion import parse_conclusion

# company_report_node = parse_pdf('2024').main_parse()

# for company_report in tqdm(company_report_node, desc="Processing Reports"):
#     response = search().get_res(company_report)
#     with open('../result/ch_sustainability_evaluate.txt', 'a') as f:
#         f.write(f"永續報告書評價：{response}\n")

with open('../result/ch_sustainability_evaluate.txt', 'r') as f:
    response = f.read()

parse_res = parse_conclusion('ch_sus').text_split()

for res in tqdm(parse_res, desc="Process Evaluate"):
    conclusion = search().get_conclusion(res.page_content)

    with open("../result/ch_evaluate_conclusion.txt", 'a+') as f:
        f.write(conclusion)

with open("../result/ch_evaluate_conclusion.txt", 'r') as f:
    response = f.read()

final_conclusion = search().get_conclusion(response)

with open("../result/method_1_final_conclusion.txt", 'w') as f:
    f.write(final_conclusion)
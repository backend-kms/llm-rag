import os
import json

# aihub 필수의료 의학지식 데이터셋 - 소아청소년과
# https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71875

input_dir = "TL_소아청소년과"  # JSON 파일들이 있는 폴더
output_file = "fine-tuning-data/ai-hub/pediatrics.jsonl"  # 최종 JSONL 파일

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in os.listdir(input_dir):
        # print(filename)
        if filename.endswith(".json"):
            path = os.path.join(input_dir, filename)
            # print(path)
            with open(path, "r", encoding="utf-8-sig") as f:  # BOM 처리
                data = json.load(f)

                prompt_text = data["question"].strip()
                completion_text = data["answer"].strip()

                if prompt_text and completion_text:
                    jsonl_item = {
                        "prompt": prompt_text + "\n\n###\n\n",
                        "completion": " " + completion_text + " END"
                    }
                    outfile.write(json.dumps(jsonl_item, ensure_ascii=False) + "\n")

print(f"JSONL 파일 생성 완료: {output_file}")
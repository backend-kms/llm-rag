import os
import json

# AIHub 초거대 AI 헬스케어 질의응답 데이터셋 - 소아청소년질환
# https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71762

base_directory = "감염성질환"
questions_directory = os.path.join(base_directory, "감염성질환_질문")
answers_directory = os.path.join(base_directory, "감염성질환_답변")

output_jsonl_file = "fine-tuning-data/ai-hub2/infectious_diseases.jsonl"
os.makedirs(os.path.dirname(output_jsonl_file), exist_ok=True)

with open(output_jsonl_file, "w", encoding="utf-8") as output_file_handle:
    for current_root, subdirectories, files_in_current_root in os.walk(questions_directory):
        relative_path_from_questions = os.path.relpath(current_root, questions_directory)
        corresponding_answers_folder = os.path.join(answers_directory, relative_path_from_questions)

        # 대응되는 답변 폴더가 없으면 건너뜀
        if not os.path.exists(corresponding_answers_folder):
            continue

        question_file_list = sorted([file_name for file_name in files_in_current_root if file_name.endswith(".json")])
        answer_file_list = sorted([file_name for file_name in os.listdir(corresponding_answers_folder) if file_name.endswith(".json")])

        number_of_pairs_to_process = min(len(question_file_list), len(answer_file_list))

        for index in range(number_of_pairs_to_process):
            question_file_name = question_file_list[index]
            answer_file_name = answer_file_list[index]

            # 질문 파일 읽기
            question_file_path = os.path.join(current_root, question_file_name)
            with open(question_file_path, "r", encoding="utf-8-sig") as question_file_handle:
                question_data = json.load(question_file_handle)
                if isinstance(question_data, list):
                    prompt_text = question_data[0].get("question", "").strip()
                elif isinstance(question_data, dict):
                    prompt_text = question_data.get("question", "").strip()
                else:
                    continue  # 형식이 이상하면 스킵

            # 답변 파일 읽기
            answer_file_path = os.path.join(corresponding_answers_folder, answer_file_name)
            with open(answer_file_path, "r", encoding="utf-8-sig") as answer_file_handle:
                answer_data = json.load(answer_file_handle)
                if isinstance(answer_data, list):
                    answer_item = answer_data[0]
                elif isinstance(answer_data, dict):
                    answer_item = answer_data
                else:
                    continue

                answer_content = answer_item.get("answer", {})
                if isinstance(answer_content, dict):
                    completion_text = " ".join([value.strip() for value in answer_content.values() if isinstance(value, str)])
                else:
                    completion_text = str(answer_content).strip()

            # prompt와 completion이 존재하면 JSONL에 기록
            if prompt_text and completion_text:
                jsonl_entry = {
                    "prompt": prompt_text + "\n\n###\n\n",
                    "completion": " " + completion_text + " END",
                    "source": "AIHub 감염성질환 Q&A 라벨링 데이터셋"
                }
                output_file_handle.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")

print(f"JSONL 파일 생성 완료: {output_jsonl_file}")
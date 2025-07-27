# data_processor.py
import json
import pandas as pd
import google.generativeai as genai

def get_extracted_content(model, prompt_template, chapter_text, chapter_title):
    prompt = prompt_template.replace("[INSERT CHAPTER TEXT HERE]", chapter_text)
    prompt = prompt.replace("Name of the Chapter", chapter_title)

    try:
        response = model.generate_content(prompt)
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        json_string = response.text[json_start:json_end]
        return json.loads(json_string)
    except Exception as e:
        print(f"Error extracting content for {chapter_title}: {e}")
        return None

def create_excel_from_json(json_data, output_filename="Science-sample-output.xlsx"):
    all_rows = []
    for chapter in json_data:
        chapter_title = chapter.get("chapter_title", "")
        for topic in chapter.get("topics", []):
            topic_name = topic.get("topic_name", "")
            for sub_topic in topic.get("sub_topics", []):
                for element in sub_topic.get("content_elements", []):
                    all_rows.append({
                        "Chapter": chapter_title,
                        "Topic": topic_name,
                        "Sub-topic": sub_topic.get("sub_topic_header", ""),
                        "Content Type": element.get("type", ""),
                        "Content": element.get("value", "")
                    })
    if all_rows:
        pd.DataFrame(all_rows).to_excel(output_filename, index=False)
        print(f"Excel file '{output_filename}' created successfully.")

def create_knowledge_graph(json_data, output_filename="knowledge_graph.txt"):
    with open(output_filename, "w", encoding="utf-8") as f:
        for chapter in json_data:
            f.write(f"Chapter: {chapter.get('chapter_title','')}\n")
            for topic in chapter.get("topics", []):
                f.write(f"  Topic: {topic.get('topic_name','')}\n")
                for sub_topic in topic.get("sub_topics", []):
                    f.write(f"    Sub-topic: {sub_topic.get('sub_topic_header','')}\n")
                    for element in sub_topic.get("content_elements", []):
                        f.write(f"      - {element.get('type','')}: {element.get('value','')[:50]}...\n")
    print(f"Knowledge graph saved to '{output_filename}'.")

def generate_study_planner(model, prompt_template, extracted_data, num_days):
    simplified_data = json.dumps(extracted_data, indent=2)
    planner_prompt = prompt_template.replace("[INSERT SIMPLIFIED CHAPTER DATA HERE]", simplified_data)
    planner_prompt = planner_prompt.replace("[NUMBER_OF_DAYS]", str(num_days))

    try:
        response = model.generate_content(planner_prompt)
        return response.text
    except Exception as e:
        print(f"Error generating study planner: {e}")
        return ""

# prompts.py

universal_extraction_prompt = """
You are an expert educational content extractor. Return ONLY valid JSON (no prose) that follows this schema:
{
  "chapter_title": "...",
  "topics": [
    {
      "topic_name": "...",
      "sub_topics": [
        {
          "sub_topic_header": "...",
          "content_elements": [
            {
              "type": "paragraph|image_description|diagram_description|table_content|example|exercise|activity|question|external_source|boxed_fact|summary_point|keywords|what_i_have_learnt|did_you_know",
              "value": "..."
            }
          ]
        }
      ]
    }
  ]
}

Extract strictly from the text provided. Do NOT invent content.

TEXT TO EXTRACT FROM (inserted by the program):
[INSERT CHAPTER TEXT HERE]
"""

study_planner_prompt = """
Create a day-wise study planner (in plain markdown text) for NCERT Grade 8 Science using the structured JSON I give you.
Respect the total number of days and distribute topics/sub-topics sensibly.

SIMPLIFIED INPUT DATA (JSON, inserted by the program):
[INSERT SIMPLIFIED CHAPTER DATA HERE]

NUMBER OF DAYS:
[NUMBER_OF_DAYS]

Output format (example):

Study Planner: NCERT Class 8 Science (Total X Days)

Day 1
- Chapter: <name>
  - Topic: <name> (Estimated: 1.5 hours)
    - Sub-topic A
    - Sub-topic B

Day 2
...

Be concise but complete. No extra explanations besides the planner itself.
"""

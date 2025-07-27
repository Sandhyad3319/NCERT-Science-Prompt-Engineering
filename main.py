# main.py
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Import functions from other modules
from pdf_extractor import extract_text_from_pdf
from prompts import universal_extraction_prompt, study_planner_prompt
from data_processor import (
    get_extracted_content,
    create_excel_from_json,
    create_knowledge_graph,
    generate_study_planner
)

if __name__ == "__main__":
    # Load environment variables (especially your GOOGLE_API_KEY)
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Define the PDF URLs and their corresponding chapter titles
    pdf_urls = [
        "https://ncert.nic.in/textbook/pdf/hesc106.pdf",
        "https://ncert.nic.in/textbook/pdf/hesc107.pdf",
        "https://ncert.nic.in/textbook/pdf/hesc108.pdf",
        "https://ncert.nic.in/textbook/pdf/hesc113.pdf"
    ]

    # Map URLs to human-readable chapter titles for better output
    chapter_mapping = {
        "https://ncert.nic.in/textbook/pdf/hesc106.pdf": "Chapter 6: Combustion and Flame",
        "https://ncert.nic.in/textbook/pdf/hesc107.pdf": "Chapter 7: Conservation of Plants and Animals",
        "https://ncert.nic.in/textbook/pdf/hesc108.pdf": "Chapter 8: Cell – Structure and Functions",
        "https://ncert.nic.in/textbook/pdf/hesc113.pdf": "Chapter 13: Sound"
    }

    chapter_texts = {}
    print("--- Starting PDF Text Extraction ---")
    for url in pdf_urls:
        chapter_title = chapter_mapping.get(url, f"Chapter from {url.split('/')[-1]}")
        print(f"Extracting text from {chapter_title}...")
        text = extract_text_from_pdf(url)
        if text:
            chapter_texts[chapter_title] = text
        else:
            print(f"Failed to extract text for {chapter_title}. Skipping.")

    all_extracted_chapters_data = []
    print("\n--- Sending to Gemini for Content Extraction ---")
    for chapter_title, text in chapter_texts.items():
        if text:
            print(f"Processing {chapter_title}...")
            # Pass the model object and prompt to the extraction function
            extracted_chapter_json = get_extracted_content(model, universal_extraction_prompt, text, chapter_title)
            if extracted_chapter_json:
                all_extracted_chapters_data.append(extracted_chapter_json)
            else:
                print(f"Failed to extract structured content for {chapter_title}.")

    if all_extracted_chapters_data:
        print("\n--- Generating Output Files ---")
        # Save all extracted data to a single JSON file
        output_json_filename = "chapter-extract.json"
        with open(output_json_filename, "w", encoding="utf-8") as f:
            json.dump(all_extracted_chapters_data, f, indent=2, ensure_ascii=False)
        print(f"All extracted chapter data saved to '{output_json_filename}'.")

        # Create Excel and Knowledge Graph from the collected JSON data
        create_excel_from_json(all_extracted_chapters_data)
        create_knowledge_graph(all_extracted_chapters_data)

        # Generate Study Planner
        print("\n--- Generating Study Planner ---")
        try:
            user_days = int(input("Enter the number of days for the study plan (e.g., 5 to 30): "))
            if 5 <= user_days <= 30:
                print(f"Generating study planner for {user_days} days...")
                # Pass the model object and prompt to the planner function
                planner_output = generate_study_planner(model, study_planner_prompt, all_extracted_chapters_data, user_days)
                planner_filename = f"study_planner_{user_days}_days.md"
                with open(planner_filename, "w", encoding="utf-8") as f:
                    f.write(planner_output)
                print(f"Study planner saved to '{planner_filename}'.")
            else:
                print("Invalid number of days. Please enter a value between 5 and 30.")
        except ValueError:
            print("Invalid input for number of days. Please enter an integer.")
    else:
        print("No chapter data was successfully extracted to proceed with further steps.")
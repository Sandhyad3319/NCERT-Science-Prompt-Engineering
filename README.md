# NCERT-Science-Prompt-Engineering

# 📘 NCERT Science AI Extractor & Study Planner

An AI-powered tool that:
- Extracts structured educational content from Class 8 NCERT Science PDFs using Google Gemini API.
- Outputs structured JSON, Excel, and a human-readable knowledge graph.
- Optionally generates a **study planner** for 5–30 days using extracted data.

---

## ⚙️ Technologies
- Python
- Google Gemini 1.5 Flash API
- PyPDF2
- Pandas
- dotenv

---

## 🧠 How it Works

1. **PDF URLs** from NCERT are processed.
2. Extracted text is passed to Gemini with a universal prompt.
3. Gemini returns structured JSON (chapters → topics → subtopics).
4. Output saved as:
   - `chapter-extract.json`
   - `Science-sample-output.xlsx`
   - `knowledge_graph.txt`
   - `study_planner_XX_days.md` (if planner requested)

---

## 🚀 Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/yourusername/ncert-science-ai-extractor.git
cd ncert-science-ai-extractor

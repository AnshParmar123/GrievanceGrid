# GrievanceGrid

GrievanceGrid is an AI-powered complaint intelligence dashboard that turns customer complaints into clear, actionable product, location, and sentiment insights. It helps users upload or paste complaint data, analyze patterns, identify the most affected product categories and locations, and generate simple reports from the results.

## Overview

Customer complaints often contain useful signals, but reading them one by one can be slow and repetitive. GrievanceGrid uses a Streamlit dashboard and a local LLM-powered analysis chain to process complaint text and summarize the most important trends.

The app focuses on answering questions like:

- Which product category is receiving the most negative feedback?
- Which store location is mentioned most often in complaints?
- What is the overall sentiment of each complaint?
- Can the results be exported for reporting or further analysis?

## Features

- Upload complaint data from a JSON file or paste complaints manually.
- Identify the most complained-about product category.
- Identify the store location with the most negative sentiment.
- View complaint sentiment in a Streamlit dashboard.
- Export analysis results as a CSV report.
- Generate summary reports for quick review.

## How It Works

1. The user provides complaint text through the Streamlit interface.
2. Complaints can be uploaded as a JSON file or pasted manually line by line.
3. The app sends the complaint list to the LangChain analysis pipeline.
4. The language model reviews the complaints and returns the product category and location with the most negative sentiment.
5. The dashboard displays the key insights, sentiment table, and basic chart.
6. The results can be downloaded as a CSV report.

## Input Format

For JSON uploads, the file should contain a list of complaint strings:

```json
[
  "The shoes I bought from the Dallas store were damaged.",
  "The phone stopped working after two days.",
  "Service at the New York location was very poor."
]
```

For manual input, paste one complaint per line in the text area.

## Tech Stack

- Python
- Streamlit
- Pandas
- LangChain
- Llama 3 through a local OpenAI-compatible endpoint

## Project Structure

```text
GrievanceGrid/
├── main.py                  # Main Streamlit dashboard
├── complaint_dashboard.py   # Extended dashboard with email/PDF options
├── llm_chain.py             # LangChain prompt and LLM pipeline
├── utils.py                 # Helper function for CSV export
├── emails.json              # Sample complaint input data
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Files ignored by Git
```

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/AnshParmar123/GrievanceGrid.git
cd GrievanceGrid
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start your local LLM endpoint.

The current setup expects an OpenAI-compatible endpoint at:

```text
http://localhost:11434/v1
```

The configured model is:

```text
llama3
```

You can change these values in `llm_chain.py` if your local model server uses a different URL or model name.

5. Run the Streamlit app:

```bash
streamlit run main.py
```

## Main App Flow

When the app starts, the user chooses one of two input methods:

- Upload a JSON file containing complaint text.
- Paste complaints manually, one complaint per line.

After clicking the analyze button, GrievanceGrid:

- Sends the complaints to the LLM chain.
- Extracts the product category with the most negative sentiment.
- Extracts the store location with the most negative sentiment.
- Displays the insights inside the Streamlit dashboard.
- Shows a simple sentiment label for each complaint.
- Creates a downloadable CSV report.

## Example Output

The language model is prompted to return output in this format:

```text
The product category with the most negative sentiment is <category>.
The store location with the most negative sentiment is <location>.
```

The app then parses this response and displays the category and location as key insights.

## Notes

- The sentiment labels in the dashboard use a simple keyword-based approach.
- The main analysis depends on the language model configured in `llm_chain.py`.
- Generated files such as CSV reports and PDF summaries are ignored by Git.
- Do not commit passwords, API keys, app passwords, or private customer data.

## Future Improvements

- Add stronger sentiment analysis using a dedicated NLP model.
- Add charts for complaint categories, locations, and trends over time.
- Support CSV and Excel uploads.
- Add authentication for private dashboards.
- Store previous analysis history in a database.
- Improve report generation with richer PDF summaries.

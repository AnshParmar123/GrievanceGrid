from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Setup deterministic LLM
llm = ChatNVIDIA(
    base_url="http://localhost:11434/v1",  # or wherever Ollama is running
    model="llama3",
    temperature=0.0  # 🔒 Make it deterministic
)

# LLM prompt template
prompt = ChatPromptTemplate.from_template("""
You are an AI assistant analyzing customer complaint emails.

Based on the following complaints, determine:
1. The product category with the most negative sentiment.
2. The store location with the most negative sentiment.

Always format your response exactly like:
"The product category with the most negative sentiment is <category>.
The store location with the most negative sentiment is <location>."

Emails: {emails}
""")

# Build chain
chain = prompt | llm | StrOutputParser()

def analyze_emails(email_list):
    return chain.invoke({"emails": email_list})

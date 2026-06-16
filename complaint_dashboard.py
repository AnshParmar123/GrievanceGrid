# main.py
import streamlit as st
import pandas as pd
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from reportlab.pdfgen import canvas
from langchain_core.prompts import PromptTemplate
from llm_chain import analyze_emails, llm

# === Email Setup ===
sender_email = "your_email@gmail.com"  # 🔁 Replace
sender_password = "your_app_password"  # 🔁 Replace (App Password)

# === Helper Functions ===
def save_results_to_csv(category, location):
    with open("complaint_analysis_results.csv", "w") as f:
        f.write("Most Complained Product,Most Complained Location\n")
        f.write(f"{category},{location}\n")

def tag_sentiment(text):
    negative_words = ["poor", "bad", "broke", "terrible", "hate", "leaks", "worst"]
    return "🔴 Negative" if any(w in text.lower() for w in negative_words) else "🟢 Positive"

reply_template = PromptTemplate.from_template("""
You're a customer support agent. Write a short, professional apology for the following customer complaint:

"{complaint}"
""")

def generate_reply(complaint):
    return llm.invoke(reply_template.format(complaint=complaint))

def export_summary_to_pdf(summary, filename="summary_report.pdf"):
    c = canvas.Canvas(filename)
    y = 800
    for line in summary.split('\n'):
        c.drawString(50, y, line.strip())
        y -= 20
    c.save()
    return filename

def send_email(summary, to_email):
    msg = MIMEText(summary)
    msg["Subject"] = "AI Complaint Summary"
    msg["From"] = sender_email
    msg["To"] = to_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error("❌ Email send failed.")
        st.exception(e)
        return False

# === Streamlit App Config ===
st.set_page_config(page_title="GrievanceGrid", layout="wide")
st.title("📬 GrievanceGrid")

# === Theme Toggle ===
theme = st.radio("🌗 Theme", ["Light", "Dark"], horizontal=True)
if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        .stTextInput > div > input { background-color: #333; color: white; }
        </style>
    """, unsafe_allow_html=True)

# === Input Mode ===
emails = []
input_mode = st.radio("Input Method", ["📁 Upload JSON", "📝 Paste Text"])

if input_mode == "📁 Upload JSON":
    uploaded_file = st.file_uploader("Upload complaints JSON", type=["json"])
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            emails = [str(item).strip() for item in data if isinstance(item, str)]
            st.success(f"✅ Loaded {len(emails)} complaints.")
        except Exception as e:
            st.error("❌ Failed to load JSON")
            st.exception(e)

elif input_mode == "📝 Paste Text":
    user_input = st.text_area("Paste complaints (1 per line)", height=200)
    if user_input:
        emails = [line.strip() for line in user_input.strip().split("\n") if line.strip()]

# === Analyze Button ===
if st.button("🔍 Analyze Complaints"):
    if not emails:
        st.warning("Please upload or paste complaints.")
    else:
        with st.spinner("🔎 Analyzing with AI..."):
            try:
                result = analyze_emails(emails)
                lines = result.split("\n")
                category = lines[0].split(" is ")[-1].strip(". ")
                location = lines[1].split(" is ")[-1].strip(". ")

                st.success("✅ Analysis Complete!")
                st.markdown(f"**🛍️ Product with Most Complaints:** `{category}`")
                st.markdown(f"**📍 Location with Most Complaints:** `{location}`")

                # Save CSV
                save_results_to_csv(category, location)
                with open("complaint_analysis_results.csv", "rb") as f:
                    st.download_button("⬇️ Download CSV", f, file_name="complaint_analysis_results.csv")

                # Show sentiment table
                df = pd.DataFrame({
                    "Complaint": emails,
                    "Sentiment": [tag_sentiment(e) for e in emails]
                })
                st.dataframe(df, use_container_width=True)

                # Keyword filter
                keyword = st.text_input("🔎 Filter complaints by keyword")
                if keyword:
                    filtered = df[df["Complaint"].str.contains(keyword, case=False)]
                    st.write(f"Showing {len(filtered)} result(s) for **'{keyword}'**")
                    st.dataframe(filtered)

                # Replies
                if st.checkbox("📨 Generate AI Replies"):
                    for i, row in df.iterrows():
                        st.markdown(f"**Complaint {i+1}:** {row['Complaint']}")
                        st.markdown(f"> 📨 Reply: {generate_reply(row['Complaint'])}")

                # Summary Text
                st.markdown("### 📄 AI Summary")
                summary_text = f"""
📨 Complaint Summary Report

🛍️ Most frequent product complaints were about **{category}**.
📍 Most affected store location appears to be **{location}**.

📌 Recommendations:
- Investigate product issues with {category}.
- Review service at {location}.

🕐 Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
                st.text_area("📄 Summary", value=summary_text, height=300)

                # PDF Export
                with open(export_summary_to_pdf(summary_text), "rb") as f:
                    st.download_button("📤 Download PDF", f, file_name="summary_report.pdf")

                # Send Email
                st.markdown("### 📧 Email Summary")
                recipient = st.text_input("Recipient Email")
                if st.button("📬 Send Email") and recipient:
                    with st.spinner("Sending email..."):
                        if send_email(summary_text, recipient):
                            st.success(f"📧 Email sent to {recipient}!")

            except Exception as e:
                st.error("⚠️ Something went wrong.")
                st.exception(e)

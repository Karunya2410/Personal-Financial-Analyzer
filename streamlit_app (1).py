import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Financial Analyzer", page_icon="📊")

st.sidebar.title("💬 Assistant Sidebar")
st.sidebar.info("""
Welcome to your AI-powered financial assistant!

👈 Upload a PDF to get started.

Tips:
- Use your monthly bank or UPI statement
- Clear text (not scanned images) works best
- Click "Rerun" if upload fails
""")
user_feedback = st.sidebar.text_area("📝 Leave your thoughts or feedback:", "")

st.title("📂 Financial Transaction Analyzer")


uploaded_file = st.file_uploader("Upload your transaction statement (PDF)", type="pdf")

if uploaded_file:
    st.success("✅ File uploaded.")
    temp_path = "/tmp/temp.pdf"  
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract text from PDF
    def extract_text_from_pdf(file_path):
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    extracted_text = extract_text_from_pdf(temp_path)
    os.remove(temp_path)

    if not extracted_text:
        st.error("❌ Could not extract text. PDF may be scanned.")
    else:
        st.info("🧠 Analyzing with Gemini...")
        model = genai.GenerativeModel("models/gemini-1.5-flash")  


        prompt = f"""
        You are a smart and friendly personal finance assistant. Your task is to deeply analyze the following financial transaction history and present insightful, clear, and actionable insights for the user.

        Transaction History:
        {extracted_text}

        Your analysis should be structured in a friendly and easy-to-understand format. Please include:

        🧾 **1. Spending Breakdown**
        - Categorize spending (e.g., Food, Travel, Shopping, Bills, Health, Entertainment)
        - Highlight any unusually high-spending categories

        📈 **2. Spending Patterns & Habits**
        - Detect any recurring patterns (e.g., weekly shopping, monthly subscriptions)
        - Identify frequent merchants or brands
        - Detect inconsistent income/expenses and cash flow irregularities

        💡 **3. Personalized Budgeting Advice**
        - Suggest a monthly budget based on spending trends
        - Recommend realistic savings targets
        - Highlight one key change that could help save more

        End the report with a friendly summary and a motivational message encouraging better financial habits.
        """

        try:
            response = model.generate_content(prompt)
            st.markdown("### 📊 Financial Insights")
            st.markdown(response.text)

            # 🎉 Success banner
            st.markdown(
                '<div style="background-color:#d4edda; padding:10px; border-radius:8px; color:#155724; font-weight:bold;">'
                '🎉 Analysis Completed! Plan your finances wisely. 🚀</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"⚠️ Gemini API failed: {e}")

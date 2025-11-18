import streamlit as st
from openai import OpenAI
import os 
import zipfile
import io


st.set_page_config(page_title="Repo Explainer", page_icon="🤓", layout="wide")
st.title("🤓 Repo Explainer")

st.markdown("**Upload any github repo (.zip) -> We will explain it in 15 seconds**")


client = OpenAI(
    api_key= st.secrets["MINIMAX_API_KEY"],
    base_url= "https://api.minimax.io/v1"
)

uploaded_zip = st.file_uploader("Drop your repo.zip here", type="zip")

if uploaded_zip:
    if st.button("Explain the entire repo ->", type="primary", use_container_width=True):
        with st.spinner("Extracting Files..."):
            code_text=""
            file_count = 0
            with zipfile.ZipFile(io.BytesIO(uploaded_zip.getvalue())) as z:
                for name in z.namelist():
                    if name.endswith('/') or '/.' in name or name.startswith('.'):
                        continue
                    if any(name.endswith(ext) for ext in ['.png', '.jpg', '.pdf', '.exe', '.jpeg', '.git']):
                           continue
                    try:
                        content = z.read(name).decode('utf-8', errors='ignore')
                        truncated = content[:6000] + ("\n .. (truncated)" if len(content) > 6000 else "")
                        code_text += f"\n\n== {name} ==\n{truncated}"
                        file_count += 1
                    except:
                        pass

        prompt = f"""
You are a senior engineer onboarding a new teammate.
Explain this entire codebase clearly and completely.

- what does this project do?
- High-level architecture
- key files and purposes
- How to run it locally
- Any gotchas or important details

Codebase ({file_count} files):
{code_text[:185000]}

"""
        with st.spinner("Generating Explanation..."):
            stream = client.chat.completions.create(
                model="MiniMax-M2-Stable",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                stream=True
            )
        
        st.success(f" Explained {file_count} files instantly!")
        response_placeholder = st.empty()
        full_response = ""

        for chunk in stream:
            if chunk.choices[0].delta.content if (hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta and hasattr(chunk.choices[0].delta, 'content')) else None:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

        st.code(full_response, language="markdown")


st.markdown("---")
st.caption("Powered by MiniMax-M2-Stable")

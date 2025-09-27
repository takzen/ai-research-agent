# app.py
import streamlit as st
from dotenv import load_dotenv
from agent_logic import create_agent_executor

# Load environment variables from .env file
load_dotenv()

st.set_page_config(layout="wide")
st.title("Autonomous AI Research Agent 🔬")

st.header("Delegate your research to an AI assistant")
research_topic = st.text_input(
    "Enter a complex topic or question for the agent to research",
    placeholder="e.g., What was the impact of GPT-4 on the development of RAG techniques in 2024?"
)

if st.button("Start Research"):
    if research_topic:
        with st.spinner("Agent has started the research. This process involves multiple steps and may take a few moments..."):
            try:
                # 1. Create the agent executor
                agent_executor = create_agent_executor()
                
                # 2. Invoke the agent with the user's topic
                response = agent_executor.invoke({"input": research_topic})
                
                # 3. Display the final report
                st.success("Research complete!")
                st.markdown("### Research Report")
                st.markdown(response['output'])

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a research topic.")
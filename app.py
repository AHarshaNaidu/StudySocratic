import streamlit as st
from groq import Groq

# Setup API key for Groqcloud
api_key = st.secrets["api_key"]
client = Groq(api_key=api_key)

# Socratic Questioning Prompts
initial_prompt = """
You are an AI assistant designed to teach Sorting Algorithms using the Socratic method. You will ask a series of questions to help the student think through and understand the material.
Start by identifying what sorting algorithm the student is trying to learn.
"""

# Narrowing Down to Sorting Algorithms
sorting_algorithm_prompt_template = """
A student is learning about sorting algorithms. Begin by asking what sorting algorithm they are trying to implement or understand (Bubble Sort, Quick Sort, etc.).
Once they answer, guide them through probing questions to help them understand the logic behind the algorithm.
"""

# Timeout Case Handling
timeout_prompt_template = """
A student’s sorting algorithm times out on large input sizes. Instead of giving them the answer, start by asking:
'What can you say about the difference between this test-case and the other test-cases that passed?'
Based on their answer, continue probing to help them realize the performance limitations.
"""

# Recursive Calls for Probing Questions
def socratic_response(user_input, topic):
    # Tailored response based on sorting algorithm or issue (e.g., timeout)
    if topic == "timeout":
        prompt_template = timeout_prompt_template
    else:
        prompt_template = sorting_algorithm_prompt_template
    
    data = {
        "model": "llama3-groq-70b-8192-tool-use-preview",
        "messages": [
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": user_input}
        ]
    }
    response = client.chat.completions.create(**data)
    return response.choices[0].message.content

# Streamlit Interface
st.set_page_config(page_title="Socratic Teaching Assistant for Sorting Algorithms", page_icon="📘")
st.title("Socratic Teaching Assistant for Sorting Algorithms 📘")

# Step 1: Student's Initial Input
st.header('Step 1: What do you need help with?')
student_input = st.text_area("Describe what sorting algorithm or issue you are facing:")

# Example topics: Bubble Sort, Quick Sort, Timeout on input, Merge Sort etc.
topic = st.selectbox("Select a category of your question:", options=["Sorting Algorithm", "Timeout", "Optimization"])

if st.button('Ask'):
    with st.spinner("Analyzing..."):
        # Socratic response generation
        socratic_reply = socratic_response(student_input, topic)
        st.write("### Socratic Assistant Response:")
        st.write(socratic_reply)

# Recursive follow-up to continue the dialogue
def recursive_follow_up():
    st.header('Step 2: Follow-up Question')
    follow_up_input = st.text_area("What do you think is the next step or problem?")
    
    if st.button('Continue'):
        with st.spinner("Analyzing..."):
            next_question = socratic_response(follow_up_input, topic)
            st.write("### Assistant Follow-up Question:")
            st.write(next_question)

recursive_follow_up()

# The AI will continue the dialogue until the student reaches the conclusion themselves.

import streamlit as st
from groq import Groq

# Setup API key for Groqcloud
api_key = st.secrets["api_key"]
client = Groq(api_key=api_key)

# Socratic Method Prompts
initial_prompt = """
You are an AI assistant designed to teach Sorting Algorithms using the Socratic method. Start by asking an introductory question on the algorithm the student wants to learn or improve.
"""

# Tailored Response Based on Student's Answer
def socratic_response(user_input, question_context):
    # Define the context based on whether the student answer is correct/incorrect
    prompt_template = f"""
    You are teaching a student sorting algorithms using the Socratic method. You asked the student the following question:
    "{question_context}"
    
    The student answered:
    "{user_input}"
    
    Analyze whether their answer is correct or incorrect. If correct, pose a new, deeper question. If incorrect, ask probing questions to guide them to the right understanding without revealing the answer directly.
    """
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
student_input = st.text_area("Describe what sorting algorithm or issue you are facing (e.g., Bubble Sort, Quick Sort, Merge Sort, Timeout on large inputs):")

# Select category of question
topic = st.selectbox("Select a category of your question:", options=["Sorting Algorithm", "Timeout", "Optimization"])

# Initialize variables to store state
if 'question_context' not in st.session_state:
    st.session_state.question_context = None

if 'response_history' not in st.session_state:
    st.session_state.response_history = []

# Handle the initial question based on topic selection
if st.button('Start Teaching'):
    with st.spinner("Generating initial question..."):
        if topic == "Sorting Algorithm":
            st.session_state.question_context = "What sorting algorithm are you trying to learn or implement?"
        elif topic == "Timeout":
            st.session_state.question_context = "What do you think is causing your algorithm to timeout?"
        else:
            st.session_state.question_context = "What part of your code do you think could be optimized?"

        # Display initial question
        st.write("### Assistant's Question:")
        st.write(st.session_state.question_context)

# Step 2: Student's Answer to the First Question
if st.session_state.question_context:  # Check if a question has been generated
    student_answer = st.text_area("Your Answer:")

    # Button to submit student's answer
    if st.button("Submit Answer"):
        with st.spinner("Evaluating answer..."):
            # Get the response from the AI based on student input and initial question
            socratic_reply = socratic_response(student_answer, st.session_state.question_context)
            
            # Show assistant's response
            st.write("### Assistant's Response:")
            st.write(socratic_reply)

            # Store the conversation history
            st.session_state.response_history.append({
                "question": st.session_state.question_context,
                "answer": student_answer,
                "assistant_response": socratic_reply
            })

    # Recursive follow-up: Probing based on the user's answer correctness
    if st.session_state.response_history:
        follow_up_answer = st.text_area("Answer the last question posed by the assistant:")

        if st.button('Submit Follow-up Answer'):
            with st.spinner("Evaluating follow-up answer..."):
                follow_up_reply = socratic_response(follow_up_answer, st.session_state.question_context)
                st.write("### Assistant's Follow-up Question or Response:")
                st.write(follow_up_reply)

                # Store follow-up conversation in history
                st.session_state.response_history.append({
                    "question": st.session_state.question_context,
                    "answer": follow_up_answer,
                    "assistant_response": follow_up_reply
                })

# End session button
if st.button("End"):
    st.write("### Session Ended. Thank you for using the Socratic Teaching Assistant!")
    st.session_state.response_history = []  # Clear history for the next session

import streamlit as st
import time

def main():
    st.title("Online Exam Platform")
    st.write("Welcome to the exam! You have 30 minutes to complete it.")

    # Get the start time if not already initialized
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    # Display countdown timer
    countdown(30)

    # Display exam questions
    display_questions()

    # Submit button
    if st.button("Submit"):
        submit_exam()

def countdown(minutes):
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(minutes * 60 - elapsed_time, 0)
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"Time Remaining: {minutes:02d}:{seconds:02d}")
    if remaining_time == 0:
        st.error("Time's up! Please submit your answers.")

def display_questions():
    # Display questions here
    # Example:
    st.header("Question 1:")
    st.write("What is 2 + 2?")
    st.session_state.answer1 = st.radio("Select an answer:", options=["3", "4", "5", "6"], key="answer1")

    st.header("Question 2:")
    st.write("What is the capital of France?")
    st.session_state.answer2 = st.radio("Select an answer:", options=["London", "Berlin", "Paris", "Rome"], key="answer2")

    st.header("Question 3:")
    st.write("What is the largest planet in our solar system?")
    st.session_state.answer3 = st.radio("Select an answer:", options=["Earth", "Jupiter", "Mars", "Venus"], key="answer3")

    # Add more questions as needed

def submit_exam():
    # Add code to handle submission of exam answers
    st.success("Your exam has been submitted successfully. Thank you!")

if __name__ == "__main__":
    main()

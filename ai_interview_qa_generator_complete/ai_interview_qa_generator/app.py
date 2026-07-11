import streamlit as st
from dotenv import load_dotenv
from interview_generator import AIInterviewGenerator
from resume_parser import extract_resume_text
from evaluator import evaluate_answer, generate_final_report

load_dotenv()

st.set_page_config(page_title="AI Interview Q&A Generator", page_icon="🎯", layout="wide")
st.title("🎯 AI Interview Q&A Generator")
st.caption("Generate tailored interview questions, run an adaptive mock interview, and receive an AI evaluation report.")

if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "evaluations" not in st.session_state:
    st.session_state.evaluations = []

with st.sidebar:
    st.header("Configuration")
    model = st.text_input("OpenAI model", value="gpt-4o-mini")
    question_count = st.slider("Number of questions", 3, 10, 5)

tab1, tab2, tab3 = st.tabs(["Generate Questions", "Mock Interview", "Final Report"])

with tab1:
    job_title = st.text_input("Job Title", placeholder="Senior Python Backend Engineer")
    job_description = st.text_area("Job Description", height=180)
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
    resume_text_manual = st.text_area("Or paste resume text", height=180)

    if st.button("Generate Tailored Questions", type="primary"):
        resume_text = extract_resume_text(uploaded_file) if uploaded_file else resume_text_manual
        if not job_title or not job_description or not resume_text:
            st.error("Please provide a job title, job description, and resume.")
        else:
            try:
                with st.spinner("Analyzing the profile..."):
                    generator = AIInterviewGenerator(model=model)
                    result = generator.generate_interview_flow(
                        job_title, job_description, resume_text, question_count
                    )
                    st.session_state.questions = result["questions"]
                    st.session_state.job_title = job_title
                    st.session_state.job_description = job_description
                    st.session_state.resume_text = resume_text
                    st.session_state.current_question = 0
                    st.session_state.answers = []
                    st.session_state.evaluations = []
                st.success("Questions generated successfully.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    for i, q in enumerate(st.session_state.questions, 1):
        with st.expander(f"{i}. {q['question']}"):
            st.write(f"**Category:** {q.get('category', 'N/A')}")
            st.write(f"**Difficulty:** {q.get('difficulty', 'N/A')}")
            st.write(f"**Intent:** {q.get('intent', 'N/A')}")
            st.write("**Ideal Answer Blueprint:**")
            for point in q.get("ideal_answer_blueprint", []):
                st.write(f"- {point}")

with tab2:
    if not st.session_state.questions:
        st.info("Generate interview questions first.")
    elif st.session_state.current_question >= len(st.session_state.questions):
        st.success("Interview completed. Open the Final Report tab.")
    else:
        idx = st.session_state.current_question
        q = st.session_state.questions[idx]
        st.subheader(f"Question {idx + 1} of {len(st.session_state.questions)}")
        st.write(q["question"])
        answer = st.text_area("Your Answer", key=f"answer_{idx}", height=180)

        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please enter an answer.")
            else:
                try:
                    with st.spinner("Evaluating answer..."):
                        evaluation = evaluate_answer(
                            model=model,
                            question=q,
                            answer=answer,
                            job_title=st.session_state.job_title
                        )
                    st.session_state.answers.append(answer)
                    st.session_state.evaluations.append(evaluation)
                    st.session_state.current_question += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"Evaluation failed: {e}")

with tab3:
    if not st.session_state.evaluations:
        st.info("Complete at least one interview answer to generate a report.")
    else:
        for i, evaluation in enumerate(st.session_state.evaluations, 1):
            with st.expander(f"Evaluation {i}"):
                st.metric("Score", f"{evaluation.get('score', 0)}/10")
                st.write("**Feedback:**", evaluation.get("feedback", ""))
                st.write("**Strengths:**", ", ".join(evaluation.get("strengths", [])))
                st.write("**Improvements:**", ", ".join(evaluation.get("improvements", [])))

        if st.button("Generate Final AI Report", type="primary"):
            try:
                with st.spinner("Creating final report..."):
                    report = generate_final_report(
                        model=model,
                        job_title=st.session_state.get("job_title", ""),
                        evaluations=st.session_state.evaluations
                    )
                st.markdown(report)
            except Exception as e:
                st.error(f"Report generation failed: {e}")

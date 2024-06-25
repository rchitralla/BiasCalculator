import streamlit as st

# Define the sections and questions
sections = {
    "General": [
        "I set clear goals for my team.",
        "I communicate effectively with team members.",
        "I provide regular feedback to my team."
    ],
    "Recruiting & Hiring": [
        "I have a clear recruitment strategy.",
        "I conduct thorough interviews.",
        "I ensure new hires are onboarded effectively."
    ],
    "Culture & Engagement": [
        "I foster a positive work environment.",
        "I recognize and reward team achievements.",
        "I encourage open communication."
    ]
}

# Function to display each section and collect responses
def display_section(section_name, questions):
    st.header(section_name)
    scores = []
    for question in questions:
        score = st.radio(question, [3, 2, 1], index=2)
        scores.append(score)
    return scores

# Main function to display the self-assessment form
def main():
    st.title("Self Assessment Tool")
    st.write(
        "Read each statement and choose a score using the rating scale provided. "
        "Once complete, subtotal the scores by section. Reflect on areas where your scores are lower than others and identify where you can continue to grow. "
        "The assessment should take you no longer than 5 – 10 mins."
    )
    st.write("### Rating Scale: 3 = all of the time, consistent application | 2 = some of the time, inconsistent application | 1 = Not done at all")

    # Dictionary to store the total scores for each section
    total_scores = {}

    # Iterate over each section and display the questions
    for section_name, questions in sections.items():
        scores = display_section(section_name, questions)
        total_scores[section_name] = sum(scores)

    # Display the results
    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")
        for section_name, score in total_scores.items():
            st.write(f"**{section_name}: {score}**")

        lowest_score_section = min(total_scores, key=total_scores.get)
        st.write(f"### Reflect on areas where your scores are lower than others. Consider focusing on improving the **{lowest_score_section}** section.")

if __name__ == "__main__":
    main()



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def main():
    st.title("Self Assessment Tool")
    st.write("Read each statement and choose a score using the rating scale provided. Once complete, subtotal the scores by section. Reflect on areas where your scores are lower than others and identify where you can continue to grow. The assessment should take you no longer than 5 – 10 mins.")
    st.write("### Rating Scale: 3 = all of the time, consistent application | 2 = some of the time, inconsistent application | 1 = Not done at all")

    scores = {}
    total_scores = {}
    max_scores = {section: len(questions) * 3 for section, questions in sections.items()}  # Maximum possible score per section

    for section, questions in sections.items():
        st.header(section)
        section_score = 0
        for question in questions:
            score = st.radio(question, [3, 2, 1], index=2, key=f"{section}_{question}")
            section_score += score
        total_scores[section] = section_score

    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")
        for section, score in total_scores.items():
            st.write(f"**{section}: {score}** out of {max_scores[section]}")
        
        lowest_score_section = min(total_scores, key=total_scores.get)
        st.write(f"### Reflect on areas where your scores are lower than others. Consider focusing on improving the **{lowest_score_section}** section.")

        # Create a DataFrame for visualization
        df_scores = pd.DataFrame.from_dict(total_scores, orient='index', columns=['Score'])
        df_scores['Max Score'] = [max_scores[section] for section in df_scores.index]
        df_scores['Percentage'] = (df_scores['Score'] / df_scores['Max Score']) * 100

        # Display the DataFrame
        st.dataframe(df_scores)

        # Create a bar chart
        fig, ax = plt.subplots()
        df_scores['Score'].plot(kind='bar', ax=ax, color='skyblue', alpha=0.7)
        ax.set_title('Scores by Section')
        ax.set_xlabel('Section')
        ax.set_ylabel('Score')
        ax.set_ylim(0, max(max_scores.values()) + 1)
        for i in ax.containers:
            ax.bar_label(i,)
        
        st.pyplot(fig)

if __name__ == "__main__":
    main()


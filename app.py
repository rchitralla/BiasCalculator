# Main function to display the self-assessment form
def main():
    st.image(logo_path, width=200)  # Add your logo at the top
    st.title("Anti-Bias Self Assessment Tool")
    st.write(
        "This tool enables you to explore your own behaviors related to bias & inclusion in the workplace. "
        "Your results are yours and yours alone -- they will not be submitted or shared in any manner unless you choose to do so."
    )
    st.write(
        "Read each statement and choose a score using the rating scale provided. "
        "Once complete, the tool subtotals the scores by section. Reflect on areas where your scores are lower than others and identify where you can continue to grow. "
        "The assessment should take you no longer than 5 – 10 mins."
    )
    st.write("### Rating Scale: 1 = Never | 2 = Rarely | 3 = Sometimes | 4 = Often | 5 = Consistently all the time")

    # Shuffle questions once per session
    if 'shuffled_questions' not in st.session_state:
        st.session_state['shuffled_questions'] = questions_list.copy()
        random.shuffle(st.session_state['shuffled_questions'])

    # Display the questions and collect responses
    responses = display_questions()

    # Calculate the total score
    total_score = calculate_total_score(responses)

    # Calculate the total scores per category
    total_scores_per_category = calculate_total_scores_per_category(responses)

    # Calculate the maximum possible scores per category
    max_scores_per_category = calculate_max_scores_per_category(categories)

    # Display the results and visualizations
    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")

        st.write("### How to interpret the results")
        st.write(
            "The questions answered fall under the individual, company, and industry related actions and choices you make every day at work. "
            "They address key areas from hiring through developing and retaining talent that we as company leaders make in relation to our peers, team members, superiors, and creating a broader impact on the industry."
        )
        st.write(
            "Take a look at the scores below and see:\n"
            "- Where do you score highest?\n"
            "- Which area has the highest potential to improve?\n"
            "- Is there anything that surprised you?\n"
            "- What are some of the actions that you can take to reduce bias and drive inclusion?\n"
            "Capture your reflection for a later conversation."
        )
        st.write("#### Development")
        st.write("Spans actions in the area of developing talent/your team")
        st.write("#### General")
        st.write("Covers general work related attitudes and actions")
        st.write("#### Recruiting & Hiring")
        st.write("Highlights potential bias in recruiting and hiring talent")
        st.write("#### Performance & Reward")
        st.write("Looks at equity in relation to this area of rewarding the team")
        st.write("#### Culture & Engagement")
        st.write("Your actions and attitudes related to organisational culture")
        st.write("#### Exit & Retention")
        st.write("Actions related to retaining and understanding the reasons for talent drain")

        # Display total scores per category
        for category_name, score in total_scores_per_category.items():
            max_score = max_scores_per_category[category_name]
            st.write(f"**{category_name}: {score} out of {max_score}**")

            # Calculate and display custom progress bar
            progress = int((score / max_score) * 100)
            custom_progress_bar(progress)

        # Prepare data for visualization
        flattened_scores = []
        for category_name, types in categories.items():
            for type_name, questions in types.items():
                response_scores = [response['score'] for response in responses if (response['category'] == category_name) and (response['type'] == type_name) and (type(response['score']) == int)]
                score = sum(response_scores)
                max_score = len(questions) * 5
                percentage = (score / max_score) * 100
                flattened_scores.append({"Category": category_name, "Type": type_name, "Score": score, "Percentage": percentage})
        scores_data = pd.DataFrame(flattened_scores)

        # Sort the scores_data based on the ordered categories
        ordered_categories = scores_data["Category"].unique()
        scores_data["Category"] = pd.Categorical(scores_data["Category"], categories=ordered_categories, ordered=True)
        scores_data = scores_data.sort_values(by=["Category", "Percentage"], ascending=[True, False])

        # Create a custom horizontal stacked bar chart for scores (percentage)
        custom_stacked_bar_chart(scores_data)

if __name__ == "__main__":
    main()

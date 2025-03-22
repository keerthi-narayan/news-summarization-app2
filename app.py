import streamlit as st
from utils import scrape_news, analyze_sentiment, extract_topics, generate_tts, perform_comparative_analysis, analyze_topic_overlap, translate_to_hindi, load_models
import os

# Load models once
sentiment_pipeline, summarizer = load_models()

# Check if models loaded successfully
if sentiment_pipeline is None or summarizer is None:
    st.error("Failed to load models. Please check your internet connection and try again.")
    st.stop()

# App Title and Description
st.title("📰 News Summarization App")
st.subheader("Get the latest news sentiment analysis and summaries for any company!")

# Sidebar for Input and Options
with st.sidebar:
    st.header("🔍 Input")
    company_name = st.text_input("Enter Company Name")
    st.markdown("---")
    st.markdown("**Note**: This app analyzes the latest news articles for the given company name.")

# Analyze button with a unique key
if st.button("Analyze", key="analyze_button"):
    if not company_name:
        st.error("Please enter a company name.")
        st.stop()
    
    # Show a progress bar while fetching news
    with st.spinner("Fetching news articles..."):
        articles = scrape_news(company_name)
    
    # Check if articles were found
    if not articles:
        st.error("Enter a valid company name. No news articles found for the given name.")
        st.stop()
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # Display only 2 articles
    st.header("📰 Latest News Articles")
    for article in articles[:2]:  # Only process the first 2 articles
        with st.expander(f"**{article['title']}**"):
            st.write(f"**Summary:** {article['summary']}")
            
            # Analyze sentiment
            sentiment = analyze_sentiment(article['summary'], sentiment_pipeline)
            st.write(f"**Sentiment:** {sentiment}")
            
            # Extract and display key topics
            topics = extract_topics(article['summary'], summarizer)
            st.write(f"**Key Topics Covered:** {topics}")
        
        # Count sentiments
        if sentiment == "POSITIVE":
            positive_count += 1
        elif sentiment == "NEGATIVE":
            negative_count += 1
        else:
            neutral_count += 1

    # Display Comparative Sentiment Score
    st.header("📊 Comparative Sentiment Score")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Positive", positive_count)
    with col2:
        st.metric("Negative", negative_count)
    with col3:
        st.metric("Neutral", neutral_count)

    # Perform Coverage Differences
    st.header("🔍 Coverage Differences")
    coverage_differences = perform_comparative_analysis(articles[:2])
    if not coverage_differences:
        st.warning("Not enough articles for comparison.")
    else:
        for difference in coverage_differences:
            with st.expander(f"**Comparison {coverage_differences.index(difference) + 1}**"):
                st.write(f"**Comparison:** {difference['Comparison']}")
                st.write(f"**Impact:** {difference['Impact']}")

    # Analyze topic overlap
    st.header("📌 Topic Overlap")
    topic_overlap = analyze_topic_overlap(articles[:2], summarizer)
    st.write(f"**Common Topics:** {', '.join(topic_overlap['Common Topics'])}")
    for key, topics in topic_overlap['Unique Topics'].items():
        with st.expander(f"**{key} Unique Topics**"):
            st.write(f"{', '.join(topics)}")

    # Determine the overall sentiment description
    if positive_count > negative_count:
        sentiment_description = "latest news coverage is mostly positive."
        stock_outlook = "Potential stock growth expected."
    elif negative_count > positive_count:
        sentiment_description = "latest news coverage is mostly negative."
        stock_outlook = "Potential stock decline expected."
    else:
        sentiment_description = "latest news coverage is neutral."
        stock_outlook = "Stock performance is uncertain."

    # Generate the final summary
    final_summary = (
        f"{company_name}'s {sentiment_description} "
        f"Out of {len(articles)} articles, "
        f"{positive_count} are positive, "
        f"{negative_count} are negative, "
        f"and {neutral_count} are neutral. "
        f"{stock_outlook}"
    )

    # Display the Final Sentiment Analysis
    st.header("📈 Final Sentiment Analysis")
    st.success(final_summary)

    # Translate the final summary to Hindi
    st.header("In Hindi Audio Summary")
    hindi_summary = translate_to_hindi(final_summary)
    if not hindi_summary:
        st.error("Error translating summary to Hindi.")
    else:
        # Generate Hindi TTS for the final summary
        output_file = generate_tts(hindi_summary)
        if output_file and os.path.exists(output_file):
            st.write("Click the play button below to listen to the Hindi summary:")
            st.audio(output_file, format="audio/mp3")
        else:
            st.error("Error generating Hindi audio. Please try again.")

# Footer
st.markdown("---")
st.markdown("### 🚀 Powered by Streamlit, NewsAPI, and Hugging Face Transformers")
st.markdown("Created with ❤️ by Keerthi N")
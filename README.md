
---

1. **Title and Description**:
   - # 📰 News Summarization App

A Streamlit-based web application that fetches the latest news articles for a given company, analyzes their sentiment, extracts key topics, and provides a summary in both English and Hindi.

2. **Features**:
   - **News Fetching**: Fetches the latest news articles using the NewsAPI.
- **Sentiment Analysis**: Analyzes the sentiment of news articles (Positive, Negative, Neutral).
- **Topic Extraction**: Extracts key topics from the news articles.
- **Comparative Analysis**: Compares the sentiment and topics of multiple articles.
- **Hindi Translation**: Translates the final summary into Hindi.
- **Hindi Audio Summary**: Generates an audio summary in Hindi.

3. **Prerequisites**:
   Before running the app, ensure you have the following installed:

    1. **Python 3.8 or higher**
    2. **Git** (for cloning the repository)
    3. **NewsAPI Key** (sign up at [NewsAPI](https://newsapi.org/) to get a free API key)

4. **Installation**:
   - **1. Clone the Repository**

        git clone https://github.com/keerthi-narayan/news-summarization-app2.git
        cd your-repo-name

   - **2. Set Up a Virtual Environment**
        # For Windows
            python -m venv venv
            .\venv\Scripts\activate

        # For macOS/Linux
            python3 -m venv venv
            source venv/bin/activate

    - **3. Install Dependencies**
            pip install -r requirements.txt

5. **Configuration**:
   - 1. Add Your NewsAPI Key
        ->Open the utils.py file.
        ->Replace the placeholder with your NewsAPI key:

            NEWS_API_KEY = "your_newsapi_key_here"

    - 2. Running the App:
        1. Start the Streamlit App
            streamlit run app.py

        2. Open the App in Your Browser
            The app will open in your default browser at http://localhost:8501.

6. **Usage**:
   -Enter a Company Name:

    -Type the name of the company you want to analyze (e.g., "Tesla").

    -Click "Analyze":

    -The app will fetch the latest news articles, analyze their sentiment, and display the results.

    -Explore the Results:

    -View the sentiment analysis, topic extraction, and comparative analysis.

    -Listen to the Hindi audio summary.

7. **File Structure**:
   - your-repo-name/
    ├── app.py                # Main Streamlit application
    ├── utils.py              # Utility functions (API calls, sentiment analysis, etc.)
    ├── requirements.txt      # List of Python dependencies
    ├── README.md             # This file
    └── output.mp3            # Generated Hindi audio summary

8. **Dependencies**:
   - The app uses the following Python libraries:

        streamlit (for the web interface)

        requests (for API calls)

        transformers (for sentiment analysis and topic extraction)

        gtts (for Hindi text-to-speech)

    All dependencies are listed in requirements.txt.

9. **Contributing**:
   Contributions are welcome! If you'd like to contribute:

    Fork the repository.

    Create a new branch (git checkout -b feature/your-feature-name).

    Commit your changes (git commit -m 'Add some feature').

    Push to the branch (git push origin feature/your-feature-name).

    Open a pull request.

10. **License**:
    This project is licensed under the MIT License. See the LICENSE file for details.

11. **Acknowledgments**:
    - Streamlit for the web framework.

    - NewsAPI for providing news data.

    - Hugging Face Transformers for sentiment analysis and topic extraction.

    - gTTS for Hindi text-to-speech..

12. **Contact**:
    - Your Name: keerthinarayan.2002@gmail.com

    - GitHub: keerthi-narayan

---

### **How to Use the README**
1. Replace placeholders (e.g., `your-username`, `your-repo-name`, `your-email@example.com`) with your actual information.
2. Add a `LICENSE` file if you want to specify a license for your project.
3. Push the updated `README.md` to your GitHub repository:
   ```bash
   git add README.md
   git commit -m "Added README file with setup instructions"
   git push origin main
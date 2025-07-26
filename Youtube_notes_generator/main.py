import streamlit as st
from google import genai
from google.genai import types
import re

PROMPT="""You are a professional YouTube video analyzer. Your task is to generate a detailed and structured analysis and summary of a given video. Follow the instructions below carefully:

Requirements:
Provide a really detailed breakdown of the video, covering the following aspects in detail:

- Visuals: Describe what is being shown on the screen.
- Actions: Explain what the speaker or demonstrator is doing step-by-step.
- Spoken Content: Summarize what is being said or explained.
- Results/Outcomes: Mention the results or changes observed after each major action.
- Conclusions or Insights: Highlight any conclusions drawn or key points emphasized by the speaker.

Instructions:
- Use accurate timestamps for each major segment or change (e.g., 00:45 - "The host name with the main topic was displayed on the screen").
- The analysis must reflect the entire video. Don't skip any parts. Be as detailed and specific as possible.
- Maintain a clean, structured, and professional format, suitable for use in documentation, research, or study purposes.

Formatting:
- Use clear headings and subheadings to organize the analysis.
- Use bullet points for lists and summaries.
- Use numbered lists for step-by-step instructions.

"""

# Page configuration
st.set_page_config(
    page_title="YouTube Video Summarizer & Chat",
    page_icon="📺",
    layout="wide"
)

def is_valid_youtube_url(url):
    """Check if the provided URL is a valid YouTube URL"""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return youtube_regex.match(url) is not None

def get_video_transcript(client, youtube_url):
    """Get the video transcript with timestamps"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=types.Content(
                parts=[
                    types.Part(
                        file_data=types.FileData(file_uri=youtube_url)
                    ),
                    types.Part(text="Please provide the complete transcript of this video with timestamps. Format it clearly with time markers.")
                ]
            )
        )
        return response.text
    except Exception as e:
        st.error(f"Error getting transcript: {str(e)}")
        return None

def chat_with_video(client, user_question, transcript, chat_history):
    """Chat about the video using the transcript"""
    try:
        # Create context from transcript and chat history
        context = f"Video Transcript:\n{transcript}\n\n"
        
        if chat_history:
            context += "Previous conversation:\n"
            for chat in chat_history:
                context += f"User: {chat['user']}\nAssistant: {chat['assistant']}\n\n"
        
        context += f"Current question: {user_question}\n\nPlease answer the question based on the video content and transcript provided above."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=types.Content(
                parts=[types.Part(text=context)]
            )
        )
        return response.text
    except Exception as e:
        return f"Error in chat: {str(e)}"

def main():
    st.title("📺 YouTube Video Summarizer & Chat")
    st.markdown("Enter a YouTube URL to get an AI-powered summary AND chat about the video!")
    
    # Initialize session state
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False
    if 'current_video_url' not in st.session_state:
        st.session_state.current_video_url = None
    if 'summary_text' not in st.session_state:
        st.session_state.summary_text = None
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input(
            "Google AI API Key", 
            type="password",
            help="Enter your Google AI Studio API key"
        )
        
        if st.button("Get API Key", help="Click to get your free API key"):
            st.info("Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to get your free API key")
        
        # Show summary in sidebar when chat is active
        if st.session_state.video_processed:
            st.markdown("---")
            st.header("📝 Video Summary")
            # We'll populate this with the actual summary after processing
            if 'summary_text' in st.session_state:
                st.write(st.session_state.summary_text)
            
            st.markdown("---")
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste any YouTube video URL here"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        process_button = st.button("🔍 Process Video", type="primary")
    
    # Process the video
    if process_button:
        if not api_key:
            st.error("Please enter your Google AI API key in the sidebar.")
            return
        
        if not youtube_url:
            st.error("Please enter a YouTube URL.")
            return
        
        if not is_valid_youtube_url(youtube_url):
            st.error("Please enter a valid YouTube URL.")
            return
        
        try:
            # Configure the API
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Processing video... Getting transcript and summary..."):
                # Get transcript first
                transcript = get_video_transcript(client, youtube_url)
                
                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.current_video_url = youtube_url
                    st.session_state.video_processed = True
                    st.session_state.chat_history = []  # Clear previous chat
                    
                    # Generate summary
                    summary_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=types.Content(
                            parts=[
                                types.Part(
                                    file_data=types.FileData(file_uri=youtube_url)
                                ),
                                types.Part(text=PROMPT)
                            ]
                        )
                    )
                    
                    # Store summary in session state
                    st.session_state.summary_text = summary_response.text
                    
                    st.success("Video processed successfully! You can now chat about it.")
                    
                    # Only show video, not summary (summary moved to sidebar)
                    st.subheader("🎥 Video")
                    st.video(youtube_url)
                
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            st.info("Make sure your API key is valid and the video is publicly accessible.")
    
    # Chat interface (only show if video is processed)
    if st.session_state.video_processed and st.session_state.transcript:
        st.markdown("---")
        st.subheader("💬 Chat with Video")
        st.markdown("Ask questions about the video content!")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["user"])
            with st.chat_message("assistant"):
                st.write(chat["assistant"])
        
        # Chat input
        user_question = st.chat_input("Ask a question about the video...")
        
        if user_question and api_key:
            # Add user message to chat
            with st.chat_message("user"):
                st.write(user_question)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    client = genai.Client(api_key=api_key)
                    response = chat_with_video(
                        client, 
                        user_question, 
                        st.session_state.transcript, 
                        st.session_state.chat_history
                    )
                    st.write(response)
            
            # Save to chat history
            st.session_state.chat_history.append({
                "user": user_question,
                "assistant": response
            })
            st.rerun()
    
    # Show instructions only when no video is processed
    if not st.session_state.video_processed:
        st.markdown("---")
        st.markdown("""
        ### How to use:
        1. Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Enter the API key in the sidebar
        3. Paste any YouTube video URL
        4. Click "Process Video" to get summary and enable chat
        5. Use the chat box to ask questions about the video
        
        ### Features:
        - **📝 Summary**: Get a detailed summary of the video
        - **💬 Chat**: Ask specific questions about video content
        - **🕐 Transcript**: Uses full transession_statescript with timestamps for accurate responses
        - **🗑️ Clear Chat**: Reset conversation anytime
        
        **Note:** This app uses Google's Gemini 2.5 Flash model to analyze YouTube videos.
        """)

if __name__ == "__main__":
    main()
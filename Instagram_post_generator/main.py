import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import time

LIMIT = 1000  # Character limit for posts

# --- CONFIG ---
st.set_page_config(page_title="🐦 AI Post + Image Generator", page_icon="🐦")
char_limits = {"Twitter/X": LIMIT, "LinkedIn": LIMIT, "Facebook": LIMIT, "Instagram": LIMIT}

# --- SESSION STATE ---
for key in ['generated_post', 'search_results', 'generated_image', 'api_key']:
    if key not in st.session_state:
        st.session_state[key] = ""

# --- FUNCTIONS ---
def get_client_and_config(api_key):
    """Return a client and a helper tool for Google search (no default response modalities)."""
    client = genai.Client(api_key=api_key)
    search_tool = types.Tool(google_search=types.GoogleSearch())
    return client, search_tool

def generate_post_and_image(api_key, topic, style, platform):
    model = "gemini-2.5-flash"
    image_model = "gemini-2.0-flash-preview-image-generation"
    client, search_tool = get_client_and_config(api_key)

    # Helper configs
    text_only_cfg = types.GenerateContentConfig(response_modalities=["TEXT"])
    # The image model requires both IMAGE and TEXT response modalities
    image_only_cfg = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])

    # Config for research (needs Google search + TEXT output)
    research_cfg = types.GenerateContentConfig(
        tools=[search_tool],
        response_modalities=["TEXT"]
    )

    # Step 1: Research latest info about the topic
    search_prompt = f"Find recent, and latest updates on: {topic}"
    search_res = client.models.generate_content(model=model, contents=search_prompt, config=research_cfg)
    search_text = search_res.text

    # Step 2: Generate the social media post (TEXT only)
    post_prompt = f"""
    Based on the following info about {topic}:
    {search_text}

    Write a {style.lower()} post for {platform}. You are the best POST generator.
    Make it engaging, informative, and suitable for the platform.
    Include relevant hashtags, emojis, and keep it under {char_limits[platform]} characters.
    """

    post_response = client.models.generate_content(
        model=model,
        contents=post_prompt,
        config=text_only_cfg
    )
    post_text = post_response.text.strip()

    # Step 3: Generate the image (IMAGE only)
    image_prompt = f"""
    Create a creative image that visually represents the topic "{topic}".
    Use the latest information provided below for inspiration:
    {search_text}
    """

    image_response = client.models.generate_content(
        model=image_model,
        contents=image_prompt,
        config=image_only_cfg
    )

    # Extract image data from response
    image_data = None
    for part in image_response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            image_data = Image.open(BytesIO(part.inline_data.data))
            break

    return post_text, search_text, image_data

# --- HEADER ---
st.title("🐦 AI Social Post + 🖼️ Image Generator")

# --- INPUTS ---
api_key = st.text_input("🔑 Google AI API Key", type="password", value=st.session_state.api_key)
if api_key:
    st.session_state.api_key = api_key

platform = st.selectbox("📱 Platform", list(char_limits.keys()))
style = st.selectbox("🎭 Post Style", ["Informative", "Professional", "Casual", "News-like"])
quick_topics = ["AI", "Climate", "Crypto", "Space", "Tech", "Health", "Sports", "Entertainment"]
topic = st.text_input("🔍 Topic", placeholder="e.g., Latest trends in crypto")
selected_quick = st.selectbox("Or pick a quick topic", [""] + quick_topics)
if selected_quick and not topic:
    topic = selected_quick

# --- GENERATE BUTTON ---
if st.button("🚀 Generate Post + Image"):
    if not api_key:
        st.error("Please enter your API key.")
    elif not topic.strip():
        st.error("Please enter a topic.")
    else:
        try:
            with st.spinner("Generating post and image..."):
                post, research, image = generate_post_and_image(api_key, topic, style, platform)
                st.session_state.generated_post = post
                st.session_state.search_results = research
                st.session_state.generated_image = image
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- OUTPUT ---
if st.session_state.generated_post:
    st.subheader("✨ Generated Post")
    char_count = len(st.session_state.generated_post)
    st.success(f"Character count: {char_count}/{char_limits[platform]}")
    st.text_area("Post:", value=st.session_state.generated_post, height=150)

    if st.session_state.generated_image:
        st.subheader("🖼️ Generated Image")
        st.image(st.session_state.generated_image, use_container_width=True)

    if st.button("🔄 Regenerate"):
        for key in ['generated_post', 'search_results', 'generated_image']:
            st.session_state[key] = ""
        st.rerun()

    with st.expander("📚 Research Summary"):
        st.write(st.session_state.search_results)

# --- API HELP ---
if not api_key:
    st.warning("Get a free API key from: https://aistudio.google.com/app/apikey")

import os
import subprocess
import re
import streamlit as st

def get_available_formats(video_url):
    """Fetch available video formats and return a dictionary of available options."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--list-formats", video_url],
            capture_output=True,
            text=True
        )
        output = result.stdout
        
        # Extract format ID and resolution (e.g., "954 mp4 854x480")
        format_lines = re.findall(r"(\d+)\s+mp4\s+(\d+x\d+)", output)
        formats = {f[0]: f[1] for f in format_lines}
        
        return formats
    except Exception as e:
        st.error(f"Error fetching formats: {e}")
        return {}

def download_video(video_url, format_id):
    """Download the selected video format along with audio and merge them."""
    st.write(f"\n✅ Downloading video (Format ID: {format_id})...\n")
    
    # Download video and best audio separately
    command = f'yt-dlp -f "{format_id}+bestaudio" "{video_url}" --merge-output-format mp4'
    os.system(command)
    
    st.success("✅ Video download completed!")

# Streamlit UI
st.title("🎥 Zee5 Video Downloader")

video_url = st.text_input("🔗 Enter the Zee5 video URL:")

if st.button("Fetch Available Formats"):
    if video_url:
        formats = get_available_formats(video_url)
        
        if formats:
            selected_format = st.selectbox("🎥 Choose a Video Quality to Download:", list(formats.keys()), format_func=lambda x: f"{x} -> {formats[x]}")
            
            if st.button("Download Video"):
                download_video(video_url, selected_format)
        else:
            st.error("⚠️ No valid video formats found.")
    else:
        st.warning("Please enter a valid Zee5 video URL.")

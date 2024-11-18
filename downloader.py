import streamlit as st
import os
import glob
import yt_dlp
import random 
import time
from pytube import Search



def search_youtube(query):
    try:
        # Perform YouTube search
        search_results = Search(query)
        return search_results.results
    except Exception as e:
        st.error(f"Дошло је до грешке при претрази: {e}")
        return []
    

def yt_download(
    yt_link: str, download_folder: str, output_format: str = "wav"
) -> tuple[str, str]:
    if output_format not in ["mp3", "wav"]:
        raise ValueError("Invalid format choice. Please choose 'mp3' or 'wav'.")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "quiet": True,  # Suppresses the verbose output
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": output_format,
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(yt_link, download=True)
        song_name = info.get("title", None)

    file_name = song_name + "." + output_format
    print(f"Download completed and saved as {output_format.upper()} file.")

    return file_name, song_name

def download_audio(url, download_path):
    try:
        # Create download directory if it doesn't exist
        os.makedirs(download_path, exist_ok=True)
        
        
        # Download the audio
        st.write(f"Downloading audio from: {url}")
        downloaded_file = yt_download(yt_link=url, download_folder=download_path, output_format="mp3")
        
        
        st.success(f"Audio download complete! File saved at: {downloaded_file}")
        return downloaded_file
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    
    
def list_downloaded_files(download_path):
    # List video files
    video_files = glob.glob(os.path.join(download_path, '*.mp4'))
    # List audio files
    audio_files = glob.glob(os.path.join(download_path, '*.mp3'))
    
    # Combine and sort files
    all_files = sorted(video_files + audio_files, key=os.path.getctime, reverse=True)
    
    return all_files


def get_funny_loading_messages():
    messages = [
        "🍺 Точење rakije за брзо преузимање...",
        "🥃 Припремам оркестар за музички download...",
        "🍸 Зовем другаре да помогну око скидања...",
        "🍹 Conditioning the folk band for digital performance...",
        "🥂 Распремам ракију за интернет журку...",
        "🍻 Договарам се са YouTube гајбом...",
        "🥃 Спремам underground muzički download...",
        "🍺 Наливам serra да убрза интернет...",
        "🍸 Позивам духове брзог интернета...",
        "🥂 Приводим крају купусијаду преузимања..."
    ]
    return random.choice(messages)



def main():
    # Initialize state variables if not already set
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'selected_url' not in st.session_state:
        st.session_state.selected_url = None

    st.title("🥃 YouTube Преузимач 🍺")
    
    # Sidebar for configuration
    st.sidebar.header("Подешавања преузимања")

    download_path = st.sidebar.text_input(
        "Путања за преузимање", 
        value=os.path.join(os.path.expanduser('~'), "Downloads", "YouTube")
    )
    
    # Search or direct URL input
    search_mode = st.radio("Режим уноса", ["Директан линк", "Претрага"])
    
    if search_mode == "Директан линк":
        url = st.text_input("Убаци YouTube линк")
        st.session_state.selected_url = url
    else:
        search_query = st.text_input("Претражи YouTube")
        
        if st.button("Пронađи 🔍"):
            # Perform search
            st.session_state.search_results = search_youtube(search_query)
    
    # Display search results if available
    if st.session_state.search_results:
        st.write("### Резултати претраге:")
        selected_video_index = st.selectbox(
            "Изабери видео за преузимање", 
            range(len(st.session_state.search_results)),
            format_func=lambda x: f"{st.session_state.search_results[x].title} (by {st.session_state.search_results[x].author})"
        )
        
        # Get the URL of the selected video
        st.session_state.selected_url = st.session_state.search_results[selected_video_index].watch_url
    
    # Download button
    if st.button("Скини 🍻"):
        if not st.session_state.selected_url:
            st.warning("Молим те убаци валидан YouTube линк или изабери видео!")
            return
        
        with st.spinner(get_funny_loading_messages()):
            time.sleep(2)
        
        download_audio(st.session_state.selected_url, download_path)
    
    # Downloaded files section
    st.header("📁 Преузете датотеке")
    files = list_downloaded_files(download_path)
    
    if files:
        for file in files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(os.path.basename(file))
            with col2:
                if st.button("Обриши 🗑️🍺", key=file):
                    os.remove(file)
                    st.experimental_rerun()
    else:
        st.write("Још увек нема преузетих фајлова. Време за ракију! 🥃")

if __name__ == "__main__":
    main()
from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')

    if not video_url:
        return 'Error: No URL provided', 400

    try:
        # Set options for yt-dlp (output location and format)
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'best',  # Download the best quality available
        }

        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_filename = ydl.prepare_filename(info_dict)

        # Return the video file to the user
        return send_file(video_filename, as_attachment=True)

    except Exception as e:
        return f'Error downloading video: {str(e)}', 500

if __name__ == "__main__":
    app.run(debug=True)

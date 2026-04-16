from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

# This is the "Frontend" - A simple page to test on your phone
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Music Proxy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #121212; color: white; font-family: sans-serif; text-align: center; padding: 50px; }
        input { padding: 10px; width: 80%; max-width: 300px; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #1DB954; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Cloud Music for ESP32</h1>
    <form action="/play" method="get">
        <input type="text" name="search" placeholder="Enter song name..." required>
        <button type="submit">Play/Test</button>
    </form>
    <p style="color: #666; font-size: 0.8em; margin-top: 20px;">Use: yoursite.com/play?search=SONGNAME on ESP32</p>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/play')
def play():
    song_name = request.args.get('search')
    if not song_name:
        return "Bro, enter a song name!", 400

    # yt-dlp configuration to get the raw audio stream
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Search and extract info
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            # Redirect the request to the direct Google Video URL
            return redirect(info['url'])
        except Exception as e:
            return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
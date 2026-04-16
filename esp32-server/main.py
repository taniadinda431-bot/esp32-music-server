from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

# This is just for your phone browser testing
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Music Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #121212; color: white; font-family: sans-serif; text-align: center; padding: 50px; }
        input { padding: 10px; width: 80%; max-width: 300px; border-radius: 5px; }
        button { padding: 10px 20px; background: #1DB954; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin: 10px; padding: 10px; background: #282828; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>ESP32 Music Cloud</h1>
    <form action="/play" method="get">
        <input type="text" name="search" placeholder="Enter song name..." required>
        <button type="submit">Play Now</button>
    </form>
</body>
</html>
'''

# Standard options to bypass bot checks and get high quality audio
YDL_OPTS_BASE = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'no_warnings': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# NEW ROUTE: ESP32 calls this to see 3 song options
@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return "No query", 400
    
    # We search for 3 entries instead of 1
    opts = YDL_OPTS_BASE.copy()
    opts['default_search'] = 'ytsearch3' 
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch3:{query}", download=False)
            # Create a list of titles, limit each to 30 characters so they fit on your screen
            titles = [entry['title'][:30] for entry in info['entries'] if entry]
            # Send them back as a single string separated by '|'
            return "|".join(titles)
        except Exception as e:
            return f"Error: {str(e)}", 500

# ESP32 calls this to actually get the music stream
@app.route('/play')
def play():
    song_name = request.args.get('search')
    if not song_name:
        return "No song name", 400

    opts = YDL_OPTS_BASE.copy()
    opts['default_search'] = 'ytsearch'

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            return redirect(info['url'])
        except Exception as e:
            return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

# --- THE HTML PART (The UI you see on your phone/browser) ---
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Music Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #121212; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px; }
        .container { max-width: 400px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h1 { color: #1DB954; font-size: 1.5em; }
        input { padding: 12px; width: 80%; border-radius: 25px; border: none; margin-bottom: 10px; outline: none; }
        button { padding: 10px 25px; background: #1DB954; color: white; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; }
        button:hover { background: #1ed760; }
        .footer { color: #666; font-size: 0.7em; margin-top: 20px; line-height: 1.5; }
        .status-ready { color: #1DB954; font-size: 0.9em; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ESP32 Music Brain</h1>
        <p class="status-ready">● Server is Live (Cookies Loaded)</p>
        <form action="/play" method="get">
            <input type="text" name="search" placeholder="Search song or artist..." required>
            <br>
            <button type="submit">Play Test</button>
        </form>
        <div class="footer">
            <p>ESP32 Endpoint: <br> <code>/play?search=SONGNAME</code></p>
            <p>Search Options: <br> <code>/search?q=SONGNAME</code></p>
        </div>
    </div>
</body>
</html>
'''

# --- THE LOGIC PART ---
YDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'nocheckcertificate': True,
    'cookiefile': 'cookies.txt', 
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query: return "Missing query", 400
    
    with yt_dlp.YoutubeDL({'quiet': True, 'default_search': 'ytsearch3', 'cookiefile': 'cookies.txt'}) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if info and 'entries' in info:
                # Filter out None and get titles
                titles = [e['title'][:30] for e in info['entries'] if e]
                return "|".join(titles)
            return "No results"
        except Exception as e:
            return f"Error: {str(e)}"

@app.route('/play')
def play():
    song_name = request.args.get('search')
    if not song_name: return "Missing song name", 400

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                first_result = info['entries'][0]
                if first_result and 'url' in first_result:
                    return redirect(first_result['url'])
            
            return "Could not find stream. Try a different name.", 404
        except Exception as e:
            return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

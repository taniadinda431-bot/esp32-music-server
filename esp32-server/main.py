from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

# Disguise the server as a mobile phone browser (they get blocked less!)
YDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'nocheckcertificate': True,
    'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
}

@app.route('/')
def index():
    return "<h1>Server is Up!</h1><p>Use /play?search=songname</p>"

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query: return "No query", 400
    
    with yt_dlp.YoutubeDL({'quiet': True, 'default_search': 'ytsearch3'}) as ydl:
        try:
            # Using a simplified extraction to avoid the NoneType error
            info = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if 'entries' in info and info['entries']:
                # Filter out any 'None' entries before grabbing titles
                titles = [e['title'][:30] for e in info['entries'] if e is not None]
                return "|".join(titles)
            return "No results found"
        except:
            return "Search failed"

@app.route('/play')
def play():
    song_name = request.args.get('search')
    if not song_name: return "No song name", 400

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        try:
            # The 'search' logic changed to be more robust
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                # Direct access with a safety check
                first_entry = info['entries'][0]
                if first_entry and 'url' in first_entry:
                    return redirect(first_entry['url'])
            
            return "YouTube blocked the link. Try again in 1 min.", 403
        except Exception as e:
            return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

# Disguise the server as a mobile phone browser (they get blocked less!)
YDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'nocheckcertificate': True,
    'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
}

@app.route('/')
def index():
    return "<h1>Server is Up!</h1><p>Use /play?search=songname</p>"

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query: return "No query", 400
    
    with yt_dlp.YoutubeDL({'quiet': True, 'default_search': 'ytsearch3'}) as ydl:
        try:
            # Using a simplified extraction to avoid the NoneType error
            info = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if 'entries' in info and info['entries']:
                # Filter out any 'None' entries before grabbing titles
                titles = [e['title'][:30] for e in info['entries'] if e is not None]
                return "|".join(titles)
            return "No results found"
        except:
            return "Search failed"

@app.route('/play')
def play():
    song_name = request.args.get('search')
    if not song_name: return "No song name", 400

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        try:
            # The 'search' logic changed to be more robust
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if info and 'entries' in info and len(info['entries']) > 0:
                # Direct access with a safety check
                first_entry = info['entries'][0]
                if first_entry and 'url' in first_entry:
                    return redirect(first_entry['url'])
            
            return "YouTube blocked the link. Try again in 1 min.", 403
        except Exception as e:
            return f"Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

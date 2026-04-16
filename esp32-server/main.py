from flask import Flask, request, redirect
import yt_dlp

app = Flask(__name__)

def get_yt_link(query):
    # Try multiple "identities" to fool the bot detector
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    ]
    
    for ua in user_agents:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'user_agent': ua,
            'extract_flat': False, # Force it to get the actual URL
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Force search specifically in YouTube Music
                search_query = f"ytsearch:{query} lyrics"
                info = ydl.extract_info(search_query, download=False)
                
                if info and 'entries' in info and len(info['entries']) > 0:
                    entry = info['entries'][0]
                    if entry and 'url' in entry:
                        return entry['url']
            except:
                continue # Try the next User Agent if this one fails
    return None

@app.route('/')
def home():
    return "Music Server Active"

@app.route('/play')
def play():
    song = request.args.get('search')
    if not song: return "Missing song name", 400
    
    link = get_yt_link(song)
    if link:
        return redirect(link)
    else:
        return "YouTube is blocking us. Try a different song name.", 403

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query: return "Missing query", 400
    
    # Simple search for titles
    with yt_dlp.YoutubeDL({'quiet': True, 'default_search': 'ytsearch3'}) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch3:{query}", download=False)
            titles = [e['title'][:30] for e in info['entries'] if e]
            return "|".join(titles)
        except:
            return "Search failed"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
import os

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Serve index.html as the homepage
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse('index.html')


# Endpoint to download a YouTube playlist
@app.post("/download/")
async def download_playlist(playlist_url: str = Form(...)):
    ydl_opts = {
        'format': 'best',  # Get the best available quality
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',  # Save files in a folder named after the playlist
    }

    try:
        # Use yt-dlp to download the playlist
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        return {"message": "Playlist download completed successfully!"}
    
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=f"Download Error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

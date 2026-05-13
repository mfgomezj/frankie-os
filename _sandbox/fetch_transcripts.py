import sys
from youtube_transcript_api import YouTubeTranscriptApi

video_ids = [
    "i4g2Po0S3G4",
    "8beheGoYTHM",
    "FyDAt4VeRiM",
    "TS2fRocN9zg",
    "CwPUOVUdApE"
]

api = YouTubeTranscriptApi()

for vid in video_ids:
    try:
        # Try Spanish first, then English
        transcript = api.fetch(vid, languages=['es', 'es-419', 'en'])
        text = " ".join([t['text'] for t in transcript])
        filepath = f"d:/Proyectos/PROYECTO_FUNNELSFOUNDRY.AI/_sandbox/{vid}.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Transcript OK: {vid}")
    except Exception as e:
        print(f"Error {vid}: {e}")

from youtube_transcript_api import YouTubeTranscriptApi
import json

video_ids = [
    "i4g2Po0S3G4",
    "8beheGoYTHM",
    "FyDAt4VeRiM",
    "TS2fRocN9zg",
    "CwPUOVUdApE"
]

for vid in video_ids:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['es', 'en', 'es-419'])
        text = " ".join([t['text'] for t in transcript])
        with open(f"d:/Proyectos/PROYECTO_FUNNELSFOUNDRY.AI/_sandbox/{vid}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"OK: {vid}")
    except Exception as e:
        print(f"Error {vid}: {e}")

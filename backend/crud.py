from datetime import datetime
from models import Video
from database import get_db
        
        
def get_all_videos():
    db = get_db()
    try:
        videos = db.query(Video).all()
        return [{
            "id": video.video_id,
            "title": video.title if video.title else None
        } for video in videos]
    
    finally:
        db.close()
        
def save_video_history(video_id, title):
    db = get_db()
    try:
        video = db.query(Video).filter(Video.video_id == video_id).first()
        
        if not video:
            video = Video(video_id = video_id, title = title)
            db.add(video)
            db.commit()
    finally:
        db.close()
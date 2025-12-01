from datetime import datetime
from models import Video, Message
from database import get_db

def save_message_pair(video_id, user_text, bot_text):
    db = get_db()
    
    try:
        video = db.query(Video).filter(Video.video_id == video_id).first()
        
        if not video:
            video = Video(video_id = video_id, title = None)
            db.add(video)
            db.commit()
        
        user_msg = Message(
            sender = "user",
            text = user_text,
            video_id = video_id,
            timestamp = datetime.utcnow().isoformat()
        )
        bot_msg = Message(
            sender = "bot",
            text = user_text,
            video_id = video_id,
            timestamp = datetime.utcnow().isoformat()
        )
        db.add(user_msg)
        db.add(bot_msg)
        db.commit()
        
    except Exception as e: 
        raise e
    finally:
        db.close()
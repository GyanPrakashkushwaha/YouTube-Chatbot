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
            text = bot_text,
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
        
        
def get_chat_history(video_id):
    db = get_db()
    try:
        messages = db.query(Message).filter(Message.video_id == video_id).order_by(Message.id.asc()).all()
        # print(messages)
        
        messages_lst = [{
            "sender": msg.sender,
            "text": msg.text,
            "timestamp": msg.timestamp
        } for msg in messages]
        
        return messages_lst
    finally:
        db.close()
        
        
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
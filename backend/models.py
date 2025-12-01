from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Video(Base):
    __tablename__ = "videos"
    video_id = Column(String, primary_key=True, index=True)
    title = Column(String(250))
    messages = relationship("Message", back_populates="video", cascade="all, delete")
    
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index= True)
    sender = Column(String)
    text = Column(String)
    timestamp = Column(String, default=lambda: datetime.utcnow().isoformat())
    video_id = Column(String, ForeignKey('videos.video_id'))
    video = relationship("Video", back_populates="messages")
    

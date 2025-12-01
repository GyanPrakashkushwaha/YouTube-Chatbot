from database import get_db
from models import Message

db = get_db()
msgs = db.query(Message).all()

for m in msgs:
    print(m.id, m.video_id, m.sender, m.text[:50])

from app.core.database import Base, engine
from app.models.user import User
from app.services.request_logger import LLMRequest


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
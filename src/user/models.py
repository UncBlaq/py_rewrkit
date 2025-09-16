from sqlalchemy import (
    Column, String, Text, Boolean, Date, TIMESTAMP,
    Integer, CheckConstraint, func, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(50), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False)
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'business', 'general')", name="check_role"),
    )

    bio = Column(Text, default='Stacked up!')
    date_of_birth = Column(Date)

    is_active = Column(Boolean, default=True)
    last_login_at = Column(TIMESTAMP)

    location = Column(String(255), nullable=False, default='Worldwide')

    industry = Column(ARRAY(String(100)), nullable=False, default=['Developer'])
    skills = Column(ARRAY(Text), nullable=False, default=['plumbing'])
    interests = Column(ARRAY(Text))  # optional
    tags = Column(Text)

    profile_picture = Column(String(255))
    website = Column(String(255))
    phone = Column(String(20))
    social_links = Column(Text)

    is_verified = Column(Boolean, default=False)

    # Vector column for semantic search (pgvector 384-dim)
    embedding = Column(Vector(384))

    # Social & engagement features
    following_user_ids = Column(ARRAY(UUID(as_uuid=True)))
    following_community_ids = Column(ARRAY(UUID(as_uuid=True)))
    bookmarked_job_ids = Column(ARRAY(Integer))

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())



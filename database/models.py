from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


def serialize_datetime(value):
    if not value:
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat(sep=" ", timespec="seconds")

    return str(value)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(40), nullable=False, default="user", index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), index=True)

    diagnoses = relationship("Diagnosis", back_populates="user")
    activities = relationship("Activity", back_populates="user")

    def to_dict(self, include_password=False):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": serialize_datetime(self.created_at),
        }

        if include_password:
            data["password_hash"] = self.password_hash

        return data


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    disease = Column(String(160), nullable=False, index=True)
    confidence = Column(Integer, nullable=True)
    symptoms = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), index=True)

    user = relationship("User", back_populates="diagnoses")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "disease": self.disease,
            "confidence": self.confidence,
            "symptoms": self.symptoms,
            "created_at": serialize_datetime(self.created_at),
        }


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    event_type = Column(String(120), nullable=False, index=True)
    details = Column(Text, nullable=True)
    path = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), index=True)

    user = relationship("User", back_populates="activities")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "details": self.details,
            "path": self.path,
            "created_at": serialize_datetime(self.created_at),
        }

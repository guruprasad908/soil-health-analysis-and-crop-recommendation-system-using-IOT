from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, index=True)
    phone = Column(String, index=True)
    location = Column(String)
    land_size = Column(Float)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    ph = Column(Float)
    rainfall = Column(Float)
    soil_type = Column(String)
    predicted_crop = Column(String)
    model_used = Column(String)  # Which ML model was used
    confidence = Column(Float)  # Prediction confidence score
    soil_health_score = Column(Float)  # Overall soil health score
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class NPKReading(Base):
    """Database model for storing NPK sensor readings"""
    __tablename__ = "npk_readings"

    id = Column(Integer, primary_key=True, index=True)
    n = Column(Integer)  # Nitrogen level
    p = Column(Integer)  # Phosphorus level
    k = Column(Integer)  # Potassium level
    device_id = Column(String, default="ESP8266", index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class UNOReading(Base):
    """Database model for storing Arduino UNO sensor readings (Temp, Humidity, Moisture)"""
    __tablename__ = "uno_readings"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)  # Temperature in Celsius
    humidity = Column(Float)     # Humidity in %
    moisture = Column(Integer)   # Soil Moisture in %
    device_id = Column(String, default="ArduinoUNO", index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
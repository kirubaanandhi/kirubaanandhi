import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_FILE = "fitbuddy.db"
# Ensure database path is in project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, DATABASE_FILE)
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(150), nullable=False)
    intensity = Column(String(50), nullable=False)
    schedule = Column(Integer, default=7)


class WorkoutPlan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)


# Create tables on import
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(id=user_id).first()
        if existing:
            # Update existing user info
            existing.name = name
            existing.age = age
            existing.weight = weight
            existing.goal = goal
            existing.intensity = intensity
        else:
            # Create a new user
            user = User(
                id=user_id,
                name=name,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                schedule=7  # default schedule or logic
            )
            db.add(user)
        db.commit()
    finally:
        db.close()


def save_plan(user_id: int, plan: str):
    """Stores or updates the initial original plan in the database."""
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if workout:
            workout.original_plan = plan
            # Reset updated plan if a brand new original plan is generated
            workout.updated_plan = None
        else:
            workout = WorkoutPlan(user_id=user_id, original_plan=plan)
            db.add(workout)
        db.commit()
    finally:
        db.close()


def update_plan(user_id: int, updated_text: str):
    """Update plan based on feedback."""
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if workout:
            workout.updated_plan = updated_text
            db.commit()
    finally:
        db.close()


def get_original_plan(user_id: int):
    """Fetch the original plan for a user."""
    db = SessionLocal()
    try:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return plan.original_plan if plan else None
    finally:
        db.close()


def get_workout_plan(user_id: int):
    """Fetch the full plan record for a user."""
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    finally:
        db.close()


def get_user(user_id: int):
    """Fetch user by id."""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def get_all_users():
    """Fetch all registered users."""
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


def get_all_plans():
    """Fetch all workout plans."""
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).all()
    finally:
        db.close()


def delete_user_and_plan(user_id: int) -> bool:
    """Delete a user and their associated plans."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if user:
            db.delete(user)
        if plan:
            db.delete(plan)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

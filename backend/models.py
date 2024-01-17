from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)
    type = db.Column(db.String(10))


class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(100))
    nightly_price = db.Column(db.Float)
    duration = db.Column(db.Integer)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    capacity = db.Column(db.Integer)


class Transportation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transport_type = db.Column(db.String(50))
    price = db.Column(db.Float)
    departure_date = db.Column(db.Date)
    departure_time = db.Column(db.Time)


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attraction_name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    ticket_price = db.Column(db.Float)


travelers_travel_plans = db.Table(
    "travelers_travel_plans",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "travel_plan_id", db.Integer, db.ForeignKey("travel_plan.id"), primary_key=True
    ),
)


class TravelPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    accommodation_id = db.Column(db.Integer, db.ForeignKey("accommodation.id"))
    transportation_id = db.Column(db.Integer, db.ForeignKey("transportation.id"))
    attraction_id = db.Column(db.Integer, db.ForeignKey("attraction.id"))
    budget_amount = db.Column(db.Float)
    # travelers = db.relationship(
    #     "Users", secondary=travelers_travel_plans, backref="travel_plans"
    # )
    accommodation = db.relationship("Accommodation")
    transportation = db.relationship("Transportation")
    attraction = db.relationship("Attraction")

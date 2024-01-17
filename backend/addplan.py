from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from models import db, TravelPlan, Accommodation, Transportation, Attraction

addplan = Blueprint("addplan", __name__, template_folder="../frontend")


@addplan.route("/addplan", methods=["GET", "POST"])
@login_required
def add_travel_plan():
    user_travel_plans = TravelPlan.query.all()
    editid = request.args.get("edit")
    edit_travel_plan = None

    if editid:
        travel_plan = TravelPlan.query.get(editid)
        accommodation_name = (
            Accommodation.query.get(travel_plan.accommodation_id).hotel_name
            if travel_plan.accommodation_id
            else "N/A"
        )
        transportation_type = (
            Transportation.query.get(travel_plan.transportation_id).transport_type
            if travel_plan.transportation_id
            else "N/A"
        )
        attraction_name = (
            Attraction.query.get(travel_plan.attraction_id).attraction_name
            if travel_plan.attraction_id
            else "N/A"
        )
        edit_travel_plan = {
            "id": travel_plan.id,
            "accommodation": accommodation_name,
            "transportation": transportation_type,
            "attraction": attraction_name,
            "budget_amount": travel_plan.budget_amount,
        }

    if request.method == "POST":
        travel_plan_id = request.form.get("travel_plan_id")
        if travel_plan_id:
            travel_plan = TravelPlan.query.get(travel_plan_id)
            if travel_plan:
                accommodation_name = request.form.get("accommodation")
                transportation_type = request.form.get("transportation")
                attraction_name = request.form.get("attraction")
                budget_amount = float(request.form.get("budget_amount"))

                accommodation = Accommodation.query.filter_by(
                    hotel_name=accommodation_name
                ).first()
                if not accommodation:
                    accommodation = Accommodation(hotel_name=accommodation_name)
                    db.session.add(accommodation)
                    db.session.commit()

                transportation = Transportation.query.filter_by(
                    transport_type=transportation_type
                ).first()
                if not transportation:
                    transportation = Transportation(transport_type=transportation_type)
                    db.session.add(transportation)
                    db.session.commit()

                attraction = Attraction.query.filter_by(
                    attraction_name=attraction_name
                ).first()
                if not attraction:
                    attraction = Attraction(attraction_name=attraction_name)
                    db.session.add(attraction)
                    db.session.commit()

                travel_plan.accommodation_id = (
                    Accommodation.query.filter_by(hotel_name=accommodation_name)
                    .first()
                    .id
                )
                travel_plan.transportation_id = (
                    Transportation.query.filter_by(transport_type=transportation_type)
                    .first()
                    .id
                )
                travel_plan.attraction_id = (
                    Attraction.query.filter_by(attraction_name=attraction_name)
                    .first()
                    .id
                )
                travel_plan.budget_amount = budget_amount

                db.session.commit()
                flash("旅行計劃已成功更新!", "success")
                return redirect("addplan")

        else:
            accommodation_name = request.form.get("accommodation")
            transportation_type = request.form.get("transportation")
            attraction_name = request.form.get("attraction")
            budget_amount = float(request.form.get("budget_amount"))

            accommodation = Accommodation.query.filter_by(
                hotel_name=accommodation_name
            ).first()
            if not accommodation:
                accommodation = Accommodation(hotel_name=accommodation_name)
                db.session.add(accommodation)
                db.session.commit()

            transportation = Transportation.query.filter_by(
                transport_type=transportation_type
            ).first()
            if not transportation:
                transportation = Transportation(transport_type=transportation_type)
                db.session.add(transportation)
                db.session.commit()

            attraction = Attraction.query.filter_by(
                attraction_name=attraction_name
            ).first()
            if not attraction:
                attraction = Attraction(attraction_name=attraction_name)
                db.session.add(attraction)
                db.session.commit()

            if (
                accommodation
                and transportation
                and attraction
                and isinstance(budget_amount, float)
            ):
                new_travel_plan = TravelPlan(
                    user_id=current_user.id,
                    accommodation_id=accommodation.id,
                    transportation_id=transportation.id,
                    attraction_id=attraction.id,
                    budget_amount=budget_amount,
                )

                db.session.add(new_travel_plan)
                db.session.commit()

                flash("旅行計劃已成功添加!", "success")
                return redirect("addplan")

    complete_travel_plans = []
    for travel_plan in user_travel_plans:
        accommodation_name = (
            Accommodation.query.get(travel_plan.accommodation_id).hotel_name
            if travel_plan.accommodation_id
            else "N/A"
        )
        transportation_type = (
            Transportation.query.get(travel_plan.transportation_id).transport_type
            if travel_plan.transportation_id
            else "N/A"
        )
        attraction_name = (
            Attraction.query.get(travel_plan.attraction_id).attraction_name
            if travel_plan.attraction_id
            else "N/A"
        )

        complete_travel_plans.append(
            {
                "id": travel_plan.id,
                "accommodation": accommodation_name,
                "transportation": transportation_type,
                "attraction": attraction_name,
                "budget_amount": travel_plan.budget_amount,
            }
        )

    return render_template(
        "addplan.html",
        travel_plans=complete_travel_plans,
        edit_travel_plan=edit_travel_plan,
    )


@addplan.route("/delete/<int:travel_plan_id>", methods=["GET"])
@login_required
def delete_travel_plan(travel_plan_id):
    travel_plan = TravelPlan.query.get(travel_plan_id)
    if travel_plan:
        db.session.delete(travel_plan)
        db.session.commit()
        flash("旅行計劃已成功刪除!", "success")

    return redirect("/addplan")

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user


from .models import Transfer
from .forms import TransferForm
from . import db

transfer = Blueprint("transfer", __name__, url_prefix="/transfer")


@transfer.get("/list")
@login_required
def list():
    transfers = Transfer.query.filter_by(user_id=current_user.id).all()
    return render_template("transfer_list.html", transfers=transfers)


@transfer.get("/<int:transfer_id>")
@login_required
def one_transfer(transfer_id):
    transfer = Transfer.query.filter_by(user_id=current_user.id, id=transfer_id).first()
    if not transfer:
        return "Forbidden"
    return render_template("transfer_one.html", transfer=transfer)


@transfer.route("/new", methods=("GET", "POST"))
@login_required
def new():
    form = TransferForm()
    if form.validate_on_submit():
        new_transfer = Transfer(
            title=form.title.data,
            date=form.date.data,
            amount=form.amount.data,
            iban=form.iban.data,
            user_id=current_user.id,
        )

        # add the new user to the database
        db.session.add(new_transfer)
        db.session.commit()

        return redirect(url_for("transfer.list"))

    return render_template("transfer_new.html", form=form)

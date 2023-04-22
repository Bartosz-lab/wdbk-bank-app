from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user


from .models import Transfer, TransferToConfirm
from .forms import TransferForm, TransferConfirmForm
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
        transfer = TransferToConfirm(
            title=form.title.data,
            date=form.date.data,
            amount=form.amount.data,
            iban=form.iban.data,
            user_id=current_user.id,
        )

        db.session.add(transfer)
        db.session.commit()

        return redirect(url_for("transfer.confirm", confirm_id=transfer.id))

    return render_template("transfer_new.html", form=form)


@transfer.route("/confirm/<int:confirm_id>", methods=("GET", "POST"))
@login_required
def confirm(confirm_id):
    form = TransferConfirmForm()
    transfer = TransferToConfirm.query.filter_by(
        user_id=current_user.id, id=confirm_id
    ).first()

    if not transfer:
        return "Forbiden"

    if form.validate_on_submit():
        confirmed_transfer = Transfer(
            title=transfer.title,
            date=transfer.date,
            amount=transfer.amount,
            iban=transfer.iban,
            user_id=current_user.id,
        )

        db.session.add(confirmed_transfer)
        db.session.delete(transfer)
        db.session.commit()
        return redirect(
            url_for("transfer.one_transfer", transfer_id=confirmed_transfer.id)
        )

    return render_template("transfer_confirm.html", transfer=transfer, form=form)


@transfer.post("/reject/<int:reject_id>")
@login_required
def reject(reject_id):
    transfer = TransferToConfirm.query.filter_by(
        user_id=current_user.id, id=reject_id
    ).first()
    if not transfer:
        return "Forbiden"

    db.session.delete(transfer)
    db.session.commit()
    return render_template("transfer_reject.html", transfer=transfer)

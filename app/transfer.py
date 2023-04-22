from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime, timedelta


from .models import Transfer, TransferToConfirm
from .forms import TransferForm, TransferConfirmForm
from . import db, scheduler

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
        return abort(403)
    return render_template("transfer_one.html", transfer=transfer)


def remove_unconfirmed(transfer_id):
    with scheduler.app.app_context():
        transfer = TransferToConfirm.query.filter_by(id=transfer_id).first()
        db.session.delete(transfer)
        db.session.commit()
    print("WYKONANO", transfer_id)


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
            task_id=str(datetime.now().timestamp()),
        )

        db.session.add(transfer)
        db.session.commit()

        scheduler.add_job(
            func=remove_unconfirmed,
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=30),
            args=[transfer.id],
            id=transfer.task_id,
        )

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
        return abort(403)

    if form.validate_on_submit():
        task_id = transfer.task_id
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

        try:
            scheduler.delete_job(task_id)
        except:
            pass

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
        return abort(403)
    task_id = transfer.task_id

    db.session.delete(transfer)
    db.session.commit()

    try:
        scheduler.delete_job(task_id)
    except:
        pass

    return render_template("transfer_reject.html", transfer=transfer)

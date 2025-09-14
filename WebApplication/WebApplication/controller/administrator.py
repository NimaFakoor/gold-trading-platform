from .packages import *

def login_administrator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("administrator"):
            flash("لطفا وارد حساب خود شوید")
            return redirect(url_for("signin"))
        return f(*args, **kwargs)
    return decorated_function
###
@app.route("/administrator/pricing", methods=["GET", "POST"])
@login_administrator_required
def administrator_pricing():
    """administrator_pricing"""
    if not session.get("logged_in"):
        abort(401)
    pricing()
    if request.method == "POST":

        BuyGram = request.form["BuyGram"]
        SellGram = request.form["SellGram"]

        bp = BuyPrice(amount = float(BuyGram.replace(",", "")), registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(bp)
        db.session.commit()
        
        sp = SellPrice(amount = float(SellGram.replace(",", "")), registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(sp)
        db.session.commit()
        
        flash("قیمت‌گذاری جدید با موفقیت ثبت شد")

        return redirect(url_for("administrator_pricing"))

    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()

    return render_template("administrator/pricing.html" , last_bp=last_bp, last_sp=last_sp,  title='pricing')
##
@app.route("/administrator/users", methods=["GET", "POST"])
@login_administrator_required
def administrator_users():
    """administrator_users"""
    if not session.get("logged_in"):
        abort(401)

    users = User.query.filter_by(role="trader").order_by(User.id.desc()).all()
    return render_template("administrator/users.html" , float=float, format_currency=format_currency, users=users, title='users')
##
@app.route("/administrator/users_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_users_verification():
    """administrator_users_verification"""
    if not session.get("logged_in"):
        abort(401)

    users = User.query.filter_by(role="trader").order_by(User.id.desc()).all()
    return render_template("administrator/users_verification.html" , users=users, title='users_verification')
#
@app.route("/administrator/user_verify/<sid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_user_verify(sid):
    """administrator_user_verify"""
    if not session.get("logged_in"):
        abort(401)

    user = User.query.filter_by(id=sid).first()
    user.verification_status = "تأیید شده"
    db.session.commit()
    db.session.close()
    flash("کاربر تأیید شده")
    return redirect(url_for("administrator_users_verification"))
##
@app.route("/administrator/deposit_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_deposit_verification():
    """administrator_deposit_verification"""
    if not session.get("logged_in"):
        abort(401)

    trs = Transactions.query.filter_by(transactions_type="واریز").order_by(Transactions.id.desc()).all()
    return render_template("administrator/deposit_verification.html" , float=float, format_currency=format_currency, trs=trs, title='deposit_verification')
#
@app.route("/administrator/deposit_verify/<sid>/<uid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_deposit_verify(sid,uid):
    """administrator_deposit_verify"""
    if not session.get("logged_in"):
        abort(401)

    tr = Transactions.query.filter_by(id=sid).first()
    tr.status = "تأیید شده"
    amount = tr.amount
    db.session.commit()
    db.session.close()
    user = User.query.filter_by(id=uid).first()
    user.credit = float(user.credit) + float(amount)
    db.session.commit()
    db.session.close()
  
    flash("تراکنش تأیید شده")
    return redirect(url_for("administrator_deposit_verification"))
##
@app.route("/administrator/withdrawal_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_withdrawal_verification():
    """administrator_withdrawal_verification"""
    if not session.get("logged_in"):
        abort(401)

    trs = Transactions.query.filter_by(transactions_type="برداشت").order_by(Transactions.id.desc()).all()
    return render_template("administrator/withdrawal_verification.html" , float=float, format_currency=format_currency, trs=trs, title='withdrawal_verification')
#
@app.route("/administrator/withdrawal_verify/<sid>/<uid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_withdrawal_verify(sid,uid):
    """administrator_withdrawal_verify"""
    if not session.get("logged_in"):
        abort(401)

    tr = Transactions.query.filter_by(id=sid).first()
    tr.status = "تأیید شده"
    amount = tr.amount
    db.session.commit()
    db.session.close()
    user = User.query.filter_by(id=uid).first()
    user.credit = float(user.credit) - float(amount)
    db.session.commit()
    db.session.close()
  
    flash("تراکنش تأیید شده")
    return redirect(url_for("administrator_withdrawal_verification"))
##
@app.route("/administrator/buy_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_buy_verification():
    """administrator_buy_verification"""
    if not session.get("logged_in"):
        abort(401)

    trs = Transactions.query.filter_by(transactions_type="خرید").order_by(Transactions.id.desc()).all()
    return render_template("administrator/buy_verification.html" , float=float, convert_gram_mithqal=convert_gram_mithqal, format_currency=format_currency, trs=trs, title='buy_verification')
#
@app.route("/administrator/buy_verify/<sid>/<uid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_buy_verify(sid,uid):
    """administrator_buy_verify"""
    if not session.get("logged_in"):
        abort(401)

    tr = Transactions.query.filter_by(id=sid).first()
    tr.status = "تأیید شده"
    amount = tr.amount
    weight = tr.weight
    db.session.commit()
    db.session.close()
    user = User.query.filter_by(id=uid).first()
    user.credit = float(user.credit) - float(amount)
    user.assets = float(user.assets) + float(weight)
    db.session.commit()
    db.session.close()
  
    flash("تراکنش تأیید شده")
    return redirect(url_for("administrator_buy_verification"))
##
@app.route("/administrator/sell_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_sell_verification():
    """administrator_sell_verification"""
    if not session.get("logged_in"):
        abort(401)

    trs = Transactions.query.filter_by(transactions_type="فروش").order_by(Transactions.id.desc()).all()
    return render_template("administrator/sell_verification.html" , float=float, convert_gram_mithqal=convert_gram_mithqal, format_currency=format_currency, trs=trs, title='sell_verification')
#
@app.route("/administrator/sell_verify/<sid>/<uid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_sell_verify(sid,uid):
    """administrator_sell_verify"""
    if not session.get("logged_in"):
        abort(401)

    tr = Transactions.query.filter_by(id=sid).first()
    tr.status = "تأیید شده"
    amount = tr.amount
    weight = tr.weight
    db.session.commit()
    db.session.close()
    user = User.query.filter_by(id=uid).first()
    user.credit = float(user.credit) + float(amount)
    user.assets = float(user.assets) - float(weight)
    db.session.commit()
    db.session.close()
  
    flash("تراکنش تأیید شده")
    return redirect(url_for("administrator_sell_verification"))
##
@app.route("/administrator/gold_deposit_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_gold_deposit_verification():
    """administrator_gold_deposit_verification"""
    if not session.get("logged_in"):
        abort(401)

    trs = Transactions.query.filter_by(transactions_type="واریز طلا").order_by(Transactions.id.desc()).all()
    return render_template("administrator/gold_deposit_verification.html" , float=float, format_currency=format_currency, trs=trs, title='deposit_verification')
#
@app.route("/administrator/gold_deposit_verify/<sid>/<uid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_gold_deposit_verify(sid,uid):
    """administrator_gold_deposit_verify"""
    if not session.get("logged_in"):
        abort(401)

    tr = Transactions.query.filter_by(id=sid).first()
    tr.status = "تأیید شده"
    weight = tr.weight
    db.session.commit()
    db.session.close()
    user = User.query.filter_by(id=uid).first()
    user.assets = float(user.assets) + float(weight)
    db.session.commit()
    db.session.close()
  
    flash("تراکنش تأیید شده")
    return redirect(url_for("administrator_gold_deposit_verification"))
####
@app.route("/administrator/gold_withdrawal_verification", methods=["GET", "POST"])
@login_administrator_required
def administrator_gold_withdrawal_verification():
    """administrator_gold_withdrawal_verification"""
    if not session.get("logged_in"):
        abort(401)

    trs = Transactions.query.filter_by(transactions_type="برداشت طلا").order_by(Transactions.id.desc()).all()
    return render_template("administrator/gold_withdrawal_verification.html" , float=float, format_currency=format_currency, trs=trs, title='withdrawal_verification')
#
@app.route("/administrator/gold_withdrawal_verify/<sid>/<uid>", methods=["GET", "POST"])
@login_administrator_required
def administrator_gold_withdrawal_verify(sid,uid):
    """administrator_gold_withdrawal_verify"""
    if not session.get("logged_in"):
        abort(401)

    tr = Transactions.query.filter_by(id=sid).first()
    tr.status = "تأیید شده"
    weight = tr.weight
    db.session.commit()
    db.session.close()
    user = User.query.filter_by(id=uid).first()
    user.assets = float(user.assets) - float(weight)
    db.session.commit()
    db.session.close()
  
    flash("تراکنش تأیید شده")
    return redirect(url_for("administrator_gold_withdrawal_verification"))
##
@app.route("/administrator/transactions", methods=["GET", "POST"])
@login_administrator_required
def administrator_transactions():
    """administrator_transactions"""
    if not session.get("logged_in"):
        abort(401)
    transactions = Transactions.query.order_by(Transactions.id.desc()).all()
    return render_template("administrator/transactions.html" , float=float, convert_gram_mithqal=convert_gram_mithqal, format_currency=format_currency, transactions=transactions, title='transactions')
##
@app.route("/administrator/messages", methods=["GET", "POST"])
@login_administrator_required
def administrator_messages():
    """administrator_messages"""
    if not session.get("logged_in"):
        abort(401)
    messages = Messages.query.order_by(Messages.id.desc()).all()
    return render_template("administrator/messages.html" , messages=messages, title='messages')
##
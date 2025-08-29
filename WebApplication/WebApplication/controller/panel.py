from .packages import *

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("trader"):
            flash("لطفا وارد حساب خود شوید")
            return redirect(url_for("signin"))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/panel/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """dashboard"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))



    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()

    user = User.query.filter_by(id=session["user_id"]).first()

    return render_template("panel/index.html" , float=float, format_currency=format_currency, last_bp=last_bp, last_sp=last_sp, user=user, title='dashboard')

@app.route("/panel/profile", methods=["GET", "POST"])
@login_required
def profile():
    """profile"""
    if not session.get("logged_in"):
        abort(401)

    user = User.query.filter_by(id=session["user_id"]).first()
    
    if request.method == "POST":

        first_and_last_name = request.form["first_and_last_name"]
        international_bank_account_number = request.form["international_bank_account_number"]
        bank_card_number = request.form["bank_card_number"]

        user = User.query.filter_by(id=session["user_id"]).first()
        
        user.first_and_last_name = first_and_last_name
        user.international_bank_account_number = international_bank_account_number
        user.bank_card_number = bank_card_number
        db.session.commit()
        db.session.close()
        
        session["first_and_last_name"] = first_and_last_name

        flash("مشخصات شما با موفقیت ثبت شد")
        flash("مشخصات شما بررسی و وضعیت حساب شما تأیید خواهد شد")

        return redirect(url_for("dashboard"))

    return render_template("panel/profile.html" ,user=user , title='profile')

@app.route("/panel/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """deposit"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        amount = request.form["amount"]

        tr = Transactions(user_id = session["user_id"], user_phone = session["user_phone"], user_name = session["first_and_last_name"],
                           transactions_type = "واریز", amount = float(amount.replace(",", "")), weight=0, gold_rate=0, description="", content="", status="تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(tr)
        db.session.commit()
        
        flash("درخواست واریز شما با موفقیت ثبت شد")
        flash("واریز شما بررسی و بعد از تأیید در حساب شما اعمال خواهد شد")

        return redirect(url_for("transactions"))

    return render_template("panel/deposit.html" , title='deposit')

@app.route("/panel/withdrawal", methods=["GET", "POST"])
@login_required
def withdrawal():
    """withdrawal"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        amount = request.form["amount"]

        tr = Transactions(user_id = session["user_id"], user_phone = session["user_phone"], user_name = session["first_and_last_name"],
                           transactions_type = "برداشت", amount = float(amount.replace(",", "")), weight=0, gold_rate=0, description="", content="", status="تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(tr)
        db.session.commit()
        
        flash("درخواست برداشت شما با موفقیت ثبت شد")
        flash("برداشت شما بررسی و بعد از تأیید از در حساب شما اعمال خواهد شد")

        return redirect(url_for("transactions"))

    return render_template("panel/withdrawal.html" , title='withdrawal')

@app.route("/panel/gold_deposit", methods=["GET", "POST"])
@login_required
def gold_deposit():
    """gold_deposit"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))


    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()


    if request.method == "POST":

        weight = request.form["weight"]
        gold_rate = last_bp.amount

        tr = Transactions(user_id = session["user_id"], user_phone = session["user_phone"], user_name = session["first_and_last_name"],
                           transactions_type = "واریز طلا", amount = 0, weight=float(weight.replace(",", "")), gold_rate=gold_rate, description="", content="", status="تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(tr)
        db.session.commit()
        
        flash("درخواست واریز طلا شما با موفقیت ثبت شد")
        flash("واریز طلا شما بررسی و بعد از تأیید در حساب شما اعمال خواهد شد")

        return redirect(url_for("transactions"))

    return render_template("panel/gold_deposit.html" ,last_bp=last_bp ,last_sp=last_sp , title='gold_deposit')

@app.route("/panel/gold_withdrawal", methods=["GET", "POST"])
@login_required
def gold_withdrawal():
    """gold_withdrawal"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))


    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()


    if request.method == "POST":

        weight = request.form["weight"]
        gold_rate = last_bp.amount

        tr = Transactions(user_id = session["user_id"], user_phone = session["user_phone"], user_name = session["first_and_last_name"],
                           transactions_type = "برداشت طلا", amount = 0, weight=float(weight.replace(",", "")), gold_rate=gold_rate, description="", content="", status="تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(tr)
        db.session.commit()
        
        flash("درخواست برداشت طلا شما با موفقیت ثبت شد")
        flash("برداشت طلا شما بررسی و بعد از تأیید در حساب شما اعمال خواهد شد")

        return redirect(url_for("transactions"))

    return render_template("panel/gold_withdrawal.html" ,last_bp=last_bp ,last_sp=last_sp , title='gold_withdrawal')

@app.route("/panel/buy", methods=["GET", "POST"])
@login_required
def buy():
    """buy"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))


    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()


    if request.method == "POST":

        amount = request.form["amount"]
        weight = request.form["weight"]
        gold_rate = last_bp.amount

        tr = Transactions(user_id = session["user_id"], user_phone = session["user_phone"], user_name = session["first_and_last_name"],
                           transactions_type = "خرید", amount = float(amount.replace(",", "")), weight=float(weight.replace(",", "")), gold_rate=gold_rate, description="", content="", status="تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(tr)
        db.session.commit()
        
        flash("درخواست خرید شما با موفقیت ثبت شد")
        flash("خرید شما بررسی و بعد از تأیید در حساب شما اعمال خواهد شد")

        return redirect(url_for("transactions"))

    return render_template("panel/buy.html" ,last_bp=last_bp ,last_sp=last_sp , title='buy')

@app.route("/panel/sell", methods=["GET", "POST"])
@login_required
def sell():
    """sell"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))


    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()


    if request.method == "POST":

        amount = request.form["amount"]
        weight = request.form["weight"]
        gold_rate = last_bp.amount

        tr = Transactions(user_id = session["user_id"], user_phone = session["user_phone"], user_name = session["first_and_last_name"],
                           transactions_type = "فروش", amount = float(amount.replace(",", "")), weight=float(weight.replace(",", "")), gold_rate=gold_rate, description="", content="", status="تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
        db.session.add(tr)
        db.session.commit()
        
        flash("درخواست فروش شما با موفقیت ثبت شد")
        flash("فروش شما بررسی و بعد از تأیید در حساب شما اعمال خواهد شد")

        return redirect(url_for("transactions"))

    return render_template("panel/sell.html" ,last_bp=last_bp ,last_sp=last_sp , title='sell')

@app.route("/panel/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    """transactions"""
    if not session.get("logged_in"):
        abort(401)
    if session["first_and_last_name"] == "":
        flash("لطفا مشخصات خود را تکمیل کنید")
        return redirect(url_for("profile"))
    if session["verification_status"] != "تأیید شده":
        flash("حساب شما تأیید نشده، لطفا صبر کنید")
        return redirect(url_for("dashboard"))


    transactions = Transactions.query.filter_by(user_id=session["user_id"]).order_by(Transactions.id.desc()).all()

    return render_template("panel/transactions.html", float=float, convert_gram_mithqal=convert_gram_mithqal, format_currency=format_currency, transactions=transactions, title='transactions')

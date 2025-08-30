from .packages import *

@app.route("/signup", methods=('GET', 'POST'))
def signup():

    if request.method == "POST":

        phone = request.form["phone"]
        password = request.form["password"]
        retypeـpassword = request.form["retypeـpassword"]

        terms = True
        # if request.form.get("terms"):
        #     terms = True
        # else:
        #     terms = False

        error1 = None
        error2 = None
        error3 = None
        error4 = None
        error5 = "There was a problem, please try again."

        if terms == True :
            if phone == "" or password == "" :
                error2 = 'Please enter your phone and password.'
            else :
                if password==retypeـpassword :
                    users = User.query.all()
                    for singleUser in users:
                        if singleUser.phone == phone:
                            error4 = 'کاربری با این شماره وجود دارد شماره دیگری استفاده کنید'
                else :
                    error3 = "پسورد و تکرار پسورد یکسان نیست"
        else :
            error1 = "Acceptance of terms and conditions is required for registration."
        
        if error1 is None and error2 is None and error3 is None and error4 is None:
            user = User(phone = phone, password = generate_password_hash(password), role = "trader", credit = 0, assets = 0, first_and_last_name="", international_bank_account_number="", bank_card_number="", verification_status = "تأیید نشده", registration = str(jdatetime.datetime.now())[0:19])
            db.session.add(user)
            db.session.commit()
            flash("ثبت نام با موفقیت انجام شد")
            return redirect(url_for("signin"))
        elif error1!= None :
            flash(error1)
        elif error2!= None :
            flash(error2)
        elif error3!= None :
            flash(error3)
        elif error4!= None :
            flash(error4)
        else :
            flash(error5)

    return render_template("authentication/signup.html", title='register')

@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Renders the login page."""

    if request.method == "POST":

        phone = request.form["phone"]
        password = request.form["password"]

        error1 = None
        error2 = None

        if phone == "" or password == "" :

            error2 = 'Please enter your phone and password'
            flash(error2)

        user = User.query.filter_by(phone=phone).first()

        if error2 is None:

            if user is None:
                error1 = "همراه اشتباه وارد شده"
            elif not user.check_password(password):
                error1 = "پسورد اشتباه وارد شده"

            if error1 is None:
                session.clear()
                session["logged_in"] = True
                session["user_id"] = user.id
                session["user_role"] = user.role
                session["user_phone"] = user.phone
                session["first_and_last_name"] = user.first_and_last_name
                session["verification_status"] = user.verification_status
                
                if session["user_role"] == "trader":
                    session["trader"] = True
                    return redirect(url_for("dashboard"))
                elif session["user_role"] == "administrator":
                    session["administrator"] = True
                    return redirect(url_for("administrator_pricing"))

            flash(error1)

    return render_template(
        "authentication/signin.html",
        title='login'
    )

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Renders the reset password page."""

    if request.method == "POST":

        phone = request.form["phone"]

        code = str(random.randint(100000, 999999))
        
        url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
        apikey = "OWZiZmUzNzgtYThjYS00N2NjLTkxMTYtODFmMDAzMTY1NmQxNzhhNDc1ZmUxZTFiYmM3M2RjZTRhNGY5YTkxMDg1NmY="
        payload = json.dumps({
        "code": "1762l6p6tvmm1dy",
        "sender": "+983000505",
        "recipient": phone,
        "variable": {
            "password": code
        }
        })
        headers = {
        'apikey': apikey,
        'Content-Type': 'application/json'
        }
        requests.request("POST", url, headers=headers, data=payload)
        
        user = User.query.filter_by(phone=phone).first()
        user.password = generate_password_hash(code)
        db.session.commit()
        db.session.close()
        
        flash("رمز عبور برای شما پیامک شد")
        return redirect(url_for("signin"))
        
    return render_template(
        "authentication/reset-password.html",
        title='reset-password'
    )

@app.route("/logout")
def logout():
    """User logout/authentication/session management."""
    session.pop("logged_in", None)
    session.pop("administrator", None)
    session.clear()
    flash("You are logged out.")
    return redirect(url_for("signin"))

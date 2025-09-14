from .packages import *

@app.route('/', methods=["GET", "POST"])
def landing():
    """Renders the landing page."""
    pricing()
    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        message = request.form["message"]
        contact = Messages(name = name, phone = phone, message = str(message), date=str(jdatetime.datetime.now())[0:19])
        db.session.add(contact)
        db.session.commit()
        flash("پیام شما ثبت شد")
        return redirect(url_for("landing"))

    last_bp = BuyPrice.query.order_by(desc(BuyPrice.id)).first()
    last_sp = SellPrice.query.order_by(desc(SellPrice.id)).first()

    return render_template(
        'pages/landing.html', format_currency=format_currency, convert_gram_mithqal=convert_gram_mithqal, last_bp=last_bp, last_sp=last_sp,
        title='landing'
    )

@app.route('/pricing', methods=["GET", "POST"])
def pricing_requests():
    """pricing requests."""

    pricing()

    return "pricing"

@app.errorhandler(404)
def not_found(e):
  return render_template("pages/error.html")

@app.errorhandler(405)
def method_not_allowed(e):
  return render_template("pages/error.html")

@app.errorhandler(500)
def error_occurs(e):
  return render_template("pages/error.html")
from flask import render_template

import os
import logging
import random
import requests
import json
import time
from datetime import datetime
import math
import pandas as pd

import jdatetime

from sqlalchemy import desc
from sqlalchemy.inspection import inspect
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
    abort,
)
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_sqlalchemy import SQLAlchemy

from WebApplication import app, db
from WebApplication.database import *

import asyncio
from multiprocessing import Process
#

## Module : Format numbers
def format_currency(amount):
    amount = float(amount)
    return '{:,.0f}'.format(amount)
##### Module : convert gram mithqal
def convert_gram_mithqal(gram_weight):
    mithqal = float(gram_weight) * 4.3318
    return mithqal
##### Module : convert mithqal gram
def convert_mithqal_gram(mithqal_weight):
    gram = float(mithqal_weight) / 4.3318
    return gram
## Module : pricing
def pricing():
    url = "https://tabangohar.com/GheymatKhan/server_update_parsian.php"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    GramPriceToman = json.loads(response.text)
    GramPriceToman = GramPriceToman['x44']
    bp = BuyPrice(amount = GramPriceToman, registration = str(jdatetime.datetime.now())[0:19])
    db.session.add(bp)
    db.session.commit()
    gm = convert_gram_mithqal(GramPriceToman)
    f = gm - 150000
    fp = convert_mithqal_gram(f)
    sp = SellPrice(amount = math.floor(float(fp)), registration = str(jdatetime.datetime.now())[0:19])
    db.session.add(sp)
    db.session.commit()
## Module : pricing
def my_func(args):
    time.sleep(10)
    print(args)
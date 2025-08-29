
from flask import render_template

import os
import logging
import random
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.inspection import inspect
from collections import defaultdict
from venv import create
import pandas as pd
import datetime as dt
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

import jdatetime

## Module : Format numbers
def format_currency(amount):
    return '{:,.2f}'.format(amount)
##### Module : convert gram mithqal
def convert_gram_mithqal(gram_weight):
    mithqal = gram_weight * 4.3318
    return mithqal
###
def test(x):
    return x
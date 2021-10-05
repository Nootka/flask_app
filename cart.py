from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import os
from flask_app import db
from flask_login import login_user, logout_user, login_required
from flask_app.models import Parent, Child, Unit



bp = Blueprint('cart', __name__)

@bp.route('/cart', methods=('GET', 'POST'))
def cart_page():
	return render_template('cart.html')
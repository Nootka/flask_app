from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import os
from flask_app import db
from flask_app.models import  Child, Parent
from flask_app.forms import ChildSearchForm
#from flask_sqlalchemy import and_

#from werkzeug.utils import secure_filename

bp = Blueprint('search', __name__)


@bp.route('/results')
def search_results(search):
	results = []
	search_string = search.data['search']
	
	if search.data['search'] == '':


		if not results:
			flash(f'no results found! for {search_string}', category='warning')
			return redirect('/')
	else:
		# display results
		data = Child.query.filter(Child.name.contains(search_string)).all()
		results_description = Child.query.filter(Child.description.contains(search_string))
		data.extend(results_description)

		results = []
		for item in data:
		    if item not in results:
		        results.append(item)
		
		
		return render_template('results.html', results=results, search_string=search_string)
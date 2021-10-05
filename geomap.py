from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import os
from flask_app import db
from flask_login import login_user, logout_user, login_required
from flask_app.models import PlaceCoordinates
from flask_app.forms import PlaceForm
import folium



bp = Blueprint('geomap', __name__)

@bp.route('/geopmap', methods=('GET', 'POST'))
def geomap_page():
		
		return render_template('geomap.html')

@bp.route('/map')
def map():
	

	start_coords = (41.888410797339574, 12.48828672528501) 
	folium_map = folium.Map(location=start_coords)

	places = PlaceCoordinates.query.all()
	#for place in places:

	data=[]
	for i in range(0,len(places)):
			folium.Marker(
		 		location=[places[i].latitude, places[i].longitude],
		 		popup=places[i].name,
		 		).add_to(folium_map)
			data.append([places[i].latitude,places[i].longitude])

	
	folium_map.fit_bounds(data)
	return folium_map._repr_html_()

@bp.route('/create-place', methods=('GET', 'POST'))
@login_required
def create_place():
	form = PlaceForm()
	if form.validate_on_submit():
		place_to_create = PlaceCoordinates(name=form.name.data,latitude=form.latitude.data,longitude=form.longitude.data)
		
		db.session.add(place_to_create)
		db.session.commit()
		flash(f'Place {place_to_create.name} created successfully', category='success')
		return redirect(url_for('home'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a product: {err_msg}', category='danger')
	
	return render_template('create_place.html', form=form)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import os
from flask_app import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask_login import login_user, logout_user, login_required
from flask_app.models import Parent, Child, Unit
from flask_app.forms import ParentForm, ChildForm, UnitForm
from werkzeug.utils import secure_filename

bp = Blueprint('relations', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.app_context_processor                                                        
def inject_template_globals():                                                   
    parents = Parent.query.first()                                              
    return dict(parents=parents)

@bp.route('/create-parent', methods=('GET', 'POST'))
@login_required
def create_parent():
	form = ParentForm()
	if form.validate_on_submit():
		parent_to_create = Parent(name=form.name.data)
		
		db.session.add(parent_to_create)
		db.session.commit()
		flash(f'Product {parent_to_create.name} created successfully', category='success')
		return redirect(url_for('relations.parents'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a product: {err_msg}', category='danger')
	
	return render_template('create_parent.html', form=form)

@bp.route('/create-unit', methods=('GET', 'POST'))
@login_required
def create_unit():
	form = UnitForm()
	if form.validate_on_submit():
		unit_to_create = Unit(name=form.name.data)
		
		db.session.add(unit_to_create)
		db.session.commit()
		flash(f'Unit {unit_to_create.name} created successfully', category='success')
		return redirect(url_for('relations.parents'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a product: {err_msg}', category='danger')
	
	return render_template('create_parent.html', form=form)

@bp.route('/create-child', methods=('GET', 'POST'))
@login_required
def create_child():
	form = ChildForm()
	form.parent.choices = [(g.id, g.name) for g in Parent.query.order_by('id')]
	form.unit.choices = [(u.id, u.name) for u in Unit.query.order_by('id')]
	
	if form.validate_on_submit():

		f = form.image.data
		img_filename = secure_filename(f.filename)
		img_mimetype = f.mimetype

		
		if f and allowed_file(f.filename):
				f.save(os.path.join(UPLOAD_FOLDER, img_filename))

		image_url=f'../static/uploads/{img_filename}'		
		child_to_create = Child(
			name=form.name.data, 
			parent_id=form.parent.data,
			unit_id=form.unit.data,
		 	image_url=image_url,
		 	description=form.description.data,
		 	price=form.price.data)
		db.session.add(child_to_create)

		db.session.commit()
		flash(f'Child {child_to_create.name} created successfully', category='success')
		return redirect(url_for('relations.parents'))
	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a product: {err_msg}', category='danger')
	
	return render_template('create_child.html', form=form)

@bp.route('/parents')
def parents():
	parents = Parent.query.all()
	return render_template('parents.html',parents=parents)

@bp.route('/category/<name>', methods=['GET'])
def parent(name):
	#parent=Parent.query.get_or_404(id) 
	parent = Parent.query.filter_by(name=name).first()
	return render_template('parent.html',parent=parent)

@bp.route('/child/<int:id>', methods=['GET'])
def child(id):
	child=Child.query.get_or_404(id)
	return render_template('child.html',child=child)

@bp.route('/child-update/<int:id>', methods=['GET','POST'])
@login_required
def update_child(id):
	form = ChildForm()
	form.parent.choices = [(g.id, g.name) for g in Parent.query.order_by('id')]
	form.unit.choices = [(u.id, u.name) for u in Unit.query.order_by('id')]
	child_to_update=Child.query.get_or_404(id)
	
	if request.method == "POST":

		child_to_update.name = request.form['name']
		child_to_update.parent_id = request.form['parent']
		child_to_update.unit_id = request.form['unit']
		child_to_update.description = request.form['description']
		child_to_update.price = request.form['price']
		
	
		
		image=request.files['image']
		img_filename = secure_filename(image.filename)
		
			

		if image and allowed_file(image.filename):
			child_to_update.image_url=f'../static/uploads/{img_filename}'
			image.save(os.path.join(UPLOAD_FOLDER, img_filename))
		
		try:
			db.session.commit()
			flash(f'Child {child_to_update.name} updated successfully', category='success')
			return redirect(url_for('relations.parents'))

			#return render_template('update.html', form=form, product_to_update=product_to_update )
		except :
			flash(f'There was an error with updating a product. Try again ...', category='danger')
			return render_template('update_child.html', form=form, child_to_update=child_to_update )
	else:
		return render_template('update_child.html', form=form, child_to_update=child_to_update)
# views.py

from flask import Flask, Blueprint, current_app, g, session, request, url_for, redirect, \
    render_template, flash, abort

from app.extensions import app_db
from app.model import Switch, Location, Fabric
from .forms import (
    SwitchNewForm, SwitchEditForm, SwitchDeleteForm,
    LocationNewForm, LocationEditForm, LocationDeleteForm,
    FabricNewForm, FabricEditForm, FabricDeleteForm,
)

manage_data_blueprint = Blueprint('manage_data', __name__)


@manage_data_blueprint.route('/switches/list', methods=['GET', 'POST'])
def switch_list():
    switches = app_db.session.query(Switch).order_by(Switch.name).all()

    thead_th_items = [
        {'col_title': '#'},
        {'col_title': 'Name'},
        {'col_title': 'Fabric'},
        {'col_title': 'Location'},
        {'col_title': 'Delete'}
    ]

    tbody_tr_items = []
    for switch in switches:
        fabric_name = '-'
        if switch.fabric:
            fabric_name = switch.fabric.name
        location_name = '-'
        if switch.location:
            location_name = switch.location.name

        tbody_tr_items.append([
            {'col_value': switch.id},
            {'col_value': switch.name,
             'url': url_for('manage_data.switch_edit', switch_id=switch.id)
             },
            {'col_value': fabric_name},
            {'col_value': location_name},
            {'col_value': 'delete',
             'url': url_for('manage_data.switch_delete', switch_id=switch.id)
             }
        ])
    return render_template('manage_data/items_list.html',
                           title='Switches',
                           thead_th_items=thead_th_items,
                           tbody_tr_items=tbody_tr_items,
                           item_new_url=url_for('manage_data.switch_new'),
                           item_new_text='New Switch')


@manage_data_blueprint.route('/location/list', methods=['GET', 'POST'])
def location_list():
    locations = app_db.session.query(Location).order_by(Location.name).all()

    thead_th_items = [
        {'col_title': '#'},
        {'col_title': 'Location'},
        {'col_title': 'Switches'},
        {'col_title': 'Delete'}
    ]

    tbody_tr_items = []
    for location in locations:
        switch_names = ''
        if location.switches:
            switch_names = ', '.join([x.name for x in location.switches])
        tbody_tr_items.append([
            {'col_value': location.id},
            {'col_value': location.name,
             'url': url_for('manage_data.location_edit', location_id=location.id)
            },
            {'col_value': switch_names},
            {'col_value': 'delete',
             'url': url_for('manage_data.location_delete', location_id=location.id)
            }
        ])

    return render_template('manage_data/items_list.html',
                           title='Locations',
                           thead_th_items=thead_th_items,
                           tbody_tr_items=tbody_tr_items,
                           item_new_url=url_for('manage_data.location_new'),
                           item_new_text='New Location')


@manage_data_blueprint.route('/fabric/list', methods=['GET', 'POST'])
def fabric_list():
    fabrics = app_db.session.query(Fabric).order_by(Fabric.name).all()

    thead_th_items = [
        {'col_title': '#'},
        {'col_title': 'Fabric'},
        {'col_title': 'Switches'},
        {'col_title': 'Delete'}
    ]

    tbody_tr_items = []
    for fabric in fabrics:
        switch_names = ''
        if fabric.switches:
            switch_names = ', '.join([x.name for x in fabric.switches])

        tbody_tr_items.append([
            {'col_value': fabric.id},
            {'col_value': fabric.name,
             'url': url_for('manage_data.fabric_edit', fabric_id=fabric.id)
             },
            {'col_value': switch_names},
            {'col_value': 'delete',
             'url': url_for('manage_data.fabric_delete', fabric_id=fabric.id)
             }
        ])

    return render_template('manage_data/items_list.html',
                           title='Fabrics',
                           thead_th_items=thead_th_items,
                           tbody_tr_items=tbody_tr_items,
                           item_new_url=url_for('manage_data.fabric_new'),
                           item_new_text='New Fabric')


### Switch
@manage_data_blueprint.route('/switch/new', methods=['GET', 'POST'])
def switch_new():
    item = Switch()
    form = SwitchNewForm()

    form.fabric.query = app_db.session.query(Fabric).order_by(Fabric.name)
    form.location.query = app_db.session.query(Location).order_by(Location.name)

    if form.validate_on_submit() and form.submit_add.data:


        form.populate_obj(item)
        app_db.session.add(item)
        app_db.session.commit()
        flash('Switch added: ' + item.name, 'info')
        return redirect(url_for('manage_data.switch_list'))

    elif form.validate_on_submit() and form.submit_reg.data:
        flash("Registration", 'info')
        return redirect(url_for('manage_data.switch_list'))

    return render_template('manage_data/item_new_edit.html', title='New Switch', form=form)


@manage_data_blueprint.route('/switch/edit/<int:switch_id>', methods=['GET', 'POST'])
def switch_edit(switch_id):
    item = app_db.session.query(Switch).filter(Switch.id == switch_id).first()
    if item is None:
        abort(403)

    form = SwitchEditForm(obj=item)
    form.fabric.query = app_db.session.query(Fabric).order_by(Fabric.name)
    form.location.query = app_db.session.query(Location).order_by(Location.name)

    if form.validate_on_submit():
        form.populate_obj(item)
        app_db.session.commit()
        flash('Switch updated: ' + item.name, 'info')
        return redirect(url_for('manage_data.switch_list'))

    return render_template('manage_data/item_new_edit.html', title='Edit Switch', form=form)


@manage_data_blueprint.route('/switch/delete/<int:switch_id>', methods=['GET', 'POST'])
def switch_delete(switch_id):
    item = app_db.session.query(Switch).filter(Switch.id == switch_id).first()
    if item is None:
        abort(403)

    form = SwitchDeleteForm(obj=item)
    item_name = item.name
    if form.validate_on_submit():
        app_db.session.delete(item)
        app_db.session.commit()
        flash('Deleted switch: ' + item_name, 'info')
        return redirect(url_for('manage_data.switch_list'))

    return render_template('manage_data/item_delete.html', title='Delete Switch', item_name=item_name, form=form)


### Location

@manage_data_blueprint.route('/location/new', methods=['GET', 'POST'])
def location_new():
    item = Location()
    form = LocationNewForm()

    if form.validate_on_submit():
        form.populate_obj(item)
        app_db.session.add(item)
        app_db.session.commit()
        flash('Location added: ' + item.name, 'info')
        return redirect(url_for('manage_data.location_list'))

    return render_template('manage_data/item_new_edit.html', title='New Location', form=form)


@manage_data_blueprint.route('/location/edit/<int:location_id>', methods=['GET', 'POST'])
def location_edit(location_id):
    item = app_db.session.query(Location).filter(Location.id == location_id).first()
    if item is None:
        abort(403)

    form = LocationEditForm(obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        app_db.session.commit()
        flash('Location updated: ' + item.name, 'info')
        return redirect(url_for('manage_data.location_list'))

    return render_template('manage_data/item_new_edit.html', title='Edit Location', methods=['GET', 'POST'])


@manage_data_blueprint.route('/location/delete/<int:location_id>', methods=['GET', 'POST'])
def location_delete(location_id):
    item = app_db.session.query(Location).filter(Location.id == location_id).first()
    if item is None:
        abort(403)

    form = LocationDeleteForm(obj=item)
    item_name = item.name
    if form.validate_on_submit():
        app_db.session.delete(item)
        app_db.session.commit()
        flash('Deleted location: ' + item_name, 'info')
        return redirect(url_for('manage_data.location_list'))

    return render_template('manage_data/item_delete.html', title='Delete Location', item_name=item_name, form=form)


### Fabric

@manage_data_blueprint.route('/fabric/new', methods=['GET', 'POST'])
def fabric_new():
    item = Fabric()
    form = FabricNewForm()

    if form.validate_on_submit():
        form.populate_obj(item)
        app_db.session.add(item)
        app_db.session.commit()
        flash('Fabric added: ' + item.name, 'info')
        return redirect(url_for('manage_data.fabric_list'))

    return render_template('manage_data/item_new_edit.html', title='New Fabric', form=form)


@manage_data_blueprint.route('/fabric/edit/<int:fabric_id>', methods=['GET', 'POST'])
def fabric_edit(fabric_id):
    item = app_db.session.query(Fabric).filter(Fabric.id == fabric_id).first()
    if item is None:
        abort(403)

    form = FabricEditForm(obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        app_db.session.commit()
        flash('Fabric updated: ' + item.name, 'info')
        return redirect(url_for('manage_data.fabric_list'))

    return render_template('manage_data/item_new_edit.html', title='Edit Fabric', methods=['GET', 'POST'])


@manage_data_blueprint.route('/fabric/delete/<int:fabric_id>', methods=['GET', 'POST'])
def fabric_delete(fabric_id):
    item = app_db.session.query(Fabric).filter(Fabric.id == fabric_id).first()
    if item is None:
        abort(403)

    form = FabricDeleteForm(obj=item)
    item_name = item.name
    if form.validate_on_submit():
        app_db.session.delete(item)
        app_db.session.commit()
        flash('Deleted fabric: ' + item_name, 'info')
        return redirect(url_for('manage_data.fabric_list'))

    return render_template('manage_data/item_delete.html', title='Delete Fabric', item_name=item_name, form=form)

import os
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, login_required
import uuid

from otherFiles.setup import *
from otherFiles.databases import *
from otherFiles.forms import *

def checkSignIn():
  if current_user.is_authenticated:
    return True
  else:
    return False

@app.route('/', methods=['POST', 'GET'])
def home():
  return render_template("home.html", signedIn=checkSignIn())


@app.route('/store', methods=['POST', 'GET'])
@login_required
def store():
  items = Item.query.filter_by(store_id=current_user.id).all()
  return render_template("store.html", items=items, signedIn=checkSignIn())

@app.route('/zip', methods=['POST','GET'])
def zip():
  return render_template("zipCode.html", signedIn=checkSignIn())


@app.route('/customer/<int:zipCode>', methods=['POST','GET'])
def customer(zipCode):
  items = []
  stores = Store.query.filter_by(zipCode=zipCode).all()
  storeMap = "false"
  for store in stores:
    for item in store.items:
      if not item.customer_name:
        items.append(item)
        storeMap = store
      if len(items) > 20:
        return render_template("customer.html", items=items, signedIn=checkSignIn(), store=storeMap)
  return render_template("customer.html", items=items, signedIn=checkSignIn(), store=storeMap)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("store"))
  form = LoginForm()
  if form.validate_on_submit():
      store = Store.query.filter_by(username=form.username.data).first()
      if store and bcrypt.check_password_hash(store.password, form.password.data):
        login_user(store)
        flash('Login Success!', 'success')
        return redirect(url_for('store'))
      else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form, signedIn=checkSignIn())
  return render_template('login.html', title='Login', form=form, signedIn=checkSignIn())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for("store"))
  form = RegistrationForm()
  if form.validate_on_submit():
      #make user
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      store = Store(username=form.username.data, name=form.name.data, addressNum=form.addressNum.data, addressStreet=form.addressStreet.data, addressCity=form.addressCity.data, zipCode=form.zipCode.data, password=hashed_password)
      db.session.add(store)
      db.session.commit()

      #return
      login_user(store, remember="False")
      flash('Your account has been created! Login Success!', 'success')
      return redirect(url_for('store'))
  return render_template("signup.html", title='Sign Up', form=form, signedIn=checkSignIn())

def save_picture(form_picture,uuid):
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = uuid + f_ext
  picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
  form_picture.save(picture_path)
  return picture_fn

@app.route('/addlisting',methods=['POST','GET'])
@login_required
def addlisting():
  form = AddItem()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data,str(uuid.uuid4()))
    else:
      picture_file = None
    item = Item(uuid=str(uuid.uuid4()), name=form.name.data,cost=float(form.cost.data)*0.2,category=form.category.data[0], weight=float(form.weight.data), sellBy=form.sellBy.data, expiration=form.expiration.data, store_id=current_user.id, img_directory=picture_file)
    db.session.add(item)
    db.session.commit()    
    for pickupTime in form.pickupTimes.entries:
      pickup = Pickup(start=pickupTime.data['start'], end=pickupTime.data['end'], item_id=item.id)
      db.session.add(pickup)
    db.session.commit()
    flash('added item', 'success')
    return redirect(url_for("store"))
  return render_template("addlisting.html",form=form, signedIn=checkSignIn())

@app.route('/editlisting/<uuid>',methods=['POST','GET'])
@login_required
def editlisting(uuid):
  item = Item.query.filter_by(uuid=uuid).first()
  form = AddItem()
  form.name.default = item.name
  form.cost.default = item.cost
  form.category.default = [item.category]
  form.weight.default = item.weight
  form.sellBy.default = item.sellBy
  form.expiration.default = item.expiration
  form.process()

  if form.validate_on_submit():
    db.session.delete(item)
    item = Item(uuid=str(uuid.uuid4()), name=form.name.data, category=form.category.data[0], weight=float(form.weight.data), sellBy=form.sellBy.data, expiration=form.expiration.data, store_id=current_user.id, cost=float(form.cost.data))
    db.session.add(item)
    db.session.commit()
    flash('fixed item', 'success')
    return redirect(url_for("store"))
  return render_template("addlisting.html",form=form, item=item, signedIn=checkSignIn())
    
@app.route('/purchase/<uuid>', methods=['POST', 'GET'])
def purchase(uuid):
  item = Item.query.filter_by(uuid=uuid).first()
  store = Store.query.filter_by(id=item.store_id).first()
  categories = [(str(c.start)+" - "+str(c.end), str(c.start)+" - "+str(c.end)) for c in item.pickupTimes]
  form = Purchase(coerce=int)
  form.pickupTimes.choices = categories
  if form.validate_on_submit():
      item.pickupTime = form.pickupTimes.data[0]
      item.customer_name = form.name.data
      db.session.commit()
      flash('You have purchased the item!', 'success')
      return redirect(url_for("zip"))
  return render_template("purchase.html",item=item,store=store, form=form, signedIn=checkSignIn())
@app.route('/map', methods=['POST', 'GET'])
def map():
  return render_template("map.html")
@login_manager.user_loader
def load_user(store_id):
    return Store.query.get(int(store_id))

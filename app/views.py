"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import UserProfile, UserProfileNew
from werkzeug.utils import secure_filename
import time, uuid


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route("/login", methods=["GET", "POST"])
def login():
    # If the user is already logged in then it will just return them to the 
    # secure page instead of logging them in again
    if (current_user.is_authenticated):
        return redirect(url_for('secure_page'))
    
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data and form.password.data:
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data
            
            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.
            user = UserProfile.query.filter_by(username=username, password=password).first()
            # get user id, load into session
            if user is not None:
                login_user(user)
                flash('Logged in successfully.', 'success')
                next = request.args.get('next')
                return redirect(url_for('secure_page'))
            else:
                flash('Email or Password is incorrect.', 'danger')
                
    return render_template("login.html", form=form)

@app.route("/secure-page")
@login_required
def secure_page():
    return render_template('securepage.html', uploads=get_uploads())

@app.route('/signup')
def signup():
    """Render the website's signup page."""
    return render_template('signup.html')

@app.route('/add-profile', methods=["GET", "POST"])
def add_file():
    if not session.get('logged_in'):
        abort(401)

    
    file_folder = app.config['UPLOAD_FOLDER']

    

    # if request.method == 'POST' and (request.form['fName'] and request.form['lName'] and request.form['email'] and 
    # request.form['gender'] and request.form['location'] and request.form['bio'] and request.form['file']):
        
    # print "First Name: %s" % request.form['fName']
    # print "Last Name: %s" % request.form['lName']
    # print "Email: %s" % request.form['email']
    # print "Gender: %s" % request.form['gender']  
    # print "Location : %s" % request.form['location'] 
    # print "Bio : %s" % request.form['bio']
    # print "File: %s" % request.files['file'].filename

    NewProfile = UserProfileNew(request.form['fName'], request.form['lName'],request.form['email'],request.form['location'], request.form['bio'], request.form['created_on'], request.files['file'].filename,request.form['gender'])
    
    # first_name = db.Column(db.String(80))
    # last_name = db.Column(db.String(80))
    # gender = db.Column(db.String(10))
    # email = db.Column(db.String(80))
    # location = db.Column(db.String(80))
    # bio = db.Column(db.String(140))
    # image = db.Column(db.String(255))
    
    db.session.add(NewProfile)
    db.session.commit()
        # fName = request.form['fName']
        # lName = request.form['lName'] 
        # gender = request.form['gender']
        # email = request.form['email']
        # location = request.form['location']
        # bio = request.form['bio']

        # file = request.files['file']
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(file_folder, filename))

    flash('Profile created and successfully saved')
    return redirect(url_for('home'))

    # return render_template('add_file.html')

def get_uploads():
    uploads = []
    for subdir, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if not file.startswith('.'): #ignores hidden files on linux
                uploads.append(file)
    return uploads

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    
@app.route('/profile', methods=['POST','GET'])
def profile():
    """Creates new profile"""
    
    if request.method == 'POST':
        uid = str(uuid.uuid4().fields[-1])[:8]
        time_created = time.strftime('%Y/%b/%d')
        fname = request.form['first_name']
        lname = request.form['last_name']
        uname = request.form['email']
        location = request.form['location']
        biography =request.form['bio']
        sex =request.form['gender']
        
        
        profilepic = request.files['file']
        if profilepic:
            uploadfolder = app.config['UPLOAD_FOLDER']
            filename = secure_filename(profilepic.filename)
            profilepic.save(os.path.join(uploadfolder, filename))
            
        user = UserProfile(id= uid, first_name=fname, last_name=lname, username=uname, location = location, gender=sex, bio=biography, created = time_created, pic=profilepic.filename)
        db.session.add(user)
        db.session.commit()
        flash('New User was successfully added')
        return redirect(url_for('home'))
    return render_template('Profile.html')

@app.route('/profiles', methods=['GET','POST'])
def profiles():
    profile_list=[]
    
    profiles= UserProfile.query.filter_by().all()
    
    if request.method == 'POST':
        for profile in profiles:
            profile_list +=[{'email':profile.email, 'userID':profile.id}]
        return jsonify(users=profile_list)
    elif request.method == 'GET':
        return render_template('profiles.html', profile=profiles)
    return redirect(url_for('home'))

@app.route('/profile/<userid>', methods=['GET', 'POST'])
def userprofile(userid):
    json={}
    user = UserProfile.query.filter_by(id=userid).first()
    if request.method == 'POST':
        json={'userid':user.id, 'email':user.email, 'profile_image':user.pic, 'gender':user.gender, 'location':user.location, 'created_on':user.created}
        return jsonify(json)

    elif request.method == 'GET' and user:
        return render_template('individual.html', profile=user)

    return render_template('profile.html')
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")

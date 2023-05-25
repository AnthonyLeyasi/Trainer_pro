from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models.trainer import Trainer
from flask_app.models.user import User
from flask_app.controllers import users
from flask import flash






@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    data = {"id": session['user_id']}
    user = User.get_by_id(data)
    trainers = Trainer.get_all()
    return render_template('dashboard.html', user=user, trainers=trainers)


@app.route('/contact.html', methods=['GET'])
def contact_page():

    return render_template('contact.html')


@app.route('/about.html', methods=['GET'])
def about_page():

    return render_template('about.html')


@app.route('/trainer/new')
def create_trainer():
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('new.html')


# @app.route('/trainers/new/process', methods=['POST'])
# def process_trainer():
#     if 'user_id' not in session:
#         return redirect('/user/login')
    
#     if not Trainer.validate_trainer(request.form):
#         flash("Validation failed. Please check the form fields.", "danger")
#         return render_template('new.html', messages=flash.get_flashed_messages())

#     data = {
#         'user_id': session['user_id'],
#         'first_name': request.form['first_name'],
#         'last_name': request.form['last_name'],
#         'city': request.form['city'],
#         'gym': request.form['gym'],
#         'description': request.form['description'],  
#     }
#     Trainer.save(data)

#     flash("Trainer created successfully!", "success")
#     return redirect('/dashboard')


@app.route('/trainers/new/process', methods=['POST'])
def process_trainer():
    if 'user_id' not in session:
        return redirect('/user/login')
    
    if not Trainer.validate_trainer(request.form):
        flash("Validation failed. Please check the form fields.")
        return render_template('new.html')

    data = {
        'user_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'city': request.form['city'],
        'gym': request.form['gym'],
        'description': request.form['description'],  
    }
    Trainer.save(data)

    flash("Trainer created successfully!", "success")
    return redirect('/dashboard')


@app.route('/trainers')
def view_trainer():
    return render_template('view.html')



@app.route('/all/trainers')
def all_trainers():
    trainers = Trainer.get_all()
    return render_template('view.html', trainers=trainers)






@app.route('/trainers/view/<int:id>')
def view_trainer_profile(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    trainer = Trainer.get_by_id({'id': id})
    return render_template('view.html', trainer=trainer)




@app.route("/trainers/delete/<int:id>")
def delete_trainer(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    data = {"id": id}
    Trainer.delete(data)
    return redirect("/dashboard")



@app.route('/trainers/update/<int:id>')
def update_trainer(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    trainer = Trainer.get_by_id({'id': id})
    return render_template('edit.html', trainer=trainer)

@app.route('/trainers/update/process/<int:id>', methods=['POST'])
def process_trainer_update(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Trainer.validate_trainer(request.form):
        return redirect('/trainers/update/' + str(id))
    data = {
        'id': id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'city': request.form['city'],
        'gym': request.form['gym'],
        'description': request.form['description'],
    }
    Trainer.update(data)
    return redirect('/dashboard')
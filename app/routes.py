import os
from flask import render_template, request, redirect, url_for, jsonify, flash, send_file, make_response
from . import db
from .models import User, Client, Event
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

def init_routes(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return render_template('index.html', current="index")
    
    @app.route('/users')
    @login_required
    def users():
        users = User.query.all()
        return render_template('users.html', current="users", users=users)


    @app.route('/clients')
    @login_required
    def clients():
        clients = Client.query.all()
        return render_template('clients.html', current="clients", clients=clients)
    
    @app.route('/client/edit/<id>', methods=["GET", "POST"])
    @login_required
    def client_edit(id):
        if request.method == "GET":
            client = db.get_or_404(Client, id)
            return render_template('client/edit.html', current="clients", client=client)
        if request.method == "POST":
            client = db.get_or_404(Client, request.form["id"])
            client.name = request.form["name"]
            client.start_date = request.form["start_date"]
            client.end_date = request.form["end_date"]
            db.session.commit()
            return redirect("/clients")

    @app.route('/client/del/<id>', methods=["GET", "POST"])
    @login_required
    def client_del(id):
        if request.method == "GET":
            client = db.get_or_404(Client, id)
            return render_template('client/del.html', current="clients", client=client)
        if request.method == "POST":
            client = db.get_or_404(Client, request.form["id"])
            db.session.delete(client)
            db.session.commit()
            return redirect("/clients")

    @app.route('/events')
    @login_required
    def events():
        events = Event.query.all()
        return render_template('events.html', current="events", events=events)

    @app.route('/user/add', methods=["GET", "POST"])
    @login_required
    def user_add():
        if request.method == "GET":
            return render_template('user/add.html', current="users")
        if request.method == "POST":
            user = User()
            user.username = request.form["username"]
            user.password = request.form["password"]
            
            db.session.add(user)
            db.session.commit()
            return redirect("/users")

    @app.route('/user/edit/<id>', methods=["GET", "POST"])
    @login_required
    def user_edit(id):
        if request.method == "GET":
            user = db.get_or_404(User, id)
            return render_template('user/edit.html', current="users", user=user)
        if request.method == "POST":
            user = db.get_or_404(User, request.form["id"])
            user.username = request.form["username"]
            user.password = request.form["password"]
            
            db.session.commit()
            return redirect("/users")

    @app.route('/user/del/<id>', methods=["GET", "POST"])
    @login_required
    def user_del(id):
        if request.method == "GET":
            user = db.get_or_404(User, id)
            return render_template('user/del.html', current="users", user=user)
        if request.method == "POST":
            user = db.get_or_404(User, request.form["id"])
            db.session.delete(user)
            db.session.commit()
            return redirect("/users")

    @app.route('/client/add', methods=["GET", "POST"])
    @login_required
    def client_add():
        if request.method == "GET":
            return render_template('client/add.html', current="clients")
        if request.method == "POST":
            client = Client()
            client.name = request.form["name"]
            client.start_date = request.form["start_date"]
            client.end_date = request.form["end_date"]
            
            db.session.add(client)
            db.session.commit()
            return redirect("/clients")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
    
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        
            user = User.query.filter_by(username=username, password=password).first()
            
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect("/")
            else:
                flash('Неверный имя пользователя или пароль', 'danger')
    
        return render_template('login.html')
    
    @app.route('/client/photo-edit/<id>', methods=["GET", "POST"])
    def client_photo_edit(id):
        if request.method == "GET":
            client = db.get_or_404(Client, id)
            return render_template('client/add_photo.html', current="clients", client=client)
        if request.method == "POST":
            # Проверяем, есть ли файл в запросе
            if 'photo' not in request.files:
                flash('No file part')
                return redirect("/clients")
        
            file = request.files['photo']
        
            # Если пользователь не выбрал файл
            if file.filename == '':
                flash('No selected file')
                return redirect("/clients")
            
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"jpg"}
            
            # Если файл разрешен и корректен
            if file and allowed_file(file.filename):
                if not os.path.exists(app.config['IMGS']):
                    os.makedirs(app.config['IMGS'])
                file.save(os.path.abspath(os.path.join(app.config['IMGS'], f"{id}.jpg")))
                return redirect("/clients")
    
        return redirect("/clients")
    
    @app.route('/client/photo/<id>', methods=["GET", "POST"])
    def client_photo(id):
        if request.method == "GET":
            client = db.get_or_404(Client, id)
            if os.path.isfile(os.path.join(app.config['IMGS'], f"{id}.jpg")):
                return send_file(os.path.abspath(os.path.join(app.config['IMGS'], f"{id}.jpg")), as_attachment=True)
            else:
                return make_response(f"File '{id}' not found.", 404)
            
    @app.route('/clients/json')
    def clients_all():
        clients = Client.query.all()
        result = []
        for client in clients:
            client_dict = client.__dict__
            client_dict.pop('_sa_instance_state', None)  # Удаляем служебное поле SQLAlchemy
            result.append(client_dict)
        return jsonify(result)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")
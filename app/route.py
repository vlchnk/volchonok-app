from app import app, api
from flask import Flask, render_template, url_for, request, redirect, session
import uuid

@app.route('/')
def index():
        return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
        try:
                article_user = api.check_session_user(session['uid'])
                article_team = api.check_member_team(article_user)
                article_member = api.get_members(article_team)
                title = "Dashboard"
                if article_user and article_team:
                        count_game = api.get_all_game(article_team)
                        count_training = api.get_all_training(article_team)
                        article_post = api.get_all_post(article_team)
                        article_event = api.get_events(article_team)
                        article_count_move = api.team_movement(article_team)
                        return render_template('dashboard.html', title=title, user=article_user, team=article_team, members=article_member, game=count_game, training=count_training, post=article_post, event=article_event, count=article_count_move)
                else:
                     return redirect('/login/')  
        except:
                return redirect('/login/')


@app.route('/register/', methods=['GET','POST'])
def register():
        if request.method == 'POST':
                status = api.create_user(request.form)
                if status:
                        return redirect('/create/')
                else:
                        error = 'Email/Username has already been taken.'
                        return render_template('/register.html', error=error)
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and status_member:
                                return redirect('/dashboard/')
                        else:
                                return render_template('/register.html', addNew=False) 
                except:
                        return render_template('/register.html', addNew=False)


@app.route('/login/', methods=['GET','POST'])
def login():
        if request.method == 'POST':
                status = api.login_user(request.form)
                if status:
                        return redirect('/dashboard/')
                else:
                        error = 'Your email or password were incorrect.'
                        return render_template('/login.html', error=error)
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and status_member:
                                return redirect('/dashboard/')
                        else:
                                return render_template('/login.html') 
                except:
                        return render_template('/login.html')



@app.route('/logout/')
def logout():
        try:
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        api.logout_user(session['uid'])
                        return redirect('/login/')
                else:
                     return redirect('/dashboard/')  
        except:
                return redirect('/login/')


@app.route('/create/', methods=['GET','POST'])
def create():
        if request.method == 'POST':
                if request.form.get('name'):
                        article_user = api.check_session_user(session['uid'])
                        status = api.create_team(request.form, article_user)
                        if status:
                                return redirect('/dashboard/')
                        else:
                                return render_template('/create/', error='Name is busy')
                else:
                        link_id = request.form.get('link')
                        article_user = api.check_session_user(session['uid'])
                        article_team = api.check_team_link(link_id)
                        if article_user and article_team:
                                api.add_member_team(article_user, link_id, position='Player')
                                return redirect('/dashboard/')
                        else:
                                return redirect('/dashboard/')
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and not status_member:
                                return render_template('/createteam.html')
                        else:
                                return redirect('/dashboard/')  
                except:
                        return redirect('/dashboard/')
                

@app.route('/team/')
def team():
        try:
                article_user = api.check_session_user(session['uid'])
                article_team = api.check_member_team(article_user)
                article_member = api.get_members(article_team)
                if article_user and article_team:
                        user_position = api.get_position(article_user)
                        if user_position.position == 'Creater':
                                return render_template('team.html', title='Team', user=article_user, team=article_team, members=article_member, edit=True)
                        else:
                                return render_template('team.html', title='Team', user=article_user, team=article_team, members=article_member, edit=False)
                else:
                     return redirect('/dashboard/')   
        except:
                return redirect('/dashboard/')


@app.route('/event/')
def event():
        try:
                article_user = api.check_session_user(session['uid'])
                article_team = api.check_member_team(article_user)
                article_event = api.get_events(article_team)
                if article_user and article_team:
                        user_position = api.get_position(article_user)
                        all_movement = api.all_movement(article_user)
                        if user_position.position == 'Creater' or user_position.position == 'Capitan':
                                return render_template('event.html', title='Event', user=article_user, team=article_team.name, event=article_event, edit=True, new=True)
                        else:
                                return render_template('event.html', title='Event', user=article_user, team=article_team.name, event=article_event, edit=False, movement=all_movement, new=True)
                else:
                     return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')


@app.route('/event/old/')
def oldEvent():
        try:
                article_user = api.check_session_user(session['uid'])
                article_team = api.check_member_team(article_user)
                article_event = api.get_old_events(article_team)
                if article_user and article_team:
                        user_position = api.get_position(article_user)
                        all_movement = api.all_movement(article_user)
                        if user_position.position == 'Creater' or user_position.position == 'Capitan':
                                return render_template('event.html', title='Event', user=article_user, team=article_team.name, event=article_event, edit=True, new=False)
                        else:
                                return render_template('event.html', title='Event', user=article_user, team=article_team.name, event=article_event, edit=False, movement=all_movement, new=False)
                else:
                     return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')


@app.route('/event/add/', methods=['GET','POST'])
def eventAdd():
        if request.method == 'POST':
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        api.add_event(request.form, article_user, status_member)
                        return redirect('/event/')
                else:
                        return render_template('/event/add/')
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and status_member:
                                return render_template('/createevent.html', user=article_user, title='Event edit')
                        else:
                                return redirect('/dashboard/')  
                except:
                        return redirect('/dashboard/')


@app.route('/event/<int:id>/edit/', methods=['GET','POST'])
def eventEdit(id):
        if request.method == 'POST':
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        api.edit_event(request.form, id)
                        return redirect('/event/')
                else:
                        return render_template('/event/add/')
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and status_member:
                                event = api.get_event(id)
                                return render_template('/editevent.html', user=article_user, title='Event', event=event, id=id)
                        else:
                                return redirect('/dashboard/')  
                except:
                        return redirect('/dashboard/')


@app.route('/event/<int:id>/delete/')
def eventDelete(id):
        try:
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        event = api.delete_event(id,article_user)
                        return redirect('/event/')
                else:
                        return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')



@app.route('/event/<int:id>/move/<int:choice>/')
def eventMove(id, choice):
        article_user = api.check_session_user(session['uid'])
        status_member = api.check_member_team(article_user)
        if article_user and status_member:
                status_move = api.check_move_event(article_user, id)
                if status_move:
                        api.move_edit(choice,status_move,id)
                        return redirect('/event/')
                else:
                        api.move_event(choice, article_user, id)
                        return redirect('/event/')
        else:
                return render_template('/login/')


@app.route('/user/')
def user():
        try:
                article_user = api.check_session_user(session['uid'])
                article_team = api.check_member_team(article_user)
                if article_user and article_team:
                        return render_template('user.html', user=article_user, title='Profile')
                else:
                     return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')


@app.route('/link/<string:id>', methods=['GET', 'POST'])
def reg_from_link(id):
        if request.method == 'POST':
                status = api.create_user(request.form)
                if status:
                        article_team = api.check_team_link(id)
                        article_user = api.check_session_user(session['uid'])
                        api.add_member_team(article_user, id, position='Player')
                        return redirect('/dashboard/')
                else:
                        return render_template('/register.html', error=error)
                pass
        else:
                article_team = api.check_team_link(id)
                if article_team:
                        return render_template('/register.html', addNew=True, team=article_team)
                else:
                     return redirect('/dashboard/')  


@app.route('/link/', methods=['POST'])
def link():
        article_user = api.check_session_user(session['uid'])
        article_team = api.check_member_team(article_user)
        # article_team = api.check_team_link(id)
        if article_user and article_team:
                mail = request.form['email']
                title = "You were invited to the team - " + article_team.name
                api.send_mail(mail,article_team, str(title))
                # api.add_member_team(article_user, id, position='Player')
                return redirect('/team/')
        else:
                return redirect('/login/')


@app.route('/team/<string:name>')
def team_id():
        pass


@app.route('/team/<int:id>/edit/', methods=['POST','GET'])
def edit_member(id):
        if request.method == 'POST':
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        api.edit_member(request.form, id)
                        return redirect('/team/')
                else:
                        return redirect('/dashboard/')
        else:
                return redirect('/dashboard/')



@app.route('/post/')
def post():
        try:
                article_user = api.check_session_user(session['uid'])
                article_team = api.check_member_team(article_user)
                if article_user and article_team:
                        article_post = api.get_all_post(article_team)
                        user_position = api.get_position(article_user)
                        if user_position.position == 'Creater' or user_position.position == 'Capitan':
                                return render_template('post.html', user=article_user, title='Post', post=article_post, edit=True)
                        else:
                                return render_template('post.html', user=article_user, title='Post', post=article_post, edit=False)
                else:
                     return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')


@app.route('/post/add/', methods=['GET','POST'])
def postAdd():
        if request.method == 'POST':
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        article_team = api.check_member_team(article_user)
                        api.add_post(request.form, article_team)
                        return redirect('/post/')
                else:
                        return render_template('/post/add/')
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and status_member:
                                return render_template('/createpost.html', user=article_user, title='Create post')
                        else:
                                return redirect('/dashboard/')  
                except:
                        return redirect('/dashboard/')


@app.route('/post/<int:id>/edit/', methods=['GET','POST'])
def editPost(id):
        if request.method == 'POST':
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        api.edit_post(request.form, id)
                        return redirect('/post/')
                else:
                        return render_template('/post/')
        else:
                try:
                        article_user = api.check_session_user(session['uid'])
                        status_member = api.check_member_team(article_user)
                        if article_user and status_member:
                                post = api.get_post(id)
                                if status_member.id == post.team_id:
                                        return render_template('/editpost.html', user=article_user, title='Post', post=post, id=id)
                                else:
                                        return redirect('/dashboard/')   
                        else:
                                return redirect('/dashboard/')  
                except:
                        return redirect('/dashboard/')


@app.route('/post/<int:id>/')
def openPost(id):
        try:
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        post = api.get_post(id)
                        if status_member.id == post.team_id:
                                return render_template('/openpost.html', user=article_user, title='Post', post=post, id=id)
                        else:
                                return redirect('/dashboard/')   
                else:
                        return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')


@app.route('/post/<int:id>/delete/')
def postDelete(id):
        try:
                article_user = api.check_session_user(session['uid'])
                status_member = api.check_member_team(article_user)
                if article_user and status_member:
                        post = api.get_post(id)
                        if status_member.id == post.team_id:
                                event = api.delete_post(id)
                                return redirect('/post/')
                        else:
                                return redirect('/post/')
                else:
                        return redirect('/dashboard/')  
        except:
                return redirect('/dashboard/')


# Redirect http to https

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


# 404 and 500

@app.errorhandler(404)
def page_not_found(e):
        try:
                article_user = api.check_session_user(session['uid'])
                return render_template('/404.html', user=article_user, title='Ooops...'), 404
        except:
                return redirect('/')


@app.errorhandler(500)
def error(e):
        try:
                article_user = api.check_session_user(session['uid'])
                return render_template('/500.html', user=article_user, title='Ooops...'), 500
        except:
                return redirect('/')
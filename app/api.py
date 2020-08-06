from flask import session
from libgravatar import Gravatar
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, date
from sqlalchemy import cast, DATE, func
import requests
import random

from app import app, db
from app.models import User, Team, Member, Event, Movement, Post, Comment


def create_user(data):
    try:
        session['uid'] = str(uuid.uuid4())
        username = data['username']
        email = data['email']
        avatar = Gravatar(email.lower()).get_image(size=500)
        password = generate_password_hash(data['password'])
        session_user = session['uid']
        article = User(username=username, email=email, password=password, session=session_user, avatar=avatar)
        db.session.add(article)
        db.session.commit()
        return True
    except:
        return False


def login_user(data):
    try:
        article = User.query.filter_by(username=data['username']).first()
        session['uid'] = str(uuid.uuid4())
        username = data['username']
        password = check_password_hash(article.password, data['password'])
        if password:
            article.session = session['uid']
            db.session.add(article)
            db.session.commit()
            return True
    except:
        return False


def logout_user(data):
    try:
        article = User.query.filter_by(session=data).first()
        article.session = ''
        db.session.add(article)
        db.session.commit()
        return True
    except:
        return False
    


def check_session_user(data):
    try:
        status = User.query.filter_by(session=data).first()
        if status:
            return status
    except:
        return False


def create_team(data,article):
    try:
        name = data['name']
        user_id = article.id
        article_team = Team(name=name,user_id=user_id)
        db.session.add(article_team)
        article_team = Team.query.filter_by(user_id=article.id).first()
        article_member = Member(user_id=article.id, team_id=article_team.id, position='Creater', name=article.username)
        db.session.add(article_member)
        db.session.commit()
        return True
    except:
        return False


def add_member_team(user,link,position='player'):
    try:
        team = Team.query.filter_by(link=link).first()
        article_member = Member(user_id=user.id, team_id=team.id, position=position, name=user.username)
        db.session.add(article_member)
        db.session.commit()
        return True
    except:
        return False


def check_member_team(user):
    try:
        get_team = Member.query.filter_by(user_id=user.id).first()
        get_name = Team.query.filter_by(id=get_team.team_id).first()
        return get_name
    except:
        return False


def get_position(user):
    try:
        get_team = Member.query.filter_by(user_id=user.id).first()
        return get_team
    except:
        return False


def check_team_link(id):
    try:
        get_team = Team.query.filter_by(link=id).first()
        if get_team:
            return get_team
        else:
            return False
    except:
        return False


def get_events(team):
    try:
        article_events = Event.query.filter(func.DATE(Event.date_event) >= datetime.utcnow(), Event.team_id == team.id).order_by(Event.date_event).all()
        return article_events
    except:
        return False


def get_old_events(team):
    try:
        article_events = Event.query.filter(func.DATE(Event.date_event) <= datetime.utcnow(), Event.team_id == team.id).order_by(Event.date_event).all()
        return article_events
    except:
        return False


def get_event(id):
    try:
        article_event = Event.query.filter_by(id=id).first()
        return article_event
    except:
        return False


def add_event(event,user,team):
    try:
        date = event['date'] + ' ' + event['time']
        date_time = datetime.strptime( date, "%Y-%m-%d %H:%M" )
        event = Event(name=event['name'], text=event['text'],date_event=date_time,type_event=event['type'], user_id=user.id, team_id=team.id)
        db.session.add(event)
        db.session.commit()
        return True
    except:
        return False


def edit_event(data,id):
    try:
        event = Event.query.filter_by(id=id).first()
        date = data['date'] + ' ' + data['time']
        date_time = datetime.strptime( date, "%Y-%m-%d %H:%M:%S" )
        event.name = data['name']
        event.text = data['text']
        event.date_event = date_time
        event.type_event = data['type']
        db.session.commit()
        return True
    except:
        return False


def delete_event(id,user):
    try:
        event = Event.query.filter_by(id=id).first()
        db.session.delete(event)
        db.session.query(Movement).filter_by(event_id=id).delete()
        db.session.commit()
        return True
    except:
        return False


def get_all_game(team):
    try:
        all_post = Event.query.filter(Event.team_id==team.id,Event.type_event=='Game').all()
        return all_post
    except:
        return False


def get_all_training(team):
    try:
        all_post = Event.query.filter(Event.team_id==team.id,Event.type_event=='Training').all()
        return all_post
    except:
        return False


def move_event(choice,user,id):
    try:
        event = Event.query.filter_by(id=id).first()
        move = Movement(user_id=user.id, user_name=user.username, event_id=id, status=choice)
        db.session.add(move)
        db.session.commit()
        return True
    except:
        return False


def move_edit(choice,move,id):
    try:
        move_edit = Movement.query.filter_by(id=move.id).first()
        move_edit.status = choice
        db.session.commit()
        return True
    except:
        return False


def check_move_event(user,id):
    try:
        move = Movement.query.filter_by(event_id=id, user_id=user.id).first()
        if move:
            return move
        else:
            return False
    except:
        return False


def member_event(id):
    try:
        move_member = Movement.query.filter_by(event_id=id).all()
        return move_member
    except:
        return False


def all_movement(user):
    try:
        all_movement = Movement.query.filter_by(user_id=user.id).all()
        return all_movement
    except:
        return False


def team_movement(team):
    try:
        all_member = Member.query.filter_by(team_id=team.id).all()
        all_move = []
        for el in all_member:
            all_user_move = Movement.query.filter(Movement.user_id==el.user_id,Movement.status==True).all()
            if all_user_move:
                el_data = {'name': el.name, 'position': el.position, 'count': len(all_user_move)}
                all_move.append(el_data)
            elif el.position != 'Creater':
                el_data = {'name': el.name, 'position': el.position, 'count': 0}
                all_move.append(el_data)
        return all_move
    except:
        return False


def get_members(team):
    try:
        article_members = Member.query.order_by(Member.date).filter_by(team_id=team.id).all()
        return article_members
    except:
        return False


def edit_member(data,id):
    try:
        member = Member.query.filter_by(id=id).first()
        member.position = data['type']
        db.session.commit()
        return True
    except:
        return False


def get_all_post(team):
    try:
        all_post = Post.query.order_by(Post.date.desc()).filter_by(team_id=team.id).all()
        return all_post
    except:
        return False 


def add_post(data, team):
    try:
        post = Post(name=data['name'], text=data['text'], team_id=team.id)
        db.session.add(post)
        db.session.commit()
        return True
    except:
        return False


def get_post(id):
    try:
        article_post = Post.query.filter_by(id=id).first()
        return article_post
    except:
        return False


def edit_post(data,id):
    try:
        post = Post.query.filter_by(id=id).first()
        post.name = data['name']
        post.text = data['text']
        db.session.commit()
        return True
    except:
        return False


def delete_post(id):
    try:
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        return True
    except:
        return False


def send_mail(mail, team, title):
    try:
        return requests.post(
            "https://api.eu.mailgun.net/v3/mail.volchonok.media/messages",
            auth=("api", "key-60808e60e192de1e03df73d6251cdce7"),
            data={"from": "app@mail.volchonok.media",
                "to": [mail],
                "subject": title,
                "template": "link_to_the_team",
                "v:link": team.link,
                "v:team": team.name
                })
    except:
        return False

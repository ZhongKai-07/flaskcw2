from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from exts import db
from form import EditForm, SelectForm, MessageForm, CommentForm
from model import User, Course, Message, Comment
import requests

main_bp = Blueprint('main', __name__)


@main_bp.route('/index/<string:username>')
@login_required
def index(username):
    #if current_user.is_authenticated:
        #return render_template('main/index', username=current_user.username)

    city = '成都'
    if city:
        resp = requests.get('http://apis.juhe.cn/simpleWeather/query?key=de7cd4c084284473dea90dd001649aff&city=%s' % city)
    # 查询城市
    newcity = resp.json()['result']['city']
    # 查询当前天气
    realtime = resp.json()['result']['realtime']


    return render_template('main/index.html', username=username, newcity=newcity, realtime=realtime)


@main_bp.route('/index/<string:username>/info', methods=['GET', 'POST'])
@login_required
def info(username):
    user = User.query.filter_by(username=username).first()
    form = EditForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        print("\nold password:", old_password)
        print("\nnew password:", new_password)
        if user.validate_password(old_password):
            user.set_password(new_password)
            db.session.add(user)
            db.session.commit()
            flash('Password updated', 'success')
            print("\nxxxxxx")
            return redirect(url_for('main.info', username=username))
    print("\neeeeee")
    return render_template('main/info.html',form=form, user=user)


@main_bp.route('/index/<string:username>/view_course', methods=['GET', 'POST'])
@login_required
def view_course(username):
    user = User.query.filter_by(username=username).first()
    course_list = user.courses

    return render_template('main/view.html', username=username, course_list=course_list)


@main_bp.route('/index/<string:username>/select_course', methods=['GET', 'POST'])
@login_required
def select(username):
    all_course = Course.query.all()
    form = SelectForm()
    if form.validate_on_submit():
        if not form.module.data:
            flash('Please enter the course code', 'warning')
        else:
            module = form.module.data
            courselist = Course.query.filter_by(module=module).first()
            if not courselist:
                flash('The code is wrong', 'warning')
            else:
                user = User.query.filter_by(username=username).first()
                if courselist in user.courses:
                    flash('You have already selected this course', 'warning')
                else:
                    user.courses.append(courselist)
                    db.session.add(user)
                    db.session.commit()
                    flash('Select Successful', 'success')
                    return redirect(url_for('main.select', username=username))
    return render_template('main/select.html',form=form, all_course=all_course, username=username)


@main_bp.route('/love')
@login_required
def love():
    message_id = request.args.get('mid')
    tag = request.args.get('tag')
    
    message = Message.query.get(message_id)
    if tag == '1':
        message.love_num -= 1
    else:
        message.love_num += 1
    db.session.commit()
    return jsonify(num=message.love_num)

    


@main_bp.route('/index/<string:username>/message', methods=['GET', 'POST'])
@login_required
def message(username):
    user = User.query.filter_by(username=username).first()
    form = MessageForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        message = Message()
        message.title = title
        message.text = text
        message.user_id = user.id
        db.session.add(message)
        db.session.commit()
        flash('Publish Successful', 'success')
        return redirect(url_for('main.message', username=username))
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('main/message.html', form=form, messages=messages)


@main_bp.route('/index/<string:username>/reply', methods=['GET', 'POST'])
@login_required
def reply(username):
    mid = request.args.get('mid')
    user = User.query.filter_by(username=username).first()
    message = Message.query.filter_by(id=mid).first()
    
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment()
        comment.body = text
        comment.user_id = user.id
        comment.message_id = message.id
        db.session.add(comment)
        db.session.commit()
        flash('You have publish the comment successfully', 'success')
        return redirect(url_for('main.reply', username=username, mid=mid))
    comments = Comment.query.filter_by(message_id=mid).order_by(Comment.timestamp.desc()).all()
    return render_template('main/reply.html', form=form, username=username, message=message, comments=comments)


@main_bp.route('/process', methods=['POST', 'GET'])
@login_required
def process():
    name = request.form['name']
    email = request.form['email']
    if name and email:
        return jsonify({'name':name})
    return jsonify({'error':'Missing data!'})



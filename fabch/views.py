import os
import payjp
import pdb;
from functools import wraps
from flask import request, redirect, url_for, render_template, \
        flash, abort, jsonify, session, g
from fabch import app, db
from fabch.models import Lectures, User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# PAY.JP 
SECRET_KEY = os.environ['SECRET_KEY']
PUBLIC_KEY = os.environ['PUBLIC_KEY']
payjp.api_key = SECRET_KEY

# setup login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "ログインしてください。"
login_manager.login_message_category = "info"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


# Routing -----------------------------------------------------
@app.route('/')
def home():
    lectures = Lectures.query.order_by(Lectures.id).filter(Lectures.lecid == 1)
    return render_template('home.html', lectures=lectures)


# クラス一覧ページへのルーティング
@app.route('/class')
def cls():
    lectures = Lectures.query.order_by(Lectures.id).filter(Lectures.lecid == 1)
    return render_template('class.html', lectures=lectures)


# 個別クラスページへのルーティング
@app.route('/class/<clsid>')
def rectures(clsid):
    lectures = Lectures.query.order_by(Lectures.id).\
            filter(Lectures.clsid == clsid)
            
    return render_template('lectures.html', lectures=lectures)


# 個別レクチャーページへのルーティング
@app.route('/class/<clsid>/lec<lecid>')
@login_required
def recture(clsid,lecid):
    one_lecture = Lectures.query.order_by(Lectures.id).\
            filter(Lectures.clsid == clsid).filter(Lectures.lecid == lecid)
    lectures = Lectures.query.order_by(Lectures.id).\
            filter(Lectures.clsid == clsid)

    return render_template('lecture.html', one_lecture=one_lecture, lectures=lectures)


# signin, signup -------------------------------------------------
# 個別ユーザーページ
@app.route('/users/mypage/')
@login_required
def mypage():
    if 'user_id' in session:
        id = session['user_id']
        user = User.query.filter_by(id=id).first()
    return render_template('user/mypage.html', name=user.name )


# サインアップ
@app.route('/users/create/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User(name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'])

        # 同じEmailで二つアカウントを作成させない
        old_user = User.query.filter_by(email=user.email).first()
        if old_user == None:
            db.session.add(user)
            db.session.commit()
            flash('アカウントを作成しました。')
            return redirect(url_for('login'))
        else:
            flash("既にアカウントが作成されています")
    return render_template('signup.html')


# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                request.form['email'], request.form['password'])
        if authenticated:
            session['user_id'] = user.id
            flash('ログインしました。')
            return redirect(url_for('home'))
        else:
            flash('ユーザー名、パスワードが正しくありません。')
    return render_template('login.html')


# ログアウト
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('home'))


# PAY.JP -----------------------------------------------------
@app.route('/pay', methods=['POST'])
def pay():

    # 顧客を作成
    customer = payjp.Customer.create(
        email='example@pay.jp',
        card=request.form['payjp-token']
    )

    # プランを作成
    plan = payjp.Plan.create(
        amount=980,
        currency='jpy',
        interval='month'
    )

    # 定期課金を作成
    payjp.Subscription.create(
        plan=plan.id,
        customer=customer.id
    )
    flash('会員登録が完了しました。')
    return redirect(url_for('home'))


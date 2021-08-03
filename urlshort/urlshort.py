from flask import render_template, request, \
                    redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp=Blueprint('urlshort',__name__)

@bp.route('/')
def home():
    return render_template('home.html' , title='HomePage' , codes=session.keys())

@bp.route('/your-url',methods=["POST","GET"])
def your_url():
    if request.method=="POST":
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls=json.load(urls_file)

        if request.form.get('code') in urls.keys():
            flash('That short name already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form.get('code')]={'url':request.form['url']}
        else:
            f=request.files['file']
            full_name=request.form['code']+"_"+secure_filename(f.filename)
            f.save('urlshort/static/user_files/'+full_name)
            urls[request.form.get('code')]={'File':full_name}

        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form.get('code')]=True
        return render_template('your_url.html',code=request.form.get('code'),)
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls=json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='user_files/'+urls[code]["File"]))
    return abort(404)




@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@bp.route('/urls')
def urls():
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urlspair=json.load(urls_file)
            return render_template('all_urls.html',codes=urlspair.keys())
    else:
        return render_template('all_urls.html',codes=None)

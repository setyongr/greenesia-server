from flask import Blueprint, render_template, request, redirect
from common import model
from werkzeug import secure_filename
import os
admin = Blueprint('admin', __name__)
# admin.config['UPLOAD_FOLDER'] = '/static/'


@admin.route('/reward')
def reward():
    return render_template('reward.html', data=model.Reward.objects())

@admin.route('/add_reward', methods=['GET'])
def add_reward():
    return render_template('add_reward.html')

@admin.route('/delete_reward', methods=['GET'])
def del_reward():
    rew = model.Reward.objects(id=request.args['id'])[0]
    rew.delete()
    return redirect('/admin/')
@admin.route('/process_add_reward', methods=['POST'])
def process_reward():
    f = request.files['file']
    fn = secure_filename(f.filename)
    f.save('static/'+fn)
    rew = model.Reward(
        nama = request.form['nama'],
        gambar = fn,
        min_point = request.form['min_point']
    )
    rew.save()
    return redirect('/admin/reward')


@admin.route('/event')
def event():
    return render_template('event.html', data=model.Event.objects())

@admin.route('/add_event', methods=['GET'])
def add_event():
    return render_template('add_event.html')

@admin.route('/delete_event', methods=['GET'])
def del_event():
    rew = model.Event.objects(id=request.args['id'])[0]
    rew.delete()
    return redirect('/admin/event')
@admin.route('/process_add_event', methods=['POST'])
def process_event():
    f = request.files['file']
    fn = secure_filename(f.filename)
    f.save('static/'+fn)
    rew = model.Event(
        nama = request.form['nama'],
        deskripsi = request.form['deskripsi'],
        tanggal = request.form['tanggal'],
        gambar = fn,
        alamat = request.form['alamat'],
        lokasi = [float(request.form['lng']), float(request.form['lat'])],
        organizer = request.form['organizer']
    )
    rew.save()
    return redirect('/admin/event')
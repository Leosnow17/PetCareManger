import os
import configparser

import smtplib
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText

from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import User, Pets, Health, Activity, Food, Vets, Consultation, Povedenie, Freetime
from . import UPLOAD_FOLDER_PETS,UPLOAD_FOLDER_VETS, ALLOWED_EXTENSIONS

main = Blueprint('main', __name__)
config = configparser.ConfigParser()
config.read("config.ini")


def send_email(addr_to, body):
    addr_from = config["send_email"]["addr_from"]

    password_em = config["send_email"]["password_em"]

    msg = MIMEMultipart()
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to
    msg['Subject'] = 'Отклик на ваш пост по поиску тиммейтов'

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(addr_from, password_em)
    server.send_message(msg)
    server.quit()


@main.route('/')
def index():
    return render_template('new_index.html')


@main.route('/services')
@login_required
def services():
    q = request.args.get('q')
    if q:
        vet = Vets.query.filter(Vets.tag.contains(f'{q}'))
    else:
        vet = Vets.query.all()
    return render_template('new_search_teammates.html', data=vet)


# @main.route('/stats')
# @login_required
# def stats():
#     q = request.args.get('q')
#     if q:
#         items = Item.query.filter(Item.tag.contains(f'{q}'))
#     else:
#         items = Item.query.all()
#     return render_template('stats.html', data=items)


# @main.route('/game/<int:id>')
# @login_required
# def game(id):
#     game_q = Game.query.filter_by(id=id).first()
#     shops = str(game_q.shops).split(', ')
#     trades = str(game_q.trade).split(', ')
#     guides = str(game_q.guide).split(', ')
#     return render_template(
#         'game.html',
#         data=game_q,
#         pic=f'/static/images/{game_q.name}.png',
#         shops=shops,
#         trades=trades,
#         guides=guides
#     )


@main.route('/create-pet', methods=['POST', 'GET'])
@login_required
def create_pet():
    id = Pets.query.all()
    my_id = len(id) + 1
    if request.method == "POST":
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        height = request.form.get('height')
        weight = request.form.get('weight')
        gender = request.form.get('gender')
        vid = request.form.get('vid')
        breed = request.form.get('breed')
        hair_length = request.form.get('hair_length')

        # if len(title) < 1 or len(description) < 1 or len(tag) < 1:
        #     flash("Заполните все поля")
        #     return redirect(url_for('main.create-post'))

        new_pet = Pets(
            id=my_id,
            user_id=current_user.id,
            name=name,
            birth_date=birth_date,
            height=height,
            weight=weight,
            gender=gender,
            vid=vid,
            breed=breed,
            hair_length=hair_length,
        )

        db.session.add(new_pet)
        db.session.commit()

        return redirect(f'/health-pet/{new_pet.id}')
    else:
        return render_template('new_offer.html', data=my_id)


@main.route('/health-pet/<int:id>', methods=['GET', 'POST'])
@login_required
def health_pet(id):
    pet = Pets.query.filter_by(id=id).first()
    if request.method == "POST":
        problems = request.form.get('problems')
        other = request.form.get('other')
        result = Health(
            id=id,
            pet_id=id,
            dermatological_problems=('dp' in problems),
            urolithiasis_disease=('ud' in problems),
            diabetes=('db' in problems),
            heart_failure=('hf' in problems),
            cardiomyopathy=('cm' in problems),
            mitral_stenosis=('ms' in problems),
            pregnancy_and_lactation=('pl' in problems),
            allergies_and_intolerances=('ai' in problems),
            stressful_conditions_and_adaptation=('sca' in problems),
            gum_deseases=('gd' in problems),
            caries=('cr' in problems),
            overweight=('ow' in problems),
            food_allergies=('fa' in problems),
            indigestion=('ind' in problems),
            liver_deseases=('ld' in problems),
            kidney_failure=('kf' in problems),
            diseases_of_the_musculoskeletal_system=('dms' in problems),
            recovery_period_after_illness=('rpi' in problems),
            other=other,
        )

        db.session.add(result)
        db.session.commit()
        return redirect(f'/activity-pet/{id}')
    else:
        return render_template('health_pet.html', data=pet)


@main.route('/activity-pet/<int:id>', methods=['GET', 'POST'])
@login_required
def activity_pet(id):
    pet = Pets.query.filter_by(id=id).first()
    if request.method == "POST":
        activites = request.form.get('activites')
        other = request.form.get('other')
        gz = request.form.get('gz')
        lvl = request.form.get('lvl')
        result = Activity(
            id=pet.id,
            pet_id=pet.id,
            progulki=('dp' in activites),
            igru_s_ball=('ud' in activites),
            igri_v_pomeshenii=('db' in activites),
            run=('hf' in activites),
            plavanie=('cm' in activites),
            agility=('ms' in activites),
            haiking=('pl' in activites),
            truks=('ai' in activites),
            ioga=('sca' in activites),
            run_with_bike=('gd' in activites),
            other=other,
            everyday=(gz is '1'),
            three_four_times=(gz is '2'),
            one_two_times=(gz is '3'),
            less_one_time=(gz is '4'),
            low=(lvl is 'l'),
            medium=(lvl is 'm'),
            hard=(lvl is 'h'),
        )
        db.session.add(result)
        db.session.commit()
        return redirect(f'/food-pet/{id}')
    else:
        return render_template('activity_pet.html', data=pet)


@main.route('/food-pet/<int:id>', methods=['GET', 'POST'])
@login_required
def food_pet(id):
    pet = Pets.query.filter_by(id=id).first()
    if request.method == "POST":
        korm = request.form.get('korm')
        eda = request.form.get('eda')
        other = request.form.get('other')
        allerg = request.form.get('allerg')
        result = Food(
            id=pet.id,
            pet_id=pet.id,
            sukhoi_korm=('1' in korm),
            vlashniy=('2' in korm),
            combinirovanniy=('3' in korm),
            meet=('1' in eda),
            fish=('2' in eda),
            fructs=('3' in eda),
            zernoviy_cultures=('4' in eda),
            other_likely=other,
            chicken=('1' in allerg),
            cow_meet=('2' in allerg),
            fish_meet=('3' in allerg),
            milk=('4' in allerg),
            eggs=('5' in allerg),
            other=('6' in allerg),
        )
        db.session.add(result)
        db.session.commit()
        return redirect(f'/povedenie-pet/{id}')
    else:
        return render_template('food_pet.html', data=pet)


@main.route('/povedenie-pet/<int:id>', methods=['GET', 'POST'])
@login_required
def povedenie_pet(id):
    pet = Pets.query.filter_by(id=id).first()
    if request.method == "POST":
        soc = request.form.get('soc')
        ter = request.form.get('ter')
        nez = request.form.get('nez')
        reac = request.form.get('reac')
        priv = request.form.get('priv')
        agr = request.form.get('agr')
        lovg = request.form.get('lovg')
        stres = request.form.get('stres')
        lovedu = request.form.get('lovedu')

        result = Povedenie(
            id=pet.id,
            pet_id=pet.id,
            lubit_obshectvo=('1' in soc),
            stesnyaetsa=('2' in soc),
            predpochitaet_peoples=('3' in soc),
            territorialnost=(ter is not None),
            nezavisimiy=('1' in nez),
            zavisit_ot_vladeltsa=('2' in nez),
            skritye=('1' in reac),
            aggressivnoe_povedenie=('2' in reac),
            projavlenie_apatii=('3' in reac),
            ne_imeet=('1' in priv),
            imeet=('2' in priv),
            aggressor_peoples=('1' in agr),
            aggressor_animals=('2' in agr),
            igrushki=('1' in lovg),
            activnye_igri=('2' in lovg),
            spokoinye=('3' in lovg),
            easy=('1' in stres),
            hard=('2' in stres),
            easy_for_learn=('1' in lovedu),
            hard_for_learn=('2' in lovedu),
        )

        db.session.add(result)
        db.session.commit()
        return redirect(f'/own')
    else:
        return render_template('povedenie-pet.html', data=pet)


@main.route('/visits-to-vets-pet/<int:id>', methods=['GET', 'POST'])
@login_required
def visits_to_vets_pet(id):
    pet = Pets.query.filter_by(id=id).first()
    if request.method == "POST":
        date = request.form.get('date')
        osmotr = request.form.get('osmotr')
        vactination = request.form.get('vactination')
        dental_procedury = request.form.get('dental_procedury')
        lab_issl = request.form.get('lab_issl')
        procedury_uhod = request.form.get('procedury_uhod')
        microchipirovanye = request.form.get('microchipirovanye')
        heal_for_blohi = request.form.get('heal_for_blohi')
        consultation = request.form.get('consultation')
        other = request.form.get('other')
        recommendation = request.form.get('recommendation')
        result = Food(
            id=pet.id,
            pet_id=pet.id,
            date=date,
            osmotr=osmotr,
            vactination=vactination,
            dental_procedury=dental_procedury,
            lab_issl=lab_issl,
            procedury_uhod=procedury_uhod,
            microchipirovanye=microchipirovanye,
            heal_for_blohi=heal_for_blohi,
            consultation=consultation,
            other=other,
            recommendation=recommendation,
        )
        db.session.add(result)
        db.session.commit()
        return redirect(f'/visits-to-vets-pet/{id}')
    else:
        return render_template('.html', data=pet)


@main.route('/profile')
@login_required
def profile():
    return render_template('new_profile.html')


@main.route('/own')
@login_required
def own_pets():
    """ Мои питомцы """
    if current_user.email == 'admin@mail.ru':
        pets = Pets.query.all()
    else:
        pets = Pets.query.filter_by(user_id=current_user.id)
    return render_template('new_my_items.html', data=pets)


@main.route('/pet/<int:id>', methods=['GET'])
@login_required
def pet_info(id):
    """Профиль питомца"""
    pet = Pets.query.filter_by(id=id).first()
    return render_template('new_info.html', data=pet, pic=f'/static/images/pets/{pet.id}.png')


@main.route('/change/<int:num>', methods=['GET'])
@login_required
def change_get(num):
    pet = Pets.query.filter_by(id=num).first()
    return render_template("new_change.html", data=pet)


@main.route('/change/<int:num>', methods=['POST'])
@login_required
def change(num):
    if current_user.email == 'admin@mail.ru':
        pets = Pets.query.all()
    else:
        pets = Pets.query.filter_by(user_id=current_user.id).all()
    name = request.form.get('name')
    birth_date = request.form.get('birth_date')
    height = request.form.get('height')
    weight = request.form.get('weight')
    gender = request.form.get('gender')
    vid = request.form.get('vid')
    breed = request.form.get('breed')
    hair_length = request.form.get('hair_length')
    pet = Pets.query.filter_by(id=num).first()

    new_pet = Pets(
        id=num,
        user_id=current_user.id,
        name=name,
        birth_date=birth_date,
        height=height,
        weight=weight,
        gender=gender,
        vid=vid,
        breed=breed,
        hair_length=hair_length,
    )
    if pet in pets:
        db.session.delete(pet)
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/own')

    else:
        flash('У вас нет доступа к чужим питомцам')
        return redirect(url_for("main.profile"))


@main.route('/delete/<int:num>')
@login_required
def delete(num):
    if current_user.email == 'admin@mail.ru':
        posts_id = Pets.query.all()
    else:
        posts_id = Pets.query.filter_by(user_id=current_user.id).all()
    post = Pets.query.filter_by(id=num).first()

    if post in posts_id:
        db.session.delete(post)
        db.session.commit()
        return redirect('/profile')
    else:
        flash('Вам не принадлежит этот питомец. Возможно произошла ошибка')
    return redirect('/own')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/uploads/pets/<int:id>', methods=['GET', 'POST'])
def upload_file_pets(id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_PETS, str(id) + ".png"))
            return redirect(url_for(f'main.create_pet({id})'))
    return '''
       <!doctype html>
       <title>Загрузите файл</title>
       <h1>Upload new File</h1>
       <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
       </form>
       '''


@main.route('/uploads/vets/<int:id>', methods=['GET', 'POST'])
def upload_file_vets(id):
    vet = Vets.query.filter_by(id=id).first()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_VETS, str(id) + ".png"))
            if vet == None:
                return redirect(url_for('main.index'))
            else:
                return redirect(url_for('main.index'))
    return '''
       <!doctype html>
       <title>Загрузите файл</title>
       <h1>Upload new File</h1>
       <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
       </form>
       '''

# @main.route('/items/<name>')
# def uploaded_file(name):
#     return send_from_directory(UPLOAD_FOLDER, name)


@main.route('/services/<int:id>', methods=['GET', 'POST'])
@login_required
def vet_info(id):
    vet = Vets.query.filter_by(id=id).first()
    pets = Pets.query.filter_by(user_id=current_user.id)

    return render_template('vet_info.html', data=vet, pets=pets, pic=f'/static/images/pets/{vet.id}.png')


@main.route('/make_consultation/<int:id>', methods=['GET', 'POST'])
@login_required
def make_consultation(id):
    vet = Vets.query.filter_by(id=id).first
    cons = Consultation.query.all().first
    pets = Pets.query.filter_by(user_id=current_user.id)
    freetime = Freetime.query.filter_by(vet_id=vet.id)
    if request.method == "POST":
        pet_name = request.form.get('pet_name')
        date = request.form.get('date')
        adress = request.form.get('adress')
        time = request.form.get('time')
        pet = Pets.query.filter_by(name=pet_name)
        if vet.email is not None:
            send_email(vet.email,
                       f" Завяка на консультацию! \n"
                       f" {current_user.name} хочет записаться на консультацию."
                       f"Его контактные данные - {current_user.phone}, {current_user.email}  \n"
                       f"Назначенные dремя и дата - {time}, {date}")
        cons = Consultation(id=cons.id + 1, pet_id=pet.id, date=date, adress=adress, time=time)
        db.session.add(cons)
        db.session.commit()
        flash('Вы успешно записались на консультацию')
        return redirect('/services')
    else:
        return render_template(
            '.html',
            data=[pet.name for pet in pets],
            vet=vet,
            freetime_date=freetime.date,
            freetime_time=freetime.time
        )

from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    """Данные о пользователе"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    city = db.Column(db.String(1000), nullable=False)
    pets = db.relationship('Pets', backref='user')


class Vets(UserMixin, db.Model):
    """Данные о ветеринарах"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    timetable = db.Column(db.String(1000), nullable=False)
    adress = db.Column(db.String(1000), nullable=False)
    vet_phone = db.Column(db.String(1000), nullable=False)
    vet_mail = db.Column(db.String(1000), nullable=False)
    education = db.Column(db.String(1000), nullable=False)
    awards = db.Column(db.String(1000), nullable=False)
    specialisation = db.Column(db.String(1000), nullable=False)
    experience = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=True, default=5)
    tag = db.Column(db.String(50), nullable=True)
    # price = db.Column(db.String(50), nullable=False)


class Pets(UserMixin, db.Model):
    """Данные о посте"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    vid = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    hair_length = db.Column(db.String(100), nullable=False)  # nullable=True
    health = db.relationship('Health', backref='pet')
    activity = db.relationship('Activity',  backref='pet')
    food = db.relationship('Food',  backref='pet')
    povedenie = db.relationship('Povedenie',  backref='pet')


class Health(db.Model):
    """Профиль питомца - здоровье"""

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    dermatological_problems = db.Column(db.Boolean, default=False)
    urolithiasis_disease = db.Column(db.Boolean, default=False)
    diabetes = db.Column(db.Boolean, default=False)
    heart_failure = db.Column(db.Boolean, default=False)
    cardiomyopathy = db.Column(db.Boolean, default=False)
    mitral_stenosis = db.Column(db.Boolean, default=False)
    pregnancy_and_lactation = db.Column(db.Boolean, default=False)
    allergies_and_intolerances = db.Column(db.Boolean, default=False)
    stressful_conditions_and_adaptation = db.Column(db.Boolean, default=False)
    gum_deseases = db.Column(db.Boolean, default=False)
    caries = db.Column(db.Boolean, default=False)
    overweight = db.Column(db.Boolean, default=False)
    food_allergies = db.Column(db.Boolean, default=False)
    indigestion = db.Column(db.Boolean, default=False)
    liver_deseases = db.Column(db.Boolean, default=False)
    kidney_failure = db.Column(db.Boolean, default=False)
    diseases_of_the_musculoskeletal_system = db.Column(db.Boolean, default=False)
    recovery_period_after_illness = db.Column(db.Boolean, default=False)
    other = db.Column(db.String(1000), nullable=True)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    progulki = db.Column(db.Boolean, default=False)
    igru_s_ball = db.Column(db.Boolean, default=False)
    igri_v_pomeshenii = db.Column(db.Boolean, default=False)
    run = db.Column(db.Boolean, default=False)
    plavanie = db.Column(db.Boolean, default=False)
    agility = db.Column(db.Boolean, default=False)
    haiking = db.Column(db.Boolean, default=False)
    truks = db.Column(db.Boolean, default=False)
    ioga = db.Column(db.Boolean, default=False)
    run_with_bike = db.Column(db.Boolean, default=False)
    other = db.Column(db.String(1000), nullable=True)
    # физ активности
    everyday = db.Column(db.Boolean, default=False)
    three_four_times = db.Column(db.Boolean, default=False)
    one_two_times = db.Column(db.Boolean, default=False)
    less_one_time = db.Column(db.Boolean, default=False)
    # уровень активности
    low = db.Column(db.Boolean, default=False)
    medium = db.Column(db.Boolean, default=False)
    hard = db.Column(db.Boolean, default=False)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    # тип питания
    sukhoi_korm = db.Column(db.Boolean, default=False)
    vlashniy = db.Column(db.Boolean, default=False)
    combinirovanniy = db.Column(db.Boolean, default=False)
    # любимые продукты
    meet = db.Column(db.Boolean, default=False)
    fish = db.Column(db.Boolean, default=False)
    fructs = db.Column(db.Boolean, default=False)
    zernoviy_cultures = db.Column(db.Boolean, default=False)
    other_likely = db.Column(db.String(1000), nullable=True)
    # продукты на которые есть аллергия
    chicken = db.Column(db.Boolean, default=False)
    cow_meet = db.Column(db.Boolean, default=False)
    fish_meet = db.Column(db.Boolean, default=False)
    milk = db.Column(db.Boolean, default=False)
    eggs = db.Column(db.Boolean, default=False)
    other = db.Column(db.Boolean, default=False)


class Povedenie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    # социализация
    lubit_obshectvo = db.Column(db.Boolean, default=False)
    stesnyaetsa = db.Column(db.Boolean, default=False)
    predpochitaet_peoples = db.Column(db.Boolean, default=False)
    # территориальность
    territorialnost = db.Column(db.Boolean, default=False)
    # независимость
    nezavisimiy = db.Column(db.Boolean, default=False)
    zavisit_ot_vladeltsa = db.Column(db.Boolean, default=False)
    # реакция на стрессовые ситуации
    skritye = db.Column(db.Boolean, default=False)
    aggressivnoe_povedenie = db.Column(db.Boolean, default=False)
    projavlenie_apatii = db.Column(db.Boolean, default=False)
    # привычки
    ne_imeet = db.Column(db.Boolean, default=False)
    imeet = db.Column(db.Boolean, default=False)
    # агрессивность
    aggressor_peoples = db.Column(db.Boolean, default=False)
    aggressor_animals = db.Column(db.Boolean, default=False)
    # любовь к играм
    igrushki = db.Column(db.Boolean, default=False)
    activnye_igri = db.Column(db.Boolean, default=False)
    spokoinye = db.Column(db.Boolean, default=False)
    # стрессоустойчивость
    easy = db.Column(db.Boolean, default=False)
    hard = db.Column(db.Boolean, default=False)
    # любовь к обучению
    easy_for_learn = db.Column(db.Boolean, default=False)
    hard_for_learn = db.Column(db.Boolean, default=False)


class VisitsToVet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    # процедуры
    date = db.Column(db.Date, nullable=False)
    osmotr = db.Column(db.Boolean, default=False)
    vactination = db.Column(db.Boolean, default=False)
    dental_procedury = db.Column(db.Boolean, default=False)
    lab_issl = db.Column(db.Boolean, default=False)
    procedury_uhod = db.Column(db.Boolean, default=False)
    microchipirovanye = db.Column(db.Boolean, default=False)
    heal_for_blohi = db.Column(db.Boolean, default=False)
    consultation = db.Column(db.Boolean, default=False)
    other = db.Column(db.Boolean, default=False)
    recommendation = db.Column(db.String(1000), nullable=True)


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    date = db.Column(db.Date, nullable=False)
    adress = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.String(1000), nullable=False)
    # price = db.Column(db.String(1000), nullable=True)


class Freetime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.id'))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))

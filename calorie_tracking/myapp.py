from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.sql.functions import user
from wtforms import StringField, PasswordField, IntegerField, FloatField, SelectField, SubmitField, SelectMultipleField, FieldList
from wtforms.validators import InputRequired, Email, Length, DataRequired, NumberRange
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from calculate_calories import findx, find_food
# Initialize app, database, and login manager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Example API URL for food calorie lookup
API_URL = "https://api.spoonacular.com/food/ingredients/search"  # Replace with your API URL
API_KEY = 'your_api_key'  # Replace with your API key




## databases
# Create User and Calorie models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(150), nullable=False)




# class CalorieIntake(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.String(50), nullable=False)
#     time = db.Column(db.String(50), nullable=False)
#     calories = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(200), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
# class CalorieBurned(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.String(50), nullable=False)
#     time = db.Column(db.String(50), nullable=False)
#     calories_burned = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(200), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class FoodIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    food = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    serving_unit = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    sodium = db.Column(db.Float, nullable=False, default=0)
    fiber = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<FoodIntake {self.food}>'


class ExerciseDone(db.Model):
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    exercise = db.Column(db.String(200), nullable=False)
    calories_burned = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<ExerciseDone {self.exercise}>'


class Custom_item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    food = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    unit = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    sodium = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Custom_item {self.food}>'

class CustomMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    total_calories = db.Column(db.Float, default=0)
    total_protein = db.Column(db.Float, default=0)
    total_sugar = db.Column(db.Float, default=0)
    total_carbohydrates = db.Column(db.Float, default=0)
    total_fiber = db.Column(db.Float, default=0)
    total_sodium = db.Column(db.Float, default=0)

    # Relationship to MealItems (instead of using secondary)
    meal_items = db.relationship('MealItems', backref='meal', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<CustomMeal {self.name}>'


class MealItems(db.Model):
    meal_id = db.Column(db.Integer, db.ForeignKey('custom_meal.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('custom_item.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationship to Custom_item (explicitly define it)
    item = db.relationship('Custom_item', backref='meal_associations')

    def __repr__(self):
        return f'<MealItem Meal: {self.meal_id}, Item: {self.item_id}, Qty: {self.quantity}>'


# class Custom_meal(db.Model):





# forms
# User registration form
class RegistrationForm(FlaskForm):
    name = StringField('What is your name?', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    age = IntegerField('Age', validators=[InputRequired()], )
    weight = FloatField('Weight (kg)', validators=[InputRequired()])
    height = FloatField('Height (cm)', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])


class EditUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=150)])
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=1)])
    height = FloatField('Height (cm)', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Changes')

# User login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])



class FoodIntakeForm(FlaskForm):
    food = StringField('Enter Food Item', validators=[InputRequired()])
    submit = SubmitField('Add Food Intake')

class ExerciseDoneForm(FlaskForm):
    exercise = StringField('Enter Exercise Name', validators=[InputRequired()])
    submit = SubmitField('Add Exercise')

class CustomItemForm(FlaskForm):
    food = StringField('Enter Food Item', validators=[InputRequired()])
    description = StringField('Enter Description', validators=[])
    # email = StringField('Enter Email', validators=[InputRequired(), Email()])
    unit = SelectField('Unit', choices=['unit','gm', 'ml',])
    quantity = IntegerField('Enter Quantity', validators=[InputRequired(), NumberRange(min=1)])
    calories = FloatField('Enter Calories(Kcal)', validators=[InputRequired()], render_kw={"placeholder": 0})
    protein = FloatField('Enter Protein(gm)', validators=[InputRequired()], render_kw={"placeholder": 0})
    sugar  = FloatField('Enter Sugar(gm)', validators=[InputRequired()], render_kw={"placeholder": 0})
    carbohydrates = FloatField('Enter Carbohydrates(gm)', validators=[InputRequired()], render_kw={"placeholder": 0})
    fiber = FloatField('Enter Fiber(gm)', validators=[InputRequired()], render_kw={"placeholder": 0})
    sodium = FloatField('Enter Sodium(mg)', validators=[InputRequired()], render_kw={"placeholder": 0})
    submit = SubmitField('Add Custom Item')


class CustomMealForm(FlaskForm):
    name = StringField('Meal Name', validators=[InputRequired()])
    items = SelectMultipleField('Select Items', coerce=int)  # Only store selected items
    submit = SubmitField('Create Custom Meal')


with app.app_context():
    db.create_all()

# some neccesaary functions
from datetime import datetime, timedelta

def get_date_range(report_type):
    today = datetime.now().date()  # Only get the date part
    if report_type == 'daily':
        start_date = today
        end_date = today
    elif report_type == 'weekly':
        start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
        end_date = today
    elif report_type == 'monthly':
        start_date = today.replace(day=1)  # Start of the month
        end_date = today
    else:
        raise ValueError("Invalid report type")
    return start_date, end_date






# basic login and logout


# Load user function for login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



# Home route after login
@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home_logged_in.html', name=current_user.name)
    return render_template('home_not_logged_in.html')


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name =form.name.data, email=form.email.data, password=form.password.data,
                    age=form.age.data, weight=form.weight.data,
                    height=form.height.data, gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Password check
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)



# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



# added functionality
# Add calorie intake route
@app.route('/add_calorie_intake', methods=['GET', 'POST'])
@login_required
def add_calorie_intake():
    form = FoodIntakeForm()

    if form.validate_on_submit():
        food_query = form.food.data
        print(food_query)

        # Make the API request to fetch food calorie data
        data , missing = find_food(food_query)
        print(data, missing)
        if data:
            for food in data:
                new_intake = FoodIntake(email=current_user.email,date = food['date'] , time = food['time'],food=food['food'],serving_unit = food['serving_unit'], calories=food['calories'],
                                        description=food['description'], quantity=food['quantity'], protein = food['protein'],carbohydrates = food['carbohydrates'],
                                        sodium = food['sodium'],sugar = food['sugar'], fiber = food['fiber'])
                db.session.add(new_intake)
                db.session.commit()

            flash('Food intake added successfully!', 'success')
            return redirect(url_for('home'))  # Redirect to home after adding intake
        elif missing:
            print(missing)
            for food in missing:
                flash(f'{food} not found!', 'danger')

    return render_template('add_calorie_intake.html', form=form)




# Add calorie burned route
@app.route('/add_exercise_done', methods=['GET', 'POST'])
@login_required
def add_exercise_done():
    form = ExerciseDoneForm()

    if form.validate_on_submit():
        exercise_query = form.exercise.data

        # Example: Simple calories burned calculation based on exercise
        # This is a placeholder logic, adjust according to your needs
        exercise_calories_burned = findx(user_input=exercise_query, gender=current_user.gender, weight=current_user.weight,age=current_user.age, height=current_user.height)  # Replace with actual logic

        if exercise_calories_burned:
            # Create a new ExerciseDone record and save it to the database
            for exercise in exercise_calories_burned:
                new_exercise = ExerciseDone(email=current_user.email, exercise=exercise['exercise'], date=exercise['date'],time=exercise['time'],
                                            calories_burned=exercise['calories'], description=exercise_query, duration=exercise['duration'])
                db.session.add(new_exercise)
                db.session.commit()
            print(exercise_calories_burned)

            flash('Exercise added successfully!', 'success')
            return redirect(url_for('home'))  # Redirect to home after adding exercise
        else:
            flash('Exercise not recognized or error occurred!', 'danger')

    return render_template('add_exercise_done.html', form=form)



# viewing functions
@app.route('/daily_report')
@login_required
def daily_report():
    start_date, end_date = get_date_range('daily')

    food_intake = FoodIntake.query.filter(
        FoodIntake.email == current_user.email,
        FoodIntake.date >= start_date,
        FoodIntake.date <= end_date
    ).all()

    exercise_done = ExerciseDone.query.filter(
        ExerciseDone.email == current_user.email,
        ExerciseDone.date >= start_date,
        ExerciseDone.date <= end_date
    ).all()

    total_intake = round(sum(item.calories for item in food_intake), 2)
    total_burned = round(sum(item.calories_burned for item in exercise_done), 2)

    return render_template(
        'daily_report.html',
        food_intake=food_intake,
        exercise_done=exercise_done,
        total_intake=total_intake,
        total_burned=total_burned
    )


@app.route('/weekly_report')
@login_required
def weekly_report():
    start_date, end_date = get_date_range('weekly')

    food_intake = FoodIntake.query.filter(
        FoodIntake.email == current_user.email,
        FoodIntake.date >= start_date,
        FoodIntake.date <= end_date
    ).all()

    exercise_done = ExerciseDone.query.filter(
        ExerciseDone.email == current_user.email,
        ExerciseDone.date >= start_date,
        ExerciseDone.date <= end_date
    ).all()

    total_intake = round(sum(item.calories for item in food_intake), 2)
    total_burned = round(sum(item.calories_burned for item in exercise_done), 2)
    return render_template(
        'weekly_report.html',
        food_intake=food_intake,
        exercise_done=exercise_done,
        total_intake=total_intake,
        total_burned=total_burned
    )


@app.route('/monthly_report')
@login_required
def monthly_report():
    start_date, end_date = get_date_range('monthly')

    food_intake = FoodIntake.query.filter(
        FoodIntake.email == current_user.email,
        FoodIntake.date >= start_date,
        FoodIntake.date <= end_date
    ).all()

    exercise_done = ExerciseDone.query.filter(
        ExerciseDone.email == current_user.email,
        ExerciseDone.date >= start_date,
        ExerciseDone.date <= end_date
    ).all()

    total_intake = round(sum(item.calories for item in food_intake),2)
    total_burned = round(sum(item.calories_burned for item in exercise_done),2)

    return render_template(
        'monthly_report.html',
        food_intake=food_intake,
        exercise_done=exercise_done,
        total_intake=total_intake,
        total_burned=total_burned
    )

@login_required
@app.route('/food_intake_record/<int:id>', methods=['GET', 'POST'])
def food_intake_record(id):
    food_intake = FoodIntake.query.filter(FoodIntake.id == id,
                                          FoodIntake.email==current_user.email).first()
    print(food_intake)
    print(type(food_intake))
    if food_intake:
        return render_template('food_intake_tabel.html', food_intake_records = food_intake, back = request.referrer)
    else:
        return redirect(request.referrer)
# date mar 25

# adding profile button

@app.route('/view_profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    back = request.referrer
    form = EditUserForm(obj=current_user)  # Prefill form with current user data

    if form.validate_on_submit():
        # Update current user details
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        current_user.weight = form.weight.data
        current_user.height = form.height.data

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profile'))

    elif request.method == 'POST':
        flash('Failed to update profile. Please check the inputs.', 'danger')

    return render_template('profile.html', form=form, back='home')


# adding custom items
@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = CustomItemForm()
    if form.validate_on_submit():
        new_item = Custom_item(food=form.food.data, email=current_user.email, description=form.description.data,
                               unit = form.unit.data, quantity=form.quantity.data,calories=form.calories.data, protein=form.protein.data,
                               sugar = form.sugar.data, carbohydrates=form.carbohydrates.data, fiber=form.fiber.data, sodium=form.sodium.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('add_item'))
    elif request.method == 'POST':
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", "danger")
        else:
            flash('Failed to update profile. Please check the inputs.', 'danger')

    return render_template('add_custom_item.html', form = form)

@app.route('/view_custom_items')
@login_required
def view_custom_items():
    items = Custom_item.query.filter_by(email=current_user.email).all()
    return render_template('view_custom_item.html', items=items)



@app.route('/edit_item/<int:id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def edit_item(id):
    item = Custom_item.query.get_or_404(id)  # Fetch item or return 404
    form = CustomItemForm(obj=item)  # Pre-fill form with item data

    if form.validate_on_submit():
    # Update the item if the form is submitted
        item.food = form.food.data
        item.description = form.description.data
        item.calories = form.calories.data
        item.unit = form.unit.data
        item.quantity = form.quantity.data
        item.protein = form.protein.data
        item.sugar = form.sugar.data
        item.carbohydrates = form.carbohydrates.data
        item.fiber = form.fiber.data
        item.sodium = form.sodium.data

        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('view_custom_items'))
    elif request.method == 'POST':
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", "danger")
        else:
            flash('Failed to update profile. Please check the inputs.', 'danger')

        return render_template('edit_item.html', form=form, item=item)

    return render_template('edit_item.html', form=form, item=item)


@app.route('/delete_item/<int:id>', methods=['POST'])
@login_required
def delete_item(id):
    item = Custom_item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'danger')
    return redirect(url_for('view_custom_items'))
#
# @app.route('/add_custom_meal', methods=['GET', 'POST'])
# @login_required
# def add_custom_meal():
#     form = CustomMealForm()
#     form.items.choices = [(item.id, item.food) for item in Custom_item.query.filter_by(email=current_user.email).all()]
#
#     if request.method == 'POST':  # Use request.form instead of form validation
#         selected_items = request.form.getlist("items")  # Get selected items as a list
#         item_quantities = request.form.getlist("quantities")  # Get corresponding quantities
#
#         if not selected_items or not item_quantities:
#             flash("Please select at least one item and enter quantities!", "danger")
#             return redirect(url_for('add_custom_meal'))
#
#         try:
#             selected_items = [int(item_id) for item_id in selected_items]
#             item_quantities = [int(qty) for qty in item_quantities]
#         except ValueError:
#             flash("Invalid input: Quantities must be numbers!", "danger")
#             return redirect(url_for('add_custom_meal'))
#
#         # Ensure lengths match
#         if len(selected_items) != len(item_quantities):
#             flash("Invalid input: Items and Quantities mismatch!", "danger")
#             return redirect(url_for('add_custom_meal'))
#
#         total_calories = total_protein = total_sugar = total_carbohydrates = total_fiber = total_sodium = 0
#
#         for item, quantity in zip(selected_items, item_quantities):
#             custom_item = Custom_item.query.get(item)
#             if custom_item:
#                 total_calories += custom_item.calories * quantity
#                 total_protein += custom_item.protein * quantity
#                 total_sugar += custom_item.sugar * quantity
#                 total_carbohydrates += custom_item.carbohydrates * quantity
#                 total_fiber += custom_item.fiber * quantity
#                 total_sodium += custom_item.sodium * quantity
#
#         # Save new meal
#         new_meal = CustomMeal(
#             name=request.form.get('name'),
#             email=current_user.email,
#             total_calories=total_calories,
#             total_protein=total_protein,
#             total_sugar=total_sugar,
#             total_carbohydrates=total_carbohydrates,
#             total_fiber=total_fiber,
#             total_sodium=total_sodium
#         )
#         db.session.add(new_meal)
#         db.session.commit()  # Commit meal first to get the ID
#
#         # Save item-quantity mapping in MealItems table
#         for item, quantity in zip(selected_items, item_quantities):
#             meal_item = MealItems(meal_id=new_meal.id, item_id=item, quantity=quantity)
#             db.session.add(meal_item)
#
#         db.session.commit()
#
#         flash("Custom Meal Created Successfully!", "success")
#         return redirect(url_for('view_custom_meals'))
#
#     return render_template('add_custom_meal.html', form=form)
#
#
#
#
# @app.route('/view_custom_meals')
# @login_required
# def view_custom_meals():
#     meals = CustomMeal.query.filter_by(email=current_user.email).all()
#
#     # Prepare a dictionary to store meal items and their quantities
#     meal_data = {}
#     for meal in meals:
#         meal_items = MealItems.query.filter_by(meal_id=meal.id).all()
#         meal_data[meal.id] = [(item.item.food, item.quantity) for item in meal_items]  # Get item names & quantities
#
#     return render_template('view_custom_meals.html', meals=meals, meal_data=meal_data)
#
#
# @app.route('/view_meal/<int:meal_id>')
# @login_required
# def view_meal(meal_id):
#     meal = CustomMeal.query.get_or_404(meal_id)
#
#     # Get meal items and their quantities
#     meal_items = MealItems.query.filter_by(meal_id=meal.id).all()
#     item_details = [(item.item.food, item.quantity) for item in meal_items]
#
#     return render_template('view_meal.html', meal=meal, meal_items=item_details)
#
#
# @app.route('/edit_meal/<int:meal_id>', methods=['GET', 'POST'])
# @login_required
# def edit_meal(meal_id):
#     meal = CustomMeal.query.get_or_404(meal_id)
#     form = CustomMealForm(obj=meal)
#
#     # Fetch items linked to the meal
#     meal_items = MealItems.query.filter_by(meal_id=meal.id).all()
#
#     # Fix incorrect attribute access
#     form.items.choices = [(item.id, item.food) for item in Custom_item.query.filter_by(email=current_user.email).all()]
#
#     if request.method == 'POST':
#         meal.name = request.form.get('name')
#
#         selected_items = request.form.getlist("items")
#         item_quantities = request.form.getlist("quantities")
#
#         try:
#             selected_items = [int(item_id) for item_id in selected_items]
#             item_quantities = [int(qty) for qty in item_quantities]
#         except ValueError:
#             flash("Invalid input: Quantities must be numbers!", "danger")
#             return redirect(url_for('edit_meal', meal_id=meal.id))
#
#         # Clear old items
#         MealItems.query.filter_by(meal_id=meal.id).delete()
#         db.session.commit()
#
#         # Recalculate total nutrition
#         total_calories = total_protein = total_sugar = total_carbohydrates = total_fiber = total_sodium = 0
#
#         for item, quantity in zip(selected_items, item_quantities):
#             custom_item = Custom_item.query.get(item)
#             if custom_item:
#                 total_calories += custom_item.calories * quantity
#                 total_protein += custom_item.protein * quantity
#                 total_sugar += custom_item.sugar * quantity
#                 total_carbohydrates += custom_item.carbohydrates * quantity
#                 total_fiber += custom_item.fiber * quantity
#                 total_sodium += custom_item.sodium * quantity
#
#                 # Save updated meal items
#                 meal_item = MealItems(meal_id=meal.id, item_id=item, quantity=quantity)
#                 db.session.add(meal_item)
#
#         # Update meal totals
#         meal.total_calories = total_calories
#         meal.total_protein = total_protein
#         meal.total_sugar = total_sugar
#         meal.total_carbohydrates = total_carbohydrates
#         meal.total_fiber = total_fiber
#         meal.total_sodium = total_sodium
#
#         db.session.commit()
#
#         flash("Meal updated successfully!", "success")
#         return redirect(url_for('view_meal', meal_id=meal.id))
#
#     return render_template('edit_meal.html', form=form, meal=meal, meal_items=meal_items)
#
# @app.route('/delete_meal/<int:meal_id>', methods=['POST'])
# @login_required
# def delete_meal(meal_id):
#     meal = CustomMeal.query.get_or_404(meal_id)
#
#     # Delete meal items first to maintain referential integrity
#     MealItems.query.filter_by(meal_id=meal.id).delete()
#     db.session.delete(meal)
#     db.session.commit()
#
#     flash('Meal deleted successfully!', 'danger')
#     return redirect(url_for('view_custom_meals'))
#
#
# @app.route('/delete_meal_item/<int:meal_id>/<int:item_id>', methods=['POST'])
# @login_required
# def delete_meal_item(meal_id, item_id):
#     meal_item = MealItems.query.filter_by(meal_id=meal_id, item_id=item_id).first()
#     if meal_item:
#         db.session.delete(meal_item)
#         db.session.commit()
#         flash('Item removed from meal!', 'success')
#     else:
#         flash('Item not found!', 'danger')
#
#     return redirect(url_for('edit_meal', meal_id=meal_id))


if __name__ == '__main__':
    app.run(debug=True)


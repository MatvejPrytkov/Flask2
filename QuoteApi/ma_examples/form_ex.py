from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)

app.secret_key = "example key"



class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=3, max=10)])


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('index.html', form=form)


@app.get("/success")
def done():
    return "Well done"


if __name__  == "__main__":
    app.run(debug=True)
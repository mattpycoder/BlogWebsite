from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreateBlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    category = StringField("Category", validators=[DataRequired(), Length(max=100)])
    description = StringField("Description", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField(label=("Submit"))


class CreatePostForm(FlaskForm):
    blog_id = SelectField(
        "Select Blog",
        coerce=int,
        validators=[DataRequired(message="Please choose a blog to publish in.")],
    )
    title = StringField(
        "Post Title", validators=[DataRequired(message="Post title is required."), Length(max=200)]
    )
    content = TextAreaField(
        "Content", validators=[DataRequired(message="Content cannot be empty.")]
    )
    submit = SubmitField(label=("Publish Post"))

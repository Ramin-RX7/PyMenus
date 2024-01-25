from ultra_cli.forms import Form, Question, ValidationError


def age_validator(raw_input, validated_input, data):
    try:
        age = int(raw_input)
    except ValueError:
        raise ValidationError
    return age


myform = Form([
    Question("name", "your name:  "),
    Question("age", "your age:  ", validators=[age_validator]),
])

results = myform.display()
print(results)

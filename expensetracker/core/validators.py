from django.core.exceptions import ValidationError

def positive_decimal_validator(value):
    if value is not None and value <= 0:
        raise ValidationError("Provided value must be greater than zero.")

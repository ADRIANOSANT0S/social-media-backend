from rest_framework import serializers


def run_validation(func, value):
    try:
        return func(value)
    except ValueError as e:
        raise serializers.ValidationError(str(e))

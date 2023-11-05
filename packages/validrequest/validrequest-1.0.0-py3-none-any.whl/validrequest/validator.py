from validrequest.exceptions import ValidationError


def _get_types(type_string):
    if type_string == 'string':
        return str
    elif type_string == 'integer':
        return int
    elif type_string == 'float':
        return float
    elif type_string == 'dictionary' or type_string == 'dict' or type_string == 'object':
        return dict
    elif type_string == 'list' or type_string == 'array':
        return list
    else:
        return str  # default


def _parse_validation_rule(key, validation_rule, request_params):
    try:
        value_type, _, length = validation_rule.split('|')
    except Exception:
        length = ""
        value_type, _ = validation_rule.split('|')
    # Make value type lowercase for compatibility reasons
    value_type = value_type.lower()
    # Split the length into threshold and value
    if length == "":
        length_threshold, length_value = [None, None]
    else:
        length_threshold, length_value = length.split(':')
    # Get expected value from request_params
    request_param_value = request_params.get(key, None)
    if request_param_value == None:
        raise ValidationError(f"{key} is required, but was not provided.")
    # For length check only
    temp_casted_value = str(request_param_value)
    # Do length evaluation
    if length_threshold == "min":
        if value_type == "list" or value_type == "array":
            if len(request_param_value) < int(length_value):
                raise ValidationError(f"{key} does not meet the minimum length of {length}")
        else:
            if len(temp_casted_value) < int(length_value):
                raise ValidationError(f"{key} does not meet the minimum length of {length}.")
    elif length_threshold == "max":
        if value_type == "list" or value_type == "array":
            if len(request_param_value) > int(length_value):
                raise ValidationError(f"{key} does not meet the maximum length of {length}")
        else:
            if len(temp_casted_value) > int(length_value):
                raise ValidationError(f"{key} exceeds the maximum length of {length_value}.")
        
    # Convert string numbers to numerics
    if value_type == "float" and "." in temp_casted_value:
        temp_casted_value = float(temp_casted_value)
    if value_type == "integer" and temp_casted_value.isdigit():
        temp_casted_value = int(temp_casted_value)
    # Check type
    if not isinstance(request_param_value, _get_types(value_type)):
        raise ValidationError(f"{key} is not the expected type. Expected type: {value_type}, actual type: {type(request_param_value)}")
    return True


def _operation(validation_rules, request_params, error_cb=None, strict=False):
    try:
        for key, value in validation_rules.items():
            if strict:
                _parse_validation_rule(key, value, request_params)
            elif 'required' in value.lower():
                _parse_validation_rule(key, value, request_params)
            else:
                continue
    except Exception as e:
        if error_cb is not None:
            return error_cb({ "message": e.message })
        raise e


def validate(func):
    def inner(*args, **kwargs):
        if kwargs["parse_level"] == "query":
            request_params = kwargs["req"].query
        else: 
            request_params = kwargs["req"].params
        error_cb = None
        strict = False
        try:
            error_cb = kwargs["next"]
            strict = kwargs['strict']
        except Exception:
            pass
        _operation(kwargs["validation_rules"], request_params, error_cb, strict)
        func(*args, **kwargs)
    return inner


def validator(validation_rules, request_params, strict=False):
    """
    :param validation_rules {dict} The validation rule dictionary
    :param request_params {dict} The incoming request parameters (query)
    :param strict {bool} If False, it will only validate 'required' fields, else all fields
    """
    _operation(validation_rules, request_params, strict=strict)

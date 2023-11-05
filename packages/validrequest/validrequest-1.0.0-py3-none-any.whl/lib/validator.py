from lib.exceptions import ValidationError
from typing import List, Dict, Callable, Union, Any, Type
from collections import namedtuple
from dataclasses import dataclass

# Global Type
ValidationRulesNamedTuple = namedtuple('ValidationRules', ['value_type', 'state', 'min_length', 'max_length'])
ExpectedTypes = Type[str] | Type[int] | Type[float] | Type[dict] | Type[bool] | tuple[type[int], type[float]]

# Model
@dataclass
class ValdationRules():
    value_type: str
    state: str
    min_length: Union[int, None]
    max_length: Union[int, None]


def _len(expected_type: ExpectedTypes, value: Any) -> float | int:
    if expected_type == str or expected_type == dict: return len(value)
    if expected_type == float: return float(value)
    if expected_type == int: return int(value)
    raise ValidationError(f'Unexpected type ({expected_type}) provided for value: {value}')


def _get_types(type_string: str) -> ExpectedTypes:
    if type_string == 'string' or type_string == 'str':
        return str
    elif type_string == 'integer' or type_string == 'int':
        return int
    elif type_string == 'float':
        return float
    elif type_string == 'number':
        return (int, float)
    elif type_string == 'dictionary' or type_string == 'dict' or type_string == 'object':
        return dict
    elif type_string == 'boolean' or type_string == 'bool':
        return bool
    raise ValidationError(f'Unknown type provided: {type_string}')


def _unpack_validation_rules(validation_rule: str) -> ValdationRules:
    _split: List[str] = validation_rule.split('|')
    _min_length: Union[int, None] = None
    _max_length: Union[int, None] = None

    for rule in _split[2:]:
        if 'min' in rule:
            _min_length = int(rule.split(':')[1])
        if 'max' in rule:
            _max_length = int(rule.split(':')[1])

    return ValdationRules(value_type=_split[0], state=_split[1], min_length=_min_length, max_length=_max_length)


def _validate_against_rules(key: str, validation_rule: str, request_params: Dict[str, Any]) -> None:
    # Unpack rules from pipe delimited string
    rules: ValdationRules = _unpack_validation_rules(validation_rule)
    # Create constant of is validation required
    is_required: bool = rules.state == 'required'
    # Only validate if field is required
    if is_required:
        # Get request value from request parameters/body
        request_value: ExpectedTypes = request_params.get(key, None)
        if request_value == None:
            raise ValidationError(f"{key} is required, but was not provided.")
        # Get expected type for value
        expected_type: ExpectedTypes = _get_types(rules.value_type)
        # Do minimum length validation
        if rules.min_length and expected_type != bool and _len(expected_type, request_value) < rules.min_length:
            raise ValidationError(f"{key} does not meet the minimum length requirement of {rules.min_length}.")
        # Do maximum length validation
        if rules.max_length and expected_type != bool and _len(expected_type, request_value) > rules.max_length:
            raise ValidationError(f"{key} exceeds the max length of {rules.max_length}.")
        # Validate expected type
        if not isinstance(request_value, expected_type):
            raise ValidationError(f"{key} is not the expected type. Expected type: {rules.value_type}, actual type: {type(request_value)}")


def _operation(validation_rules: Dict[str, Any], request_params: Dict[str, Any]):
    for valdation_rule_key, validation_rule in validation_rules.items():
        _validate_against_rules(valdation_rule_key, validation_rule.lower(), request_params)


def validate(func: Callable):
    def inner(*args, **kwargs):
        # Get the Request argument from function definition
        request_params: Dict[str, Any] = kwargs.get('request', kwargs.get('req', None))
        if not request_params:
            raise ValidationError("Request argument must be provided. Acceptable names are 'request' or 'req'")
        # Get the payload parsing level, this is data send in the request at the query or body level
        payload_parsing_level: str = kwargs.get("payload_level", None)
        if not payload_parsing_level:
            raise ValidationError("payload_level argument must be provided. Example: 'body' or 'query'.")
        # Finally get the Request data
        request_params = request_params.__dict__[payload_parsing_level]
        # Optional callback that will be used if an error is thrown
        error_cb: Union[Callable, None] = kwargs.get("next", None)
        # Begin validation process
        try:
            _operation(kwargs["validation_rules"], request_params)
        except Exception as e:
            if error_cb:
                return error_cb(f'{type(e).__name__} - {e}')
            raise e
        # If validation was successful, run the endpoint as expected.
        return func(*args, **kwargs)
    return inner


def validator(validation_rules: Dict[str, str], request_params: Dict[str, Any]):
    """
    :param validation_rules {dict} The validation rule dictionary
    :param request_params {dict} The incoming request parameters (query)
    """
    _operation(validation_rules, request_params)

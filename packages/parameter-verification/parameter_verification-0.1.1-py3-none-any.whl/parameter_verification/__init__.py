""" Functions to be used to validate parameters for a function """

VERSION = (0, 1, 1)    # updated 2023-10-31 23:07:57.833243 from : (0, 1, 0)

class ParameterError(Exception):
    """ Class to contain the descripton of a parameter error to raise """
    def __init__(self, parameters, error, failed_param, failed_check):
        super().__init__()
        self.error = error
        self.parameters = parameters
        self.failed_param = failed_param
        self.failed_check = failed_check

    def __str__(self):
        return "Parameter `" + str(self.failed_param) + "` failed check `" + str(self.failed_check) + "` with error: " + str(self.error)

def verify_params(no_raise=False, **kwargs):
    """ Function to validate params match requirements.  Each argument is a tuple that includes at minimum
        the value and variable type.  Additional checks can be added:
        i.e.:
            str1=('abc123', str)
            float1=(12.2, float)
            int1=(123, int, '>100')
        Supported checks :
            'len=x' - String must be x characters
            'len>=x' - string must be >= x characters
            '>x' - Numeric comparison
        Multiple checks and multiple variables can be provided.  All must pass for a True return.  Any checks that fail will return False.
        The param name is used to log the parameter that triggered the failure.

        no_raise=True sets the function to return False rather than raise an error.

        Returns True if all checks pass """
    for key, value in kwargs.items():
        # check we have a valid type
        if not isinstance(value, tuple) or len(value) < 2:
            if no_raise:
                return False
            raise ParameterError(kwargs, 'Argument error, NOT a Tuple', key, 'INIT')
        # check the value against the provided type
        try:
            if not isinstance(value[0], value[1]):
                if no_raise:
                    return False
                raise ParameterError(kwargs, "Value is type " + str(type(value[0])) + " not " + str(value[1]), key, 'TYPE')
        except NameError as err:
            if no_raise:
                return False
            raise ParameterError(kwargs, err, key, 'TYPE') from NameError
        # loop through any additional checks and compare
        if len(value) > 2:
            pos = 2
            # verify check is a string
            if not isinstance(value[pos], str):
                if no_raise:
                    return False
                raise ParameterError(kwargs, 'Provided check is not a string',key, value[pos])
            while pos < len(value):
                # loop through supported tests
                if value[pos][0:3] == 'len':
                    # check the string length
                    try:
                        return_value = _check_value_operands(len(str(value[0])), value[pos][3:], value[1])
                    except ValueError as err:
                        raise ParameterError(kwargs, err, key, value[pos]) from ValueError
                else:
                    return_value = _check_value_operands(value[0], value[pos], value[1])
                if return_value is None:
                    if no_raise:
                        return False
                    raise ParameterError(kwargs, 'No supported operand found', key, value[pos])
                elif not return_value:
                    if no_raise:
                        return False
                    raise ParameterError(kwargs, 'Failed check', key, value[pos])
                pos += 1
    return True


def _check_value_operands(value1, value2, val_type):
    """ Check two values using the provided operator """
    if value2[0:2] == '==':
        return True if val_type(value1).lower() == val_type(value2.split('==')[1]).lower() else False
    elif value2[0] == '=':
        return True if val_type(value1) == val_type(value2.split('=')[1]) else False
    elif value2[0:2] == '<=':
        return True if val_type(value1) <= val_type(value2.split('<=')[1]) else False
    elif value2[0] == '<':
        return True if val_type(value1) < val_type(value2.split('<')[1]) else False
    elif value2[0:2] == '>=':
        return True if val_type(value1) >= val_type(value2.split('>=')[1]) else False
    elif value2[0] == '>':
        return True if val_type(value1) > val_type(value2.split('>')[1]) else False
    # return None if we didn't hit a matching comparison
    return None

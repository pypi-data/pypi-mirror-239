# Python Parameter Verification

Homepage: <a href="https://www.learningtopi.com/python-modules-applications/parameter_verification/">https://www.learningtopi.com/python-modules-applications/parameter_verification/<a>

This is a simple Python function that can be used to test variable types and values.  The intended purpose is to check the parameters of a function to ensure that appropriate types and values have been passed.

The function is specifically written to support Python >=3.3 so it can be used with a wide array of applications.  There are also no dependencies that need to be installed.

## Usage

    from parameter_verification import verify_params, ParameterError

    def test_function_1(param1, param2, param3, param4):
        ''' Sample function to show verify_params usage '''
        try:
            verify_params(param1=(param1,int), param2=(param2,str,'=abc'), param3=(param3,float, '>100.2', '<110.0'), param4=(param4,str,'len=4','=abcd'))
        except ParameterError as e:
            # some code to handle an exception if desired

        # proceed with your function!

The verify_param function takes keyword arguments for each parameter to check.  The value of each parameter is passed as a tuple consisting of:

- The value to check (i.e. the variable)
- The variable type to check against
- (optional) an additional check to perform (i.e. '>100.2' or '=abc')
- (optional) more additional checks can be added, i.e. '>100.2', '<110.0'

## Supported Checks

The following checks are supported (in addition to the data type which can be any Python type):

- '==' or '=': Both perform the same check and can be used interchangably
- '<', '<=', '>', '>=': Perform the typical checks
- 'len=x', 'len>x', 'len>=x', etc: Check the length of a string

## Returns and Errors

The function returns True if all parameters pass.  If a parameter check fails, the function raises a ParameterError exception.  If desired, this behavior can be changed by setting "no_raise=True". With no_raise set to True, False will be returned in the case of a failed parameter check rather than raising an exception.
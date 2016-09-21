# Written by Will Bond <will@wbond.net>
#
# The author or authors of this code dedicate any and all copyright interest in
# this code to the public domain. We make this dedication for the benefit of the
# public at large and to the detriment of our heirs and successors. We intend
# this dedication to be an overt act of relinquishment in perpetuity of all
# present and future rights to this code under copyright law.


def data(provider_method, first_param_name_suffix=False):
    """
    A method decorator for unittest.TestCase classes that configured a
    static method to be used to provide multiple sets of test data to a single
    test

    :param provider_method:
        The name of the staticmethod of the class to use as the data provider

    :param first_param_name_suffix:
        If the first parameter for each set should be appended to the method
        name to generate the name of the test. Otherwise integers are used.

    :return:
        The decorated function
    """

    def test_func_decorator(test_func):
        test_func._provider_method = provider_method
        test_func._provider_name_suffix = first_param_name_suffix
        return test_func

    return test_func_decorator


def data_decorator(cls):
    """
    A class decorator that works with the @provider decorator to generate test
    method from a data provider
    """

    # noinspection PyProtectedMember
    def generate_test_func(m_name, original_function, m_num, m_params):
        if original_function._provider_name_suffix:
            data_name = m_params[0]
            m_params = m_params[1:]
        else:
            data_name = m_num
        expanded_name = 'test_%s_%s' % (m_name, data_name)
        # We used expanded variable names here since this line is present in
        # backtraces that are generated from test failures.
        # noinspection PyPep8
        generated_test_function = lambda self: original_function(self, *m_params)
        setattr(cls, expanded_name, generated_test_function)

    for name in dir(cls):
        func = getattr(cls, name)
        if hasattr(func, '_provider_method'):
            num = 1
            # noinspection PyProtectedMember
            for params in getattr(cls, func._provider_method)():
                generate_test_func(name, func, num, params)
                num += 1

    return cls

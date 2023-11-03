def two_plus_three():
    a = 2
    b = 3
    c = a+b
    print (f'The result of adding {a}+{b} is {c}')

def add_100(my_previous_variable):
    my_previous_variable = my_previous_variable + 100
    print (f'The result of adding 100 to my_previous_variable is {my_previous_variable}')

def hybrid():
    x = 3
    x = x + 4
    print (x)

# -----------------------------------------------------
# pipeline
# -----------------------------------------------------
def index_pipeline (test=False, load=True, save=True, result_file_name="index_pipeline"):
    """Pipeline calling each one of the functions defined in this module."""
    
    # load result
    result_file_name += '.pk'
    path_variables = Path ("index") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    two_plus_three ()
    add_100 (my_previous_variable)
    hybrid ()

    # save result
    result = Bunch ()
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result


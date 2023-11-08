def puhoo(sooboo):
    print(sooboo)

def fooloo(n, i, operation):
    # check if operation is a lambda function
    if callable(operation) and operation.__name__ == '<lambda>':
        # iteration from start i to end n
        while i <= n:
            # execute the operation function, passing through i and increment at the end of function call
            operation(i)
            i += 1
    # if operation is not a lambda function, print it must be a lambda function
    else:
        print("The 'operation' argument must be a lambda function")

def fuh(condition, if_true, if_false):
    """
    If Statement for babies.
    
    :param condition: Boolean condition to evaluate.
    :param if_true: Callable to execute if the condition is True.
    :param if_false: Callable to execute if the condition is False.
    :return: The result of either the if_true or if_false callable.
    """
    
    if callable(if_true) and callable(if_false):
        return if_true() if condition else if_false()
    else:
        raise ValueError("Both if_true and if_false must be callable.")


def wuhoo(condition, operation):
    """
    While Loop for babies.
    
    :param condition: A callable that returns a Boolean result for loop continuation.
    :param operation: A callable that represents the loop to execute.
    """
    
    while condition():
        operation()

def lizzie(object):
    """
    len() function for babies.
    accepts an object parameter, 
    verifies if it is a commonly accepted parameter of len(), 
    and returns the length of the object
    """

    if isinstance(object, (str, list, tuple, dict, set)):
        return len(object)
    else:
        raise TypeError("Unsupported type")
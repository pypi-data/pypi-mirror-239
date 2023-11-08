from babpy import puhoo, fooloo, fuh, wuhoo, lizzie

def main():
    # PRINT
    puhoo("Print Statement:\nHi :D")
    
    # FOR
    puhoo("\nFor Loop:")
    fooloo(5, 1, lambda x: puhoo(x))
    
    # IF
    puhoo("\nIf Statement:")
    fuh(1 > 2, lambda: puhoo("1 > 2 is true :)"), lambda: puhoo("1 > 2 is false :("))
    fuh(2 > 1, lambda: puhoo("2 > 1 is true :)"), lambda: puhoo("2 > 1 is false :("))
    
    # WHILE
    puhoo("\nWhile Loop:")
    counter = [0]
    wuhoo(lambda: counter[0] < 5, lambda: (puhoo(counter[0]), counter.__setitem__(0, counter[0] + 1))[0])

    # LEN
    puhoo("\nLen Function:")

    # LEN OF LIST
    puhoo("\nCalculating length of a list:")
    my_list = [1, 2, 3, 4, 5]
    lizzie(my_list, lambda length: puhoo("\nLength of the list is: " + str(length)))

    # LEN OF STRING
    puhoo("\nCalculating length of a string:")
    my_string = "Hello, World!"
    lizzie(my_string, lambda length: puhoo("\nLength of the string is: " + str(length)))

    # LEN OF TUPLE
    puhoo("\nCalculating length of a tuple:")
    my_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    lizzie(my_tuple, lambda length: puhoo("\nLength of the tuple is: " + str(length)))

    # LEN OF DICT
    puhoo("\nCalculating length of a dict:")
    my_dict = {
        "name": "Liatha",
        "age": 3,
        "pet": "cat",
        "shoe size": 8
    }
    lizzie(my_dict, lambda length: puhoo("\nLength of the dict is: " + str(length)))

    # LEN OF SET
    puhoo("\nCalculating length of a set:")
    my_set = {1, 2, 3, 4, 5, 6, 7, 8}
    lizzie(my_set, lambda length: puhoo("\nLength of the set is: " + str(length)))
    
if __name__ == '__main__':
    main()
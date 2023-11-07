
def prit_lol(the_list, level):
    for each_item in the_list:
        if isinstance(each_item, list):
            prit_lol(each_item, level + 1)
        else:
            for i in range(level):
                print('\t', end='')
            print(each_item)

    return each_item

def add(a, b):
    return a + b

#
# the_list = ['A', 'a', 'B', 'b', 'C', 'c', ['1', '2', '3']]
# prit_lol(the_list, 0)

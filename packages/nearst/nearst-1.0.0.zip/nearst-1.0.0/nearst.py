def print_lol(the_list): #the_list �O���ܼơA�H�A���W�F��A����lol(movies) �N�|�i��H�U�ʧ@�C' 
        for each_item in the_list:
                if isinstance (each_item,list):
                        print_lol(each_item)
                else:
                        print each_item

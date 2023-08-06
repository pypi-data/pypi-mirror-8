def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fh)
        else:
            if indent:
                print("\t"*level,end='',fh)
            print(each_item,file=fh)

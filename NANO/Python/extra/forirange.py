
def main():
   x = 1

if __name__ == '__main__':
   main()



match 1:

    case 1:
        pass

    case 2:
        pass

    case 3:
        pass

    case _:
        pass


a = ['a','b','c']
b = [ 4 , 5 , 6 ]

for i, v in enumerate(a):
   print(i,v)

for av, bv in zip(a,b):
   print(av,bv)





try:
    if 1 != 2:
        raise ValueError

    pass

except ValueError:
    print("error")
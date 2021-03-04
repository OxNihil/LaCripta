import math
import cmath

min_lenght = 1
max_lenght = 16
hashpersec = 1371300000
hashperhour = hashpersec*3600

def table_entropy():
        print("-----------\nBit Entropy\n-----------")
        print("Len\tNumeric(10)\t\tHex (16)\tAlphabetic(27)\tAlphanum (37)\t\tAscii (94)")
        for i in range(min_lenght,max_lenght):
            print(str(i)+"\t"+str(bitentropy(10,i))+"\t"+str(bitentropy(16,i))
                  +"\t"+str(bitentropy(27,i))+"\t"+str(bitentropy(37,i))+"\t"+str(bitentropy(94,i)))
    
def bitentropy(charset,lenght):
    return math.log(charset,2)*lenght

def table_combinations():
    print("-----------\nCombinations\n-----------")
    print("Len\tNumeric(10)\t\tHex (16)\tAlphabetic(27)\t\tAlphanum (37)\t\tAscii (94)")
    for i in range(min_lenght,max_lenght+1):
         print(str(i)+"\t"+str('{:<8}'.format(combinations(10,i)))+"\t\t"+str('{:<8}'.format(combinations(16,i)))
                  +"\t\t"+str('{:<8}'.format(combinations(27,i)))+"\t\t"+str('{:<8}'.format(combinations(37,i)))+"\t\t"+str('{:<8}'.format(combinations(94,i))))


def combinations(charset,lenght):
    total = 0
    for i in range(min_lenght,lenght+1):
        if i == 1:
            total += charset
        else:
            total += pow(charset,i)
    return total

def table_time(hashpersec):
    vel = hashpersec * 3600
    print("-----------\nTime(Hours)-"+str(hashpersec)+" Hash/sec \n-----------")
    print("Len\tNumeric(10)\t\tHex (16)\tAlphabetic(27)\t\tAlphanum (37)\t\tAscii (94)")
    for i in range(min_lenght,max_lenght):
         print(str(i)+"\t"+str('{:<8}'.format(combinations(10,i)//vel))+"\t\t"+str('{:<8}'.format(combinations(16,i)//vel))
                  +"\t\t"+str('{:<8}'.format(combinations(27,i)//vel))+"\t\t"+str('{:<8}'.format(combinations(37,i)//vel))+"\t\t"+str('{:<8}'.format(combinations(94,i)//vel))) 
    
table_entropy()
print("\n")
table_combinations()
print("\n")
table_time(hashpersec)
print("")


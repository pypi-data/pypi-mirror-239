import random
import string
__doc__="""
uuid is a module that provides efficient and easy method for generating universal unique identity (uuid)

author: Rijul Dhungana

"""

  
        
        
    


def __generate_pieces(security, level, split):
    chars = list(string.ascii_letters+string.digits)
    uuid = list()
    for i in range(security):
        uid = list()
        for j in range(level):
            uid.append(random.choice(chars))
            random.shuffle(chars)
        uuid.append("".join(uid))
    return split.join(uuid)
        
    



def generate_uuid(security=2, level=4, join='-'):
    uuid = __generate_pieces(security, level, join)
    return uuid
    



#generate_token():
#a = generate_uuid()
#a = a.split("-")
#print(a)
#b = ''.join(a)
#print(b)
#print(dir(string))
#b = a
#print(b)

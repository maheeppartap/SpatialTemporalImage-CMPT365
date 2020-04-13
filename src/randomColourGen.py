
import random

# when asking for a random number set, specify type:
#   'n' neon, 'p' pastel, 'v' vibrant, 'g' greyish,  'l' lyl
# to add new colours to these pallettes, follow the format: [type as above] R G B
# example: n 255 0 3


class color:
    def __init__(self):
        with open('../assets/colors.dat') as f:
            array = [[x for x in line.split()] for line in f]

        self.neon = []
        self.pastel = []
        self.vibrant = []
        self.grey = []
        self.lyl = []
        for col in array:
            if col[0] == 'n':
                self.neon.append(col[1:])
                continue
            if col[0] == 'p':
                self.pastel.append(col[1:])
                continue
            if col[0] == 'v':
                self.vibrant.append(col[1:])
                continue
            if col[0] == 'g':
                self.grey.append(col[1:])
                continue
            if col[0] == 'l':
                self.lyl.append(col[1:])



    def retCol(self, type)-> (int,int,int):
        random.seed()
        if type == 'n':
            try:
                rand = random.randint(0, len(self.neon)-1)
            except:
                print("No neon colours. Sorry.")
                return []
            return int(self.neon[rand][0]), int(self.neon[rand][1]), int(self.neon[rand][2])
        if type == 'p':
            try:
                rand = random.randint(0, len(self.pastel)-1)
            except:
                print("No pastel colours. Sorry.")
                return []
            return int(self.pastel[rand][0]), int(self.pastel[rand][1]), int(self.pastel[rand][2])
        if type == 'v':
            try:
                rand = random.randint(0,len(self.vibrant)-1)
            except:
                print("No vibrant colours. Sorry.")
                return []
            return int(self.vibrant[rand][0]), int(self.vibrant[rand][1]), int(self.vibrant[rand][2])
        if type== 'g':
            try:
                rand = random.randint(0, len(self.grey)-1)
            except:
                print("No grey colours. Sorry.")
                return []
            return int(self.grey[rand][0]), int(self.grey[rand][1]), int(self.grey[rand][2])
        if type == 'l':
            try:
                rand = random.randint(0,len(self.lyl)-1)
            except:
                print("No lyl colours. Sorry.")
                return []
            return int(self.lyl[rand][0]), int(self.lyl[rand][1]), int(self.lyl[rand][2])

        #default in case the user messes up the input
        return 0, 0, 255


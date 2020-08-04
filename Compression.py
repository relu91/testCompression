import csv
import math

CODE = [0] * 5000
IDIM, FDIM, IMAX, FMAX= 0

cont = 0
DIFF = [0 for i in range(500)]

NODE = [[[-2] * 2] * 5000] * 5000
SA = [''] * 5000 

class Compression:

    def __init__(self):
        
        global CODE, cont, IMAX, DIFF, IDIM, FMAX, NODE, SA
        with open('piezo.csv', 'r') as csv_file:
            cvs_reader = csv.reader(csv_file, delimiter = ',')
            
            next(cvs_reader) 

            for line in cvs_reader:
                CODE[cont] = int(line[0])
                #print(CODE[cont])

                if(math.ceil(math.log(int(CODE[cont]))/math.log(2)) > IMAX):
                    IMAX = math.ceil(math.log(int(CODE[cont]))/math.log(2))
                cont += 1
            IMAX *= 5000 
            print (IMAX)
        
        self.ENCODE()

    def HuffMan(self, max, dim):
        
        global CODE, cont, IMAX, DIFF, IDIM, FMAX, NODE, SA

        level = [0] * dim
        S = [0] * dim
        P = [0] * dim
        F = [0] * dim
        lc = [0] * dim
        c = 0
        
        for j in range(0,28):
            min = max + 1
            last = max + 1
            
            contStop = 0
            for z in range(0, max + 1):
                if((S[z] == 0) and (DIFF[j] != 0)):
                    contStop += 1
            
            if(contStop == 1):
                break
            
            for j in range(0,cont):
                if(DIFF[j] != 0) and (S[j] == 0):
                    print('code',j,DIFF[j])
                    #pass

            for z in range(0,max):
                if((DIFF[z]<DIFF[min]) and (S[z]!=1) and (DIFF[z]!=0)):
                    min = z
            
            for z in range(0,max):
                if(DIFF[z]<DIFF[last]) and (S[z]!=1) and (DIFF[z]!=0) and (z != min):
                    last = z
            print(last, min)

            if(P[last]==0) and (P[min]==0):
                P[last] = 1
                S[min] = 1
                F[last] = c
                nlv = c
                level[nlv] = level[0]
                lc[nlv] += DIFF[min] + DIFF[last]
                DIFF[last] += DIFF[min]
                c += 1
                NODE[level[nlv]][nlv][0] = last
                NODE[level[nlv]][nlv][1] = min
            elif(P[last]==1) and w(P[min]==1):
                if(F[last]<F[min]):
                    nlv = F[last]
                    S[min] = 1
                    DIFF[last] += DIFF[min]
                    lc[nlv] += DIFF[min]
                else:
                    nlv = F[min]
                    S[last] = 1
                    DIFF[min] += DIFF[last]
                    lc[nlv] += DIFF[last]
                level[nlv] += 1
                NODE[level[nlv]][nlv][0] = -1
                NODE[level[nlv]][nlv][1] = -1
            elif(P[last]==1):
                DIFF[last] += DIFF[min]
                S[min] = 1
                nlv = F[last]
                level[nlv] += 1
                lc[nlv] += DIFF[min]
                NODE[level[nlv]][nlv][0] = -1
                NODE[level[nlv]][nlv][1] = min
            else:
                DIFF[min] += DIFF[last]
                S[last] = 1
                nlv = F[min]
                level[nlv] += 1 
                lc[nlv] += DIFF[last]
                NODE[level[nlv]][nlv][0] = -1
                NODE[level[nlv]][nlv][1] = last
        
        #print(last, min, NODE[level[nlv]][nlv][0], NODE[level[nlv]][nlv][1])
        #self.Huff_to_Encode(max, level[nlv], 0, lc, 0, 0)
        
    def Huff_to_Encode(self, Max, Top, Bottom, lc, StL, StnLg):
        
        global CODE, cont, IMAX, DIFF, IDIM, FMAX, NODE, SA

        contt = 0
        for j in range(Top, Bottom, -1):
        
            sa = ""
            for z in range(0, contt):
                sa += "0"
            
            if(NODE[j][0][0] == -1) and (NODE[j][0][1] == -1):
                self.S1S1(j, Top, lc, sa)              
            
            elif(NODE[j][0][0] == -1):
                SA[NODE[j][0][1]] = sa+"1"
            
            else:
                SA[NODE[j][0][1]] = sa+"1"
                SA[NODE[j][0][0]] = sa+"0"
            
            contt += 1
        
        
        for j in range(Max, 0, -1):
                print(j, SA[j], sep = ' ')
        
        
        for j in range (0, cont):
            FDIM += len(SA[CODE[j]])

        FDIM += 13+22*(5+15+4)

    def S1S1(self, j, Top, lc, sa):

        global CODE, cont, IMAX, DIFF, IDIM, FMAX, NODE, SA

        contlv = Top
        max = 499
        sa += "1"
        for z in range(1,500):
            if(lc[z]>lc[max]):
                max = z
        
        lc[max] = 0
        while(NODE[contlv][max][0] == -2):
            contlv -= 1

        if(NODE[contlv][max][1] != -1):
            SA[NODE[contlv][max][1]] = sa+"1"
        if(NODE[contlv][max][0] != -1):
            SA[NODE[contlv][max][0]] = sa+"0"
        if(NODE[contlv][max][0] == -1) and (NODE[contlv][max][1] == -1):
            self.S1S1(j, Top, lc, sa)
        
        if(NODE[contlv][max][0] == -1):
            while(NODE[contlv][max][0] == -1):
                contlv -= 1
                sa += "0"
                if(NODE[contlv][max][1]!=-1):         
                    SA[NODE[contlv][max][1]] = sa+"1"               
                else:
                    self.S1S1(j, Top, lc, sa)

            if(NODE[contlv][max][0] != -1):
                SA[NODE[contlv][max][0]] = sa+"0"
    
    def ENCODE(self):
        
        global CODE, cont, IMAX, DIFF, IDIM, FMAX, NODE, SA
        
        Max = 0
        
        for j in range(0,cont):

            a = CODE[j]
            if(a > Max):
                 Max = CODE[j]
        
        for j in range(0,cont):
            DIFF[CODE[j]] += 1
        
        for j in range(0,cont):
            if(DIFF[j] != 0):
                print('code',j,DIFF[j])
                

        DIFF[Max + 1] = 10000

        self.HuffMan(Max, 5000)


OB = Compression()

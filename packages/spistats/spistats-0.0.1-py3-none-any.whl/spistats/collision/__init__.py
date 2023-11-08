import math
import numpy as np

class Collision:
    def __init__(self,nbr_dev,nbr_adr,adr_per_dev):
        self.M = nbr_dev
        self.p = 1/nbr_adr
        self.q = 1-(1-self.p)**adr_per_dev

        mass = []
        for i in range(0,self.M-1):
            mass += [math.comb(nbr_dev-1,i)*self.q**i*(1-self.q)**(self.M-1-i)]
        self.mas = np.array(mass)
        self.cd = np.cumsum(mass)

    def mean(self):
        return 1+(self.M-1)*self.q

    def mass(self, n):
        if n==0:
            return 0
        elif n<=self.M:
            return self.mas[n-1]
        else:
            return 0

    def cdf(self, n):
        if n==0:
            return 0
        elif n<=self.M:
            return self.cd[n-1]
        else:
            return 1

    def cdfinv(self, p):
        n = 1+np.argwhere(self.cd>=p)[0][0]
        return n




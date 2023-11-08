from scipy.stats import iqr
import numpy as np

from .law import Law

class Law_multip:
    def __init__(self, p,m):
        self.p = p
        self.m = m

    def cdf(self,n):
        #Bin width Freedman–Diaconis rule
        bw = 2*iqr(self.p)/(n**(1/3))
        m = np.min(self.p)
        M = np.max(self.p)
        size = int(np.ceil((M-m)/bw))
        bins_borders = np.linspace(m,M,size)
        bins_midles = (bins_borders[1:]+bins_borders[:-1])/2


        #Use total probablity formula 
        P_D = 0
        for bi,bins_midle in enumerate(bins_midles):
            law = Law(bins_midle,self.m)
            law.eigenvalues()
            mask = bins_borders[:-1][bi]<self.p
            mask = mask&(bins_borders[1:][bi]>self.p)
            P_plf = np.sum(mask)/len(self.p)
            P_D += P_plf*law.cdf(n)

        return P_D

    def cdf_position(self):
        #Use smallest p to find the farther point
        law = Law(np.min(self.p), self.m)
        _,end = law.cdf_position()

        #Use bigest p to find the closest point
        law = Law(np.max(self.p), self.m)
        law.eigenvalues()
        start,_ = law.cdf_position()

        return start, end

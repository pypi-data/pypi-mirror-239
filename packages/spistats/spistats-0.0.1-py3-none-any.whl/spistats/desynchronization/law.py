import math
import numpy as np

class Law:
    def __init__(self, p, m):
        self.p = p
        self.q = 1-p
        self.a = (1-p)*p**m
        self.m = m
        self.eigen_computed = False

    def eigenvalues(self):
        p = self.p 
        q = self.q 
        a = self.a
        m = self.m 

        pol_char = np.zeros(m+2).astype(float)
        pol_char[0] = 1
        pol_char[1] = -1
        pol_char[-1] = a
        roots = np.roots(pol_char)
        roots = roots.reshape(m+1)
        self.l = roots
        self.eigen_computed = True

        #Finding initial conditions
        u = np.zeros(m+1).astype(float)
        for n in range(m+1):
            u[n] = 1-p**m-n*(1-p)*p**m
        I = u[:m+1].reshape(-1,1)
        L = np.zeros([m+1,m+1]).astype(np.complex_)
        for i in range(m+1):
            L[i,:] = roots**(i)
        self.c = np.matmul(np.linalg.inv(L),I).reshape(m+1)

    def mass(self, N):
        m = self.m
        p = self.p
        if N<m:
            return 0
        elif N==m:
            return p**m
        elif N<=2*m:
            return (1-p)*p**m
        else:
            return np.real(np.sum(self.c*self.l**(N-2*m-1))*(1-p)*p**m)

    def cdf(self, N):
        if not(self.eigen_computed):
            self.eigenvalues()
        p = self.p 
        q = self.q 
        a = self.a
        m = self.m 
        l = self.l
        c = self.c

        """P(D<=N)"""
        if N<m:
            return 0
        elif N<=2*m:
            return p**m+(N-m)*(1-p)*p**m
        else:
            un_sum = np.sum(c*(1-l**(N-2*m))/(1-l))
            return np.real(p**m+m*(1-p)*p**m + (1-p)*p**m*un_sum)

    def cdf_position(self):
        self.eigenvalues()
        p = self.p 
        q = self.q 
        a = self.a
        m = self.m 
        l = self.l
        c = self.c
         
        #cdf start point
        s = 0.01
        if self.cdf(m)<0.01:
            start = m
        else:
            x0=2*m+1
            x1 = x0
            #for i in range(1,niter):
            #while (np.abs(f(x0,p,m,l,c,s))>1):
            while (np.abs(self.cdf(x0)-s)>1):
                left = (s-p**m-m*q*p**m)/(q*p**m)
                f = np.real(np.sum(c*(1-l**(x0-2*m))/(1-l))) - left
                fp = (-1)*np.real(np.sum(c*(l**(x0-2*m)*np.log(l))/(1-l)))
                x1 = x0 - f/fp
                x0 = x1
            start = x1

        #cdf end point
        s = 0.99
        x0=2*m+1
        x1 = x0
        i = 0

        while (np.abs(self.cdf(x1)-s)>0.005):
            for i in range(1000):
                left = (s-p**m-m*q*p**m)/(q*p**m)
                f = np.real(np.sum(c*(1-l**(x0-2*m))/(1-l))) - left
                fp = (-1)*np.real(np.sum(c*(l**(x0-2*m)*np.log(l))/(1-l)))
                x1 = x0 - f/fp
                x0 = x1
                i += 1
            if math.isnan(x1):
                x0 = 2*m+1
                x1 = x0
                s = s - 0.1*s
            elif (np.abs(self.cdf(x1)-s)>0.005):
                s = s - 0.1*s

        end = x1

        return start, end

    def mean(self):
        m = self.m
        p = self.p
        q = 1-p
        E = 0
        E += m*p**m + q*p**m*(3*m**2+m)/2
        E += q*p**m*(np.sum(self.c*self.l/(1-self.l)**2)+(2*m+1)*np.sum(self.c/(1-self.l)))
        return np.real(E)

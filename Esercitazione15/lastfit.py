import sys
import numpy as np
from numpy.lib.stride_tricks import as_strided
import pylab
from scipy.optimize import curve_fit
from scipy.stats import chisqprob

import getpass
users={"candi": "C:\\Users\\candi\\Documents\\GitHub\\Lab3.2\\",
"silvanamorreale":"C:\\Users\\silvanamorreale\\Documents\\GitHub\\Lab3.2\\" ,
"Studenti": "C:\\Users\\Studenti\\Desktop\\Lab3\\",
"User":"C:\\Users\\User\\Documents\\GitHub\\Lab3.2\\",
"andrea": "/home/andrea/Documenti/Da salvare 12-5-2017/Documenti/GitHub/Lab3.2/"
}
try:
    user=getpass.getuser()
    path=users[user]
    print("buongiorno ", user, "!!!")
except:
    raise Error("unknown user, please specify it and the path in the file Esercitazione*.py")


sys.path = sys.path + [path]
dir= path + "Esercitazione15/"



from BuzzLightyear import * 
from lab import *
import uncertainties
import uncertainties.unumpy
###########################################################################


print("===============Fit finale=================")



#####stima paramretri....

kbT=1.38e-23*300*4
Df=1e3
v_rum=11e-9 #volt*hertz**0.5
r_rum=v_rum**2/(4*kbT*Df)

i_rum=0.4e-12
r_rum_par=v_rum/i_rum

#####stimati dal datasheet dell'ina...


pylab.figure(figsnum)
figsnum+=1


#pylab.close("all")
dir_grph=dir+"grafici/"
dir = dir + "data/"


file="lastfit1.txt"
data = np.loadtxt(dir+file,unpack=True)
R=data[0]
VS=data[1:]*1e-3
Vmedio=np.mean(VS, 0)
N=np.shape(VS)[0]
M=np.shape(VS)[1]
Vmediop=as_strided(Vmedio, (N, M), (Vmedio.strides[0],0))
VStd=np.sqrt(np.sum((VS-Vmedio)**2, 0)/(N-1))

Vmedio=Vmedio[R<20000]
VStd=VStd[R<20000]
R=R[R<20000]


foo=lambda R, V0, RT, RS: V0*np.sqrt(1+R/RT+(R/RS)**2)
p0=(2, r_rum, r_rum_par) #dati iniziali dati dal datasheet, se sono interpretati bene (sono a iKH, ma che ci posso fare?)

pars, covs=curve_fit(foo, R, Vmedio, sigma=VStd)
V0, RT, RS=uncertainties.correlated_values(pars, covs)

print("risutati: {} {} {}".format(V0, RT, RS))


pylab.errorbar(R, Vmedio, VStd/N, fmt=".")
domain=np.linspace(min(R), max(R), 1000)
pylab.plot(domain, foo(domain,*pars))
pylab.savefig(dir_grph+"lastfit.pdf")

pylab.show()

chisq=np.sum((Vmedio-foo(R, *pars))**2/(VStd)**2)
prob=chisqprob(chisq,dof)
chisq1=np.sum((Vmedio-foo(R, *pars))**2/(VStd/N)**2)
print("chisq={} {} {}/{}".format(chisq, prob,chisq1,len(R)-3))

print("non fitta manco per il cazzo...evidentemente abbiamo sbagliato qualcosa in lab...forse andava in saturazione anche con resistenze più piccole, ma non in tutto il periodo, quindi non ce ne siamo accorti?\n\n\n")


print("#####risultati con il prodotto dei guadagni...")

Atot=A1*A2*A3*A4
print("Atot={}".format(Atot))
print("A1={} A2={} A3={} A4={}".format(A1, A2, A3, A4))


Df=2*np.pi*Dw
print("Df={}".format(Df))
T=uncertainties.ufloat(273+28, 5)

k_b=V0**2/(4*T*Atot**2*Df*RT) 

print("K_b={} vs K_b_exp=1.380e-23".format(k_b))

print('########risultati con il guadagno totale stimato con il partitore 1000:1...')

Atot=A_supp*A4
print("Atot={}".format(Atot))
print("A1={} A2={} A3={} A4={}".format(A1, A2, A3, A4))


Df=2*np.pi*Dw_supp
print("Df={}".format(Df))
T=uncertainties.ufloat(273+28, 5)

k_b=V0**2/(4*T*Atot**2*Df*RT) 





print("K_b={} vs K_b_exp=1.380e-23".format(k_b))


#fit non torna manco per nulla...domani prendo delle misure sere...
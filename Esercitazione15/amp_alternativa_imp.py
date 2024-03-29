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
"andrea": "/home/andrea/Documenti/Da salvare 12-5-2017/Documenti/GitHub/Lab3.2/",
"viviana": "C:\\Users\\viviana\\Documents\\GitHub\\Lab3.2\\"
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


print("===============Amplificazione alternativa=================")


pylab.figure(figsnum)
figsnum+=1
pylab.title("f vs amplificazione totale")
pylab.xlabel("frequenza [Hz]")
pylab.ylabel("A(f)")

dir_grph=dir+"grafici/"
dir = dir + "data/"
#####partitore....

R1=uncertainties.ufloat(9.91e3, mme(9.91e3, "ohm"))
R2=uncertainties.ufloat(10.1, mme(10.1, "ohm"))



####dati...

file="totamp.txt"
f, Vin, Vout, Vrms = np.loadtxt(dir+file,unpack=True)
df=51/1e6*f
Vin=Vin*1e-3
dVin=mme(Vin, "volt", "oscil")
dVout=mme(Vout, "volt", "oscil")

UVin=uncertainties.unumpy.uarray(Vin, dVin)*R2/(R1+R2)
UVout=uncertainties.unumpy.uarray(Vout, dVout)
Uamp=UVout/UVin

amp=uncertainties.unumpy.nominal_values(Uamp)
damp=uncertainties.unumpy.std_devs(Uamp)


#####fit...
#modello come se fosse un unico passabanda amplificato, con amplificatori ideali (con frequenza di taglio costante...)
g=lambda w, A, Q, w0, wt:1/(1+(w/wt)**2)**0.5*A*w/((w**2-w0**2)**2+w**2*w0**2/Q)**0.5

p0=(1e8, 10, 6.5e3, 1e4)
dof=len(f)-3
pars, covs = curve_fit(g, f, amp,p0, damp, maxfev=10000)
A, Q, w0, wt=uncertainties.correlated_values(pars, covs)
print("A= {} \n Q={}\n w0={}\n wt={}".format(A, Q**0.5, w0, wt))

######plot...
pylab.loglog()
pylab.errorbar(f, amp, damp,df, fmt='.')
domain=np.linspace(min(f), max(f), 1000)
gdomain = g(domain, *pars)
pylab.plot(domain, gdomain)
# xlim(0,17000)
# ylim(6000,80000)
vint = pylab.vectorize(int)
pylab.xlim(min(domain)*0.9,max(domain)*1.1)
pylab.xticks(vint((pylab.logspace(log10(min(domain)*0.9),log10(max(domain)*1.1), 5)//100)*100),vint((pylab.logspace(log10(min(domain)*0.9),log10(max(domain)*1.1), 5)//100)*100))
pylab.ylim(min(gdomain)*0.9, max(gdomain)*1.1)
pylab.yticks(vint((pylab.logspace(log10(min(gdomain)*0.9),log10(max(gdomain)*1.1), 5)//10)*10),vint((pylab.logspace(log10(min(gdomain)*0.9),log10(max(gdomain)*1.1), 5)//10)*10))
pylab.savefig(dir_grph+"amp_alternativa_imp.pdf")


chisq=np.sum((amp-g(f, *pars))**2/damp**2)
print(chisq, dof, chisqprob(chisq,dof))

Dw_supp=w0/Q**0.5

print("controllo di essere davvero a -3dB")

print("2**0.5  - g(w0, A, Q, w0, wt)/g(w0+Dw/2, A, Q, w0, wt) =  ",sqrt(2)-g(w0, A, Q, w0, wt)/g(w0+Dw_supp/2, A, Q, w0, wt))

print("2**0.5  - g(w0, A, Q, w0, wt)/g(w0-Dw/2, A, Q, w0, wt) =  ",sqrt(2)-g(w0, A, Q, w0, wt)/g(w0-Dw_supp/2, A, Q, w0, wt))


A_supp=g(w0, A, Q, w0, wt)

print("A_centrobanda={} \n ampiezza_banda={}".format(A_supp, Dw_supp))
#Dw_supp=w0/Q**0.5



dom=np.linspace(min(f), max(f), 1000)
integrale=np.sum(g(dom, A, Q, w0, wt)**2)*(max(f)-min(f))/1000/A_supp**2
print("-----------", integrale, np.pi/2*Dw_supp)

Df_true_2=integrale






import numpy as np
import matplotlib.pyplot as plt
import MaxwellConstruction as mx
import collections

#%%

if __name__ == "__main__":

    def ordToList( dict ):
    
        col = collections.OrderedDict(sorted(dict.items()))

        x = []
        
        y = []
    
        for k,v in col.items():

            x.append(k)
            y.append(v)

        return x,y

    # Arreglo con los valores de temperatura reducida para calcular las densidades de coexistencia

    TEos = np.concatenate( [np.arange(0.6,0.925,0.025) , np.array([0.925, 0.95, 0.975, 0.99, 0.995]) ] )
    
    # Curva de coexistencia de Van Der Waals

    vdw = mx.EOS('VanDerWaals', a=0.5, b=4.0)

    # Diccionario para facilitar el grafico: coex{ rho_r : T_r  }
    
    coex = {1:1}

    # Calculo de densidades de coexistencia para las teperaturas reducidas de TEos
    # Como se grafican valores reducidos (adimensionales), la curva es universal: no depende de las constantes a y b

    for i,T in enumerate(TEos):


        # Argumento necesario para la integracion de la EOS a T bajas
        
        step = 0.999
        if T < 0.6:
            step = 0.9999


        # Calculo de volumen reducido

        Vrmin,Vrmax = mx.coexistencia(vdw, T, plotPV=False, step_size=step)

        coex[1/Vrmin] = T
        coex[1/Vrmax] = T


    # Ordenamiento de coex para graficacion
        
    coex = ordToList( collections.OrderedDict(sorted(coex.items())) )

#    plt.plot(coex[0], coex[1], label='VdW')


#%%     Datos obtenidos de MaxwellConstruction para mesh = 100 x 100 tiempo 50000

lst = [ '6','625','65','675','7','725','75','775','8','825','85','875','9','925','95','975' ]
number = len(lst)

rhoc =  vdw.rhoc()

rhol = []
rhog = []


for idx in range(0,len(lst)):

    rhol.append( np.max(np.loadtxt('/home/coronelth/validacion_MxC/'+lst[idx] +'/rhoaux',np.float32) ) ) 
    rhog.append( np.min(np.loadtxt('/home/coronelth/validacion_MxC/'+lst[idx] +'/rhoaux',np.float32) ) ) 


Tr = np.arange(0.6,1.0,0.025)
Tr = np.concatenate([Tr,Tr])

rhor = np.concatenate([rhol,rhog])



#%%

plt.figure()

plt.plot(rhor/rhoc,Tr,'r.',ms=15)
plt.plot(coex[0], coex[1], label='VdW',linewidth=2.5)
plt.ylabel(r'$T/T_c$',fontsize=14)
plt.xlabel(r'$\rho/\rho_c$',fontsize=14)
plt.xscale('log')
plt.legend(loc = 'best', framealpha=1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.savefig('validacion_MxC_Tr_rhor.png')
plt.show()

plt.close
    
    

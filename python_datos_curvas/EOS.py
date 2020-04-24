import numpy as np
import matplotlib.pyplot as plt
import MaxwellConstruction as mx
import collections


# Este es un scrip de ejemplo para calcular las densidades de coexistencia definidas por la EOS de Van der Waals
# Para poder usarlo es necesario tener scipy, matplotlib y PyAstronomy (pip install PyAstronomy)
#
# Uso:
#
# Una vez que se importo el modulo MaxwellConstruction, ej:
#
#   import MaxwellConstruction as mx
#
# es necesario inicializar la ecuacion de estado con las constantes adecuadas
#
#   vdw = mx.EOS('VanDerWaals', a=0.5, b=4.0)
#
# A partir de esta EOS pueden obtenerse parametros criticos:
#
#   vdw.Tc()    ->  temperatura critica
#   vdw.rhoc()  ->  densidad critica
#   vdw.Pc()    ->  presion critica
#
# Hay que recordar que por definicion, una variable reducida corresponde al valor de la variable "normal" sobre su valor critico. Por ejemplo, para la densidad se tiene
#
#   rho_r = rho / rho_c
#
# Tambien puede usarse para calcular las densidades de coexistencia. La integral necesaria para realizar la construccion de Maxwell propiamente dicha esta resuelta de manera adimensional.
# Por lo tanto, para una temperatura reducida Tr = 0.9, se obtienen como resulado los volumenes reducidos de coexistencia
#
#   Vrmin,Vrmax = mx.coexistencia(vdw, Tr=0.9, plotPV=False)
#
# Si se desean obtener valores de densidad, simplemente queda por usar los valores criticos:
#
#   1/Vrmax -> Densidad reducida de la fase gaseosa
#   1/Vrmin -> Densidad reducida de la fase liquida
#
#   vdw.rhoc()/Vrmax -> Densidad de la fase gaseosa
#   vdw.rhoc()/Vrmin -> Densidad de la fase liquida




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

    plt.plot(coex[0], coex[1], label='VdW')

    


    plt.ylabel(r'$T/T_c$')

    plt.xlabel(r'$\rho/\rho_c$')

    plt.xscale('log')

    plt.legend(loc = 'best', framealpha=1)

    # plt.grid()

    # plt.rcParams['figure.dpi'] = 150

    plt.show()

    # plt.savefig( 'Imagenes/FC72_EOS.eps', format='eps', dpi=600 )

    # plt.savefig( 'Imagenes/FC72_EOS.png', format='png', dpi=600 )    

    # plt.gcf().clear()

    # plt.ioff()
#%%     Datos obtenidos de MaxwellConstruction para mesh = 100 x 100 tiempo 50000

rho_l  = np.array( [1.9e-1 ,1.9e-1 ,1.8e-1 ,1.7e-1, 1.6e-1, 1.5e-1, 1.4e-1, 1.2e-1])/vdw.rhoc()
rho_g  = np.array( [4.9e-3, 7.3e-3 ,1.1e-2 ,1.5e-2 ,2.0e-2, 2.7e-2, 3.6e-2, 4.8e-2])/vdw.rhoc()
T      = np.array ([ 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95])


#%%

plt.figure()
plt.plot(rho_l,T,'r.',ms=15)
plt.plot(rho_g,T,'r.',ms=15)
plt.plot(coex[0], coex[1], label='VdW',linewidth=2.5)
plt.ylabel(r'$T/T_c$',fontsize=14)
plt.xlabel(r'$\rho/\rho_c$',fontsize=14)
plt.xscale('log')
plt.legend(loc = 'best', framealpha=1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.show()
#plt.savefig('TP_4_ej_7_loss_conv.png')
plt.close









#%%
import VdWColumn as vdw

import matplotlib.pyplot as plt

import numpy as np

import os
#%%


if __name__ == "__main__":

        
    # Solucion analitica (todo en unidades reducidas)
    #
    #   Ttop    = 0.99 
    #   Tbottom = 0.9  
    #   Et = 0.001 (energia gravitacional reducida maxima)
    #   Densidad inicial = 1
    #   updateT. Si es verdadero, resuelve ecuacion de energia. Sino, perfil lineal fijo de temperatura entre Tt y Tb
    #
    #   Sol[0] = Arreglo con coordenadas donde se calculo la solucion. En este caso, estan dadas en unidades de energia gravitacional reducida. Por lo tanto, el ultimo valor es Et.
    #   Sol[1] = Arreglo con densidad de gas. Tiene el tamanio de Sol[0], asi que por debajo de la interfase tiene valor de coexistencia (para no dejar el arreglo vacio)
    #   Sol[2] = Arreglo con densidad de liquido. Tiene el tamanio de Sol[0], asi que por encima de la interfase tiene valor de coexistencia (para no dejar el arreglo vacio)
    #   Sol[3] = Posicion (indice) de la interfase dentro del arreglo Sol[0]
    #   Sol[4] = Arreglo con temperatura en cada uno de los nodos calculados



    # Calculo de solucion semi-analitica
    
    Sol = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.9, kappa = 1.0, updateT = True, thcond = 'linear' )
    

    
    # Grafico. Por simplicida, se grafican los valores de densidad cada un cierto numero de puntos

    # Liquido (debajo de Sol[3])
    
    for k in np.linspace(0,Sol[3],20):
            
        plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[2][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')


    # Gas (encima de Sol[3])        
                
    for k in np.linspace(Sol[3],len(Sol[0])-1,20):
            
        plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[1][np.int(k)],  linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
            

                       


    plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

    plt.xlabel(r'$y \, / \, H$')        
   
    plt.legend( loc='best' )

    plt.show() 
#%%

# Temperatura y densidad critica para a = 0.5 y b = 4.0

Tc   =  0.037037037037037035
rhoc =  0.08333333333333333   
    
    
import numpy as np

rho_l  = []
rho_g  = []
T_l    = []
T_g    = []
rhoaux = []
Taux   = []

#lst = [ '6','625','65','675','7','725','75','775','8','85','875','9','925','95','975' ]
lst = [ '6','65','7','75','8','85','9','95' ]

number = len(lst)



#%%
for idx in range(0,len(lst)):

    rhoaux.append(np.loadtxt('/home/coronelth/VdWColumnHT_note/simple_precision/'+lst[idx] +'/rhoaux',np.float32).reshape([300,3]).mean(1,np.float32)) # 300 x 1
    Taux.  append(np.loadtxt('/home/coronelth/VdWColumnHT_note/simple_precision/'+lst[idx] +'/Taux',np.float32).reshape([300,3]).mean(1,np.float32)) # 300 x 1

#%%
rhoaux = np.array(rhoaux)
for idx in range(0,len(lst)):
    
    rho_l.append(  rhoaux [idx][0 ] )
    rho_g.append(  rhoaux [idx][-1] )
    T_l.  append(  Taux   [idx][0 ] )
    T_g.  append(  Taux   [idx][-1] )

#%%

H = (rhoaux.shape[1])*1.0

Y_r = np.arange(H).astype(np.float32) / H

#%% 
rho_r = rhoaux/np.float32(rhoc)

for k in np.linspace(0,rho_r.shape[1]-1,20):
            
    plt.plot( Y_r[np.int(k)], rho_r[2][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
    
    plt.plot( Y_r[np.int(k)], rho_r[4][np.int(k)], linestyle = 'None', color = 'r', marker = 'o', mfc = 'None')


#%%
T_r = Taux/np.float32(Tc)

for k in np.linspace(0,T_r.shape[1]-1,20):
            
    plt.plot( Y_r[np.int(k)], T_r[2][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
    
    plt.plot( Y_r[np.int(k)], T_r[5][np.int(k)], linestyle = 'None', color = 'r', marker = 'o', mfc = 'None')





#%%
Tr_l   = np.array(T_l,np.float32) / Tc
Tr_g   = np.array(T_g,np.float32) / Tc
Rhor_l = np.array(rho_l,np.float32) / rhoc
Rhor_g = np.array(rho_g,np.float32) / rhoc

# %%
plt.figure()
plt.plot(Rhor_l,Tr_l,'b.',ms=5)
plt.plot(Rhor_g,Tr_g,'r.',ms=5)
#plt.plot(coex[0], coex[1], label='VdW',linewidth=2.5)
plt.ylabel(r'$T/T_c$',fontsize=14)
plt.xlabel(r'$\rho/\rho_c$',fontsize=14)
#plt.xscale('log')
plt.legend(loc = 'best', framealpha=1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.show()
#plt.savefig('TP_4_ej_7_loss_conv.png')
plt.close  

#%%
    # Grafico. Por simplicida, se grafican los valores de densidad cada un cierto numero de puntos

    # Liquido (debajo de Sol[3])
    
    for k in np.linspace(0,rhoaux.shape[1],20):
            
        plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[2][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')


    # Gas (encima de Sol[3])        
                
    for k in np.linspace(Sol[3],len(Sol[0])-1,20):
            
        plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[1][np.int(k)],  linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
            

                       


    plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

    plt.xlabel(r'$y \, / \, H$')        
   
    plt.legend( loc='best' )

    plt.show() 









        
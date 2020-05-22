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
    
    Sol = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.8, kappa = 1.0, updateT = True, thcond = 'linear' )
    

# %%
    # Grafico. Por simplicida, se grafican los valores de densidad cada un cierto numero de puntos

    # Liquido (debajo de Sol[3])
    
    for k in np.linspace(0,Sol[3],20):
            
        plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[2][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')


    # Gas (encima de Sol[3])        
                
    for k in np.linspace(Sol[3],len(Sol[0])-1,20):
            
        plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[1][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
            

                       


    plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

    plt.xlabel(r'$y \, / \, H$')        
   
    plt.legend( loc='best' )

    plt.show() 
#%% Densidades concatenadas
    
    rho_analitico = np.concatenate( ( Sol[2][:Sol[3]], Sol[1][Sol[3]:] ) )
    
    E_r = Sol[0] / Sol[0][-1]
    
#    plt.plot( E_r,rho_semi_empirico ,'.')
    
#%% Obtención de densidad y temperaturas reducidadas calculadas de forma semi-empíricas
    
    Sol_5 = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.5, kappa = 1.0, updateT = True, thcond = 'linear' )
    Sol_6 = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.6, kappa = 1.0, updateT = True, thcond = 'linear' )
    Sol_7 = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.7, kappa = 1.0, updateT = True, thcond = 'linear' )
    Sol_8 = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.8, kappa = 1.0, updateT = True, thcond = 'linear' )
    Sol_9 = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.9, kappa = 1.0, updateT = True, thcond = 'linear' )
    
    rho_5 = np.concatenate( ( Sol_5[2][:Sol_5[3]], Sol_5[1][Sol_5[3]:] ) )
    rho_6 = np.concatenate( ( Sol_6[2][:Sol_6[3]], Sol_6[1][Sol_6[3]:] ) )
    rho_7 = np.concatenate( ( Sol_7[2][:Sol_7[3]], Sol_7[1][Sol_7[3]:] ) )
    rho_8 = np.concatenate( ( Sol_8[2][:Sol_8[3]], Sol_8[1][Sol_8[3]:] ) )
    rho_9 = np.concatenate( ( Sol_9[2][:Sol_9[3]], Sol_9[1][Sol_9[3]:] ) )
    
    T_5 =Sol_5 [4]
    T_6 =Sol_6 [4]
    T_7 =Sol_7 [4]
    T_8 =Sol_8 [4]
    T_9 =Sol_9 [4]

    Er_5 = Sol_5[0] / Sol_5[0][-1]
    Er_6 = Sol_6[0] / Sol_5[0][-1]
    Er_7 = Sol_7[0] / Sol_5[0][-1]
    Er_8 = Sol_8[0] / Sol_5[0][-1]
    Er_9 = Sol_9[0] / Sol_5[0][-1]
    
    Y_sol = np.arange(10000)/10000.0
    
# %%

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

lst = [ '6','625','65','675','7','725','75','775','8','825','85','875','9','925','95','975' ]
#lst = [ '6','65','7','75','8','85','9','95' ]

number = len(lst)



#%%
for idx in range(0,len(lst)):

    rhoaux.append(np.loadtxt('/home/coronelth/exp_mas_tiempo_VdWColumnHT_note/simple_precision/'+lst[idx] +'/rhoaux',np.float32).reshape([300,3]).mean(1,np.float32)) # 300 x 1
    Taux.  append(np.loadtxt('/home/coronelth/exp_mas_tiempo_VdWColumnHT_note/simple_precision/'+lst[idx] +'/Taux',np.float32).reshape([300,3]).mean(1,np.float32)) # 300 x 1


rhoaux = np.array(rhoaux)


H = (rhoaux.shape[1])*1.0

Y_r = np.arange(H).astype(np.float32) / H

rho_r = rhoaux/np.float32(rhoc)

#%% 

for k in np.linspace(0,rho_r.shape[1]-1,30):
    
     plt.plot( Y_r[np.int(k)], rho_r[ 0 ][np.int(k)], linestyle = '--', color = 'r', marker =  '>', mfc = 'None')
     
     plt.plot( Y_r[np.int(k)], rho_r[ 4 ][np.int(k)], linestyle = '--', color = 'c', marker =  'o', mfc = 'None')
     
     plt.plot( Y_r[np.int(k)], rho_r[ 8 ][np.int(k)], linestyle = 'None', color = 'b', marker = '.', mfc = 'None')
     
     plt.plot( Y_r[np.int(k)], rho_r[ 12 ][np.int(k)], linestyle = 'None', color = 'g', marker = 'x', mfc = 'None')
     


plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15,fontsize=14)

plt.xlabel(r'$y \, / \, H$',fontsize=14)        
   
plt.legend( loc='best' )
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(False)
plt.show()
#plt.savefig('')

plt.show()    
#%% Curvas obtenidas y analíticas

esp = np.int32(15)
ms = '6'

plt.figure()
    
plt.plot( Y_r[0:rho_r.shape[1]:esp], rho_r[ 0 ][0:rho_r.shape[1]:esp], label ='$T_r = 0.6$', linestyle = 'None', color = 'r', marker =  'D', mfc = 'r', ms = ms ) 
plt.plot( Y_r[0:rho_r.shape[1]:esp], rho_r[ 4 ][0:rho_r.shape[1]:esp], label ='$T_r = 0.7$', linestyle = 'None', color = 'm', marker =  '>', mfc = 'm', ms = ms)     
plt.plot( Y_r[0:rho_r.shape[1]:esp], rho_r[ 8 ][0:rho_r.shape[1]:esp], label ='$T_r = 0.8$', linestyle = 'None', color = 'b', marker = 's', mfc = 'b', ms = ms)     
plt.plot( Y_r[0:rho_r.shape[1]:esp], rho_r[12 ][0:rho_r.shape[1]:esp], label ='$T_r = 0.9$', linestyle = 'None', color = 'g', marker = 'v', mfc = 'g', ms = ms)

plt.plot(Y_sol,rho_6,'k')
plt.plot(Y_sol,rho_7,'k')
plt.plot(Y_sol,rho_8,'k')
plt.plot(Y_sol,rho_9,'k')

plt.legend( loc='best' )
plt.ylabel(r'$\rho/\rho_c$',fontsize=14)
plt.xlabel(r'$y/H$',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig('rhor_vs_Yr_VdWColumnHT.png')

plt.show()

#%%
T_r = Taux/np.float32(Tc)

for k in np.linspace(0,T_r.shape[1]-1,20):
    
    plt.plot( Y_r[np.int(k)], T_r [ 3 ][np.int(k)], linestyle = 'None', color = 'r', marker =  'o', mfc = 'None')
    
    plt.plot( Y_r[np.int(k)], T_r [ 5 ][np.int(k)], linestyle = 'None', color = 'b', marker = '.', mfc = 'None')
    
    plt.plot( Y_r[np.int(k)], T_r [ 11 ][np.int(k)], linestyle = 'None', color = 'g', marker = 'x', mfc = 'None')
    
 
plt.ylabel(r'$T_r$', rotation='horizontal', labelpad=15, fontsize=14)

plt.xlabel(r'$y \, / \, H$', fontsize =14)        
   
plt.legend( loc='best' )
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.show()
#plt.savefig('')

plt.show()    

#%%

esp = np.int32(15)
ms = '6'

plt.figure()
    
plt.plot( Y_r[0:T_r.shape[1]:esp], T_r[ 0 ][0:T_r.shape[1]:esp], label ='$T_r = 0.6$', linestyle = 'None', color = 'r', marker =  'D', mfc = 'r', ms = ms ) 
plt.plot( Y_r[0:T_r.shape[1]:esp], T_r[ 4 ][0:T_r.shape[1]:esp], label ='$T_r = 0.7$', linestyle = 'None', color = 'm', marker =  '>', mfc = 'm', ms = ms)     
plt.plot( Y_r[0:T_r.shape[1]:esp], T_r[ 8 ][0:T_r.shape[1]:esp], label ='$T_r = 0.8$', linestyle = 'None', color = 'b', marker = 's', mfc = 'b', ms = ms)     
plt.plot( Y_r[0:T_r.shape[1]:esp], T_r[12 ][0:T_r.shape[1]:esp], label ='$T_r = 0.9$', linestyle = 'None', color = 'g', marker = 'v', mfc = 'g', ms = ms)

plt.plot(Y_sol,T_6,'k')
plt.plot(Y_sol,T_7,'k')
plt.plot(Y_sol,T_8,'k')
plt.plot(Y_sol,T_9,'k')

plt.legend( loc='best' )
plt.ylabel(r'$T/T_c$',fontsize=14)
plt.xlabel(r'$y/H$',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig('Tr_vs_Yr_VdWColumnHT.png')

plt.show()






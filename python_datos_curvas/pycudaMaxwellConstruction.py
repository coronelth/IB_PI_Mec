#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 08:22:01 2020

@author: coronelth
"""
# %%
from time import time
import numpy as np
import pycuda
from pycuda import gpuarray
import pycuda.autoinit
import argparse
import ctypes
import random

random.seed(0)
# %%
# cuEColl_mod         = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaEnergiaEcu/cudaEnergyCollision.ptx')
# cuEEqDistNode_mod   = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaEnergiaEcu/cudaEnergyEqDistNode.ptx')
# #cuESource_mod       = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaEnergiaEcu/cudaEnergySource.ptx')
# cuETemo_mod         = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaEnergiaEcu/cudaEnergyTemp.ptx')
# #cuEFixedTBound_mod  = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaEnergiaEcu/cudaFixedTBoundary.ptx')

# cuF_ker         = cuEColl_mod.get_function('cudaEnergyCollision')
# cuFEqDistNode_ker   = cuEEqDistNode_mod.get_function('cudaEnergyEqDistNode')
#cuFSource_ker       = zm_mod.get_function('cudaEnergySource')
#cuETemo_ker         = zm_mod.get_function('cudaEnergyTemp')
#cuEFixedTBound_ker  = zm_mod.get_function('cudaFixedTBoundary')

#%% Inclusión de bibliotecas de C y extracción de funciones
 
from bibliotecas_c import load_lib_c

load_lib_c()

basicmes = libbasic.basicMesh

#%%

basicMesh()


#%%
# Inclusión de librerias de CUDA y extracción de funciones
#
#cuFFint_mod     = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaFuerza/cudaFuerzaFuerzaint.ptx')
cuFFtotal_mod   = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaFuerza/cudaFuerzaFuerzatotal.ptx')
#
#cudaFuerzaFuerzaint     = zm_mod.get_function('cudaFuerzaFuerzaint')
cudaFuerzaFuerzatotal   = cuFFtotal_mod.get_function('cudaFuerzaFuerzatotal')
#
#cuMColl_mod     = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaMomentoFunciondist/cudaMomentoCollision.ptx')
cuMDensity_mod  = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaMomentoFunciondist/cudaMomentoDensity.ptx')
cuMVelosity_mod = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaMomentoFunciondist/cudaMomentoVelocity.ptx')
cuSStre_mod     = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaStreaming/cudaStream.ptx')
cuSSwap_mod     = pycuda.driver.module_from_file('/home/utnsistemas/Downloads/ptx/objects-Release/cudalbequationPTX/cudaStreaming/cudaSwap.ptx')
#
#cudaMomentoCollision      = cuMColl_mod.get_function('cudaMomentoCollision')
cudaMomentoDensity        = cuMDensity_mod.get_function('cudaMomentoDensity')
cudaMomentoVelocity       = cuMVelosity_mod.get_function('cudaMomentoVelocity')
cudaStream                = cuSStre_mod.get_function('cudaStream')
cudaSwap                  = cuSSwap_mod.get_function('cudaSwap')

#%%


if __name__ == '__main__':



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='pycudaMaxwellConstruction Construccion de Maxwell isotérmica en dominio bidimensional')

    parser.add_argument('--timeSteps', help='Pasos de tiempo', type = np.uint32, default = 100)
    
    parser.add_argument('--wrtInterval', help='Intervalo de escritura', type = np.uint32, default = 10)

    parser.add_argument('--xgrid', help='Tamano de grilla', type = np.int32, default = 256)    

    args = parser.parse_args()
    
    print( "                    \n" )
    print( "     o-----o-----o  \n" )
    print( "     | -   |   - |  \n" )
    print( "     |   - | -   |                pycudaMaxwellConstruction \n" )
    print( "     o<----o---->o  \n" )
    print( "     |   - | -   |  Construccion de Maxwell isotérmica en dominio bidimensional\n" )
    print( "     | -   |   - |  \n" )
    print( "     o-----o-----o  \n\n" )


    nwrite =   np.uint32( (timeSteps/wrtInterval + 1) )

    timeList = np.uint32( np.ones( nwrite, dtype=np.uint32 ) * [ (x * args.wrtInterval ) for x in range(nwrite)] ) # Estaba definido como entero
    
    delta_t = np.float32(1.0)
    
    
    # Lectura de vecinos

    with open( 'lattice/neighbours' ) as nbfile:

        nPoints, meshQ = nbfile.readline().split()

        
    nPoints = np.int32( nPoints )

    meshQ = np.int32( meshQ )    
            
    print( '\n Lectura de {} vecinos con {} componentes\n'.format(nPoints, meshQ) )

#%%    Parámetros a Inicializar
    
#   Parametros del modelo

    G = -1.0 

    c = 1.0 

    sigma = 0.125 
                   
#   Constantes de EOS

    a = 0.5 

    b = 4.0
    
#    Gravedad

    g = np.zeros( 3, dtype=np.float32 ) 

#    Temperatura de referencia

    Tr = 0.9

#    Temperatura critica

    Tc = 0.037037037

#    Densidad critica

    Rhoc = 0.083333333

#%% Inicialización de parámetros
    
#    readInitialParameters (G, c, sigma, a, b, g, Tr, Tc, Rhoc)

    temp = Tr * Tc
    
    
#%%
#    # Inicializacion
#
#    hostField = np.zeros( nPoints*meshQ, dtype=np.float32 )  #Field
#
#    hostRho   = np.ones( nPoints, dtype=np.float32 ) * Rhoc + 
#    [random.uniform(-Rhoc/100.0,Rhoc/100.0) for x in range(nPoints)]  #Density
#  
#    hostU     = np.zeros( nPoints*3, dtype=np.float32 )  #Velocity macroscopic
#
#    hostT     = np.ones( nPoints, dtype=np.float32 ) * temp      #Temperature
#
#    hostFint  = np.zeros( nPoints*3, dtype=np.float32 )     #Interaction force
#
#    hostF     = np.zeros( nPoints*3, dtype=np.float32 ) #Total force ( volumetric add interaction )

#
#    cuFFint_ker( hostFint, hostRho, hostT, mesh, G, c, mesh.lattice.cs2 , a, b)
#    
#    cuFFtotal_mod( hostF, hostFint, hostRho, g, &mesh )
    
#    momentoFeq = ( &mesh, hostField, hostRho, hostU)
#    
#%%     Arreglos de device
#
#    deviceField = gpuarray.to_gpu( hostField )

#    deviceSwap = gpuarray.zeros( nPoints * meshQ, np.float32)

#
#    deviceRho = gpuarray.to_gpu( hostRho )    
#
#    deviceU = gpuarray.to_gpu( hostU )
#
#    deviceT = gpuarray.to_gpu( hostT )        
#
#    deviceFint = gpuarray.to_gpu( hostFint )
#
#    deviceF = gpuarray.to_gpu( hostF )

#    deviceGravity = gpuarray.to_gpu( g )
#%%
    
    # Factores de relajacion para colision

    Tau= np.array([ 1.0 , 0.8 , 1.1 , 1.0 , 1.1 , 1.0 , 1.1 , 0.8 , 0.8], dtype=np.float32)
#    deviceTau = gpuarray.to_gpu( Tau )
    
    #Antes de comenzar la simulacion, escritura de los campos iniciales
    
    scfields = np.chararray((1, 2))
    scfields = ('rho' , 'T' )
    
    scfields = ["rho" , "T" ]
    
    scfields_array = (ctypes.c_char_p * (len(scfields)+1))()
    
    
    vfields = np.chararray((1, 1))

    vfields = ('U')
#
    updateCaseFile(scfields, 2, vfields, 1, timeList, nwrite);
#%%# 
from ctypes import *

dll = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/libio.so')
dll.updateCaseFile.argtypes = POINTER(c_char * 100),c_uint,POINTER(c_char * 100),c_uint,POINTER(c_uint),c_uint
dll.updateCaseFile.restype = None

A = c_char * 100  # make a name for the char[100] type.

# This is *not* fast.  Use a numpy array if you need speed
def make(*args):
    a = (A * len(args))()          # create a[n][100] array
    for i,arg in enumerate(args):  # initialize each element
        a[i].value = arg.encode()  # encode for byte strings.  Alternatively, pass bytes strings.
    return a

scfields = make('Rho','T')
vfields = make('U')
timeList = (c_uint * 2)(1,2)
dll.updateCaseFile(scfields,2,vfields,1,timeList,2)    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
#%%
#    writeMeshToEnsight( &mesh );
#
#    writeScalarToEnsight(scfields[0], rho, &mesh, 0);
#
#    writeScalarToEnsight(scfields[1], Temp, &mesh, 0);
#
#    writeVectorToEnsight(vfields[0], U, &mesh, 0);

    gs = int( nPoints*meshQ/args.xgrid ) + 1


    # Ejecucion LB
    for ts in range(1,(timeSteps+1)):

    

    	# Colision

    	cudaMomentoCollision( deviceField,
                          deviceRho,
                          deviceU,
                          deviceF,
                          deviceFint,
                          deviceT,
                          deviceTau,
                          cmesh.lattice.M,
                          cmesh.lattice.invM,
                          cmesh.nPoints,
                          cmesh.Q,
                          delta_t,
                          a,
                          b,
                          c,
                          mesh.lattice.cs2,
                          G,
                          sigma,
                          block=( args.xgrid, 1, 1 ),
                          grid=( gs, 1, 1) )          
        pycuda.driver.Context.synchronize()

    	# Streaming

	    cudaStreaming( deviceField,
                   deviceSwap,
                   cmesh.nb,
                   cmesh.nPoints,
                   cmesh.Q,
                   block=( args.xgrid, 1, 1 ),
                   grid=( gs, 1, 1) )          
         pycuda.driver.Context.synchronize()


	
    	# Actualizacion de densidad macroscopica
	
    	cudaMomentoDensity( deviceField,
                        deviceRho,
                        cmesh.nPoints,
                        cmesh.Q,
                        block=( args.xgrid, 1, 1 ),
                        grid=( gs, 1, 1) )          
        pycuda.driver.Context.synchronize()
                        



    	# Actualizacion de fuerzas

    	cudaFuerzaFuerzain( deviceFint,
                        deviceRho,
                        deviceT,
                        cmesh.nPoints,
                        cmesh.Q,
                        cmesh.lattice.vel,
                        cmesh.lattice.reverse,
                        cmesh.nb,
                        G,
                        c,
                        mesh.lattice.cs2,
                        a,
                        b,
                        block=( args.xgrid, 1, 1 ),
                        grid=( gs, 1, 1) )          
        pycuda.driver.Context.synchronize()

    	cudaFuerzaFuerzatotal( deviceF,
                           deviceFint,
                           deviceRho,
                           deviceGravity,
                           cmesh.nPoints,
                           block=( args.xgrid, 1, 1 ),
                           grid=( gs, 1, 1) )          
        pycuda.driver.Context.synchronize()



    	# Actualizacion de velocidad macroscopica

    	cudaMomentoVelocity(deviceField,
                         deviceRho,
                         deviceU,
                         deviceF,
                         cmesh.lattice.vel,
                         mesh.nPoints,
                         mesh.Q,
                         block=( args.xgrid, 1, 1 ),
                         grid=( gs, 1, 1) )          
        pycuda.driver.Context.synchronize()

	
	


    	# Escritura de campos
        for wt in range(0,nwrite):
	
    	  	    if( timeList[wt] == ts ) :


                # Copia de vuelta al host
                
                hostField = deviceField.get()

                hostRho = deviceRho.get()

                hostU = deviceU.get()

                hostT = deviceT.get()

                                   
                t2 = time()
		
    	    	scalar elap = elapsedTime(&Time);

    	    	print( ' Tiempo = {:g}\n'.format(t2) );
		   	    	
                print(' Tiempo de ejecución {:g} segundos\n'.format(t2) )

    	    	writeScalarToEnsight(scfields[0], rho, &mesh, wt);

    	    	writeScalarToEnsight(scfields[1], Temp, &mesh, wt);

    	    	writeVectorToEnsight(vfields[0], U, &mesh, wt);


    t2 = time()
    print( '\n Fin. Tiempo total = {:g} segundos\n\n'.format(t2-t1) );
    print(' --------------------------------------------')
     

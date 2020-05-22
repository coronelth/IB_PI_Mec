#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 03:22:01 2020

@author: coronelth
"""
#%%
# Inclusión de bibliotecas de C y extracción de funciones

import ctypes


#def load_lib_c():

libbasic        = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/libbasic.so')
libd2q9         = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/libd2q9.so')
libbio          = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/libio.so')
libfdoperations = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/libfdoperations.so')
liblatticemesh  = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/liblatticemesh.so')
liblatticemodel = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/liblatticemodel.so')
liblbequation   = ctypes.CDLL('/home/coronelth/Desktop/Tesis_Grado_Ing_Mec_IB/LBCUDA_Test/lib/liblbequation.so')

readInitialParameters = libbasic.readInitialParameters
writeMeshToEnsigh     = libbio.writeMeshToEnsight
writeScalarToEnsight  = libbio.writeScalarToEnsight
writeVectorToEnsight  = libbio.writeVectorToEnsight
updateCaseFile        = libbio.updateCaseFile
readBasicMesh         = liblatticemesh.readBasicMesh
momentoFeq            = liblbequation.momentoFeq

#    %%
#    basicMesh =libbasic.basicMesh
#    basicMesh.argtypes = (  )
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 22:41:31 2020

@author: coronelth
"""

class lattice():
    def __init__ (self):
        self.DdQq   = 'D2Q9'
        self.q      = None
        self.c2s    = (1.0/3.0)
        self.vel    = None
        self.reverse= None
        self.M      = None
        self.invM   = None


class basicMesh(lattice):
    
    def __init__ (self):
        self.nPoints        = None
        self.Q              = None
        self.nb             = None
        self.ncells         = None
        self.vtkCells       = None
        self.lattice        = None
            
        
        
    def iniciar(self):
        
        with open( 'lattice/neighbours' ) as nbfile:

            self.nPoints, self.Q = nbfile.readline().split()
        
            self.nb = nbfile.read().split()
        
            self.nb = np.int32(np.ravel(neighbours)).reshape((np.int32(self.nPoints), np.int32(self.Q)))
            
            
        
        if len(self.layers) > 0 :
            layer.init_w(self.layers[-1].dim_output())
        
        self.layers.append(layer)   
        self.count_layers = len(self.layers)
        
        
    def predict(self,x):
        
        for i in range (self.count_layers):
            x = self.layers[i].forward(x)
            
        self.end_score = x
       
        return x
        #return np.argmax( aux ,axis = 1)
    
    def SGD(self,costo,y,lr =1e-4,reg = 1e-5):
        
        aux = costo.grad(self.end_score,y)
               
        for i in range (self.count_layers,0,-1):
            aux = self.layers[i-1].back(aux,lr,reg)
    
                    
    def fit(self,costo,metrica, x_train,y_train,epocas,sizebatch=1,lr =1e-5,
            reg=1e-5,x_test=None , y_test=None):
        
        nro_batchs=int(y_train.shape[0]/sizebatch)
        error = np.zeros(epocas) 
        accuracy = np.zeros(epocas)
        
        if x_test is not None:
            val_acc = np.zeros(epocas)
            val_loss = np.zeros(epocas) 

        for i in range(epocas):
                    
            indexrandom=np.arange(x_train.shape[0])
            np.random.shuffle(indexrandom)
            
            for js in range (nro_batchs):
                       
                x_batch=x_train[indexrandom[(js*sizebatch):((js+1)*sizebatch)],:]
                y_batch=y_train[indexrandom[(js*sizebatch):((js+1)*sizebatch)]]
                
                
                y_predict = self.predict(x_batch)
                self.SGD(costo,y_batch,lr,reg)
                
                error[i]+= costo.loss(self.end_score,y_batch) 
                accuracy[i] += metrica(y_predict,y_batch)
            
            error[i]= error[i]/nro_batchs
            accuracy[i]= accuracy[i]/nro_batchs
            
#            #voy a tomar los 1000 primeros valores y ver cuanto le pega
#            tamano_prueba=4
#    
#            y_pred_prueba = self.predict(x_train[:,:tamano_prueba])
#            accuracy[i] = metrica(y_pred_prueba,y_train[:tamano_prueba])
            
            if x_test is not None:
                print("epoca:{} acc:{:.2f} loss:{:.2f} val_acc:{:.2f} val_loss:{:.2f}".format(i,
                      accuracy[i],error[i],val_acc[i],val_loss[i]))
                history = { "loss": error, "acc": accuracy,
                           "loss_val": val_loss,"val_acc" : val_acc }    
            
            
                y_pred_test = self.predict(x_test)
                val_loss[i]=costo.loss(self.end_score,y_test) 
                val_acc[i]=metrica(y_pred_test,y_test)
            
            if x_test is None:            
                print("epoca:{} acc:{:.2f} loss:{:.2f} ".format(i,accuracy[i],error[i]))
                history = { "loss": error, "acc": accuracy }   
                       
        return history
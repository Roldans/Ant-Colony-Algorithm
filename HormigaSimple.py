
# coding: utf-8

# In[1]:

import copy
import random


# In[2]:

def LanzadorPruebas(FicheroTexto,CapacidadMax,Ajuste,TasaDeAumento,TasaDeEvaporacion,NumHormigas):
    Objetos= LeeFichero(FicheroTexto)
    Objetos=OrdenaObjetos(Objetos)
    NumObjetos= len(Objetos)
    Feromonas=[]
    for i in range(NumObjetos):
        Feromonas.append(100000)
    Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)
    return Hormiguero(Objetos,Feromonas,CapacidadMax,Ajuste,TasaDeAumento,TasaDeEvaporacion,NumHormigas)



# In[3]:

#Lanzador de hormigas y actualizador del valir de feromonas a uno mas alto
def Lanzador(FicheroTexto,CapacidadMax,TasaDeAumento,TasaDeEvaporacion,NumHormigas):
    Ajuste=[0.5,0.5,2]
    Objetos= LeeFichero(FicheroTexto)
    Objetos=OrdenaObjetos(Objetos)
    NumObjetos= len(Objetos)
    Feromonas=[]
    for i in range(NumObjetos):
        Feromonas.append(100000)
    Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)
    solucion=Hormiguero(Objetos,Feromonas,CapacidadMax,Ajuste,TasaDeAumento,TasaDeEvaporacion,NumHormigas)
    solucionDescodificada=[[],]
  
    for o in range(NumObjetos):        
        if(solucion[1][o]==1):
            solucionDescodificada[0].append(Objetos[o])
    solucionDescodificada.append(solucion[2])
    solucionDescodificada.append(solucion[0])   
    return solucionDescodificada


# In[4]:

#Generador de las soluciones para un hormiguero
def Hormiguero(Objetos=[[],],Feromonas=[],CapacidadMax=0,Ajuste=[0,0,0],TasaDeAumento=0,TasaDeEvaporacion=0,NumeroHormigas=0):

    MejorSolucion=[0,InstanciaArray(Objetos),0]#{ValorTotal,{Lista de objetos cogidos}}
    #SolucionActual=[0,[0,0,0,0,0,0,0,0,0,0],0]#Solucion para la hormiga
    Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)#Calcula las probabilidades según la formula mágica
   
    for i in range(NumeroHormigas):#Bucle Hormiguero,se repite una vez por cada hormiga
        SolucionActual=[0,InstanciaArray(Objetos),0]#Solucion para la hormiga
        SolucionActual[1]=Hormiga(Objetos,Probabilidades,CapacidadMax)#el recorrido de cada hormiga individual
       
       
        for z in range(len(SolucionActual[1])):
            SolucionActual[0]+=SolucionActual[1][z]*Objetos[z][2]#Sumatorio de valor
            
        if(MejorSolucion[0]<SolucionActual[0]):#Actualizacion de Mejor Solución
            MejorSolucion=SolucionActual
            
        ActualizaFeromonas(Feromonas,MejorSolucion[1],TasaDeAumento,TasaDeEvaporacion)#Actualiza las feromonas tras cada hormiga
        Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)#se actualiza las probabilidades con las nuevas feromonas

    #print(Feromonas)
    for y in range(len(MejorSolucion[1])):
        MejorSolucion[2]+=MejorSolucion[1][y]*Objetos[y][1]#Sumatorio de pesos
    return MejorSolucion


# In[5]:

#Ordena la lista de objetos en funcion de su Valor/Peso de mayor a menor
def OrdenaObjetos(Objetos=[[],]):
    res=[]
    ls = copy.deepcopy(Objetos)       #copia la lista
    max=0                             #objeto con mayor ratio
    for j in range(len(Objetos)):     #bucle en para toda la lista de objetos
        maxvp=0                       #mayor ratio
        
        for i in range(len(ls)):      #bucle interno para los objetos que queda sin seleccionar
            
            if maxvp<ls[i][2]/ls[i][1]:#si se encuentra un objeto mejor se actualiza
                
                maxvp=ls[i][2]/ls[i][1]#actualizamos el maximo ratio
                max=i                  #actualizamos el objeto
        res.append(ls[max])            #terminado el bucle se añade el objeto seleccionado
        ls.pop(max)                    #el objeto seleccionado se elimina de la lista copia
    return res


# In[6]:

#Creacion de una solucion para una hormiga a partir de un numero rando y de el conjunto de valoresç
#obtenidos a partir de las feromonas
def Hormiga(Objetos=[],Probabilidades=[],CapacidadMAX=0):
    Solucion=InstanciaArray(Objetos)
    Capacidad=0
    for i in range(len(Probabilidades)): 
        alea=random.random()
        #print(alea)
        if(alea<Probabilidades[i]):
            if(CapacidadMAX>Capacidad+Objetos[i][1]):
                Solucion[i]=1
                Capacidad = Capacidad+Objetos[i][1]
        else:
            Solucion[i]=0
    return Solucion         


# In[7]:

#Actualizacion de la lista de feromonas tras un viaje de una hormiga
def ActualizaFeromonas(Feromonas=[],UltimaSolucion=[],TasaDeAumento=0,TasaDeEvaporacion=0):
    for i in range(len(Feromonas)):
        if(UltimaSolucion[i]==1):
            Feromonas[i]=Feromonas[i]+TasaDeAumento
        if(Feromonas[i]>=TasaDeEvaporacion):
            Feromonas[i]=Feromonas[i]-TasaDeEvaporacion     


# In[8]:

#Transformacion del array inicial en un array numerico
def TransformaArray(Arr=[]):
    Arrf=Arr
    for i in range(len(Arr)):
        for z in range(len(Arr[i])):
            Arrf[i][z]=int(Arr[i][z])
    return Arrf


# In[13]:

#print(TransformaArray([['4', '7', '8'], ['3', '5', '6'], ['2', '3', '4'], ['1', '2', '3']]))


# In[10]:

#Fichero en formato 'nombre,peso,valor/n nombre,peso,valor/n ...... nombre,peso,valor/n '
def LeeFichero(FicheroHormigas):#Fichero en formato '......'
    infile = open(FicheroHormigas, 'r')
    ArSal=[]
    for line in infile:
        lines=line.rstrip('\n')
        i=0
        ArSal.insert(i,lines.split(','))
        i=i+1
    # Cerramos el fichero.
    infile.close()
    return TransformaArray(ArSal)


# In[12]:

#LeeFichero('Test2.txt')


# In[ ]:

#Calculo de las probabilidades a partir de la lista de objetos, las feromonas y el ajuste
def CalculaProbabilidades(Objetos=[[],],Feromonas=[],Ajuste=[]):
    Acum=0
    F=[]
    P=[]
    for i in range(len(Feromonas)):
        F.append((Feromonas[i]**Ajuste[0])*((1/Objetos[i][1])**Ajuste[1])*((1-(1/Objetos[i][2]))**Ajuste[2]))
        Acum+=F[i]
    for f in F:
        P.append(f/Acum)
   
    return P


# In[ ]:

def InstanciaArray(Objetos=[[],]):#devuelve una lista llena de 0 del tamaño de la lista Objetos
    res=[]
    for i in Objetos:
        res.append(0)
    return res


# In[ ]:

#Tests con ficheros y valores diferentes, creo que introducir un valor inicial xa las feromonas
#en el marco generico seria lo suyo
def Pruebas():
    for i in range(1,11):

        Ponderadores=[0.5,0.5,0.5]
        Capacidad=0
        #print(Ponderadores)
        archi=open('ResultadosPruebas/SolucionesSimple '+'Test '+str(i)+'.txt','w')
        archi2=open('ResultadosPruebasExcel/SolucionesExcelSimple '+'Test '+str(i)+'.txt','w')

        if i==1:
            Capacidad=123
        if i==2:
            Capacidad=28
        if i==3:
            Capacidad=22
        if i==4:
            Capacidad=36
        if i==5:
            Capacidad=48
        if i==6:
            Capacidad=290
        if i==7:
            Capacidad=91
        if i==8:
            Capacidad=168
        if i==9:
            Capacidad=306
        if i==10:
            Capacidad=360
        for Y in range(0,10):
            archi2.write(str(Ponderadores)+';')
            for z in range(0,10):
                MejorSolucion=LanzadorPruebas('Objetos/Test'+str(i)+'.txt',Capacidad,Ponderadores,2,0.5,1000)
                #print("Test"+str(i)+",Intento:"+str(z)+str(MejorSolucion))#100000
                archi.write("Test"+str(i)+",Ponderadores: "+str(Ponderadores)+",Intento:"+str(z)+str(MejorSolucion)+',')
                archi2.write(str(MejorSolucion[0])+';')
                #print('-----------------------------------------------------------------------------------------')
            if Y==0:
                Ponderadores[0]=Ponderadores[0]*2
            if Y==1:
                Ponderadores[1]=Ponderadores[1]*2
            if Y==2:
                Ponderadores[0]=Ponderadores[0]/2
            if Y==3:
                Ponderadores[2]=Ponderadores[2]*2
            if Y==4:
                Ponderadores[1]=Ponderadores[1]/2
            if Y==5:
                Ponderadores[2]=Ponderadores[2]*2
            if Y==6:
                Ponderadores[1]=Ponderadores[1]*4
            if Y==7:
                Ponderadores[2]=Ponderadores[2]/4
            if Y==8:
                Ponderadores[0]=Ponderadores[0]*4



            archi.write('-----------------------------------------------------------------------------------------'+'\n')
            archi2.write('\n')

        archi.write('-----------------------------------------------------------------------------------------'+'\n')
        archi2.write('-----------------------------------------------------------------------------------------'+'\n')
        print('----------------------------------------------'+str(i)+'-------------------------------------------')
        archi.close()
        archi2.close()


# In[ ]:




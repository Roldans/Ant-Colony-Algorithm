
# coding: utf-8

# In[1]:

import random
import copy


# In[2]:

#Actualizacion de la lista de feromonas tras un viaje de una hormiga
def ActualizaFeromonas(Feromonas=[],UltimaSolucion=[],TasaDeAumento=0,TasaDeEvaporacion=0):
    for i in range(len(Feromonas)):
        if(UltimaSolucion[i]==1):
            Feromonas[i]=Feromonas[i]+TasaDeAumento
        if(Feromonas[i]>=TasaDeEvaporacion):
            Feromonas[i]=Feromonas[i]-TasaDeEvaporacion   


# In[3]:

#Transformacion del array inicial en un array numerico
def TransformaArray(Arr=[]):
    Arrf=Arr
    for i in range(len(Arr)):
        for z in range(len(Arr[i])):
            Arrf[i][z]=int(Arr[i][z])
    return Arrf


# In[4]:

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


# In[5]:

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


# In[6]:


#Creacion de una solucion para una hormiga a partir de un numero rando y de el conjunto de valoresç
#obtenidos a partir de las feromonas
def HormigaIterativa(Objetos=[],Probabilidades=[],CapacidadMAX=0):
    Solucion=[0,InstanciaArray(Objetos),0]
    NuevaSolucion=[0,InstanciaArray(Objetos),0]
    Capacidad=0
    for i in range(len(Probabilidades)): 
        alea=random.random()
        #print(alea)
        if(alea<Probabilidades[i]):
            if(CapacidadMAX>Capacidad+Objetos[i][1]):
                Solucion[1][i]=1
                Capacidad = Capacidad+Objetos[i][1]
        else:
            Solucion[1][i]=0
    NuevaSolucion=Iterativa(Solucion[1],CapacidadMAX,Capacidad,Objetos)
   
    while(NuevaSolucion[1]!=Solucion[1]):
       
        Solucion[1]=copy.copy(NuevaSolucion[1])
        NuevaSolucion=Iterativa(Solucion[1],CapacidadMAX,NuevaSolucion[2],Objetos)
            
    return NuevaSolucion[1]


# In[7]:


def Iterativa(Solucion=[],CapacidadMAX=0,Capacidad=0,Objetos=[]):
    NuevaSolucion=[0,[0,],0]#Objetos,peso
    NuevaSolucion[1]=copy.copy(Solucion)
    i=len(NuevaSolucion[1])-1
   
    #for i in range(len(NuevaSolucion[1])):  
    while(i>=0):
        if Solucion[i]==0:
            if CapacidadMAX>Capacidad+Objetos[i][1]:
                
                NuevaSolucion[1][i]=1  
                Capacidad+=Objetos[i][1]
                NuevaSolucion[2]=Capacidad
                break
        i=i-1
    NuevaSolucion[2]=Capacidad
    return NuevaSolucion


# In[8]:

def HormigueroIterativo(Objetos=[[],],Feromonas=[],CapacidadMax=0,Ajuste=[0,0,0],TasaDeAumento=0,TasaDeEvaporacion=0,NumeroHormigas=0):

    MejorSolucion=[0,InstanciaArray(Objetos),0]#{ValorTotal,{Lista de objetos cogidos}}
    #SolucionActual=[0,[0,0,0,0,0,0,0,0,0,0],0]#Solucion para la hormiga
    Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)#Calcula las probabilidades según la formula mágica
   
    for i in range(NumeroHormigas):#Bucle Hormiguero,se repite una vez por cada hormiga
        SolucionActual=[0,InstanciaArray(Objetos),0]#Solucion para la hormiga
        SolucionActual[1]=HormigaIterativa(Objetos,Probabilidades,CapacidadMax)#el recorrido de cada hormiga individual
       
       
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


# In[9]:

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


# In[10]:

#Lanzador de hormigas y actualizador del valir de feromonas a uno mas alto
def LanzadorIterativoPruebas(FicheroTexto,CapacidadMax,Ajuste,TasaDeAumento,TasaDeEvaporacion,NumHormigas):
    Objetos= LeeFichero(FicheroTexto)
    Objetos=OrdenaObjetos(Objetos)
    NumObjetos= len(Objetos)
    Feromonas=[]
    for i in range(NumObjetos):
        Feromonas.append(100000)
    Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)
    return HormigueroIterativo(Objetos,Feromonas,CapacidadMax,Ajuste,TasaDeAumento,TasaDeEvaporacion,NumHormigas)


# In[11]:

#Lanzador de hormigas y actualizador del valir de feromonas a uno mas alto
def LanzadorIterativo(FicheroTexto,CapacidadMax,TasaDeAumento,TasaDeEvaporacion,NumHormigas):
    Ajuste=[0.5,0.5,2]
    Objetos= LeeFichero(FicheroTexto)
    Objetos=OrdenaObjetos(Objetos)
    NumObjetos= len(Objetos)
    Feromonas=[]
    for i in range(NumObjetos):
        Feromonas.append(100000)
    Probabilidades=CalculaProbabilidades(Objetos,Feromonas,Ajuste)
    solucion=HormigueroIterativo(Objetos,Feromonas,CapacidadMax,Ajuste,TasaDeAumento,TasaDeEvaporacion,NumHormigas)
    solucionDescodificada=[[],]
  
    for o in range(NumObjetos):        
        if(solucion[1][o]==1):
            solucionDescodificada[0].append(Objetos[o])
    solucionDescodificada.append(solucion[2])
    solucionDescodificada.append(solucion[0])   
    return solucionDescodificada


# In[12]:

def InstanciaArray(Objetos=[[],]):#devuelve una lista llena de 0 del tamaño de la lista Objetos
    res=[]
    for i in Objetos:
        res.append(0)
    return res


# In[15]:

#Tests con ficheros y valores diferentes, creo que introducir un valor inicial xa las feromonas
#en el marco generico seria lo suyo
def Pruebas():
    for i in range(1,11):
        a=0
        capacidadMax=0
        Ponderadores=[0.5,0.5,0.5]
        archi=open('ResultadosPruebas/SolucionesIterativas '+'Test '+str(i)+'.txt','w')
        archi2=open('ResultadosPruebasExcel/SolucionesExcellIterativas '+'Test '+str(i)+'.txt','w')
        if i==1:
            capacidadMax=123
        if i==2:
            capacidadMax=28
        if i==3:
            capacidadMax=22
        if i==4:
            capacidadMax=36
        if i==5:
            capacidadMax=48
        if i==6:
            capacidadMax=290
        if i==7:
            capacidadMax=91
        if i==8:
            capacidadMax=168
        if i==9:
            capacidadMax=306
        if i==10:
            capacidadMax=360
        for Y in range(0,10):
            archi2.write(str(Ponderadores)+';')
            for z in range(0,10):          
                MejorSolucion=LanzadorIterativoPruebas('Objetos/Test'+str(i)+'.txt',capacidadMax,Ponderadores,2,0.5,1000)
                #print("Test"+str(i)+",Intento:"+str(z)+str(MejorSolucion))#100000
                archi.write("Test"+str(i)+",Ponderadores: "+str(Ponderadores)+",Intento:"+str(z)+str(MejorSolucion)+'\n')
                archi2.write(str(MejorSolucion[0])+';')
                #print('-----------------------------------------------------------------------------------------')
            if a==0:
                Ponderadores[0]=Ponderadores[0]*2
            if a==1:
                Ponderadores[1]=Ponderadores[1]*2
            if a==2:
                Ponderadores[0]=Ponderadores[0]/2
            if a==3:
                Ponderadores[2]=Ponderadores[2]*2
            if a==4:
                Ponderadores[1]=Ponderadores[1]/2
            if a==5:
                Ponderadores[2]=Ponderadores[2]*2
            if a==6:
                Ponderadores[1]=Ponderadores[1]*4
            if a==7:
                Ponderadores[2]=Ponderadores[2]/4
            if a==8:
                Ponderadores[0]=Ponderadores[0]*4


            a=a+1
            archi.write('-----------------------------------------------------------------------------------------'+'\n')
            archi2.write('\n')
        archi.write('-----------------------------------------------------------------------------------------'+'\n')
        archi2.write('-----------------------------------------------------------------------------------------'+'\n')

        print('------------------------------------------'+str(i)+'-----------------------------------------------')
        archi.close()
        archi2.close()


# In[ ]:




# In[ ]:




from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTiposAlimentos=4
numCaracteristicas = 5

# Conjuntos
A=RangeSet(1,numTiposAlimentos)

C=RangeSet(1, numCaracteristicas)
 
# Parámetros

    # carne:{"calorias": ..., "proteinas":..., "azucar": ..., "grasa":..., "carbohidratos":...}
    # 1    :{   1      : ...,       2    :...,      3  : ...,    4   :...,      5         :...}

alimentos = {
    1: {1: 287, 2: 26, 3: 0, 4:19.3, 5:0 }, #carne
    2: {1: 204, 2: 4.2, 3: 0.01, 4:0.5, 5:44.1 }, #arroz
    3: {1: 146, 2: 8, 3: 13, 4:8, 5:11 }, #leche
    4: {1: 245, 2: 6, 3: 25, 4:0.8, 5:55 }, #pan
}

precios = [3000,1000,600,700] # recorre con i

limites = [1500, 63, 25, 50, 200] # recorre con j



# Variable de decisión
Model.x = Var(A, domain=NonNegativeReals)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*precios[i-1] for i in A), sense=minimize)

# Restricciones

Model.res1=ConstraintList()
for j in C:
    if j==1 or j ==2:
        Model.res1.add(sum(Model.x[i]*alimentos[i][j] for i in A) >= limites[j-1])
    elif j==3 or j ==4 or j==5:
        Model.res1.add(sum(Model.x[i]*alimentos[i][j] for i in A) <= limites[j-1])



# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()
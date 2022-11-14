import pandas as pd
import re
from pyparsing import javaStyleComment

def extract():
    detalles = pd.read_csv("order_details.csv", sep =',')
    pizzas = pd.read_csv("pizzas.csv", sep =',')
    ingredientes = pd.read_csv("pizza_types.csv", sep =',', encoding = 'unicode-escape')
    orders = pd.read_csv("orders.csv", sep =',')
    return detalles, pizzas, ingredientes, orders

def transfrom(detalles, pizzas, ingredientes, orders):
    semana = []
    contador = 0
    h = len(orders.axes[0])-1
    fecha = ""
    while contador <= 6:
        if str(orders.loc[h]['date']) != fecha:
            fecha = str(orders.loc[h]['date'])
            semana.append(fecha)
            contador += 1
        h -= 1
    pedidos_semana = []
    for i in range(len(orders.axes[0])):
        if orders.loc[i]['date'] in semana:
            pedidos_semana.append(orders.loc[i]['order_id'])
    pizzas_pedidas = {}
    for order in range(len(detalles.axes[0])):
        if detalles.loc[order]['order_id'] in pedidos_semana:
            pizza_id = detalles.loc[order]['pizza_id']
            m = detalles.loc[order]['quantity']
            for fila in range(len(pizzas.axes[0])):
                if pizzas.loc[fila]['pizza_id'] == pizza_id:
                    for i in range(0,m):
                        pizzas_pedidas[pizzas.loc[fila]['pizza_type_id']] = pizzas.loc[fila]['size']
    porciones_ingredientes = {}
    for pizza in pizzas_pedidas:
        for k in range(len(ingredientes.pizza_type_id)):
            if ingredientes.loc[k]['pizza_type_id'] == pizza:
                ing = ingredientes.loc[k]['ingredients'].split(',')
                for j in range(len(ing)):
                    if ing[j][0] == " ":
                        ing[j] = re.sub(" ","",ing[j], 1)
                    if ing[j] in porciones_ingredientes:
                        if pizzas_pedidas[pizza] == 'S':
                            porciones_ingredientes[ing[j]] += 1
                        elif pizzas_pedidas[pizza] == 'M':
                            porciones_ingredientes[ing[j]] += 2
                        elif pizzas_pedidas[pizza] == 'L':
                            porciones_ingredientes[ing[j]] += 3
                        elif pizzas_pedidas[pizza] == 'XL':
                            porciones_ingredientes[ing[j]] += 4
                        elif pizzas_pedidas[pizza] == 'XLL':
                            porciones_ingredientes[ing[j]] += 5
                    else:
                        if pizzas_pedidas[pizza] == 'S':
                            porciones_ingredientes[ing[j]] = 1
                        elif pizzas_pedidas[pizza] == 'M':
                            porciones_ingredientes[ing[j]] = 2
                        elif pizzas_pedidas[pizza] == 'L':
                            porciones_ingredientes[ing[j]] = 3
                        elif pizzas_pedidas[pizza] == 'XL':
                            porciones_ingredientes[ing[j]] = 4
                        elif pizzas_pedidas[pizza] == 'XLL':
                            porciones_ingredientes[ing[j]] = 5
    return porciones_ingredientes

def load(porciones_ingredientes):
    comprar = pd.DataFrame(columns =  ['Ingredientes', 'Porciones'])
    i = 0
    for ingrediente in porciones_ingredientes:
        comprar.loc[i] = (str(ingrediente), porciones_ingredientes[ingrediente])
        i += 1
    comprar.to_csv('compra_semanal.csv', index=False)


if "__main__" == __name__:
    detalles, pizzas, ingredientes, orders = extract()
    porciones_ingredientes = transfrom(detalles, pizzas, ingredientes, orders)
    load(porciones_ingredientes)
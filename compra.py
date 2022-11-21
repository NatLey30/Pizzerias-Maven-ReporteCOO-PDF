import pandas as pd
import re


def extract():
    '''
    Extraemos todos los dataframes
    '''
    detalles = pd.read_csv("order_details_ordenado.csv", sep=',')
    pizzas = pd.read_csv("pizzas.csv", sep=',')
    ingredientes = pd.read_csv("pizza_types.csv", sep=',', encoding='unicode-escape')
    orders = pd.read_csv("orders_ordenado.csv", sep=',')
    return detalles, pizzas, ingredientes, orders


def transfrom(detalles, pizzas, ingredientes, orders):
    '''
    En esta función vamos a transformar los datos de los datasets
    sacando los pedidos de la última semana y mirando cuantas porciones
    de cada ingrdiente se han usado en esa semana.
    '''
    # Sacamos los pedidos de la semana
    semana = []
    pedidos_semana = []
    contador = 0
    h = len(orders.axes[0])-1
    fecha = ""
    while contador <= 7:
        dia = str(orders.loc[h, 'dates_std']).split(' ')[0]
        if dia != fecha:
            fecha = dia        
            semana.append(fecha)
            contador += 1
        pedidos_semana.append(orders.loc[h, 'order_id'])
        h -= 1
    pedidos_semana.pop(len(pedidos_semana)-1)
    semana.pop(len(semana)-1)
    # Cogemos las pizzas pedidad esa semana
    pizzas_pedidas = {}
    for order in range(len(detalles.axes[0])):
        if detalles.loc[order, 'order_id'] in pedidos_semana:
            pizza_id = detalles.loc[order, 'pizza_id']
            m = detalles.loc[order, 'quantity']
            for fila in range(len(pizzas.axes[0])):
                if pizzas.loc[fila, 'pizza_id'] == pizza_id:
                    for i in range(0, m):
                        pizzas_pedidas[pizzas.loc[fila, 'pizza_type_id']] = pizzas.loc[fila, 'size']
    # Cogemos las porciones dependiendo del tamaño de la pizza
    porciones_ingredientes = {}
    for pizza in pizzas_pedidas:
        for k in range(len(ingredientes.pizza_type_id)):
            if ingredientes.loc[k, 'pizza_type_id'] == pizza:
                ing = ingredientes.loc[k, 'ingredients'].split(',')
                for j in range(len(ing)):
                    if ing[j][0] == " ":
                        ing[j] = re.sub(" ", "", ing[j], 1)
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
    '''
    Función para cargar los datos obtenidos en un csv
    '''
    # Creamos un dataframe donde guardar todo
    comprar = pd.DataFrame(columns=['Ingredientes', 'Porciones'])

    # Añadimos al dataframe los ingredientes con sus porciones
    i = 0
    for ingrediente in porciones_ingredientes:
        comprar.loc[i] = (str(ingrediente), porciones_ingredientes[ingrediente])
        i += 1
    comprar.to_csv('compra_semanal.csv', index=False)


if "__main__" == __name__:
    detalles, pizzas, ingredientes, orders = extract()
    porciones_ingredientes = transfrom(detalles, pizzas, ingredientes, orders)
    load(porciones_ingredientes)

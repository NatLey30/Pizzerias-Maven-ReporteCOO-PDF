import pandas as pd
import re
import dateutil.parser as dp
from datetime import datetime
from word2number import w2n


if __name__ == "__main__":

    # Abrimos ficheros
    orders = pd.read_csv("orders.csv", sep=';')
    detalles = pd.read_csv("order_details.csv", sep=';')

    # # Eliminamos los nans que haya en las columnas que necesitemos
    # orders = orders.dropna(subset=['order_id'])
    # detalles = detalles.dropna(subset=['order_id', 'order_details_id'])

    # Ordenamos los datasets
    orders = orders.sort_values(by='order_id')
    detalles = detalles.sort_values(by='order_details_id')

    # En order_details ponemos las quantities como integers
    for i in range(len(detalles.axes[0])):
        if str(detalles.loc[i, 'quantity']) != 'nan':
            try:
                int(detalles.loc[i, 'quantity'])
            except ValueError:
                cantidad = w2n.word_to_num(str(detalles.loc[i, 'quantity']))
                detalles.loc[i, 'quantity'] = cantidad

    # Rellenamos los huecos vacios copiando lo que hay en la fila anterior
    orders = orders.fillna(method='ffill')
    detalles = detalles.fillna(method='ffill')

    # En orders añadimos una nueva columna con las fechas en el mismo formato
    orders['dates_std'] = ''
    dates_std = []
    for index, row in orders.iterrows():
        txt = row['date']
        try:
            #La libreria daeutil.parser pasa las fechas al mismo formato
            date_std = dp.parse(txt)
            dates_std.append(date_std)
        except:
            # Pero si la fecha está en formato unix, lo hacemos con otro metodo
            try:
                # La librería datetime nos lo hace
                date_std = datetime.fromtimestamp(float(txt))
                dates_std.append(date_std)
            except:
                # Para evaluar que se ha hecho el parseo completo, a modo de
                # ejemplo se deja una fecha para que no falle
                dates_std.append('Err')

    # Order_details
    for fila in range(len(detalles.axes[0])):
        if re.findall(str('-'), detalles.loc[fila, 'pizza_id'], re.IGNORECASE) != []:
            detalles.loc[fila, 'pizza_id'] = re.sub("-", "_", detalles.loc[fila, 'pizza_id'])
        elif re.findall(str(' '), detalles.loc[fila, 'pizza_id'], re.IGNORECASE) != []:
            detalles.loc[fila, 'pizza_id'] = re.sub(" ", "_", detalles.loc[fila, 'pizza_id'])
        if re.findall(str('@'), detalles.loc[fila, 'pizza_id'], re.IGNORECASE) != []:
            detalles.loc[fila, 'pizza_id'] = re.sub("@", "a", detalles.loc[fila, 'pizza_id'])
        if re.findall(str('3'), detalles.loc[fila, 'pizza_id'], re.IGNORECASE) != []:
            detalles.loc[fila, 'pizza_id'] = re.sub("3", "e", detalles.loc[fila, 'pizza_id'])
        if re.findall(str('0'), detalles.loc[fila, 'pizza_id'], re.IGNORECASE) != []:
            detalles.loc[fila, 'pizza_id'] = re.sub("0", "o", detalles.loc[fila, 'pizza_id'])

    orders['dates_std'] = dates_std
    orders['dates_std'] = pd.to_datetime(orders['dates_std'], format='%Y-%m-%d')

    orders.to_csv('orders_ordenado.csv', index=False)
    detalles.to_csv('order_details_ordenado.csv', index=False)

import pandas as pd
import xml.etree.ElementTree as ET
from lxml import etree

def archivo(fichero):
    df = pd.read_csv(fichero, sep = ',', encoding = 'LATIN1')
    fichero = ET.SubElement(root, 'fichero', {'nombre': fichero})

    nans = str(df.isna().sum().sum())
    NaN = ET.SubElement(fichero, 'NaN_en_todo_el_fichero', {'nº': nans})

    nulls = str(df.isnull().sum().sum())
    Null = ET.SubElement(fichero, 'Null_en_todo_el_fichero', {'nº': nulls})

    columnas = df.columns.values
    for colum in range(len(columnas)):

        nombre = columnas[colum]
        columna = ET.SubElement(fichero, 'columna', {'nombre': nombre})

        tipo_col = str(df[columnas[colum]].dtype)
        tipo_columna = ET.SubElement(columna, 'tipo_dato', {'tipo': tipo_col})

if __name__ == "__main__":

    root = ET.Element('Análisis')

    fichero = archivo('order_details.csv')
    fichero = archivo('orders.csv')
    fichero = archivo('data_dictionary.csv')
    fichero = archivo('pizzas.csv')
    fichero = archivo('pizza_types.csv')

    # escribimos en el xml

    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write('Analisis_datos.xml', xml_declaration=True, encoding='utf-8')


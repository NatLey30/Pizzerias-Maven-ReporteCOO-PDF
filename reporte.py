import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from xhtml2pdf import pisa


# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err


if "__main__" == __name__:

    # Abrimos y leemos los csv necesarios para crear el reporte
    archivo = open('compra_semanal.csv')
    contenido = archivo.readlines()
    archivo.close()

    # Creamos un string con el mensaje que añadiremos al HTML
    mensaje = """<html>
    <head><h1>Reporte COO de Pizzerias Maven</h1></head>
    <p>A continuación se mostrará una aproximación de las compras semanales de
    Pizzerías Maven.</p>
    <table>
        <tr>
            <td>Ingredientes</td>
            <td>Porciones</td>
        </tr>"""

    # Añadimos gráfica de ingredientes y porciones
    for i in range(1, len(contenido)-1):
        ing = contenido[i].split(',')
        mensaje += f"""<tr>
            <td>{ing[0]}</td>
            <td>{ing[1]}</td>
        </tr>
        """

    mensaje += """</table>"""

    df1 = pd.read_csv('compra_semanal.csv')
    df2 = pd.read_csv('order_details_ordenado.csv')
    df3 = pd.read_csv('pizzas.csv')

    # Creamos gráficos
    ## Ingredientes menos usados
    pequeños = df1.nsmallest(5, 'Porciones')
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x='Ingredientes', y='Porciones', data=pequeños, palette='rocket_r')
    plt.savefig('Ingredientes_menos_usados.jpg')

    ## Ingredientas más usados
    mayores = df1.nlargest(5, 'Porciones')
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x='Ingredientes', y='Porciones', data=mayores, palette='rocket_r')
    plt.savefig('Ingredientes_mas_usados.jpg')

    ## Pizzas más pedidas
    plt.figure(figsize=(10, 5))
    ax = sns.countplot(data=df2, x='pizza_id', order=pd.value_counts(df2['pizza_id']).iloc[:5].index)
    ax.set(xlabel='pizza_id', ylabel='Cantidad')
    plt.savefig('Pizzas_mas_pedidas.jpg')

    ## Pizzas más caras
    data = df3.sort_values('price', ascending=False).head(6)
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x='pizza_id', y='price', data=data, palette='rocket_r')
    ax.set(xlabel='pizza_id', ylabel='price')
    plt.savefig('Pizzas_mas_caras.jpg')

    ## Pizzas más baratas
    data = df3.sort_values('price', ascending=False).tail(6)
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x='pizza_id', y='price', data=data, palette='rocket_r')
    ax.set(xlabel='pizza_id', ylabel='price')
    plt.savefig('Pizzas_mas_baratas.jpg')

    # Añadimos los gráficos al HTML
    mensaje += """
    <p><h3>Ingredientes menos usados</h3></p>
    <p><img src="Ingredientes_menos_usados.jpg"
        width="600"
        height="340"></p>
    <p><h3>Ingredientes más usados</h3></p>
    <p><img src="Ingredientes_mas_usados.jpg"
        width="600"
        height="340"></p>
    <p><h3>Pizzas más pedidas</h3></p>
    <p><img src="Pizzas_mas_pedidas.jpg"
        width="600"
        height="340"></p>
    <p><h3>Pizzas más caras</h3></p>
    <p><img src="Pizzas_mas_caras.jpg"
        width="600"
        height="340"></p>
    <p><h3>Pizzas más baratas</h3></p>
    <p><img src="Pizzas_mas_baratas.jpg"
        width="600"
        height="340"></p>
    </html>"""

    # creamos un archivo HTML
    f = open('reporte.html', 'w')
    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab('reporte.html')

    convert_html_to_pdf(mensaje, 'reporteCOO.pdf')

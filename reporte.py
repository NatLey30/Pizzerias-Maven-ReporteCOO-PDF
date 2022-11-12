import csv
import html
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xhtml2pdf
from IPython.display import HTML, display
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

    # cramos un html
    f = open('reporte.html','w')

    archivo = open('compra_semanal.csv')
    contenido = archivo.readlines()
    archivo.close()

    mensaje = """<html>
    <head><h1>Reporte COO de Pizzerias Maven</h1></head>
    <p>A continuación se mostrará una aproximación de las compras semanales de Pizzerías Maven.</p>
    <table>
        <tr>
            <td>Ingredientes</td>
            <td>Porciones</td>
        </tr>"""

    for i in range(1,len(contenido)-1):
        ing = contenido[i].split(',')
        mensaje += f"""<tr>
            <td>{ing[1]}</td>
            <td>{ing[2]}</td>
        </tr>
        """

    mensaje += """</table>"""

    df1 = pd.read_csv('compra_semanal.csv')

    pequeños = df1.nsmallest(20, 'Porciones')
    pequeños = pequeños.drop('Unnamed: 0', axis=1)
    mayores = df1.nlargest(5, 'Porciones')
    mayores = mayores.drop('Unnamed: 0', axis=1)

    plt.figure(figsize=(10, 5))
    plt.title("Ingredientes menos usados")
    ax = sns.barplot(x='Ingredientes', y='Porciones', data=pequeños, palette='rocket_r')
    plt.xticks(rotation=70)
    plt.savefig('Ingredientes_menos_usados.jpg')

    plt.figure(figsize=(10, 5))
    plt.title("Ingredientes más usados")
    ax = sns.barplot(x='Ingredientes', y='Porciones', data=mayores, palette='rocket_r')
    plt.xticks(rotation=70)
    plt.savefig('Ingredientes_mas_usados.jpg')

    mensaje += """
    <p><img src="Ingredientes_menos_usados.jpg"
        width="600"
        height="340"></p>
    <p><img src="Ingredientes_mas_usados.jpg"
        width="600"
        height="340"></p>
    </html>"""

    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab('reporte.html')

    convert_html_to_pdf(mensaje, 'reporteCOO.pdf')
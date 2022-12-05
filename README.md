# Pizzerias-Maven-ReporteCOO-PDF
Repositorio en el que se limpian los datos de los dataframes orders.csv y order_details.csv, para realizar un predicción de los ingredientes a comprar para la siguiente semana, para lo cual cogemos la última semana del dataset y miramos cuantos ingredientes hacen falta.

Por otro lado, también se realiza un reporte COO en pdf sobre los datos sacados.

Los ficheros de entrada son:
- orders.csv
- order_details.csv
- pizza_types.csv
- pizzas.csv
- data_dictionary.csv

Los ficheros de salida son:
- order_details_ordenado.csv
- orders_ordenado.csv
- compra_semanal.csv
- analisis_archivos.txt
- reporte.html
- reporteCOO.pdf

Los archivos de transformación son:
- limpiar_datos.py
- compra.py
- reporte.py.py

Librerías
- pandas
- re
- dateutil.parser
- datetime
- word2number
- webbrowser
- matplotlib.pyplot
- seaborn
- xhtml2pdf

# DS_A1_MatrixMultiplication
 Programa en Python para la multiplicación paralela y distribuida de dos matrices
## Configuración del entorno de ejecución
 Este programa construído en Python necesita de la versión 3.7 del mismo. Además, previamente a la ejecución del código, hay que tener el paquete pywren-ibm-cloud instalado (link *[aquí][1]*)
 Además, hace falta incluir la configuración necesaria de COS y CF, en el fichero ~/.pywren_config (situado en el directorio HOME del usuario)
## Explicación de ejecución del algoritmo
 El programa invocando en línea de comandos se encarga de generar dos matrices de valores enteros aleatorios entre -5 y 5 y de devolver su producto:
 
 > ./main.py m n l w
 
 ,donde:
 
    1. m = numero de filas de la 1a matriz
    2. n = numero de columnas de la 1a matriz = numero de filas de la 2a matriz
    3. l = numero de columnas de la 2a matriz
    4, w = numero de subdivisiones de cada matriz(1a row-wise, 2a column-wise). El número de workers vendrá determinado por w^2. 

 [1]: https://github.com/pywren/pywren-ibm-cloud
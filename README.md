# HybridOperatorsExam
Este repositorio forma parte de un Trabajo de Fin de Grado (TFG) en la Universidad Politécnica de Madrid (UPM). Contiene herramientas para la generación, hibridación, derivación y análisis estadístico de claves criptográficas, incluyendo medidas de entropía y correlación.

## 📁 Estructura del Proyecto

### Key Generators
Estos cuatro primeros scripts tienen un fucnionamieto análogo, incializan un intercambio entre dos extremos a y b y establecen el secreto compartido.
- **`ClassicKeyGenerator448.py`**: Generador de claves clásicas ECDH de la curva X448.
- **`ClassicKeyGenerator25519*.py`**: Generador de claves clásicas ECDH de la curva X25519.
- **`ClassicKeyGeneratorNistp256.py`**: Generador de claves clásicas ECDH de la curva Nist p-256.
- **`PQCKeyGenerator.py`**: Generador de claves poscuánticas siguiendo el esquema Kyber-768.

Este script, segun el valor de VALOR escogido en el import "from ClassicKeyGenerator[VALOR] import generate_ecdh_key" genera un fichero por tipo de clave escogida con tantas claves como se quiera.
- **`KeysGenerator.py`**: Genera un conjunto masivo de claves (500000 por lote).

De los dos ficheros fuente, crea en KEYS_COMBINED un fichero por tipo con los resultados de hibridar las misma claves segun los cuatro métodos escogidos.
- **`Hybridation.py`**: Hibrida diferentes tipos de claves.

Aplica HKDF a los fichero de KEYS_COMBINED y deja el resutlado en KEYS_DERIVED
- **`Derivation.py`**: Deriva nuevas claves a partir de otras.

Aplica varios examenes de entropía a los ficheros con las claves.
- **`EntropyCalculator.py`**: Calcula la entropía de los ficheros de claves.

Aplica un examen de correlación entre los bytes de las claves
- **`Correlation.py`**: Analiza la correlación entre claves generadas.

Crea un plot con una curva de entropía maxíma teorica según longitud de clave
- **`MaxEntropyCurve.py`**: Analiza curvas de entropía máxima.

Ejecuta el test chi² y la distancia Jense-Shannon, devuelve el resultado por la salida estandar.
- **`Test.py`**: Script de prueba general.

Script para lanzar el pipeline de operaciones
- **`run.sh`**: Ejecuta automáticamente el pipeline principal.

## 📂 Carpetas

- `KEYS/`: Claves generadas individualmente.
- `KEYS_COMBINED/`: Claves combinadas tras hibridación.
- `KEYS_DERIVED/`: Claves derivadas a partir de otras.
- `CORRELATION/`: Resultados de análisis de correlación, excels con matrices y plots de Correlation.py..
- `RESULTS/`: Resultados numéricos y métricas de EntopyCalculator.py.
- `PLOT/`: Gráficas generadas por EntropyCalculator.py.
- `SAVES/`: Copias o resultados intermedios de examenes con diferentes curvas.

## ▶️ Uso

- Primero, asegúrate de tener Python 3.8+ y las dependencias necesarias instaladas.
- Segundo, modifica en KeysGenerator el import y escoge el fichero que quieras importar segun la curva elíptica objeto de análisis.
- Tercero, crea los directorios KEYS*
### 1. Ejecutar el flujo completo

```bash
./run.sh


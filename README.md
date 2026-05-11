# Travesia Genica

RPG de consola sobre expresion genica. El jugador toma el rol de la ARN Polimerasa II y debe transcribir y traducir secuencias de ADN para sintetizar proteinas.

## Requisitos

- Python 3.6 o superior instalado
- pip instalado

### Como instalar Python y pip

**Mac:**
1. Descarga el instalador desde https://www.python.org/downloads/
2. Ejecuta el instalador. pip se instala automaticamente junto con Python.
3. Verificá que funcione abriendo la terminal y escribiendo:
```bash
python3 --version
```

**Windows:**
1. Descarga el instalador desde https://www.python.org/downloads/
2. Durante la instalacion, tilda la opcion **"Add Python to PATH"**.
3. pip se instala automaticamente. Verificá con:
```bash
python --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3 python3-pip
```

## Como ejecutar

Una vez que tenés Python instalado, corré:

```bash
bash setup.sh
```

Esto crea el entorno virtual, instala las dependencias y lanza el juego automaticamente.

Para volver a jugar despues del setup inicial:

```bash
source .venv/bin/activate
python3 game.py
```

Para modo **dificil** (1 vida):

```bash
python3 game.py --dificultad dificil
```

## Como se juega

El juego tiene 4 partes:

- **Parte I** — introduccion narrativa al contexto biologico.
- **Parte II** — dada una hebra molde de ADN, obtenés la hebra codificante y luego la transcribis a ARNm.
- **Parte III** — el espliceosoma elimina los intrones y te muestra el ARNm maduro.
- **Parte IV** — identificas el codon de inicio, y para cada codon indicás el aminoacido y el anticodon del ARNt.

En cualquier momento podés escribir `tabla` para ver el codigo genetico completo.

Al terminar cada partida podés elegir jugar de nuevo con un gen distinto. Los genes ya completados aparecen marcados como **(Resuelto)**.

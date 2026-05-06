# Travesia Genica

RPG de consola sobre expresion genica. El jugador toma el rol de la ARN Polimerasa II y debe transcribir y traducir secuencias de ADN para sintetizar proteinas.

## Dependencias

Requiere Python 3 y la libreria `rich`:

```bash
pip3 install rich
```

## Como ejecutar

```bash
python3 game.py
```

Por defecto el juego corre en modo **facil** (3 vidas). Para modo **dificil** (1 vida):

```bash
python3 game.py --dificultad dificil
```

## Como se juega

El juego tiene 4 partes:

- **Parte I** — introduccion narrativa al contexto biologico.
- **Parte II** — dada una secuencia de ADN, escribis el ARNm resultante (recordá: T → U).
- **Parte III** — el espliceosoma elimina los intrones automaticamente y te muestra el ARNm maduro.
- **Parte IV** — identificas el codon de inicio, y para cada codon indicás el aminoacido y el anticodon del ARNt.

En cualquier momento podés escribir `tabla` para ver el codigo genetico completo.

Al terminar cada partida podés elegir jugar de nuevo con un gen distinto. Los genes ya completados aparecen marcados como **(Resuelto)**.

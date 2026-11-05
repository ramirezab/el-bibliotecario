"""Crisol: generador local de pixel art guiado por Forja.

Forja da la estructura (el modelo 3D con su esqueleto, en cada ángulo y cuadro); un modelo de difusión local
(Stable Diffusion XL con el ajuste pixel-art-xl) la pinta en pixel art siguiendo sus bordes (ControlNet); y la
limpieza la lleva a una cuadrícula y una paleta fijas, iguales para todos los ángulos y cuadros.
"""

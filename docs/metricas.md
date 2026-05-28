# Métricas del Datamart

## Objetivo

Este documento resume las métricas que se usarán para analizar las condiciones de vivienda, servicios básicos, conectividad y bienestar habitacional de los hogares.

Las métricas serán utilizadas en dashboards, reportes y data storytelling.

## Consideración principal

Los indicadores finales deben calcularse usando el factor de expansión:

FACTOR07

Esto permite obtener resultados representativos a nivel poblacional.

## Fórmulas generales

Porcentaje ponderado:

SUM(flag * FACTOR07) / SUM(FACTOR07)

Promedio ponderado:

SUM(valor * FACTOR07) / SUM(FACTOR07)

Total ponderado:

SUM(valor * FACTOR07)

## Métricas base

### Hogares observados

Cantidad de hogares en la muestra.

COUNT(hogar_id)

### Hogares ponderados

Cantidad estimada de hogares usando factor de expansión.

SUM(FACTOR07)

### Cantidad de hogares

Medida auxiliar para conteos.

cantidad_hogar = 1

## Métricas de vivienda y habitabilidad

### Promedio de habitaciones

SUM(habitaciones_total * FACTOR07) / SUM(FACTOR07)

### Promedio de habitaciones para dormir

SUM(habitaciones_dormir * FACTOR07) / SUM(FACTOR07)

### Porcentaje de viviendas inadecuadas

SUM(flag_vivienda_inadecuada * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con hacinamiento

SUM(flag_hacinamiento * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con al menos una NBI

SUM(tiene_nbi * FACTOR07) / SUM(FACTOR07)

### Promedio de NBI por hogar

SUM(nbi_total * FACTOR07) / SUM(FACTOR07)

## Métricas de agua

### Porcentaje de hogares con agua por red pública

SUM(flag_agua_red_publica * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con agua potable

SUM(flag_agua_potable * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con agua todos los días

SUM(flag_agua_todos_los_dias * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con agua discontinua

SUM(flag_agua_discontinua * FACTOR07) / SUM(FACTOR07)

### Promedio de horas de agua al día

SUM(horas_agua_dia * FACTOR07) / SUM(FACTOR07)

### Promedio de días de agua por semana

SUM(dias_agua_semana * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con cloro seguro

SUM(flag_agua_cloro_seguro * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con agua no segura

SUM(flag_agua_no_segura * FACTOR07) / SUM(FACTOR07)

## Métricas de saneamiento

### Porcentaje de hogares con saneamiento adecuado

SUM(flag_saneamiento_adecuado * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con saneamiento precario

SUM(flag_saneamiento_precario * FACTOR07) / SUM(FACTOR07)

## Métricas de energía

### Porcentaje de hogares con electricidad

SUM(flag_tiene_electricidad * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares sin electricidad

SUM(flag_sin_electricidad * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con combustible adecuado

SUM(flag_combustible_adecuado * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con combustible precario

SUM(flag_combustible_precario * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares que cocinan con GLP

SUM(cocina_glp * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares que cocinan con gas natural

SUM(cocina_gas_natural * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares que cocinan con leña

SUM(cocina_lena * FACTOR07) / SUM(FACTOR07)

## Métricas de conectividad

### Porcentaje de hogares con celular

SUM(tiene_celular * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con internet

SUM(flag_tiene_internet * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares sin internet

SUM(flag_sin_internet * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con conectividad básica

SUM(flag_conectividad_basica * FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares sin TIC

SUM(flag_sin_tic * FACTOR07) / SUM(FACTOR07)

## Métricas de tenencia y propiedad

### Porcentaje de hogares con vivienda propia

SUM(hogares con P105A en 2, 3 o 4 ponderados con FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares en vivienda alquilada

SUM(hogares con P105A = 1 ponderados con FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con título de propiedad

SUM(hogares con P106A = 1 ponderados con FACTOR07) / SUM(FACTOR07)

### Porcentaje de hogares con título registrado en SUNARP

SUM(hogares con P106B = 1 ponderados con FACTOR07) / SUM(FACTOR07)

### Promedio de alquiler pagado

SUM(alquiler_pagado_mensual * FACTOR07) / SUM(FACTOR07)

### Promedio de alquiler estimado

SUM(alquiler_estimado_mensual * FACTOR07) / SUM(FACTOR07)

## Métricas de crédito de vivienda

### Porcentaje de hogares con crédito de vivienda

SUM(flag_tuvo_credito_vivienda * FACTOR07) / SUM(FACTOR07)

### Monto total de crédito de vivienda

SUM(monto_credito_total * FACTOR07)

### Promedio de crédito por hogar con crédito

SUM(monto_credito_total * FACTOR07) / SUM(flag_tuvo_credito_vivienda * FACTOR07)

## Métricas de gasto en servicios

### Gasto total en servicios

gasto_total_servicios = gasto_pagado_servicios + gasto_donado_servicios + gasto_autoconsumo_servicios

### Promedio de gasto mensual en servicios

SUM(gasto_total_servicios * FACTOR07) / SUM(FACTOR07)

### Promedio de gasto pagado por miembros del hogar

SUM(gasto_pagado_servicios * FACTOR07) / SUM(FACTOR07)

### Promedio de gasto donado o regalado

SUM(gasto_donado_servicios * FACTOR07) / SUM(FACTOR07)

### Promedio de gasto por autoconsumo o autosuministro

SUM(gasto_autoconsumo_servicios * FACTOR07) / SUM(FACTOR07)

## Índice de Brecha de Bienestar Habitacional

El índice resume cuántas carencias acumula cada hogar.

indice_brecha_bienestar =
flag_vivienda_inadecuada
+ flag_hacinamiento
+ flag_saneamiento_precario
+ flag_agua_no_segura
+ flag_agua_discontinua
+ flag_sin_electricidad
+ flag_combustible_precario
+ flag_sin_internet

## Clasificación del índice

| Puntaje | Categoría |
|---:|---|
| 0 - 1 | Brecha baja |
| 2 - 3 | Brecha media |
| 4 - 5 | Brecha alta |
| 6 o más | Brecha crítica |

## KPIs principales

Los principales indicadores del dashboard serán:

- Total de hogares ponderados.
- Porcentaje de hogares con NBI.
- Porcentaje de hogares con brecha alta o crítica.
- Porcentaje de hogares con agua todos los días.
- Porcentaje de hogares con agua no segura.
- Porcentaje de hogares con saneamiento precario.
- Porcentaje de hogares con electricidad.
- Porcentaje de hogares sin internet.
- Promedio de gasto mensual en servicios.
- Promedio del índice de brecha.

## Uso de las métricas

Las métricas se usarán para comparar hogares según:

- Dominio geográfico.
- Estrato geográfico.
- Tipo de vivienda.
- Material de paredes.
- Material de pisos.
- Material de techos.
- Régimen de tenencia.
- Acceso a agua.
- Tipo de saneamiento.
- Tipo de energía.
- Acceso a internet.
- Categoría de brecha.

El objetivo es identificar qué hogares presentan mayores brechas de bienestar habitacional y en qué territorios se concentran.
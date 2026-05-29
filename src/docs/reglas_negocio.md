# Reglas de negocio

## Problemática

En el Perú, se espera que los hogares cuenten con condiciones mínimas adecuadas de vivienda, habitabilidad, acceso continuo y seguro a servicios básicos, energía y conectividad. Sin embargo, la situación actual muestra que estas condiciones no se distribuyen de manera uniforme, existiendo hogares con carencias simultáneas en materiales de vivienda, hacinamiento, agua segura, saneamiento, energía doméstica y acceso digital.

Esta desviación configura una brecha multidimensional de bienestar habitacional.

## Alcance

El datamart se construirá usando el Módulo 100 de la ENAHO 2025, correspondiente a características de la vivienda y del hogar.

Se analizarán principalmente:

- Vivienda.
- Habitabilidad.
- Agua.
- Saneamiento.
- Energía.
- Conectividad.
- Tenencia de vivienda.
- Créditos de vivienda.
- Gastos en servicios.
- Necesidades Básicas Insatisfechas.

No se incluirán módulos de educación, salud, empleo, programas sociales ni ingresos individuales.

## Unidad de análisis

La unidad de análisis será el hogar.

Cada fila de la tabla de hechos representará un hogar entrevistado completo.

## Filtro principal

Solo se considerarán hogares con entrevista completa:

RESULT = 1

## Identificador del hogar

Se construirá un identificador único del hogar con:

hogar_id = AÑO + CONGLOME + VIVIENDA + HOGAR

## Factor de expansión

Para los indicadores finales se usará el factor de expansión anual:

FACTOR07

Los conteos simples servirán para validación, pero los resultados del dashboard deberán calcularse de forma ponderada.

## Tratamiento de valores monetarios

Para variables monetarias se seguirá este orden de preferencia:

I > D > P

Donde:

- I: valor imputado, deflactado y anualizado.
- D: valor deflactado.
- P: valor corriente de campo.

Cuando exista una variable imputada, se usará la variable I. Si no existe, se usará D. Si tampoco existe D, se usará P.

## Tratamiento de valores perdidos

Los valores definidos como missing en el diccionario serán tratados como nulos.

Ejemplos:

- 9
- 99
- 99999
- 999999
- 9999999

Estos valores no deben entrar en promedios, sumas ni indicadores.

## Reglas principales de indicadores

### Vivienda inadecuada

flag_vivienda_inadecuada = 1 si NBI1 = 1.

### Hacinamiento

flag_hacinamiento = 1 si NBI2 = 1.

### Hogar con NBI

nbi_total = NBI1 + NBI2 + NBI3 + NBI4 + NBI5

tiene_nbi = 1 si nbi_total > 0.

### Agua por red pública

flag_agua_red_publica = 1 si P110 está en 1 o 2.

### Agua potable

flag_agua_potable = 1 si P110A1 = 1.

### Agua segura

flag_agua_cloro_seguro = 1 si P110A = 1.

### Agua no segura

flag_agua_no_segura = 1 si P110A1 = 2 o P110A está en 2 o 3.

### Agua todos los días

flag_agua_todos_los_dias = 1 si P110C = 1.

### Agua discontinua

flag_agua_discontinua = 1 si P110C = 2.

### Horas de agua al día

horas_agua_dia = P110C1 si P110C = 1.

horas_agua_dia = P110C3 si P110C = 2.

### Días de agua por semana

dias_agua_semana = 7 si P110C = 1.

dias_agua_semana = P110C2 si P110C = 2.

### Saneamiento adecuado

flag_saneamiento_adecuado = 1 si P111A está en 1, 2, 3 o 4.

### Saneamiento precario

flag_saneamiento_precario = 1 si P111A está en 5, 6, 7 o 9.

### Electricidad

flag_tiene_electricidad = 1 si P1121 = 1.

flag_sin_electricidad = 1 si P1121 es diferente de 1.

### Combustible adecuado

flag_combustible_adecuado = 1 si P113A está en 1, 2 o 3.

### Combustible precario

flag_combustible_precario = 1 si P113A está en 5, 6, 7 o 9.

### Internet

flag_tiene_internet = 1 si P1144 = 1.

flag_sin_internet = 1 si P1144 es diferente de 1.

### Conectividad básica

flag_conectividad_basica = 1 si P1142 = 1 o P1144 = 1.

### Hogar sin TIC

flag_sin_tic = 1 si P1145 = 1.

### Crédito de vivienda

flag_tuvo_credito_vivienda = 1 si P107B1 = 1 o P107B2 = 1 o P107B3 = 1 o P107B4 = 1.

### Monto total de crédito

monto_credito_total = D107D1 + D107D2 + D107D3 + D107D4

Si no se usan valores deflactados, se puede trabajar con:

monto_credito_total = P107D1 + P107D2 + P107D3 + P107D4

### Gasto total en servicios

gasto_total_servicios = P117T2 + P117T3 + P117T4

Donde:

- P117T2: gasto pagado por miembros del hogar.
- P117T3: gasto donado o regalado por otro hogar.
- P117T4: gasto por autoconsumo o autosuministro.

## Índice de Brecha de Bienestar Habitacional

Se construirá un índice para medir la acumulación de carencias del hogar:

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

## Forma de agregación

Los porcentajes se calcularán como:

SUM(flag * FACTOR07) / SUM(FACTOR07)

Los promedios se calcularán como:

SUM(valor * FACTOR07) / SUM(FACTOR07)

Los totales ponderados se calcularán como:

SUM(valor * FACTOR07)
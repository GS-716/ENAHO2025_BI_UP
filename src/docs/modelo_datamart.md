# Modelo del Datamart

## Objetivo

El datamart busca organizar la información del Módulo 100 de la ENAHO 2025 para analizar las condiciones de vivienda, servicios básicos, conectividad y bienestar habitacional de los hogares peruanos.

El modelo permitirá construir dashboards e historias de datos sobre la brecha multidimensional de bienestar habitacional.

## Fuente de datos

Archivo principal:

Enaho01-2025-100.csv

Este archivo contiene información sobre:

- Características de la vivienda.
- Características del hogar.
- Acceso a agua.
- Saneamiento.
- Energía.
- Conectividad.
- Tenencia de vivienda.
- Créditos de vivienda.
- Gastos mensuales en servicios.
- Necesidades Básicas Insatisfechas.

## Tipo de modelo

Se usará un modelo dimensional tipo estrella.

Este modelo tendrá una tabla de hechos central y varias dimensiones conectadas a ella.

## Grano del modelo

El grano de la tabla de hechos será:

1 fila por hogar entrevistado completo.

Por ello, cada registro de la fact table representará un hogar.

## Identificador del hogar

Se construirá el campo hogar_id con:

hogar_id = AÑO + CONGLOME + VIVIENDA + HOGAR

## Tabla de hechos

La tabla central será:

fact_hogar_bienestar

Esta tabla almacenará las principales métricas del hogar y las llaves hacia las dimensiones.

### Campos principales

- hogar_id
- tiempo_key
- geografia_key
- vivienda_key
- habitabilidad_key
- tenencia_key
- agua_key
- saneamiento_key
- energia_key
- conectividad_key
- credito_key
- cantidad_hogar
- factor_expansion
- habitaciones_total
- habitaciones_dormir
- nbi_total
- tiene_nbi
- gasto_pagado_servicios
- gasto_donado_servicios
- gasto_autoconsumo_servicios
- gasto_total_servicios
- alquiler_pagado_mensual
- alquiler_estimado_mensual
- monto_credito_total
- horas_agua_dia
- dias_agua_semana
- cloro_residual
- indice_brecha_bienestar
- categoria_brecha_bienestar

## Dimensiones

### dim_tiempo

Permite analizar los datos por año, mes, periodo y fecha de entrevista.

Variables principales:

- AÑO
- MES
- PERIODO
- FECENT

### dim_geografia

Permite analizar las brechas por ubicación territorial.

Variables principales:

- UBIGEO
- DOMINIO
- ESTRATO
- CODCCPP
- NOMCCPP
- LONGITUD
- LATITUD

### dim_vivienda

Describe las características físicas de la vivienda.

Variables principales:

- P101: tipo de vivienda.
- P102: material de paredes.
- P103: material de pisos.
- P103A: material de techos.

### dim_habitabilidad

Permite analizar condiciones internas del hogar, hacinamiento y necesidades básicas insatisfechas.

Variables principales:

- P104: total de habitaciones.
- P104A: habitaciones para dormir.
- NBI1: vivienda inadecuada.
- NBI2: hacinamiento.
- NBI3: vivienda sin servicios higiénicos.
- NBI4: niños que no asisten a la escuela.
- NBI5: alta dependencia económica.

### dim_tenencia_propiedad

Describe la situación de propiedad o uso de la vivienda.

Variables principales:

- P105A: régimen de tenencia.
- P106A: título de propiedad.
- P106B: registro del título en SUNARP.

### dim_agua

Describe el acceso, continuidad y calidad del agua.

Variables principales:

- P110: fuente principal de agua.
- T110: fuente de agua recodificada.
- P110A1: agua potable.
- P110A: nivel de cloro.
- P110A_MODIFICADA: valor de cloro residual.
- P110C: agua todos los días.
- P110C1: horas de agua al día.
- P110C2: días de agua por semana.
- P110C3: horas de agua cuando no hay servicio diario.
- P110D: quién extrajo la muestra de agua.
- P110E: origen de la muestra de agua.

### dim_saneamiento

Describe el tipo de baño o servicio higiénico del hogar.

Variables principales:

- P111A: tipo de servicio higiénico.
- T111A: servicio higiénico recodificado.

### dim_energia

Describe el tipo de alumbrado y el combustible usado para cocinar.

Variables principales:

- P1121: electricidad.
- P1123: lámpara de petróleo o gas.
- P1124: vela.
- P1125: generador.
- P1126: otro tipo de alumbrado.
- P1127: no usa alumbrado.
- P112A: tipo de medidor eléctrico.
- P113A: combustible principal para cocinar.
- P1131: cocina con electricidad.
- P1132: cocina con GLP.
- P1133: cocina con gas natural.
- P1135: cocina con carbón.
- P1136: cocina con leña.
- P1139: cocina con bosta o estiércol.

### dim_conectividad

Describe el acceso del hogar a tecnologías de información y comunicación.

Variables principales:

- P1141: teléfono fijo.
- P1142: celular.
- P1143: TV cable o satelital.
- P1144: internet.
- P1145: no tiene TIC.
- P1146: televisión digital terrestre.
- P114B1 o P1144B1: internet fijo.
- P114B2 o P1144B2: internet móvil postpago.
- P114B3 o P1144B3: internet móvil prepago.

### dim_credito_vivienda

Describe si el hogar accedió a créditos relacionados con vivienda.

Variables principales:

- P107B1: crédito para compra de casa o departamento.
- P107B2: crédito para compra de terreno.
- P107B3: crédito para mejoramiento o ampliación.
- P107B4: crédito para construcción de vivienda.
- P107D1: monto de crédito para compra de casa.
- P107D2: monto de crédito para compra de terreno.
- P107D3: monto de crédito para mejoramiento.
- P107D4: monto de crédito para construcción.

## Estructura general

El modelo queda organizado así:

dim_tiempo
dim_geografia
dim_vivienda
dim_habitabilidad
dim_tenencia_propiedad
dim_agua
dim_saneamiento
dim_energia
dim_conectividad
dim_credito_vivienda

Todas estas dimensiones se conectan con:

fact_hogar_bienestar

## Uso esperado

El modelo permitirá analizar:

- Brechas territoriales.
- Calidad de vivienda.
- Hacinamiento.
- Acceso a agua segura.
- Continuidad del agua.
- Saneamiento adecuado o precario.
- Acceso a electricidad.
- Uso de combustibles adecuados o precarios.
- Brecha digital.
- Gasto mensual en servicios.
- Acceso a créditos de vivienda.
- Índice de brecha de bienestar habitacional.
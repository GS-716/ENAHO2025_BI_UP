Fuente principal:
ENAHO01-2025-100.csv

Tabla raw:
enaho\_raw\_hogar

Dimensiones:
dim\_tiempo
dim\_ubicacion
dim\_vivienda
dim\_material\_vivienda
dim\_servicios\_basicos
dim\_tecnologia
dim\_tenencia

Fact:
fact\_condiciones\_hogar

Grano:
1 hogar encuestado

Link para ingresar al NeonDB: https://console.neon.tech/app/projects/broad-darkness-49139138
### Profesor, le dimos acceso a su correo de la up.


# Marco Teórico del Datamart de Bienestar Habitacional, Servicios y Conectividad (ENAHO)

El análisis del bienestar habitacional exige integrar dimensiones de vulnerabilidad que no pueden capturarse mediante un único indicador. La pobreza monetaria, las necesidades básicas insatisfechas (NBI), la habitabilidad, el acceso a servicios, la conectividad digital y el gasto del hogar son fenómenos interdependientes que requieren una infraestructura de datos especialmente diseñada. Un datamart de propósito específico responde a este requerimiento al concentrar en un modelo dimensional la información necesaria para el análisis multidimensional del bienestar.

El sustento teórico descansa en el paradigma de la pobreza multidimensional. Alkire y Foster (2007, revisado en 2008) proponen un procedimiento de doble umbral (de privación individual y de agregación multidimensional) que permite medir la pobreza en varias dimensiones simultáneamente, superando las limitaciones de los enfoques monetarios unidimensionales. Feres y Mancero (2001) sistematizan el método de las NBI para América Latina, estableciendo dimensiones estructurales como vivienda inadecuada, hacinamiento, servicios insuficientes, inasistencia escolar y dependencia económica, que informan directamente las variables de la fuente de datos empleada.

## Fuente de datos: ENAHO, Módulo de Características de la Vivienda y del Hogar

La fuente primaria de este trabajo es el Módulo 100 (Características de la Vivienda y del Hogar) de la Encuesta Nacional de Hogares sobre Condiciones de Vida y Pobreza (ENAHO), producida por el Instituto Nacional de Estadística e Informática del Perú (INEI). Los microdatos corresponden al periodo 2025 y fueron obtenidos del repositorio oficial del INEI (2025a). La ENAHO tiene cobertura nacional, representatividad urbana y rural, y desagregación departamental, lo que la convierte en la fuente más adecuada para el análisis del bienestar habitacional en el contexto peruano (Clausen et al., 2025). La unidad de análisis es el hogar, y sus variables registran condiciones estructurales de la vivienda, acceso a servicios básicos, tenencia y equipamiento.

## El Modelo Dimensional como Fundamento Estructural

El modelo estrella es el paradigma de organización de datos adoptado para este datamart. Kimball y Ross (2013) argumentan que el modelo dimensional es una filosofía de diseño orientada a la comprensibilidad y la velocidad de consulta: las tablas de dimensiones describen el contexto de los hechos, mientras que la tabla de hechos registra las métricas numéricas de interés analítico. El *grain statement* (la declaración explícita de la granularidad) establece que cada fila representa un hogar en un año de encuesta. Moody y Kortink (2000) complementan este marco con una metodología para derivar modelos dimensionales a partir de estructuras relacionales preexistentes, relevante dado que la ENAHO tiene un esquema relacional ya establecido que debe traducirse sin pérdida de coherencia analítica.

Un concepto central es el de las *Slowly Changing Dimensions* (SCD), que describen cómo gestionar los cambios en los atributos de las dimensiones a lo largo del tiempo. Kimball y Ross (2013) proponen tres estrategias: sobreescritura (Type 1), historial completo (Type 2) o registro del valor previo (Type 3), cada una con implicaciones distintas sobre la comparabilidad de los indicadores entre rondas de encuesta.

## El Proceso ETL como Garantía de Calidad del Dato

La integración de los datos en el datamart se realiza mediante un flujo de Extracción, Transformación y Carga (ETL). Kimball y Ross (2013) subrayan que el ETL no es un traslado mecánico de datos, sino un proceso de aseguramiento de calidad que determina la confiabilidad de todos los análisis subsecuentes. La extracción transfiere los datos desde la fuente al entorno de procesamiento y puede ser completa (*full extraction*) para la carga histórica inicial, o incremental para actualizaciones periódicas.

El área de *staging* preserva los datos en su estado original antes de cualquier transformación, mientras que el *data profiling* permite evaluar su calidad mediante el análisis de distribuciones, valores nulos, outliers e integridad referencial entre módulos a través de las claves de unión de la ENAHO (`CONGLOME + VIVIENDA + HOGAR`) (Rahm & Do, 2000). Durante la transformación, las reglas de negocio traducen las definiciones conceptuales de los indicadores, como el índice de hacinamiento, las dimensiones NBI y el gasto per cápita, en fórmulas computables sobre las variables del Módulo 100 (Alkire & Foster, 2007, revisado en 2008; Feres & Mancero, 2001). La asignación de claves subrogadas desacopla el modelo de las claves naturales de la encuesta, protegiéndolo ante cambios entre rondas (Kimball & Ross, 2013). Finalmente, la carga sigue un orden dimensional estricto: las tablas de dimensión se pueblan antes que la tabla de hechos, y la validación post-carga reconcilia los conteos entre el *staging* y el datamart para garantizar que ningún registro fue perdido ni duplicado.

## Infraestructura de Almacenamiento: PostgreSQL y Neon

El almacenamiento del datamart se apoya en PostgreSQL. Para su despliegue en la nube se utiliza Neon, una plataforma serverless que separa el almacenamiento del cómputo, permitiéndole escalar dinámicamente según la carga de trabajo y reducir a cero el consumo de recursos en periodos de inactividad (Neon, 2024). Esta arquitectura elimina la necesidad de gestionar infraestructura manualmente y mantiene plena compatibilidad con el ecosistema estándar de PostgreSQL.

## Dimensiones Temáticas del Bienestar Habitacional

Las dimensiones temáticas del datamart corresponden a los dominios conceptuales del bienestar habitacional reconocidos en la literatura. La habitabilidad considera calidad estructural, seguridad de tenencia y espacio suficiente (Naciones Unidas, 2021), con el hacinamiento como indicador de vulnerabilidad asociado a riesgos sanitarios documentados (Lorentzen et al., 2022; World Health Organization, 2018; Villanueva-Paredes & Villanueva-Paredes, 2023). La conectividad digital se incorpora como dimensión de desigualdad estructural, dado que el acceso diferenciado a internet tiene efectos probados sobre la inclusión educativa y económica (Flores-Cueto et al., 2020; INEI, 2025b). El gasto del hogar añade la capa económica que permite evaluar la carga financiera de mantener condiciones adecuadas de vivienda y servicios (Deaton, 1997; Galarza et al., 2022). La integración de estas dimensiones en un modelo dimensional soportado por un flujo ETL auditado y una infraestructura serverless es lo que distingue a este datamart de una simple consolidación de tablas.

---

# Descripción de la Empresa y Problemática

El Instituto Nacional de Estadística e Informática (INEI) es un organismo técnico especializado con autonomía técnica y de gestión, cuya misión es producir y difundir información estadística oficial para el diseño, seguimiento y evaluación de políticas públicas en el Perú (INEI, s.f.). Como organismo central y rector del Sistema Estadístico Nacional, el INEI es responsable de normar, planear, dirigir y supervisar las actividades estadísticas oficiales del país. Entre sus principales investigaciones se encuentra la Encuesta Nacional de Hogares (ENAHO), estudio de alcance nacional que recopila información sobre las condiciones de vida de la población peruana en aspectos relacionados con vivienda, educación, salud, empleo, ingresos y acceso a servicios básicos. Dentro de esta encuesta, el Módulo 100, denominado "Características de la Vivienda y del Hogar", concentra variables vinculadas a condiciones habitacionales como el tipo de vivienda, materiales de construcción, acceso a agua potable, saneamiento, electricidad, conectividad y gastos asociados a estos servicios.

En el Perú, durante el año 2025, persisten brechas significativas en las condiciones de vivienda, acceso a servicios básicos y conectividad de los hogares. En cuanto a habitabilidad, el déficit habitacional se estima en aproximadamente 1.6 millones de viviendas, y alrededor de 1.1 millones de hogares viven en condiciones de hacinamiento, materiales irrecuperables o servicios básicos deficitarios (INEI, 2025a). Esto refleja que, en muchos casos, el problema no es la ausencia de vivienda, sino la inadecuación de las condiciones en que esta se habita (Banco Mundial, 2022).

Respecto al acceso a servicios básicos, si bien el 90.4% de los hogares accede a agua mediante red pública a nivel nacional, en áreas rurales esta cobertura desciende al 80.5%, y solo el 29.4% de la población rural elimina excretas mediante red pública de alcantarillado, frente al 87.5% en zonas urbanas (INEI, 2025e). A esto se suma que el acceso no garantiza continuidad: en 2024, la continuidad del servicio en las empresas prestadoras fue de 18.5 horas diarias en promedio (INEI, 2025e). En materia de conectividad digital, el 60.1% de los hogares del país contaba con internet durante el segundo trimestre de 2025, cifra que cae al 23.6% en el área rural, frente al 80.5% en Lima Metropolitana (INEI, 2025b). Esta brecha digital limita el acceso a oportunidades educativas y económicas de manera desigual según el territorio (Flores-Cueto et al., 2020).

Del mismo modo, existen diferencias importantes en el gasto que realizan los hogares para mantener estos servicios, evidenciando desigualdades económicas y limitaciones en la capacidad de acceso a condiciones de vida adecuadas (Deaton, 1997; Galarza et al., 2022). Estas brechas afectan directamente la calidad de vida de la población y dificultan el desarrollo equitativo entre regiones y estratos socioeconómicos del país.

Frente a esta problemática, se propone el desarrollo de un datamart orientado al análisis de las condiciones de vivienda y acceso a servicios básicos de los hogares peruanos, utilizando información del Módulo 100 de la ENAHO 2025. El objetivo es integrar, transformar y estructurar los datos mediante procesos ETL y modelado dimensional, facilitando la generación de indicadores que permitan identificar patrones, comparar niveles de acceso y analizar las diferencias existentes entre hogares, regiones y grupos poblacionales (Kimball & Ross, 2013).


---

# METODOLOGÍA

El proyecto se desarrolló a partir del Módulo 100 de la Encuesta Nacional de Hogares sobre Condiciones de Vida y Pobreza (ENAHO) 2025, que recoge información sobre tipo de vivienda, materiales de construcción, habitaciones, tenencia, agua, saneamiento, alumbrado, combustible para cocinar, conectividad y gasto en servicios del hogar. La elección de esta fuente responde a que la ENAHO permite generar indicadores de pobreza multidimensional, bienestar y condiciones habitacionales con cobertura nacional y representatividad urbano-rural (INEI, 2025a). La problemática que orientó el datamart fue la existencia de una brecha multidimensional de bienestar habitacional, entendida como la distribución desigual de condiciones mínimas adecuadas de vivienda, servicios básicos, energía y conectividad entre los hogares peruanos.

La primera etapa consistió en la revisión documental de los archivos técnicos de la ENAHO 2025, incluyendo la ficha técnica, el cuestionario, el diccionario de datos, el documento de valores monetarios y la documentación del marco muestral. A partir de esta revisión se seleccionaron las variables relevantes para el datamart, priorizando identificadores del hogar, ubicación geográfica, diseño muestral, características físicas de la vivienda, acceso a servicios, conectividad, gastos y los indicadores NBI1 a NBI5. También se incluyó el factor de expansión anual FACTOR07, que permite realizar estimaciones ponderadas representativas a nivel poblacional.

Posteriormente se ejecutó el proceso de data profiling en Python, en el que se validó la estructura del archivo CSV original, los tipos de datos, los valores nulos, la codificación de variables categóricas, la duplicidad de hogares y la consistencia de la llave natural. Esta fase permitió detectar que varias variables monetarias del diccionario se encontraban expandidas en columnas específicas en la base real, lo cual requirió ajustes en la selección de campos. Como resultado del profiling se establecieron las reglas de limpieza y transformación: se trabajó únicamente con hogares con entrevista completa (RESULT = 1), se construyó una llave única del hogar combinando AÑO, CONGLOME, VIVIENDA y HOGAR, y se mantuvieron los códigos categóricos como texto para evitar errores de interpretación.

El flujo de trabajo se organizó en tres capas: una base raw sin modificaciones, una base intermedia validada y una tabla staging denominada stg_enaho_hogar_100_limpio. En esta última se aplicaron las transformaciones orientadas al negocio: renombrado de variables, mapeo de códigos a descripciones, creación de indicadores binarios y cálculo de variables derivadas como horas de agua al día, días de abastecimiento semanal y gastos estimados en servicios. Para las variables monetarias se priorizó el uso de valores imputados, deflactados y anualizados (prefijo I), siguiendo la documentación metodológica oficial, ya que reducen el efecto de valores perdidos y garantizan la comparabilidad entre hogares.

A partir de la tabla staging se diseñó el modelo dimensional bajo un esquema estrella, tomando como grano una fila por hogar entrevistado completo (Kimball & Ross, 2013). La tabla de hechos fact_hogar_bienestar concentra las claves foráneas hacia diez dimensiones (dim_tiempo, dim_geografia, dim_vivienda, dim_materiales_vivienda, dim_habitabilidad, dim_tenencia_propiedad, dim_agua, dim_saneamiento, dim_energia y dim_conectividad), junto con las métricas principales del análisis. Entre los indicadores construidos destaca la brecha multidimensional, definida como la presencia de dos o más carencias en las dimensiones consideradas, lo que permite aproximarse a una medición integrada del bienestar habitacional (Alkire & Foster, 2007, revisado en 2008; Feres & Mancero, 2001).

Finalmente, el modelo estrella se cargó en una base de datos PostgreSQL alojada en Neon (2024), utilizando Python con las bibliotecas pandas, SQLAlchemy y psycopg2. El proceso incluyó la creación de un esquema específico, la carga ordenada de dimensiones antes de la tabla de hechos, la definición de claves primarias, foráneas e índices, y la ejecución de consultas de validación para verificar integridad referencial y conteos de filas. Como documentación técnica complementaria se generó un diagrama relacional del modelo estrella con Graphviz y un diccionario del datamart en Excel que registra tablas, columnas, tipos de datos, origen de variables, reglas de transformación y relaciones entre tablas dando como resultado las siguientes tablas y el diagrama relacional modelo estrella.

---


## Dim_tiempo 
Dimensión que registra los atributos temporales asociados a cada registro de la encuesta, permitiendo el análisis del bienestar habitacional por año, mes y periodo de ejecución de la ENAHO.

| Columna    | PK/FK | Tipo de dato | Definición                                      | Nullable |
|------------|-------|--------------|------------------------------------------------|----------|
| tiempo_key | PK    | BIGINT       | Identificador único de combinación temporal.   | No       |
| anio       |       | TEXT         | Año de la encuesta.                            | No       |
| mes        |       | TEXT         | Mes de ejecución de la encuesta.               | No       |
| periodo    |       | TEXT         | Periodo de ejecución de la encuesta.           | No       |

## Dim_geografia
Dimensión que describe la ubicación geográfica de cada hogar encuestado, incluyendo el código UBIGEO, el dominio y estrato geográfico, y las coordenadas espaciales cuando están disponibles.

| Columna       | PK/FK | Tipo de dato     | Definición                                        | Nullable |
|---------------|-------|------------------|---------------------------------------------------|----------|
| geografia_key | PK    | BIGINT           | Identificador único de combinación geográfica.    | No       |
| ubigeo        |       | TEXT             | Código de ubicación geográfica del hogar.         | No       |
| dominio_cod   |       | TEXT             | Código de dominio geográfico.                     | No       |
| dominio       |       | TEXT             | Etiqueta del dominio geográfico.                  | No       |
| estrato_cod   |       | TEXT             | Código de estrato geográfico.                     | No       |
| estrato       |       | TEXT             | Etiqueta del estrato geográfico.                  | No       |
| latitud       |       | FLOAT | Latitud del registro cuando está disponible.      | Sí       |
| longitud      |       | FLOAT | Longitud del registro cuando está disponible.     | Sí       |
| altitud       |       | FLOAT | Altitud del registro cuando está disponible.      | Sí       |

## Dim_vivienda
Dimensión que clasifica los hogares según el tipo de vivienda que habitan, asociando cada código con su descripción correspondiente.

| Columna          | PK/FK | Tipo de dato | Definición                          | Nullable |
|------------------|-------|--------------|-------------------------------------|----------|
| vivienda_key     | PK    | BIGINT       | Identificador de tipo de vivienda.  | No       |
| tipo_vivienda_cod|       | TEXT         | Código del tipo de vivienda.        | Sí       |
| tipo_vivienda    |       | TEXT         | Descripción del tipo de vivienda.   | Sí       |

## Dim_materiales_vivienda
Dimensión que registra los materiales predominantes en paredes, pisos y techos de la vivienda, incluyendo indicadores de precariedad estructural para cada elemento y para la vivienda en su conjunto.

| Columna                        | PK/FK | Tipo de dato | Definición                                                  | Nullable |
|--------------------------------|-------|--------------|-------------------------------------------------------------|----------|
| materiales_vivienda_key        | PK    | BIGINT       | Identificador de combinación de materiales.                 | No       |
| material_pared_cod             |       | TEXT         | Código del material predominante en paredes exteriores.     | Sí       |
| material_pared                 |       | TEXT         | Etiqueta del material predominante en paredes exteriores.   | Sí       |
| material_piso_cod              |       | TEXT         | Código del material predominante en pisos.                  | Sí       |
| material_piso                  |       | TEXT         | Etiqueta del material predominante en pisos.                | Sí       |
| material_techo_cod             |       | TEXT         | Código del material predominante en techos.                 | Sí       |
| material_techo                 |       | TEXT         | Etiqueta del material predominante en techos.               | Sí       |
| pared_precaria_ind             |       | BIGINT       | Indica pared precaria.                                      | Sí       |
| piso_precario_ind              |       | BIGINT       | Indica piso precario.                                       | Sí       |
| techo_precario_ind             |       | BIGINT       | Indica techo precario.                                      | Sí       |
| vivienda_material_precario_ind |       | BIGINT       | Indica si existe al menos un material precario.             | Sí       |

## Dim_habitabilidad
Dimensión que caracteriza las condiciones de habitabilidad del hogar a partir de los indicadores NBI oficiales de la ENAHO, incluyendo clasificaciones de hacinamiento, carencias acumuladas y una medida sintética de brecha multidimensional.

| Columna                        | PK/FK | Tipo de dato | Definición                                                  | Nullable |
|--------------------------------|-------|--------------|-------------------------------------------------------------|----------|
| habitabilidad_key              | PK    | BIGINT       | Identificador de categoría de habitabilidad.                | No       |
| rango_habitaciones_total       |       | TEXT         | Rango de habitaciones totales.                              | Sí       |
| rango_habitaciones_dormir      |       | TEXT         | Rango de habitaciones usadas para dormir.                   | Sí       |
| nbi_vivienda_inadecuada_ind    |       | BIGINT       | Indicador ENAHO de vivienda inadecuada.                     | Sí       |
| nbi_hacinamiento_ind           |       | BIGINT       | Indicador ENAHO de hacinamiento.                            | Sí       |
| nbi_sin_servicio_higienico_ind |       | BIGINT       | Indicador ENAHO de hogar sin servicio higiénico.            | Sí       |
| nbi_ninios_no_asisten_ind      |       | BIGINT       | Indicador ENAHO de niños que no asisten a la escuela.       | Sí       |
| nbi_alta_dependencia_ind       |       | BIGINT       | Indicador ENAHO de alta dependencia económica.              | Sí       |
| categoria_carencias            |       | TEXT         | Clasificación ordinal del total de carencias.               | Sí       |
| brecha_multidimensional_ind    |       | BIGINT       | Hogar con brecha multidimensional.                          | No       |

## Dim_tenencia_propiedad
Dimensión que clasifica los hogares según el régimen de tenencia de su vivienda, diferenciando modalidades como propiedad, alquiler u otras formas de ocupación.

| Columna               | PK/FK | Tipo de dato | Definición                                  | Nullable |
|-----------------------|-------|--------------|---------------------------------------------|----------|
| tenencia_propiedad_key| PK    | BIGINT       | Identificador del régimen de tenencia.      | No       |
| tenencia_vivienda_cod |       | TEXT         | Código del régimen de tenencia.             | Sí       |
| tenencia_vivienda     |       | TEXT         | Descripción del régimen de tenencia.        | Sí       |

## Dim_agua
Dimensión que caracteriza el acceso al agua del hogar según la fuente de abastecimiento, la calidad del suministro y su disponibilidad, incluyendo indicadores de seguridad hídrica derivados de la ENAHO.

| Columna              | PK/FK | Tipo de dato | Definición                                                   | Nullable |
|----------------------|-------|--------------|--------------------------------------------------------------|----------|
| agua_key             | PK    | BIGINT       | Identificador de combinación de acceso y seguridad del agua. | No       |
| fuente_agua_cod      |       | TEXT         | Código de fuente principal de agua.                          | Sí       |
| fuente_agua          |       | TEXT         | Descripción de la fuente principal de agua.                  | Sí       |
| nivel_cloro_cod      |       | TEXT         | Código del nivel de cloro residual.                          | Sí       |
| nivel_cloro          |       | TEXT         | Descripción del nivel de cloro residual.                     | Sí       |
| agua_red_publica_ind |       | BIGINT       | Acceso a agua por red pública.                               | Sí       |
| agua_potable_ind     |       | BIGINT       | Agua declarada potable.                                      | Sí       |
| cloro_seguro_ind     |       | BIGINT       | Nivel de cloro seguro.                                       | Sí       |
| agua_todos_dias_ind  |       | BIGINT       | Disponibilidad de agua todos los días.                       | Sí       |
| agua_segura_ind      |       | BIGINT       | Agua segura estricta.                                        | Sí       |

## Dim_saneamiento
Dimensión que clasifica el tipo de servicio higiénico disponible en el hogar e incluye indicadores sobre la adecuación del saneamiento y la carencia registrada como NBI.

| Columna                        | PK/FK | Tipo de dato | Definición                                       | Nullable |
|--------------------------------|-------|--------------|--------------------------------------------------|----------|
| saneamiento_key                | PK    | BIGINT       | Identificador de tipo de saneamiento.            | No       |
| servicio_higienico_cod         |       | TEXT         | Código recodificado del servicio higiénico.      | Sí       |
| servicio_higienico             |       | TEXT         | Descripción del servicio higiénico.              | Sí       |
| saneamiento_adecuado_ind       |       | BIGINT       | Saneamiento considerado adecuado.                | Sí       |
| nbi_sin_servicio_higienico_ind |       | BIGINT       | NBI de hogar sin servicio higiénico.             | Sí       |


## Dim_energia
Dimensión que caracteriza el acceso a energía del hogar según el tipo de alumbrado eléctrico y el combustible utilizado para cocinar, incluyendo indicadores de uso de combustibles limpios y contaminantes.

| Columna                | PK/FK | Tipo de dato | Definición                                      | Nullable |
|------------------------|-------|--------------|-------------------------------------------------|----------|
| energia_key            | PK    | BIGINT       | Identificador de energía y combustible.         | No       |
| combustible_cocina_cod |       | TEXT         | Código del combustible principal para cocinar.  | Sí       |
| combustible_cocina     |       | TEXT         | Descripción del combustible principal.          | Sí       |
| tiene_electricidad_ind |       | BIGINT       | Hogar tiene alumbrado eléctrico.                | Sí       |
| combustible_limpio_ind |       | BIGINT       | Uso de combustible limpio para cocinar.         | Sí       |
| combustible_solido_ind |       | BIGINT       | Uso de combustible sólido/contaminante.         | Sí       |


## Dim_conectividad
Dimensión que registra la disponibilidad de tecnologías de información y comunicación en el hogar, incluyendo telefonía, televisión por suscripción, internet y un indicador de exclusión digital total.

| Columna                | PK/FK | Tipo de dato | Definición                                                   | Nullable |
|------------------------|-------|--------------|--------------------------------------------------------------|----------|
| conectividad_key       | PK    | BIGINT       | Identificador de combinación TIC.                            | No       |
| tiene_telefono_fijo_ind|       | BIGINT       | Hogar tiene teléfono fijo.                                   | Sí       |
| tiene_celular_ind      |       | BIGINT       | Hogar tiene teléfono celular.                                | Sí       |
| tiene_tv_cable_ind     |       | BIGINT       | Hogar tiene TV por cable o satelital.                        | Sí       |
| tiene_internet_ind     |       | BIGINT       | Hogar tiene conexión a internet fijo o móvil.                | Sí       |
| sin_tic_ind            |       | BIGINT       | Hogar no tiene teléfono fijo, celular, TV cable ni internet. | Sí       |
| tiene_tdt_ind          |       | BIGINT       | Hogar tiene Televisión Digital Terrestre.                    | Sí       |

## Fact_hogar_bienestar
Tabla de hechos central del datamart que registra un hogar por fila, consolidando las claves foráneas hacia todas las dimensiones junto con las métricas numéricas y los indicadores derivados de habitabilidad, servicios, conectividad y gasto.

| Columna                               | PK/FK | Tipo de dato     | Definición                                                                         | Nullable |
|---------------------------------------|-------|------------------|------------------------------------------------------------------------------------|----------|
| hogar_id                              | PK    | TEXT             | Identificador único del hogar en el datamart.                                      | No       |
| conglome                              |       | TEXT             | Campo original CONGLOME conservado para trazabilidad.                              | No       |
| vivienda                              |       | TEXT             | Campo original VIVIENDA conservado para trazabilidad.                              | No       |
| hogar                                 |       | TEXT             | Campo original HOGAR conservado para trazabilidad.                                 | No       |
| tiempo_key                            | FK    | BIGINT           | Clave foránea hacia dim_tiempo.                                                    | No       |
| geografia_key                         | FK    | BIGINT           | Clave foránea hacia dim_geografia.                                                 | No       |
| vivienda_key                          | FK    | BIGINT           | Clave foránea hacia dim_vivienda.                                                  | No       |
| materiales_vivienda_key               | FK    | BIGINT           | Clave foránea hacia dim_materiales_vivienda.                                       | No       |
| habitabilidad_key                     | FK    | BIGINT           | Clave foránea hacia dim_habitabilidad.                                             | No       |
| tenencia_propiedad_key                | FK    | BIGINT           | Clave foránea hacia dim_tenencia_propiedad.                                        | No       |
| agua_key                              | FK    | BIGINT           | Clave foránea hacia dim_agua.                                                      | No       |
| saneamiento_key                       | FK    | BIGINT           | Clave foránea hacia dim_saneamiento.                                               | No       |
| energia_key                           | FK    | BIGINT           | Clave foránea hacia dim_energia.                                                   | No       |
| conectividad_key                      | FK    | BIGINT           | Clave foránea hacia dim_conectividad.                                              | No       |
| factor_expansion                      |       | FLOAT | Factor de expansión del hogar.                                                     | Sí       |
| habitaciones_total                    |       | FLOAT | Número total de habitaciones, sin baño, cocina, pasadizos ni garaje.               | Sí       |
| habitaciones_dormir                   |       | FLOAT | Número de habitaciones usadas exclusivamente para dormir.                          | Sí       |
| alquiler_mensual_reportado            |       | FLOAT | Monto mensual reportado por alquiler o compra.                                     | Sí       |
| alquiler_estimado_mensual             |       | FLOAT | Alquiler mensual estimado si se alquilara la vivienda.                             | Sí       |
| alquiler_anual_imputado               |       | FLOAT | Alquiler/compra imputado, deflactado y anualizado.                                 | Sí       |
| alquiler_estimado_anual_imputado      |       | FLOAT | Alquiler estimado imputado, deflactado y anualizado.                               | Sí       |
| horas_agua_dia                        |       | FLOAT | Horas de abastecimiento de agua por día.                                           | Sí       |
| dias_agua_semana                      |       | FLOAT | Días de abastecimiento de agua por semana.                                         | Sí       |
| gasto_anual_servicios_pagado_hogar    |       | FLOAT | Gasto anual imputado en servicios pagado por miembros del hogar.                   | Sí       |
| gasto_anual_servicios_donado          |       | FLOAT | Gasto anual imputado en servicios donado/regalado por otro hogar.                  | Sí       |
| gasto_anual_servicios_autoconsumo     |       | FLOAT | Gasto anual imputado por autoconsumo/autosuministro.                               | Sí       |
| gasto_anual_servicios_total           |       | FLOAT | Gasto anual total imputado en servicios.                                           | Sí       |
| gasto_mensual_servicios_estimado      |       | FLOAT | Estimación mensual del gasto total en servicios.                                   | Sí       |
| total_carencias_bienestar_habitacional|       | BIGINT           | Número total de carencias del hogar.                                               | Sí       |
| agua_red_publica_ind                  |       | BIGINT           | Indicador derivado agua_red_publica_ind.                                           | Sí       |
| agua_potable_ind                      |       | BIGINT           | Indicador derivado agua_potable_ind.                                               | Sí       |
| cloro_seguro_ind                      |       | BIGINT           | Indicador derivado cloro_seguro_ind.                                               | Sí       |
| agua_todos_dias_ind                   |       | BIGINT           | Indicador derivado agua_todos_dias_ind.                                            | Sí       |
| agua_segura_ind                       |       | BIGINT           | Indicador derivado agua_segura_ind.                                                | Sí       |
| saneamiento_adecuado_ind              |       | BIGINT           | Indicador derivado saneamiento_adecuado_ind.                                       | Sí       |
| pared_precaria_ind                    |       | BIGINT           | Indicador derivado pared_precaria_ind.                                             | Sí       |
| piso_precario_ind                     |       | BIGINT           | Indicador derivado piso_precario_ind.                                              | Sí       |
| techo_precario_ind                    |       | BIGINT           | Indicador derivado techo_precario_ind.                                             | Sí       |
| vivienda_material_precario_ind        |       | BIGINT           | Indicador derivado vivienda_material_precario_ind.                                 | Sí       |
| nbi_vivienda_inadecuada_ind           |       | BIGINT           | Indicador derivado nbi_vivienda_inadecuada_ind.                                    | Sí       |
| nbi_hacinamiento_ind                  |       | BIGINT           | Indicador derivado nbi_hacinamiento_ind.                                           | Sí       |
| nbi_sin_servicio_higienico_ind        |       | BIGINT           | Indicador derivado nbi_sin_servicio_higienico_ind.                                 | Sí       |
| nbi_ninios_no_asisten_ind             |       | BIGINT           | Indicador derivado nbi_ninios_no_asisten_ind.                                      | Sí       |
| nbi_alta_dependencia_ind              |       | BIGINT           | Indicador derivado nbi_alta_dependencia_ind.                                       | Sí       |
| tiene_electricidad_ind                |       | BIGINT           | Indicador derivado tiene_electricidad_ind.                                         | Sí       |
| combustible_limpio_ind                |       | BIGINT           | Indicador derivado combustible_limpio_ind.                                         | Sí       |
| combustible_solido_ind                |       | BIGINT           | Indicador derivado combustible_solido_ind.                                         | Sí       |
| tiene_telefono_fijo_ind               |       | BIGINT           | Indicador derivado tiene_telefono_fijo_ind.                                        | Sí       |
| tiene_celular_ind                     |       | BIGINT           | Indicador derivado tiene_celular_ind.                                              | Sí       |
| tiene_tv_cable_ind                    |       | BIGINT           | Indicador derivado tiene_tv_cable_ind.                                             | Sí       |
| tiene_internet_ind                    |       | BIGINT           | Indicador derivado tiene_internet_ind.                                             | Sí       |
| sin_tic_ind                           |       | BIGINT           | Indicador derivado sin_tic_ind.                                                    | Sí       |
| tiene_tdt_ind                         |       | BIGINT           | Indicador derivado tiene_tdt_ind.                                                  | Sí       |
| carencia_materiales_vivienda_ind      |       | BIGINT           | Indicador derivado carencia_materiales_vivienda_ind.                               | Sí       |
| carencia_hacinamiento_ind             |       | BIGINT           | Indicador derivado carencia_hacinamiento_ind.                                      | Sí       |
| carencia_agua_segura_ind              |       | BIGINT           | Indicador derivado carencia_agua_segura_ind.                                       | Sí       |
| carencia_saneamiento_ind              |       | BIGINT           | Indicador derivado carencia_saneamiento_ind.                                       | Sí       |
| carencia_electricidad_ind             |       | BIGINT           | Indicador derivado carencia_electricidad_ind.                                      | Sí       |
| carencia_combustible_limpio_ind       |       | BIGINT           | Indicador derivado carencia_combustible_limpio_ind.                                | Sí       |
| carencia_internet_ind                 |       | BIGINT           | Indicador derivado carencia_internet_ind.                                          | Sí       |
| brecha_multidimensional_ind           |       | BIGINT           | Indicador derivado brecha_multidimensional_ind.                                    | Sí       |

# DIAGRAMA MODELO ESTRELLA

<img src="src/outputs/diagrams/erd_enaho2025_resumen_compacto.png" alt="Modelo relacional" width="800">

---

## Referencias

Alkire, S., & Foster, J. (2007, revisado en 2008). *Counting and multidimensional poverty measurement* (OPHI Working Paper No. 7). Oxford Poverty and Human Development Initiative. https://ophi.org.uk/sites/default/files/ophi-wp7_vs2.pdf

Clausen, J., Barrantes, N., Trivelli, C., & Salas, F. (2025). Evaluating poverty in all its forms and dimensions: Monetary, multidimensional, and subjective poverty in Peru. *Social Indicators Research, 179*, 861–893. https://doi.org/10.1007/s11205-025-03641-7

Deaton, A. (1997). *The analysis of household surveys: A microeconometric approach to development policy*. Johns Hopkins University Press.

Feres, J. C., & Mancero, X. (2001). *El método de las necesidades básicas insatisfechas y sus aplicaciones en América Latina*. Comisión Económica para América Latina y el Caribe.

Flores-Cueto, J. J., Hernández, R. M., & Garay-Argandoña, R. (2020). Tecnologías de información: Acceso a internet y brecha digital en Perú. *Revista Venezolana de Gerencia, 25*(90), 504–527.

Galarza, F. B., Carbajal, M., & Aguirre, J. (2022). *Willingness to pay for improved water service: Evidence from urban Peru*. Peruvian Economic Association.

Instituto Nacional de Estadística e Informática. (2025a). *Encuesta Nacional de Hogares sobre Condiciones de Vida y Pobreza — ENAHO 2025: Módulo de características de la vivienda y del hogar* [Microdatos]. [https://proyectos.inei.gob.pe/microdatos/](https://proyectos.inei.gob.pe/microdatos/Detalle_Encuesta.asp?CU=19558&CodEncuesta=1031&CodModulo=01&NombreEncuesta=Condiciones+de+Vida+y+Pobreza+-+ENAHO&NombreModulo=Caracter%C3%ADsticas+de+la+Vivienda+y+del+Hogar)

Instituto Nacional de Estadística e Informática. (2025b). *Perú: Tecnologías de información y comunicación en los hogares, II trimestre 2025*. https://www.inei.gob.pe/biblioteca-virtual/boletines/tecnologias-de-la-informacion-y-comunicacion/

Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). John Wiley & Sons.

Lorentzen, J. C., Johanson, G., Björk, F., & Stensson, S. (2022). Overcrowding and hazardous dwelling condition characteristics. *International Journal of Environmental Research and Public Health, 19*(23), 15542. https://doi.org/10.3390/ijerph192315542

Moody, D. L., & Kortink, M. A. R. (2000). From enterprise models to dimensional models: A methodology for data warehouse and data mart design. En M. Jeusfeld, H. Shu, M. Staudt & G. Vossen (Eds.), *Proceedings of the 2nd International Workshop on Design and Management of Data Warehouses (DMDW'2000)* (pp. 5-1–5-12). CEUR Workshop Proceedings. https://ceur-ws.org/Vol-28/paper5.pdf

Naciones Unidas. (2021). *Metadata for Sustainable Development Goal indicator 11.1.1*. United Nations Statistics Division. https://unstats.un.org/sdgs/metadata/?Text=&Goal=11&Target=11.1

Neon. (2024). *Neon documentation: Introduction to Neon serverless Postgres*. https://neon.com/docs/introduction

Rahm, E., & Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.

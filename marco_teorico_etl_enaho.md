# Marco Teórico del Datamart de Bienestar Habitacional, Servicios y Conectividad (ENAHO) con Enfoque ETL Profesional

El análisis del bienestar habitacional exige integrar dimensiones de vulnerabilidad que no pueden capturarse mediante un único indicador: pobreza monetaria, necesidades básicas insatisfechas (NBI), habitabilidad, acceso a servicios, conectividad digital y gasto del hogar son fenómenos interdependientes cuya comprensión conjunta requiere una infraestructura de datos especialmente diseñada. Un datamart de propósito específico constituye la respuesta técnica a este requerimiento, al concentrar en un modelo dimensional la información necesaria para el análisis multidimensional del bienestar. La Encuesta Nacional de Hogares (ENAHO), con su cobertura nacional y representatividad urbano-rural y departamental, es la fuente primaria que hace viable este enfoque en el contexto peruano (Instituto Nacional de Estadística e Informática [INEI], 2025a; Clausen et al., 2025).

El sustento teórico del datamart descansa en el paradigma de la pobreza multidimensional y las NBI. La metodología de Alkire y Foster (2007, revisado en 2008) propone un procedimiento de doble umbral —de privación individual y de agregación multidimensional— que permite identificar simultáneamente a los hogares pobres en varias dimensiones y medir la intensidad de esa pobreza, superando las limitaciones de los enfoques monetarios unidimensionales. Feres y Mancero (2001) sistematizan el método de las NBI para América Latina, estableciendo las dimensiones estructurales —vivienda inadecuada, hacinamiento, servicios insuficientes, inasistencia escolar y dependencia económica— que informan directamente las variables del Módulo 100 de la ENAHO. Ambos marcos justifican la necesidad de que el datamart preserve la granularidad a nivel de hogar y soporte consultas desagregadas por múltiples atributos simultáneamente.

---

## El Modelo Dimensional como Fundamento Estructural

El modelo estrella es el paradigma de organización de datos adoptado para este datamart. Kimball y Ross (2013) argumentan que el modelo dimensional no es simplemente una técnica de almacenamiento, sino una filosofía de diseño orientada a la comprensibilidad y la velocidad de consulta: las tablas de dimensiones describen el contexto de los hechos (quién, qué, dónde, cuándo), mientras que la tabla de hechos registra las métricas numéricas de interés analítico. El *grain statement* —la declaración explícita de la granularidad— es el punto de partida conceptual del diseño: en este caso, cada fila de la tabla de hechos representa un hogar en un año de encuesta ENAHO, lo que determina el nivel de detalle de todos los atributos dimensionales posibles. Moody y Kortink (2000) complementan este marco al proponer una metodología sistemática para derivar modelos dimensionales a partir de modelos de entidad-relación existentes, lo que resulta especialmente relevante cuando la fuente de datos —como la ENAHO— tiene una estructura relacional preestablecida que debe traducirse al esquema estrella sin pérdida de coherencia analítica.

Un concepto central en el diseño de dimensiones es el de las *Slowly Changing Dimensions* (SCD), tratado extensamente por Kimball y Ross (2013). Las SCDs describen el problema conceptual de cómo gestionar los cambios en los atributos de las dimensiones a lo largo del tiempo: si una provincia es reclasificada geográficamente o un hogar cambia su categoría de pobreza entre rondas ENAHO, el modelo dimensional debe disponer de una estrategia explícita —sobreescritura (Type 1), historial completo (Type 2) o registro del valor previo (Type 3)— para preservar la integridad analítica de las series temporales. La elección entre tipos de SCD no es trivial y tiene implicaciones directas sobre la comparabilidad de los indicadores entre años de encuesta.

---

## El Proceso ETL como Garantía de Calidad del Dato

La integración de los datos de la ENAHO en el datamart se realiza mediante un flujo de Extracción, Transformación y Carga (ETL). Conceptualmente, el ETL no es un procedimiento técnico de traslado de datos, sino un proceso de aseguramiento de calidad que determina la confiabilidad de todos los análisis subsecuentes. Kimball y Ross (2013) identifican 34 subsistemas en un sistema ETL completo, organizados en cuatro funciones principales: extracción, limpieza y conformación, entrega, y gestión. Este marco conceptual subraya que la calidad del dato en el datamart es una propiedad que debe construirse activamente en cada etapa del flujo, no una característica que pueda darse por sentada en la fuente.

### Extracción

La extracción es la etapa en que los datos son transferidos desde los sistemas fuente al entorno de procesamiento del datamart. Su complejidad conceptual reside en que la fuente —en este caso, los microdatos de la ENAHO publicados por el INEI en formatos propietarios— puede contener inconsistencias, versiones distintas de un mismo módulo y estructuras que no corresponden directamente al modelo dimensional destino. Por ello, la extracción requiere un análisis previo de las fuentes (*source system analysis*) que documente la estructura de cada módulo, sus claves candidatas y su volumen, antes de que cualquier dato sea movido. Kimball y Ross (2013) distinguen además entre una extracción completa (*full extraction*), apropiada para la carga histórica inicial, y una extracción incremental o delta, que transfiere únicamente los registros nuevos o modificados desde la última ejecución del pipeline, lo que resulta esencial para sostener cargas periódicas eficientes en encuestas anuales como la ENAHO.

### Staging y Data Profiling

El área de *staging* es un espacio de trabajo intermedio donde los datos extraídos son almacenados antes de su transformación. Su función conceptual es preservar los datos crudos en su estado original, garantizando que siempre sea posible reprocesar el pipeline desde la fuente sin afectar los sistemas de origen ni el datamart destino. Kimball y Ross (2013) enfatizan que el *staging* no es un repositorio permanente, sino una zona transitoria de trabajo que separa físicamente el proceso de extracción del de transformación, lo que permite auditar y corregir errores en cada etapa de forma independiente.

Sobre los datos en *staging* se ejecuta el *data profiling*, proceso que Rahm y Do (2000) describen como el análisis sistemático de la estructura, el contenido y las relaciones de los datos para evaluar su calidad antes de cualquier transformación. El *profiling* opera en tres niveles analíticos complementarios: a nivel de columna, examina la distribución de valores, la cardinalidad, el porcentaje de nulos y la presencia de outliers en cada variable; a nivel de relaciones entre columnas (*cross-column*), verifica reglas de integridad intra-módulo, como la coherencia entre una variable que indica el material de las paredes y las subvariables que lo especifican; y a nivel de relaciones entre tablas (*cross-table*), controla la integridad referencial entre módulos a través de las claves de unión de la ENAHO (`CONGLOME + VIVIENDA + HOGAR`), identificando registros huérfanos que carecen de contraparte en otro módulo. El resultado del *profiling* es un reporte formal que documenta el estado de calidad de los datos y fundamenta las decisiones de limpieza y transformación, constituyendo evidencia auditada del proceso.

### Transformación

La transformación es la etapa conceptualmente más rica del flujo ETL, pues es donde los datos crudos son convertidos en información analíticamente útil. Rahm y Do (2000) clasifican los problemas de calidad del dato que la transformación debe resolver en dos grandes grupos: los problemas de instancia —valores incorrectos, nulos, duplicados y formatos inconsistentes— y los problemas de esquema —diferencias estructurales entre la fuente y el modelo destino—. El *data cleansing* aborda los primeros mediante estrategias de imputación, exclusión o marcado con valores centinela, y estandariza codificaciones al estándar UBIGEO del INEI para garantizar la comparabilidad geográfica entre módulos y años de encuesta.

La aplicación de reglas de negocio (*business rule application*) es el subproceso que traduce las definiciones conceptuales de los indicadores —índice de hacinamiento, dimensiones NBI, pobreza multidimensional, gasto per cápita— en fórmulas computables sobre las variables del Módulo 100, documentando explícitamente la lógica de cálculo y su fundamento metodológico (Alkire & Foster, 2007, revisado en 2008; Feres & Mancero, 2001). Estos indicadores se materializan como columnas derivadas que enriquecen el modelo dimensional con atributos que no existen directamente en la fuente pero que son esenciales para el análisis del bienestar habitacional.

La asignación de claves subrogadas (*surrogate key assignment*) es un mecanismo conceptual que desacopla el modelo dimensional de las claves naturales de la ENAHO, protegiéndolo ante reclasificaciones o cambios en los identificadores de la encuesta entre rondas. Kimball y Ross (2013) subrayan que las claves subrogadas son la base de la estabilidad del modelo dimensional a lo largo del tiempo, y que su ausencia haría que cualquier cambio en la fuente se propagara directamente al esquema del datamart. El *data lineage* —la documentación de la trazabilidad de cada campo del datamart hasta su variable fuente en el módulo ENAHO correspondiente— completa el marco de transparencia de la transformación, y junto con el repositorio de metadatos ETL centraliza las definiciones, las reglas aplicadas y el versionado del proceso.

### Carga

La carga es la etapa en que el modelo dimensional es poblado con los datos transformados. Su principio conceptual fundamental, establecido por Kimball y Ross (2013), es el orden de carga dimensional: las tablas de dimensión deben poblarse antes que la tabla de hechos, porque esta última contiene referencias a todas las primeras, y cualquier inversión del orden produciría violaciones de integridad referencial que invalidarían el modelo. La estrategia de carga de la tabla de hechos —inserción pura (`INSERT`), actualización selectiva (`UPSERT`) o recarga completa (`TRUNCATE + INSERT`)— no es una decisión técnica arbitraria, sino una elección conceptual determinada por la naturaleza histórica o revisable de los datos de encuesta y por los requisitos de auditoría del proceso.

La validación post-carga (*post-load validation*) cierra el ciclo de aseguramiento de calidad del ETL al reconciliar los conteos y sumas de control entre el *staging* y el datamart cargado, verificando que ningún registro fue perdido ni duplicado durante el proceso. La gestión orquestada del pipeline —mediante herramientas como Apache Airflow, dbt o SSIS— no es un detalle de implementación, sino la garantía conceptual de que el orden de las etapas, las dependencias entre pasos y los mecanismos de reintento ante fallos están formalmente definidos y son reproducibles, condición necesaria para la auditabilidad del proceso en su conjunto.

---

## Dimensiones Temáticas del Bienestar Habitacional

Las dimensiones temáticas del datamart corresponden a los dominios conceptuales del bienestar habitacional reconocidos en la literatura especializada. La habitabilidad considera calidad estructural, seguridad de tenencia, espacio suficiente y asequibilidad (Naciones Unidas, 2021), con el hacinamiento y el déficit cualitativo de vivienda como indicadores de vulnerabilidad asociados a riesgos sanitarios documentados, entre ellos enfermedades respiratorias, estrés y exposición a condiciones ambientales precarias (Lorentzen et al., 2022; World Health Organization, 2018; Villanueva-Paredes & Villanueva-Paredes, 2023). La conectividad digital se incorpora como dimensión de desigualdad estructural, dado que el acceso diferenciado a internet y a equipos computacionales tiene efectos probados sobre la inclusión educativa y económica de los hogares (Flores-Cueto et al., 2020; INEI, 2025d). El gasto del hogar, por su parte, añade la capa económica que permite evaluar la carga financiera que implica para los hogares mantener condiciones adecuadas de vivienda y servicios (Deaton, 1997; Galarza et al., 2022).

La integración de estas dimensiones en un único modelo dimensional, soportada por un flujo ETL con subprocesos conceptualmente fundamentados y auditables en cada etapa, es lo que distingue a este datamart de una simple consolidación de tablas. El resultado es una infraestructura de datos que no solo almacena información, sino que garantiza su consistencia, trazabilidad y pertinencia para el análisis multidimensional del bienestar habitacional en todo el territorio peruano.

---

## Referencias

Alkire, S., & Foster, J. (2007, revisado en 2008). *Counting and multidimensional poverty measurement* (OPHI Working Paper No. 7). Oxford Poverty and Human Development Initiative. https://ophi.org.uk/sites/default/files/ophi-wp7_vs2.pdf

Clausen, J., Barrantes, N., Trivelli, C., & Salas, F. (2025). Evaluating poverty in all its forms and dimensions: Monetary, multidimensional, and subjective poverty in Peru. *Social Indicators Research, 179*, 861–893. https://doi.org/10.1007/s11205-025-03641-7

Deaton, A. (1997). *The analysis of household surveys: A microeconometric approach to development policy*. Johns Hopkins University Press.

Feres, J. C., & Mancero, X. (2001). *El método de las necesidades básicas insatisfechas y sus aplicaciones en América Latina*. Comisión Económica para América Latina y el Caribe.

Flores-Cueto, J. J., Hernández, R. M., & Garay-Argandoña, R. (2020). Tecnologías de información: Acceso a internet y brecha digital en Perú. *Revista Venezolana de Gerencia, 25*(90), 504–527.

Galarza, F. B., Carbajal, M., & Aguirre, J. (2022). *Willingness to pay for improved water service: Evidence from urban Peru*. Peruvian Economic Association.

Instituto Nacional de Estadística e Informática. (2025a). *Encuesta Nacional de Hogares 2024: Diccionario de datos*. https://www.inei.gob.pe/microdatos/

Instituto Nacional de Estadística e Informática. (2025d). *Perú: Tecnologías de información y comunicación en los hogares, II trimestre 2025*. https://www.inei.gob.pe/biblioteca-virtual/boletines/tecnologias-de-la-informacion-y-comunicacion/

Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3.ª ed.). John Wiley & Sons.

Lorentzen, J. C., Johanson, G., Björk, F., & Stensson, S. (2022). Overcrowding and hazardous dwelling condition characteristics. *International Journal of Environmental Research and Public Health, 19*(23), 15542. https://doi.org/10.3390/ijerph192315542

Moody, D. L., & Kortink, M. A. R. (2000). From enterprise models to dimensional models: A methodology for data warehouse and data mart design. En M. Jeusfeld, H. Shu, M. Staudt & G. Vossen (Eds.), *Proceedings of the 2nd International Workshop on Design and Management of Data Warehouses (DMDW'2000)* (pp. 5-1–5-12). CEUR Workshop Proceedings. https://ceur-ws.org/Vol-28/paper5.pdf

Naciones Unidas. (2021). *Metadata for Sustainable Development Goal indicator 11.1.1*. United Nations Statistics Division. https://unstats.un.org/sdgs/metadata/?Text=&Goal=11&Target=11.1

Rahm, E., & Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.

Villanueva-Paredes, K. S., & Villanueva-Paredes, G. X. (2023). Policies and mechanisms of public financing for social housing in Peru. *Sustainability, 15*(11), 8919. https://doi.org/10.3390/su15118919

World Health Organization. (2018). *WHO housing and health guidelines*. World Health Organization. https://www.who.int/publications/i/item/9789241550376

# ERD Datamart ENAHO 2025

```mermaid
erDiagram
    DIM_AGUA ||--o{ FACT_HOGAR_BIENESTAR : agua_key
    DIM_CONECTIVIDAD ||--o{ FACT_HOGAR_BIENESTAR : conectividad_key
    DIM_ENERGIA ||--o{ FACT_HOGAR_BIENESTAR : energia_key
    DIM_GEOGRAFIA ||--o{ FACT_HOGAR_BIENESTAR : geografia_key
    DIM_HABITABILIDAD ||--o{ FACT_HOGAR_BIENESTAR : habitabilidad_key
    DIM_MATERIALES_VIVIENDA ||--o{ FACT_HOGAR_BIENESTAR : materiales_vivienda_key
    DIM_SANEAMIENTO ||--o{ FACT_HOGAR_BIENESTAR : saneamiento_key
    DIM_TENENCIA_PROPIEDAD ||--o{ FACT_HOGAR_BIENESTAR : tenencia_propiedad_key
    DIM_TIEMPO ||--o{ FACT_HOGAR_BIENESTAR : tiempo_key
    DIM_VIVIENDA ||--o{ FACT_HOGAR_BIENESTAR : vivienda_key
```
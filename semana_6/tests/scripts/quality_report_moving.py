
def generate_domain_specific_report():
    """Generar reporte específico para Moving (Mudanzas)"""
    report = {
        "dominio": "Moving (Mudanzas)",
        "metricas": {
            "Cobertura validaciones de traslados": ">= 90%",
            "Tests de seguridad de accesos": "100%",
            "Validación de rutas críticas de negocio": ">= 85%",
            "Cobertura en integridad de datos": ">= 80%"
        },
        "rutas_criticas": [
            "POST /moving_traslados/ -> Crear traslado",
            "PUT /moving_traslados/{id} -> Actualizar traslado",
            "DELETE /moving_traslados/{id} -> Cancelar traslado",
            "GET /moving_traslados/{id} -> Consultar estado del traslado"
        ],
        "roles_clave": [
            "Cliente: Solicita y consulta traslados",
            "Operario: Gestiona embalaje y carga",
            "Conductor: Ejecuta el traslado",
            "Supervisor: Valida asignaciones",
            "Administrador: Control total del sistema"
        ]
    }
    return report

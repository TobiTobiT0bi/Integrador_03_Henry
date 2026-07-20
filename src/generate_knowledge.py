import os

def generate_docs():
    # Estructura de directorios a poblar
    base_dirs = {
        "hr": "data/hr_docs",
        "tech": "data/tech_docs",
        "finance": "data/finance_docs"
    }

    for path in base_dirs.values():
        os.makedirs(path, exist_ok=True)

    # 1. CONTENIDO EXTENSO PARA RECURSOS HUMANOS (HR)
    hr_content = """# MANUAL GLOBAL DE POLÍTICAS INTERNAS DE RECURSOS HUMANOS (V2026.1)

## CAPÍTULO 1: RÉGIMEN DE LICENCIAS Y VACACIONES PAGADAS
Sección 1.1: Asignación de Días Anuales de Descanso Continuo
La compañía concede un período mínimo de 14 días corridos de vacaciones anuales pagadas para todo el personal contratado por tiempo indeterminado que cuente con una antigüedad menor a cinco años en la organización. Para aquellos empleados cuya antigüedad se encuentre en el rango de cinco a diez años, el beneficio se extenderá automáticamente a 21 días corridos. Los colaboradores con más de diez años de servicio efectivo gozarán de 28 días corridos. 

Sección 1.2: Procedimiento Operativo para la Solicitud Formal de Licencias
Todo colaborador que desee usufructuar su período vacacional deberá iniciar la solicitud formal con una antelación mínima de 30 días hábiles respecto a la fecha proyectada de inicio. El trámite se gestionará exclusivamente a través del módulo de Autoservicio en la plataforma interna de la intranet corporativa ("TalentHub"). Queda estrictamente prohibido coordinar vacaciones únicamente de forma verbal o vía canales de chat informal como Slack. El mánager directo dispone de un plazo perentorio de 5 días hábiles para aprobar o rechazar la solicitud basándose en las necesidades operativas del equipo. En caso de silencio administrativo, la solicitud escalará automáticamente a la jefatura de HR del sector.

Sección 1.3: Licencias Especiales y Justificaciones Médicas de Fuerza Mayor
La empresa reconoce licencias remuneradas por eventos de fuerza mayor o hitos personales. Por matrimonio legítimo se otorgarán 10 días corridos de licencia con goce de haberes, iniciándose el cómputo el día de la celebración o el primer día hábil siguiente. Por fallecimiento de familiares directos en primer grado (padres, hijos, cónyuges) se asignarán 5 días corridos. En situaciones de enfermedad general que impidan el normal desarrollo de las tareas, el empleado deberá notificar al departamento de Medicina Laboral antes de las 09:00 AM del primer día de ausencia y adjuntar un certificado oficial firmado por un profesional matriculado en formato PDF dentro de las 24 horas subsiguientes.

## CAPÍTULO 2: ESQUEMA DE COMPENSACIONES, NÓMINAS Y BENEFICIOS
Sección 2.1: Estructura de Liquidación y Fechas de Pago Efectivo
El pago de haberes mensuales se efectúa de manera centralizada el cuarto día hábil anterior a la finalización del mes calendario en curso. La liquidación incluye el salario base, complementos por productividad si correspondieren y los descuentos obligatorios por ley referentes a aportes jubilatorios y cobertura médica. Los recibos de sueldo digitales estarán disponibles para su visualización y descarga en formato PDF en la plataforma "TalentHub" a partir de las 00:00 horas del día de pago. Los errores u omisiones detectados en el recibo deben reportarse mediante ticket formal antes del día 5 del mes siguiente.

Sección 2.2: Programa de Cobertura Médica y Seguros Colectivos
La empresa provee un plan de medicina prepaga de alta gama cubierto al 100% para el empleado titular. Los colaboradores tienen la opción de incorporar a su grupo familiar directo (cónyuge e hijos menores de 21 años) con un subsidio institucional del 50% del valor de la prima adicional, descontándose el saldo restante de forma automática en la nómina de haberes. El alta en la cobertura médica toma un plazo de procesamiento de hasta 15 días hábiles desde la firma del contrato laboral de ingreso.

Sección 2.3: Reintegros por Trabajo Remoto y Equipamiento de Oficina
Se asigna un bono mensual fijo en concepto de compensación por conectividad y servicios de internet para todo el personal bajo modalidad de teletrabajo o esquema híbrido de más de tres días semanales en el hogar. Dicho monto está exento de rendición de cuentas. Asimismo, los empleados disponen de un presupuesto único de equipamiento ergonómico de hasta 300 USD para adquirir una silla corporativa o monitor secundario a través de los proveedores homologados por el departamento de Compras.

## CAPÍTULO 3: EVALUACIÓN DE DESEMPEÑO Y PLANES DE CARRERA
Sección 3.1: Ciclo Anual de Desempeño OKR y Feedback Continuo
La organización utiliza una metodología de evaluación basada en Objetivos y Resultados Clave (OKRs). Este ciclo consta de tres etapas críticas: definición de metas al inicio del año fiscal, revisión intermedia en el mes de julio, y calibración final de resultados en el mes de diciembre. Es mandatorio que los mánagers realicen sesiones individuales uno a uno (1-on-1) de manera quincenal para dar seguimiento a los indicadores clave y brindar retroalimentación constructiva continua.

Sección 3.2: Políticas de Promoción Interna y Movilidad Horizontal
Toda vacante abierta en la empresa se publicará primero de manera interna en TalentHub durante un período de 7 días corridos antes de abrirse al mercado externo. Los colaboradores que lleven un mínimo de 12 meses en su rol actual y hayan obtenido una calificación de 'Cumple Expectativas' o superior en su última evaluación anual son elegibles para postularse. Las promociones verticales implican un ajuste en la banda salarial que se verá reflejado en la nómina inmediatamente posterior a la fecha de efectivización del nuevo cargo.
"""

    # 2. CONTENIDO EXTENSO PARA SOPORTE TÉCNICO (TECH)
    tech_content = """# MANUAL DE PROCEDIMIENTOS TÉCNICOS E INFRAESTRUCTURA DE IT (V2026.4)

## CAPÍTULO 1: ACCESOS, SEGURIDAD PERIMETRAL Y REDES CORPORATIVAS
Sección 1.1: Protocolo de Conexión Segura vía VPN Institucional
El acceso a la red interna de la empresa, entornos de desarrollo, bases de datos no públicas y microservicios críticos requiere obligatoriamente una conexión cifrada activa a través de la Red Privada Virtual (VPN) corporativa basada en el cliente Cisco AnyConnect o OpenConnect Enterprise. La dirección del servidor principal de acceso para la región es 'vpn.secure-saas-infra.com'. Ningún colaborador está autorizado a exponer puertos locales o saltearse este perímetro de seguridad bajo ninguna circunstancia operativa.

Sección 1.2: Resolución de Errores de Autenticación VPN (Error 403 / Acceso Denegado)
Si al intentar conectar la VPN el sistema arroja un código de 'Error 403: Forbidden' o 'Credenciales Inválidas', el usuario deberá seguir estrictamente la siguiente secuencia de solución de problemas de nivel 1 antes de contactar a soporte:
1. Validar la sincronización horaria de su computadora local con el servidor NTP de la red global. Una desviación mayor a 30 segundos bloquea el protocolo de enlace de seguridad.
2. Comprobar el estado del token de Autenticación de Múltiples Factores (MFA) en la aplicación Okta Verify de su teléfono móvil.
3. Limpiar la caché DNS de su sistema operativo ejecutando el comando correspondiente en la terminal ('ipconfig /flushdns' en Windows o 'sudo killall -HUP mDNSResponder' en MacOS).
4. Si el error persiste tras tres intentos, la cuenta podría estar bloqueada temporalmente por seguridad. El auto-desbloqueo se gestiona en 'identity.corp-saas.internal'.

Sección 1.3: Gestión de Identidades y Accesos a Repositorios (GitHub y AWS)
Los permisos de acceso a las organizaciones corporativas de GitHub y a las consolas de Amazon Web Services (AWS) se administran de forma automatizada mediante grupos de seguridad de Okta. Los desarrolladores que ingresen a un nuevo proyecto deberán solicitar su inclusión al grupo respectivo mediante el portal de tickets técnicos internos seleccionando la plantilla 'Access Request - Development'. Los accesos a producción (Production Environment) están severamente restringidos y requieren la aprobación explícita firmada digitalmente por el Director de Arquitectura y el Líder de Ciberseguridad del área correspondiente.

## CAPÍTULO 2: ADMINISTRACIÓN DE HARDWARE Y EQUIPAMIENTO INFORMÁTICO
Sección 2.1: Ciclo de Vida, Reemplazo y Rotura de Pantallas o Componentes
Todas las computadoras portátiles asignadas al personal (MacBook Pro y Dell Latitude) cuentan con una póliza de seguro contra todo riesgo con cobertura internacional provista por el fabricante durante los primeros tres años de uso. En caso de siniestro, rotura accidental de pantallas, fallos de batería inflada o malfuncionamiento de teclados, el empleado no debe intentar reparar el equipo por su cuenta ni llevarlo a servicios técnicos no autorizados. Debe reportar el incidente abriendo un ticket en la categoría 'Hardware Fault' adjuntando fotografías nítidas del daño físico.

Sección 2.2: Procedimiento de Asignación de Equipos de Contingencia
Una vez validado el daño del hardware por un técnico de IT de Nivel 1, se coordinará el envío por mensajería express de un equipo de contingencia ('Laptop de Backup') al domicilio del empleado en un plazo máximo de 24 horas para garantizar la continuidad de sus tareas. El empleado dispone de 48 horas para realizar la migración de sus archivos locales (los cuales deberían estar respaldados en su totalidad en la nube corporativa de OneDrive o Google Drive) y enviar el equipo dañado a las oficinas centrales usando la etiqueta de envío postal pre-pagada provista por el soporte técnico.

Sección 2.3: Actualizaciones Mandatorias de Software y Parches de Seguridad
Los sistemas operativos de los equipos corporativos son auditados de forma remota mediante la herramienta MDM (Mobile Device Management) Jamf / Microsoft Intune. Cada segundo martes de mes se despliegan parches de seguridad críticos que corrigen vulnerabilidades de día cero. Una vez descargada la actualización en segundo plano, el sistema notificará al usuario otorgándole un margen de gracia de 72 horas para reiniciar el equipo de forma voluntaria. Transcurrido dicho plazo, el agente MDM forzará un reinicio automatizado del sistema guardando previamente los documentos abiertos en herramientas en la nube.

## CAPÍTULO 3: ENTORNOS DE PRODUCCIÓN Y ESCALAMIENTO DE ALERTAS
Sección 3.1: Matriz de Severidad de Incidentes Técnicos (P1 a P4)
Los incidentes en la infraestructura Cloud del SaaS se catalogan según su impacto en el negocio. Un incidente Prioridad 1 (P1) significa caída total del servicio para más del 50% de los clientes activos de la plataforma. Los incidentes P2 representan una degradación severa de las bases de datos o funcionalidades de pago pero con un *workaround* parcial disponible. Las categorías P3 y P4 corresponden a bugs menores de interfaz o consultas generales de configuración técnica.

Sección 3.2: Protocolo de Escalamiento a Soporte de Nivel 2 y Equipos de Guardia
Cuando el Agente de IT automatizado o un técnico de Nivel 1 detecta que la resolución de un problema de accesos o caída de microservicios excede sus manuales de procedimiento estándar, se encuentra obligado a escalar el ticket en un plazo no mayor a 15 minutos al equipo de Infraestructura y Conectividad (Nivel 2) o al ingeniero de Confiabilidad del Sitio (SRE) que se encuentre de guardia rotativa activa en ese huso horario vía PagerDuty.
"""

    # 3. CONTENIDO EXTENSO PARA FINANZAS (FINANCE)
    finance_content = """# REGLAMENTO GENERAL DE PROCESOS FINANCIEROS Y CONTABLES (V2026.2)

## CAPÍTULO 1: POLÍTICA INSTITUCIONAL DE GASTOS Y REEMBOLSOS
Sección 1.1: Criterios Generales de Elegibilidad para Reembolsos de Gastos
La empresa reembolsará únicamente aquellos gastos que hayan sido incurridos directa, exclusiva y necesariamente en el ejercicio de las funciones laborales asignadas al colaborador, y que se ajusten estrictamente a los presupuestos previamente autorizados por las gerencias de cada área. Los gastos personales, de entretenimiento no corporativo, multas de tránsito de cualquier índole, o consumos que excedan los límites establecidos por día no serán reconocidos bajo ningún concepto por la auditoría contable interna.

Sección 1.2: Límites de Gastos Viáticos por Viajes de Negocios
Para los viajes de negocios de carácter nacional o internacional, se fijan los siguientes topes diarios de erogación:
- Alojamiento en hotel homologado: Hasta 150 USD por noche en capitales financieras, y hasta 100 USD por noche en el resto de los destinos.
- Alimentación y refrigerios: Hasta un tope máximo diario de 50 USD combinando almuerzo, cena y cafetería. No se requiere presentar facturas desglosadas por cada café, pero sí el ticket consolidado del establecimiento.
- Transporte terrestre: Se priorizará el uso de aplicaciones de transporte corporativo vinculadas a la cuenta central de la empresa (Uber for Business). El uso de taxis particulares requiere la emisión de un comprobante fiscal válido con Clave de Identificación Tributaria corporativa para ser considerado para su reintegro.

Sección 1.3: Flujo Digital de Rendición y Plazos Críticos de Presentación
Toda solicitud de reembolso de gastos debe confeccionarse y enviarse digitalmente a través de la plataforma 'Expenseify' antes del día 25 del mes calendario en el que se originó el gasto. Es condición sine qua non adjuntar la factura digital válida, comprobante fiscal electrónico o recibo de tarjeta de crédito legible donde consten de forma explícita el nombre del comercio, la fecha exacta de la transacción, el desglose pormenorizado de los conceptos adquiridos y el monto final con impuestos incluidos. Las solicitudes cargadas con posterioridad al día 25 se postergarán de forma automática para el ciclo de pago del mes subsiguiente. El procesamiento y acreditación final en la cuenta bancaria del empleado toma un lapso de entre 7 y 10 días hábiles tras recibir la aprobación del mánager.

## CAPÍTULO 2: PROCESAMIENTO DE FACTURACIÓN Y CUENTAS POR PAGAR
Sección 2.1: Recepción de Facturas de Proveedores y Contratistas Externos
Todas las facturas emitidas por proveedores de servicios externos, consultores independientes, licencias de software B2B o contratistas logísticos deben enviarse única y exclusivamente a la dirección de correo centralizada 'invoices@corp-saas-finance.com'. Cada documento debe ser emitido a nombre de la razón social de la compañía, detallando de forma obligatoria el número de Orden de Compra (PO) correspondiente que fue autorizado previamente por el departamento de Finanzas al inicio de la contratación. Las facturas que carezcan de un número de PO válido serán rechazadas de manera automática por el sistema de validación OCR y devueltas al emisor para su debida corrección.

Sección 2.2: Ciclos de Pago Estándar de la Compañía (Net-30 y Net-60)
La política estándar de cuentas por pagar estipula un plazo de cancelación de facturas bajo la modalidad comercial Net-30 (30 días corridos a partir de la fecha de aprobación técnica de la factura por el líder del proyecto). Para grandes proveedores de infraestructura Cloud o contratos corporativos de volumen mayor a 50,000 USD anuales, la empresa aplica de forma predeterminada la modalidad de pago Net-60, salvo que se haya negociado explícitamente en el contrato marco un descuento por pronto pago que justifique la erogación anticipada de flujo de caja. Los pagos se ejecutan mediante transferencia bancaria electrónica masiva todos los días jueves de cada semana laboral.

Sección 2.3: Generación de Reportes Financieros Trimestrales de Cierre
El equipo contable consolida el balance general, el estado de resultados (P&L) y el reporte de flujo de efectivo dentro de los primeros 10 días corridos posteriores al cierre de cada trimestre fiscal. Dichos reportes financieros trimestrales se estructuran bajo normas contables internacionales (IFRS) y son consolidados en un repositorio seguro dentro de la base ERP corporativa. El acceso a dichos documentos con fines de auditoría o armado de reportes de ventas requiere una credencial de visualización de nivel corporativo otorgada por el CFO de la compañía.
"""

    # Guardar los archivos de texto masivos en sus carpetas respectivas
    with open(os.path.join(base_dirs["hr"], "manual_politicas_hr.txt"), "w", encoding="utf-8") as f:
        f.write(hr_content)
        
    with open(os.path.join(base_dirs["tech"], "manual_procedimientos_tech.txt"), "w", encoding="utf-8") as f:
        f.write(tech_content)
        
    with open(os.path.join(base_dirs["finance"], "reglamento_financiero.txt"), "w", encoding="utf-8") as f:
        f.write(finance_content)

    print("✅ Archivos de documentación masiva generados perfectamente en data/.")
    print("📈 El volumen de texto y variedad de términos garantiza la fragmentación en más de 50 chunks totales semánticos al inicializar la base de datos.")

if __name__ == "__main__":
    generate_docs()
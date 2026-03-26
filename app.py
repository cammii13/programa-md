from nicegui import ui
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

from sqlalchemy import Float

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    service = Column(String)
    date = Column(Date)
    suggested_treatment = Column(String)
    suggested_price = Column(Float)
    abono = Column(Float)
    notes = Column(String)

engine = create_engine('sqlite:///cammseb_v2.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Estado Global para Sugerencias Automáticas
state = {
    'treatment': '',
    'price': 0.0
}


def add_appointment(client, service, date_str, treatment, price, abono, notes):
    if not client or not service or not date_str:
        ui.notify('Por favor, complete todos los campos.', type='warning')
        return

    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        app = Appointment(
            client_name=client, 
            service=service, 
            date=date,
            suggested_treatment=treatment,
            suggested_price=float(price or 0),
            abono=float(abono or 0),
            notes=notes
        )
        session.add(app)
        session.commit()
        update_table()
        ui.notify('🌸 Cita agregada exitosamente 🌸', type='positive')
        # Limpiar campos tras agregar
        client_input.value = ''
        service_input.value = ''
        date_input.value = ''
        treatment_input.value = ''
        price_input.value = 0
        abono_input.value = 0
        notes_input.value = ''
    except ValueError:
        ui.notify('Formato de fecha inválido o valores numéricos erróneos.', type='negative')

def update_table():
    rows = []
    for a in session.query(Appointment).all():
        price = a.suggested_price or 0
        abono = a.abono or 0
        balance = price - abono
        rows.append({
            'id': a.id, 
            'Cliente': a.client_name, 
            'Servicio': a.service, 
            'Fecha': str(a.date),
            'Tratamiento': a.suggested_treatment,
            'Precio': f'${price:.2f}',
            'Abono': f'${abono:.2f}',
            'Saldo': f'${balance:.2f}',
            'Alergias': a.notes
        })
    table.rows = rows
    table.update()

# Diagnóstico (Lógica de IA Simplificada)
diagnoses = {
    'seca': 'Hidratar profundamente con cremas y mascarillas.',
    'grasa': 'Limpiar con productos astringentes y seborreguladores.',
    'mixta': 'Balancear con tratamientos combinados y limpieza T.',
    'cabello seco': 'Nutrir intensamente con aceites y mascarillas.',
    'cabello graso': 'Lavar con shampoo específico y evitar aceites.',
    'cabello normal': 'Mantenimiento básico y protección térmica.'
}

def diagnose(skin, hair):
    if not skin and not hair:
        ui.notify('Por favor, seleccione al menos un tipo de piel o cabello.', type='warning')
        return
    
    rec = 'Recomendación 🌿: '
    if skin:
        rec += diagnoses.get(skin, 'Consulta personalizada para piel.')
    if hair:
        rec += ' ' + diagnoses.get('cabello ' + hair, 'Consulta personalizada para cabello.')
    
    # Guardar sugerencia para el formulario de citas
    state['treatment'] = rec.replace('Recomendación 🌿: ', '')
    treatment_input.value = state['treatment']
    
    ui.notify(rec, type='info', position='center')
    ui.notify('✨ Sugerencia enviada al formulario de Citas', type='positive', position='bottom')

# Calculadora de Costos (Robusta)
def calculate(cost, time, margin):
    try:
        # Usamos 0 si el campo está vacío para evitar errores
        rate_hr = 50  
        cost_float = float(cost or 0)
        time_float = float(time or 0)
        margin_float = float(margin or 0)

        # Fórmula: (Costo Insumos + Costo Tiempo) * Margen Ganancia
        price = (cost_float + (time_float * rate_hr)) * (1 + (margin_float / 100))
        
        # Guardar precio para el formulario de citas
        state['price'] = price
        price_input.value = price
        
        ui.notify(f'💰 Precio final sugerido: ${price:.2f}', type='positive', position='center')
        ui.notify('✨ Precio enviado al formulario de Citas', type='positive', position='bottom')
    except ValueError:
        ui.notify('Ingrese valores numéricos válidos.', type='negative')

# --- UI con DISEÑO MEJORADO "Elegant Pastel Cute Luxe" ---
ui.page_title('🌸 cammseb - Gestión de Estética 🌸')

# Importar Fuentes de Google
ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Quicksand:wght@400;700&display=swap" rel="stylesheet">
''')

# CSS Personalizado (Elegant Pastel Cute Luxe)
ui.add_css('''
    body {
        background: linear-gradient(135deg, #FFFDF5 0%, #FFF0F5 100%);
        font-family: 'Quicksand', sans-serif;
        color: #4A148C;
    }
    .playfair {
        font-family: 'Playfair Display', serif;
    }
    .spa-header {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(12px);
        border-bottom: 2px solid rgba(230, 230, 250, 0.5);
        color: #4A148C;
    }
    .main-tab-panel {
        background: transparent !important;
        padding-top: 20px;
    }
    .spa-card-form {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 32px;
        box-shadow: 0 15px 35px rgba(147, 112, 219, 0.15);
        padding: 40px;
        max-width: 550px;
        width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    .spa-button {
        background: linear-gradient(45deg, #DCD0FF, #E6E6FA);
        color: #4A148C !important;
        border: none;
        border-radius: 30px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(220, 208, 255, 0.4);
    }
    .spa-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(220, 208, 255, 0.6);
        background: linear-gradient(45deg, #E6E6FA, #DCD0FF);
    }
    .spa-input .q-field__inner {
        background: rgba(230, 230, 250, 0.2);
        border-radius: 12px;
    }
    .ui-tabs .q-tab {
        color: #9370DB;
        transition: all 0.3s ease;
    }
    .ui-tabs .q-tab--active {
        color: #4A148C;
        font-weight: 700;
    }
    .bubble-table {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        background: white;
    }
    .q-table__card {
        box-shadow: none;
    }
''')

# Encabezado Persistente (App Bar)
with ui.header().classes('spa-header justify-between items-center px-8 py-4'):
    with ui.row().classes('items-center gap-4'):
        ui.label('🌸').classes('text-3xl animate-bounce')
        ui.label('cammseb').classes('playfair text-3xl font-bold')
    ui.label('Centro de Estética & Cosmetología').classes('text-sm uppercase tracking-widest opacity-70 hide-on-mobile')

# Sistema de Pestañas Centrado
with ui.tabs().classes('w-full justify-center q-mt-md') as tabs:
    ui.tab('Citas', icon='event_note')
    ui.tab('Diagnóstico', icon='spa')
    ui.tab('Calculadora', icon='calculate')
    ui.tab('Visualización', icon='table_chart')

# Paneles de las pestañas
with ui.tab_panels(tabs, value='Citas').classes('main-tab-panel w-full'):
    
    # --- Pestaña: CITAS ---
    with ui.tab_panel('Citas').classes('items-center'):
        with ui.row().classes('justify-center w-full gap-8'):
            # Tarjeta de Formulario
            with ui.card().classes('spa-card-form'):
                ui.label('Agendar Cita').classes('playfair text-3xl text-center q-mb-lg font-bold')
                
                client_input = ui.input('Nombre de la Cliente').classes('w-full q-mb-md spa-input').props('rounded outlined')
                service_input = ui.input('Servicio').classes('w-full q-mb-md spa-input').props('rounded outlined')
                
                # Selector de Fecha con Calendario Visual
                with ui.input('Fecha (Seleccionar)').classes('w-full q-mb-md spa-input').props('rounded outlined') as date_input:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.date().bind_value(date_input):
                            with ui.row().classes('justify-end'):
                                ui.button('Cerrar', on_click=menu.close).props('flat')
                    with date_input.add_slot('append'):
                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')

                treatment_input = ui.input('Tratamiento Sugerido').classes('w-full q-mb-md spa-input').props('rounded outlined')
                
                with ui.row().classes('w-full gap-4 q-mb-md'):
                    price_input = ui.number('Precio ($)', format='%.2f').classes('flex-grow spa-input').props('rounded outlined')
                    abono_input = ui.number('Abono ($)', format='%.2f').classes('flex-grow spa-input').props('rounded outlined')
                
                notes_input = ui.textarea('Notas y Alergias').classes('w-full q-mb-lg spa-input').props('rounded outlined')
                
                ui.button('CONFIRMAR CITA', on_click=lambda: add_appointment(
                    client_input.value, service_input.value, date_input.value, 
                    treatment_input.value, price_input.value, abono_input.value, notes_input.value
                )).classes('spa-button w-full q-py-md text-lg')

            # Calendario Lateral (Solo visual/informativo como en el mockup)
            with ui.card().classes('spa-card-form hidden lg:block').style('max-width: 400px'):
                ui.label('Vista Mensual').classes('playfair text-2xl text-center q-mb-md font-bold')
                ui.date().classes('w-full shadow-none').props('flat color="purple-4"')

    # --- Pestaña: DIAGNÓSTICO ---
    with ui.tab_panel('Diagnóstico').classes('items-center'):
        with ui.row().classes('justify-center w-full'):
            with ui.card().classes('spa-card-form'):
                ui.label('Asistente de Diagnóstico').classes('playfair text-3xl text-center q-mb-lg font-bold')
                
                skin_select = ui.select(['seca', 'grasa', 'mixta'], label='Tipo de Piel').classes('w-full q-mb-md').props('rounded outlined')
                hair_select = ui.select(['seco', 'graso', 'normal'], label='Estado del Cabello').classes('w-full q-mb-lg').props('rounded outlined')
                
                ui.button('GENERAR RECOMENDACIÓN', on_click=lambda: diagnose(skin_select.value, hair_select.value)).classes('spa-button w-full q-py-sm')

    # --- Pestaña: CALCULADORA ---
    with ui.tab_panel('Calculadora').classes('items-center'):
        with ui.row().classes('justify-center w-full'):
            with ui.card().classes('spa-card-form'):
                ui.label('Calculadora Premium').classes('playfair text-3xl text-center q-mb-lg font-bold')
                
                cost_input = ui.number('Costo de Materiales ($)', format='%.2f').classes('w-full q-mb-md').props('rounded outlined')
                time_input = ui.number('Tiempo Estimado (horas)', format='%.1f').classes('w-full q-mb-md').props('rounded outlined')
                margin_input = ui.number('Margen Deseado (%)', format='%.0f').classes('w-full q-mb-lg').props('rounded outlined')
                
                ui.button('CALCULAR Y ENVIAR A CITA', on_click=lambda: calculate(cost_input.value, time_input.value, margin_input.value)).classes('spa-button w-full q-py-sm')

    # --- Pestaña: VISUALIZACIÓN ---
    with ui.tab_panel('Visualización'):
        ui.label('Historial de Clientas').classes('playfair text-4xl text-center text-purple-900 q-mb-lg font-bold')
        
        with ui.card().classes('bubble-table w-full q-pa-lg'):
            table = ui.table(
                columns=[
                    {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
                    {'name': 'Cliente', 'label': 'Cliente', 'field': 'Cliente', 'align': 'left'},
                    {'name': 'Servicio', 'label': 'Servicio', 'field': 'Servicio', 'align': 'left'},
                    {'name': 'Fecha', 'label': 'Fecha', 'field': 'Fecha', 'align': 'left'},
                    {'name': 'Tratamiento', 'label': 'Tratamiento', 'field': 'Tratamiento', 'align': 'left'},
                    {'name': 'Precio', 'label': 'Precio', 'field': 'Precio', 'align': 'left'},
                    {'name': 'Abono', 'label': 'Abono', 'field': 'Abono', 'align': 'left'},
                    {'name': 'Saldo', 'label': 'Saldo', 'field': 'Saldo', 'align': 'left'},
                ],
                rows=[]
            ).classes('w-full').props('flat')
            
            table.on('rowClick', lambda e: open_edit_dialog(e.args[1]))
            update_table()

# Diálogo de Edición Refinado
edit_dialog = ui.dialog()
selected_appointment_id = None

def open_edit_dialog(row):
    global selected_appointment_id
    selected_appointment_id = row['id']
    
    with edit_dialog, ui.card().classes('spa-card-form'):
        ui.label(f'Cita #{selected_appointment_id}').classes('playfair text-3xl text-purple-900 font-bold q-mb-md')
        
        edit_client = ui.input('Nombre Cliente', value=row['Cliente']).classes('w-full q-mb-sm spa-input').props('rounded outlined')
        edit_service = ui.input('Servicio', value=row['Servicio']).classes('w-full q-mb-sm spa-input').props('rounded outlined')
        
        # Selector de Fecha en Edición
        with ui.input('Fecha', value=row['Fecha']).classes('w-full q-mb-sm spa-input').props('rounded outlined') as edit_date:
            with ui.menu().props('no-parent-event') as menu:
                with ui.date().bind_value(edit_date):
                    with ui.row().classes('justify-end'):
                        ui.button('Cerrar', on_click=menu.close).props('flat')
            with edit_date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')

        edit_treatment = ui.input('Tratamiento', value=row['Tratamiento']).classes('w-full q-mb-sm spa-input').props('rounded outlined')
        
        with ui.row().classes('w-full gap-4 q-mb-sm'):
            edit_price = ui.number('Precio ($)', value=float(row['Precio'].replace('$',''))).classes('flex-grow spa-input').props('rounded outlined')
            edit_abono = ui.number('Abono ($)', value=float(row['Abono'].replace('$',''))).classes('flex-grow spa-input').props('rounded outlined')
        
        edit_notes = ui.textarea('Notas y Alergias', value=row['Alergias']).classes('w-full q-mb-md spa-input').props('rounded outlined')
        
        with ui.row().classes('w-full justify-end gap-2'):
            ui.button('CANCELAR', on_click=edit_dialog.close).props('flat').classes('text-purple-400')
            ui.button('GUARDAR', on_click=lambda: save_edit(
                edit_client.value, edit_service.value, edit_date.value,
                edit_treatment.value, edit_price.value, edit_abono.value, edit_notes.value
            )).classes('spa-button px-6')
            
    edit_dialog.open()

def save_edit(client, service, date_str, treatment, price, abono, notes):
    try:
        app = session.query(Appointment).filter(Appointment.id == selected_appointment_id).first()
        if app:
            app.client_name = client
            app.service = service
            app.date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            app.suggested_treatment = treatment
            app.suggested_price = float(price)
            app.abono = float(abono)
            app.notes = notes
            session.commit()
            update_table()
            edit_dialog.close()
            ui.notify('Cita actualizada ✅', type='positive')
    except Exception as e:
        ui.notify(f'Error al guardar: {e}', type='negative')

# Ejecutar la aplicación
ui.run()
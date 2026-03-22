from nicegui import ui
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    service = Column(String)
    date = Column(Date)

engine = create_engine('sqlite:///cammseb.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Funciones
def add_appointment(client, service, date_str):
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        app = Appointment(client_name=client, service=service, date=date)
        session.add(app)
        session.commit()
        update_table()
        ui.notify('Cita agregada exitosamente', type='positive')
    except ValueError:
        ui.notify('Formato de fecha inválido. Use YYYY-MM-DD', type='negative')

def update_table():
    rows = [{'ID': a.id, 'Cliente': a.client_name, 'Servicio': a.service, 'Fecha': str(a.date)} for a in session.query(Appointment).all()]
    table.rows = rows
    table.update()

# Diagnóstico
diagnoses = {
    'seca': 'Hidratar con cremas y mascarillas.',
    'grasa': 'Limpiar con productos astringentes.',
    'mixta': 'Balancear con tratamientos combinados.',
    'cabello seco': 'Nutrir con aceites.',
    'cabello graso': 'Lavar frecuentemente.',
    'cabello normal': 'Mantenimiento básico.'
}

def diagnose(skin, hair):
    rec = 'Recomendación: '
    if skin:
        rec += diagnoses.get(skin, 'Consulta personalizada para piel.')
    if hair:
        rec += ' ' + diagnoses.get('cabello ' + hair, 'Consulta personalizada para cabello.')
    ui.notify(rec, type='info')

# Calculadora
def calculate(cost, time, margin):
    try:
        rate = 50  # tarifa por hora
        price = float(cost) + float(time) * rate * (1 + float(margin) / 100)
        ui.notify(f'Precio final: ${price:.2f}', type='positive')
    except ValueError:
        ui.notify('Ingrese valores numéricos válidos', type='negative')

# UI con diseño mejorado
ui.page_title('cammseb - Gestión de Estética')
ui.add_css('''
    body {
        background: linear-gradient(135deg, #e1bee7, #f3e5f5);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .spa-header {
        text-align: center;
        color: #4a148c;
        margin-bottom: 20px;
    }
    .spa-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        padding: 20px;
        margin: 10px;
    }
    .spa-button {
        background: linear-gradient(45deg, #ab47bc, #ba68c8);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .spa-button:hover {
        transform: scale(1.05);
    }
''')

with ui.column().classes('spa-header'):
    ui.label('🌸 cammseb 🌸').classes('text-h3')
    ui.label('Centro de Estética y Cosmetología').classes('text-h5')

with ui.tabs() as tabs:
    ui.tab('Citas', icon='event_note')
    ui.tab('Diagnóstico', icon='spa')
    ui.tab('Calculadora', icon='calculate')
    ui.tab('Visualización', icon='table_chart')

with ui.tab_panels(tabs, value='Citas'):
    with ui.tab_panel('Citas'):
        ui.label('Gestión de Citas').classes('text-h4 text-center')
        with ui.card().classes('spa-card'):
            client_input = ui.input('Nombre de la Cliente', placeholder='Ingrese nombre').classes('w-full')
            service_input = ui.input('Servicio', placeholder='Ingrese servicio').classes('w-full')
            date_input = ui.input('Fecha (YYYY-MM-DD)', placeholder='2026-03-21').classes('w-full')
            ui.button('Agregar Cita', on_click=lambda: add_appointment(client_input.value, service_input.value, date_input.value)).classes('spa-button w-full')

    with ui.tab_panel('Diagnóstico'):
        ui.label('Asistente de Diagnóstico').classes('text-h4 text-center')
        with ui.card().classes('spa-card'):
            skin_select = ui.select(['seca', 'grasa', 'mixta'], label='Tipo de Piel').classes('w-full')
            hair_select = ui.select(['seco', 'graso', 'normal'], label='Estado del Cabello').classes('w-full')
            ui.button('Obtener Recomendación', on_click=lambda: diagnose(skin_select.value, hair_select.value)).classes('spa-button w-full')

    with ui.tab_panel('Calculadora'):
        ui.label('Calculadora de Costos e Insumos').classes('text-h4 text-center')
        with ui.card().classes('spa-card'):
            cost_input = ui.number('Costo de Materiales ($)', min=0).classes('w-full')
            time_input = ui.number('Tiempo Invertido (horas)', min=0).classes('w-full')
            margin_input = ui.number('Margen de Ganancia (%)', min=0).classes('w-full')
            ui.button('Calcular Precio Final', on_click=lambda: calculate(cost_input.value, time_input.value, margin_input.value)).classes('spa-button w-full')

    with ui.tab_panel('Visualización'):
        ui.label('Registros de Citas').classes('text-h4 text-center')
        with ui.card().classes('spa-card'):
            table = ui.table(
                columns=[
                    {'name': 'ID', 'label': 'ID', 'field': 'ID'},
                    {'name': 'Cliente', 'label': 'Cliente', 'field': 'Cliente'},
                    {'name': 'Servicio', 'label': 'Servicio', 'field': 'Servicio'},
                    {'name': 'Fecha', 'label': 'Fecha', 'field': 'Fecha'}
                ],
                rows=[]
            ).classes('w-full')
            update_table()

ui.run()
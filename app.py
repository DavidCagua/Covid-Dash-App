import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import pathlib



PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
data = pd.read_excel(DATA_PATH.joinpath("Datos_Comorbilidades1.xlsx"), header=0, index_col=0)



options=[{'label':'Colombia','value':'Colombia'}]
cities=data.Ciudad.unique()
cities.sort()
encoding: utf-8
for city in cities:
    dic={'label':city,'value':city}
    options.append(dic)


data_enf=data.rename(columns={'Cancer': 'Cancer', 'Hta': 'Hipertension','Cardiopatia':'Cardiopatia','Ecv':'Cerebrovascular','Hipotiroidismo':'Tiroides','Epoc':'PulmonarObstructiva','EnfermedadRenal':'Renal','Vih':'VIH','ExpHumoDeLenia':'ExposicionLena','EnEstudio':'En Estudio','OxigenoRequirente':'OxigenoRequirente','HtPulmonar':'Pulmonar','Cistostomia':'Cistostomia','Neumonia':'Neumonia','Depresion':'Depresion','Civ':'Cardiopatia','Desnutricion':'Desnutricion','CirrosisHepatica':'CirrosisHepatica','Sifilis':'Sifilis','FibrosisPulmonar':'Pulmonar','EnfermedadPulmonar':'Pulmonar','Ehi':'Encefalopatia','Hepatopatia':'Hepatopatia','Ela':'Esclerosis','Polineuropatia':'Neuropatia','Pti':'Purpura','Cch':'Cistoadenoma','Hbp':'Hiperplasia','Pad':'EnfermedadArterial','EnfermedadAutoinmune':'Autoinmune','Fq':'FibrosisQuistica','Eh':'Huntington','Trm':'TraumaRaquimedular','Tce':'TraumaCraneoencefalico','Gf':'Gangrena','Sii':'IntestinoIrritable','Migrania':'Migrana','Sahs':'ApneaDelSueno','Eu':'Encefalopatia','Smd':'SindromeMielodisplasico','Mg':'MiasteniaGravis'})
data_enf=list(data_enf.iloc[0, 10:135].index)

enf_options=[]
for enf in data_enf:
    dic={'label':enf,'value':enf}
    enf_options.append(dic)


app = dash.Dash(__name__,suppress_callback_exceptions=True)

navbar=dbc.NavbarBrand(
    id='my_navbar',
    children=[
        html.H1(
            'Muertes por Covid-19 en Colombia',
            style={'font-size':'3vw','color':'#002C5C'}
        ),
        html.P([
            'La información fue obtenida del Instituto Nacional de Salud, desde el 03 de Abril hasta el 14 de Julio del 2020',
        ],
        style={'border-left':'6px solid #00D1D6','padding-left':'5px','font-size':'1.3vw','color':'#002C5C'}
        )
    ],
    style={'width':'100%','margin':'0','padding-left':'5%','padding-right':'5%','padding-top':'2%','padding-bottom':'1%','vertical-align':'middle','background-color':'white'}
)


body= dbc.Container([
    dbc.Tabs(
    [
        dbc.Tab(tab_id='tab1_content', label="INFORMACIÓN POR CIUDAD", label_style={'font-weight': 'bold'}),
        dbc.Tab(tab_id='tab2_content', label="COMPARACIÓN ENTRE CIUDADES", label_style={'font-weight': 'bold'}),
        dbc.Tab(tab_id='tab3_content', label="ENFERMEDADES", label_style={'font-weight': 'bold'}),
    ],
    id='tabs',
    active_tab='tab1_content',
    style={'padding-left':'5%'}
    ),
    html.Div(id='tab-content')
],
style={}
)



app.layout = html.Div([navbar, body])


@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'active_tab')]
)
def render_tab_content(active_tab):
    if active_tab == 'tab1_content':
        return dbc.Container([
            html.H5(
            'Seleccionar ciudad y meses para la visualización',
            style={'padding-left':'5%','padding-top':'3%','padding-right':'5%','color':'#002C5C'}
            ),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        dcc.Dropdown(
                            id='cities_dropdown',
                            options=options,
                            value='Colombia',
                            multi=False,
                            clearable=False,
                            style={'width':'100%','margin':'0.5rem'}
                        )
                    )
                ],
                width=3
                ),
                dbc.Col([
                    html.Div(
                        dcc.RangeSlider(
                            id='range_slider',
                            step=None,
                            value=[4,7]
                        ),
                        style={'margin':'0.5rem','padding-left':'5%'},
                    )
                ],
                width=3
                ),
                dbc.Col([
                    html.Div(
                        id='date_displayed',
                        style={'margin':'0.5rem','padding-left':'5%'}
                    )
                ],
                width=6
                )
        
            ],
            style={'border-radius':'5px','background-color':'#F0F0F0','margin':'0.5rem','padding-left':'5%','padding-right':'5%','position':'relative'}
            ),
            dbc.Row([
                dbc.Col([
                    html.H6(
                        'Distribución por Sexo',
                        style={'padding-left':'5%','color':'#002C5C'}
                    ),
                    html.Div(
                        dcc.Graph(id='sex_graph',config={'displayModeBar': False}),
                        style={'border-radius':'5px','background-color':'white','margin':'0.3rem','padding':'0','position':'relative','border':'1px solid #f1f1f1'},
                    )
                ],
                width=12,md=3
                ),
                dbc.Col([
                    html.H6(
                        'Distribución por edad',
                        style={'padding-left':'5%','color':'#002C5C'}
                    ),
                    html.Div(
                        dcc.Graph(id='age_graph',config={'displayModeBar': False}),
                        style={'border-radius':'5px','background-color':'white','margin':'0.3rem','padding':'0','position':'relative','border':'1px solid #f1f1f1'}
                    )
                ],
                width=12,md=4
                ),
                dbc.Col([
                    html.H6(
                        'Días entre inicio de síntomas y muerte',
                        style={'padding-left':'5%','color':'#002C5C'}
                    ),
                    html.Div(
                        dcc.Graph(id='days_graph',config={'displayModeBar': False}),
                        style={'border-radius':'5px','background-color':'white','margin':'0.3rem','padding':'0','position':'relative','border':'1px solid #f1f1f1'}
                    )
                ],
                width=12,md=5
                )
        
            ],
            no_gutters=True,
            style={'padding-top':'3%','padding-left':'5%','padding-right':'5%'}
            ),
            dbc.Row([
                html.H5(
                    'Top de comorbilidades',
                    style={'padding-left':'3%','color':'#002C5C'}
                ),
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id='age_dropdown',
                            value='Todas las edades',
                            multi=False,
                            clearable=False,
                            style={'width':'50%','margin-top':'3%','margin-left':'auto','margin-right':'auto'}
                        ),
                        dcc.Graph(id='top20_graph',config={'displayModeBar': False}),
                    ],
                    style={'border-radius':'5px','background-color':'white','margin':'0.3rem','padding':'0','position':'relative','border':'1px solid #f1f1f1'}),
                    width=12
                ),
            ],
            style={'padding-top':'3%','padding-left':'5%','padding-right':'5%','padding-bottom':'5%'}
            )
        ],
        style={'height': '100%','width':'100%','background-color':'#F0F0F0'}
        )

    elif active_tab == 'tab2_content':
        return dbc.Container([
            dbc.Row([
                html.H5(
                    'Top de comorbilidades',
                    style={'padding-left':'3%','padding-top':'0','color':'#002C5C'}
                ),
                dbc.Col(
                    html.Div([
                        html.Div(
                            dcc.Dropdown(
                                id='cities1_dropdown',
                                options=options,
                                value='Colombia',
                                multi=False,
                                clearable=False,
                                style={'width':'70%','margin':'auto'}
                            ),
                            style={'display':'inline-block','width':'50%','margin-top':'3%','margin-left':'auto','margin-right':'auto'}
                        ),
                        html.Div(
                            dcc.Dropdown(
                                id='cities2_dropdown',
                                value='Bogotá D.C.',
                                multi=False,
                                clearable=False,
                                style={'width':'70%','margin':'auto'}
                            ),
                            style={'display':'inline-block','width':'50%','margin-top':'3%','margin-left':'auto','margin-right':'auto'}
                        ),
                        html.Div(
                            dcc.Graph(id='top20_2cities_graph',config={'displayModeBar': False}),
                            style={}
                        )
                    ],
                    style={'border-radius':'5px','background-color':'white','margin':'0.3rem','padding':'0','position':'relative','border':'1px solid #f1f1f1'}),
                    width=12
                )
            ],
            style={'padding-top':'3%','padding-left':'5%','padding-right':'5%','padding-bottom':'5%'}
            )
        ],
        style={'height': '100%','width':'100%','background-color':'#F0F0F0'}
        )

    elif active_tab == 'tab3_content':
        return dbc.Container([
            dbc.Row([
                html.H5(
                    'Número de fallecidos por enfermedad',
                    style={'padding-left':'3%','padding-top':'0','color':'#002C5C'}
                ),
                dbc.Col(
                    html.Div([
                        html.Div(
                            dcc.Dropdown(
                                id='enf1_dropdown',
                                options=enf_options,
                                value='Diabetes',
                                multi=False,
                                clearable=False,
                                style={'width':'70%','margin':'auto'}
                            ),
                            style={'display':'inline-block','width':'33%','margin-top':'3%','margin-left':'auto','margin-right':'auto'}
                        ),
                        html.Div(
                            dcc.Dropdown(
                                id='enf2_dropdown',
                                value='Hipertensión',
                                multi=False,
                                clearable=False,
                                style={'width':'70%','margin':'auto'}
                            ),
                            style={'display':'inline-block','width':'33%','margin-top':'3%','margin-left':'auto','margin-right':'auto'}
                        ),
                        html.Div(
                            dcc.Dropdown(
                                id='enf3_dropdown',
                                value='Obesidad',
                                multi=False,
                                clearable=False,
                                style={'width':'70%','margin':'auto'}
                            ),
                            style={'display':'inline-block','width':'33%','margin-top':'3%','margin-left':'auto','margin-right':'auto'}
                        ),
                        html.Div(
                            dcc.Graph(id='enf_graph',config={'displayModeBar': False},style={'width':'50%','margin-left':'25%'})
                        )
                    ],
                    style={'border-radius':'5px','background-color':'white','margin':'0.5rem','padding':'1rem','position':'relative','border':'1px solid #f1f1f1'}),
                    width=12
                )
            ],
            style={'padding-top':'3%','padding-left':'5%','padding-right':'5%','padding-bottom':'5%'}
            )
        ],
        style={'height': '100%','width':'100%','background-color':'#F0F0F0'}
        )


@app.callback(
    Output(component_id='range_slider',component_property='value'),
    [Input(component_id='cities_dropdown',component_property='value')],
)
def force_slider(cities_dropdown):
    if cities_dropdown=='Colombia':
        value=[3,7]
    else:
        df=data[data['Ciudad']==cities_dropdown]
        df['mes']=df['FechaDeMuerte'].dt.month
        months=df['mes'].unique()
        minimo=min(months)
        maximo=max(months)
        value=[minimo,maximo]
    return(value)


@app.callback(
    [Output(component_id='range_slider',component_property='min'),
    Output(component_id='range_slider',component_property='max'),
    Output(component_id='range_slider',component_property='marks')],
    [Input(component_id='cities_dropdown',component_property='value')],
)
def update_slider(cities_dropdown):
    if cities_dropdown=='Colombia':
        minimo=3
        maximo=7
        marks={3:'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio'}
    else:
        df=data[data['Ciudad']==cities_dropdown]
        df['mes']=df['FechaDeMuerte'].dt.month
        months=df['mes'].unique()
        minimo=min(months)
        maximo=max(months)
        marks={}
        for month in months:
            if month==3:
                marks[3]='Marzo'
            if month==4:
                marks[4]='Abril'
            if month==5:
                marks[5]='Mayo'
            if month==6:
                marks[6]='Junio'
            if month==7:
                marks[7]='Julio'

    return (minimo,maximo,marks)

@app.callback(
    [Output(component_id='age_dropdown',component_property='value'),
    Output(component_id='age_dropdown',component_property='options')],
    [Input(component_id='cities_dropdown',component_property='value')]
)
def update_agedropdown_value(cities_dropdown):
    if cities_dropdown=='Colombia':
        age_options=[{'label':'Todas las edades','value':'Todas las edades'},{'label':'0-9 años','value':'[0, 10)'},{'label':'10-19 años','value':'[10, 20)'},{'label':'20-29 años','value':'[20, 30)'},{'label':'30-39 años','value':'[30, 40)'},{'label':'40-49 años','value':'[40, 50)'},{'label':'50-59 años','value':'[50, 60)'},{'label':'60-69 años','value':'[60, 70)'},{'label':'70-79 años','value':'[70, 80)'},{'label':'80-89 años','value':'[80, 90)'},{'label':'90-99 años','value':'[90, 100)'},{'label':'100 años o más','value':'100+'}]
    else:
        df=data[data['Ciudad']==cities_dropdown]
        grouped_data_age = df.groupby('Grupo_Edad')
        ages=list(grouped_data_age.groups.keys())
        ages.append(ages.pop(0))
        age_options=[{'label':'Todas las edades','value':'Todas las edades'}]
        for age in ages:
            if age=='[0, 10)':
                dic={'label':'0-9 años','value':age}
                age_options.append(dic)
            elif age=='[10, 20)':
                dic={'label':'10-19 años','value':age}
                age_options.append(dic)
            elif age=='[20, 30)':
                dic={'label':'20-29 años','value':age}
                age_options.append(dic)
            elif age=='[30, 40)':
                dic={'label':'30-39 años','value':age}
                age_options.append(dic)
            elif age=='[40, 50)':
                dic={'label':'40-49 años','value':age}
                age_options.append(dic)
            elif age=='[50, 60)':
                dic={'label':'50-59 años','value':age}
                age_options.append(dic)
            elif age=='[60, 70)':
                dic={'label':'60-69 años','value':age}
                age_options.append(dic)
            elif age=='[70, 80)':
                dic={'label':'70-79 años','value':age}
                age_options.append(dic)
            elif age=='[80, 90)':
                dic={'label':'80-89 años','value':age}
                age_options.append(dic)
            elif age=='[90, 100)':
                dic={'label':'90-99 años','value':age}
                age_options.append(dic)
            elif age=='100+':
                dic={'label':'100 años o más','value':age}
                age_options.append(dic)

    default_value = 'Todas las edades'
    return (default_value,age_options)


@app.callback(
    [Output(component_id='sex_graph',component_property='figure'),
    Output(component_id='age_graph',component_property='figure'),
    Output(component_id='days_graph',component_property='figure'),
    Output(component_id='date_displayed',component_property='children')],
    [Input(component_id='cities_dropdown',component_property='value'),
    Input(component_id='range_slider',component_property='value')]
)
def update_graphs(cities_dropdown,range_slider):
    if cities_dropdown=='Colombia':
        data['mes']=data['FechaDeMuerte'].dt.month
        grouped_data_month=data.groupby('mes')
        if range_slider==[3,7]:
            df=data
        elif range_slider==[3,6]:
            df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
        elif range_slider==[3,5]:
            df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4),grouped_data_month.get_group(5)])
        elif range_slider==[3,4]:
            df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4)])
        elif range_slider==[3,3]:
            df=grouped_data_month.get_group(3)
        elif range_slider==[4,7]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[4,6]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
        elif range_slider==[4,5]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5)])
        elif range_slider==[4,4]:
            df=grouped_data_month.get_group(4)
        elif range_slider==[5,7]:
            df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[6,7]:
            df=pd.concat([grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[7,7]:
            df=grouped_data_month.get_group(7)
        elif range_slider==[5,5]:
            df=grouped_data_month.get_group(5)
        elif range_slider==[6,6]:
            df=grouped_data_month.get_group(6)
        elif range_slider==[5,6]:
            df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
        else:
            df=data
        
        grouped_data = df.groupby('Sexo')
        M=grouped_data.get_group('M')['Grupo_Edad'].value_counts().sort_index()
        F=grouped_data.get_group('F')['Grupo_Edad'].value_counts().sort_index()

        M=M.reindex(['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])
        F=F.reindex(['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])

        fig = go.Figure()
        fig.add_trace(go.Bar(x=M.values, y=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'],
                marker_color='#53A68D',
                name='Hombres',
                orientation='h'))
        fig.add_trace(go.Bar(x=F.values, y=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'],
                marker_color='#AAF2DD',
                name='Mujeres',
                orientation='h'))
        fig.update_layout(
            xaxis_title='Número de fallecidos',
            yaxis_title='Rango de edad',
            yaxis = dict(
                tickmode = 'array',
                tickvals = ['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'],
                ticktext = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59','60-69','70-79','80-89','90-99','100+']
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )

        M1=grouped_data.get_group('M')['Grupo_Dias'].value_counts().sort_index()
        F1=grouped_data.get_group('F')['Grupo_Dias'].value_counts().sort_index()

        M1=M1.reindex(['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'])
        F1=F1.reindex(['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'])

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=M1.values, y=['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'],
                marker_color='#5C8C9E',
                name='Hombres',
                orientation='h'))
        fig1.add_trace(go.Bar(x=F1.values, y=['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'],
                marker_color='#B7DDEB',
                name='Mujeres',
                orientation='h'))
        fig1.update_layout(
            xaxis_title='Número de fallecidos',
            yaxis_title='Días entre inicio de síntomas y muerte',
            yaxis = dict(
                tickmode = 'array',
                tickvals = ['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'],
                ticktext = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29','30-34','35-39','40-44','45-49','50+']
            ),
            plot_bgcolor='rgba(0,0,0,0)',
        )
    else:
        df=data[data['Ciudad']==cities_dropdown]
        df['mes']=df['FechaDeMuerte'].dt.month
        grouped_data_month=df.groupby('mes')
        if range_slider==[3,7]:
            df=df
        elif range_slider==[3,6]:
            if (df.mes==4).any():
                if (df.mes==5).any():
                    df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
                else:
                    df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4),grouped_data_month.get_group(6)])
            else:
                if (df.mes==5).any():
                    df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
                else:
                    df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(6)])
                    
        elif range_slider==[3,5]:
            if (df.mes==4).any():
                df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4),grouped_data_month.get_group(5)])
            else:
                df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(5)])

        elif range_slider==[3,4]:
            df=pd.concat([grouped_data_month.get_group(3),grouped_data_month.get_group(4)])

        elif range_slider==[3,3]:
            df=grouped_data_month.get_group(3)

        elif range_slider==[4,7]:
            if (df.mes==5).any():
                if (df.mes==6).any():
                    df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
                else:
                    df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(7)])
            else:
                if (df.mes==6).any():
                    df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
                else:
                    df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(7)])
        elif range_slider==[4,6]:
            if (df.mes==5).any():
                df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
            else:
                df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(6)])
                    
        elif range_slider==[4,5]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5)])

        elif range_slider==[4,4]:
            df=grouped_data_month.get_group(4)
        
        elif range_slider==[5,7]:
            if (df.mes==6).any():
                df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
            else:
                df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(7)])
        elif range_slider==[6,7]:
            df=pd.concat([grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[7,7]:
            df=grouped_data_month.get_group(7)
        elif range_slider==[5,5]:
            df=grouped_data_month.get_group(5)
        elif range_slider==[6,6]:
            df=grouped_data_month.get_group(6)
        elif range_slider==[5,6]:
            df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6)])


        grouped_data = df.groupby('Sexo')
        if (df.Sexo=='M').any():
            M=grouped_data.get_group('M')['Grupo_Edad'].value_counts().reindex(data.Grupo_Edad.unique(), fill_value=0).sort_index()
            M1=grouped_data.get_group('M')['Grupo_Dias'].value_counts().reindex(data.Grupo_Dias.unique(), fill_value=0).sort_index()        
        else:
            M=pd.Series(0,index=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])
            M1=pd.Series(0,index=['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'])
        if (df.Sexo=='F').any():
            F=grouped_data.get_group('F')['Grupo_Edad'].value_counts().sort_index().reindex(data.Grupo_Edad.unique(), fill_value=0).sort_index()
            F1=grouped_data.get_group('F')['Grupo_Dias'].value_counts().sort_index().reindex(data.Grupo_Dias.unique(), fill_value=0).sort_index()
        else:
            F=pd.Series(0,index=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])
            F1=pd.Series(0,index=['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'])

        M=M.reindex(['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])
        F=F.reindex(['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])
        M1=M1.reindex(['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'])
        F1=F1.reindex(['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'])

        fig = go.Figure()
        fig.add_trace(go.Bar(x=M.values, y=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'],
                marker_color='#53A68D',
                name='Hombres',
                orientation='h'))
        fig.add_trace(go.Bar(x=F.values, y=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'],
                marker_color='#AAF2DD',
                name='Mujeres',
                orientation='h'))

        fig.update_layout(
            xaxis_title='Número de fallecidos',
            yaxis_title='Rango de edad',
            yaxis = dict(
                tickmode = 'array',
                tickvals = ['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'],
                ticktext = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59','60-69','70-79','80-89','90-99','100+']
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )


        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=M1.values, y=['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'],
                marker_color='#5C8C9E',
                name='Hombres',
                orientation='h'))
        fig1.add_trace(go.Bar(x=F1.values, y=['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'],
                marker_color='#B7DDEB',
                name='Mujeres',
                orientation='h'))
        fig1.update_layout(
            xaxis_title='Número de fallecidos',
            yaxis_title='Días entre inicio de síntomas y muerte',
            yaxis = dict(
                tickmode = 'array',
                tickvals = ['[0, 5)','[5, 10)','[10, 15)','[15, 20)','[20, 25)','[25, 30)','[30, 35)','[35, 40)','[40, 45)','[45, 50)','50+'],
                ticktext = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29','30-34','35-39','40-44','45-49','50+']
            ),
            plot_bgcolor='rgba(0,0,0,0)',
        )

        
    piechart=px.pie(
        data_frame=df,
        names=df.Sexo,
        color=df.Sexo,
        color_discrete_map={'M':'#A67263','F':'#FFD7CC'},
        hole=.5,
    )

    df_date=df.copy()
    df_date['FechaDeMuerte'] = pd.to_datetime(df_date['FechaDeMuerte']).dt.date
    min_date=min(df_date['FechaDeMuerte'])
    max_date=max(df_date['FechaDeMuerte'])

    date_displayed='Información desde {}'.format(min_date)+' hasta {}'.format(max_date)    
    
    return(piechart,fig,fig1,date_displayed)

@app.callback(
    Output(component_id='top20_graph',component_property='figure'),
    [Input(component_id='cities_dropdown',component_property='value'),
    Input(component_id='age_dropdown',component_property='value'),
    Input(component_id='range_slider',component_property='value')]
)
def update_top20graph(cities_dropdown,age_dropdown,range_slider):
    if cities_dropdown=='Colombia':
        data['mes']=data['FechaDeMuerte'].dt.month
        grouped_data_month=data.groupby('mes')
        if range_slider==[4,7]:
            df=data
        elif range_slider==[4,6]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
        elif range_slider==[4,5]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5)])
        elif range_slider==[4,4]:
            df=grouped_data_month.get_group(4)
        elif range_slider==[5,7]:
            df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[6,7]:
            df=pd.concat([grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[7,7]:
            df=grouped_data_month.get_group(7)
        elif range_slider==[5,5]:
            df=grouped_data_month.get_group(5)
        elif range_slider==[6,6]:
            df=grouped_data_month.get_group(6)
        elif range_slider==[5,6]:
            df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
        else:
            df=data
        if age_dropdown=='Todas las edades':
            df=df
        else:
            grouped_data_age = data.groupby('Grupo_Edad')
            df = grouped_data_age.get_group(age_dropdown)

        top20=df['Enfermedades'].value_counts().head(20).sort_values()
        
        fig = go.Figure(go.Bar(
            x=top20.values,
            y=top20.index,
            marker={'color':'#FF9BAA'},
            orientation='h'))
        fig.update_layout(
            xaxis_title='Número de fallecidos',
            yaxis= {'dtick': 1},
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
    else:
        df=data[data['Ciudad']==cities_dropdown]
        df['mes']=df['FechaDeMuerte'].dt.month
        grouped_data_month=df.groupby('mes')
        if range_slider==[4,7]:
            df=df
        elif range_slider==[4,6]:
            if (df.mes==5).any():
                df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5),grouped_data_month.get_group(6)])
            else:
                df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(6)])
        elif range_slider==[4,5]:
            df=pd.concat([grouped_data_month.get_group(4),grouped_data_month.get_group(5)])
        elif range_slider==[4,4]:
            df=grouped_data_month.get_group(4)
        elif range_slider==[5,7]:
            if (df.mes==6).any():
                df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
            else:
                df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(7)])
        elif range_slider==[6,7]:
            df=pd.concat([grouped_data_month.get_group(6),grouped_data_month.get_group(7)])
        elif range_slider==[7,7]:
            df=grouped_data_month.get_group(7)
        elif range_slider==[5,5]:
            df=grouped_data_month.get_group(5)
        elif range_slider==[6,6]:
            df=grouped_data_month.get_group(6)
        elif range_slider==[5,6]:
            df=pd.concat([grouped_data_month.get_group(5),grouped_data_month.get_group(6)])

        if age_dropdown=='Todas las edades':
            df2=df
            top20=df2['Enfermedades'].value_counts().head(20).sort_values()
        else:
            grouped_data_age = df.groupby('Grupo_Edad')
            if (df.Grupo_Edad==age_dropdown).any():
                df2 = grouped_data_age.get_group(age_dropdown)
                top20=df2['Enfermedades'].value_counts().head(20).sort_values()
            else:
                top20 = pd.Series(0,index=['[0, 10)','[10, 20)','[20, 30)','[30, 40)','[40, 50)','[50, 60)','[60, 70)','[70, 80)','[80, 90)','[90, 100)','100+'])
        
        fig = go.Figure(go.Bar(
            x=top20.values,
            y=top20.index,
            marker={'color':'#FF9BAA'},
            orientation='h'))
        fig.update_layout(
            xaxis_title='Número de fallecidos',
            yaxis= {'dtick': 1},
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
    
    return(fig)

@app.callback(
    Output(component_id='cities2_dropdown',component_property='options'),
    [Input(component_id='cities1_dropdown',component_property='value')]
)
def update_cities2dropdown_value(cities1_dropdown):
    options=[]
    cities=data.Ciudad.unique()
    cities.sort()
    for city in cities:
        if city!=cities1_dropdown:
            dic={'label':city,'value':city}
            options.append(dic)

    return(options)

@app.callback(
    Output(component_id='top20_2cities_graph',component_property='figure'),
    [Input(component_id='cities1_dropdown',component_property='value'),
    Input(component_id='cities2_dropdown',component_property='value')]
)
def update_top20_2cities_graph(cities1_dropdown,cities2_dropdown):
    if cities1_dropdown=='Colombia':
        df=data
    else:
        df=data[data['Ciudad']==cities1_dropdown]
    
    df2=data[data['Ciudad']==cities2_dropdown]
    top20=df['Enfermedades'].value_counts().head(20).sort_values()
    top20=top20.rename('enf_city1')
    top202=df2['Enfermedades'].value_counts().head(20).sort_values()
    top202=top202.rename('enf_city2')
    data_top20=pd.concat([top20, top202], axis=1)
    data_top20=data_top20.fillna(0).sort_values(by=['enf_city1'])


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_top20['enf_city1'],
        y=data_top20.index,
        marker={'color':'#F7EF94'},
        name=cities1_dropdown,
        orientation='h'))
    fig.add_trace(go.Bar(
        x=data_top20['enf_city2'],
        y=data_top20.index,
        marker={'color':'#D1C575'},
        name=cities2_dropdown,
        orientation='h'))
    fig.update_layout(
        xaxis_title='Número de fallecidos',
        yaxis= {'dtick': 1},
        plot_bgcolor='rgba(0,0,0,0)',
        height=600
    )
    return(fig)

@app.callback(
    Output(component_id='enf2_dropdown',component_property='options'),
    [Input(component_id='enf1_dropdown',component_property='value')]
)
def update_enf2dropdown_value(enf1_dropdown):
    ind=data_enf.index(enf1_dropdown)
    new_data_enf=[]
    for i in range(ind+1,len(data_enf)):
        new_data_enf.append(data_enf[i])
    enf_options=[]
    for enf in new_data_enf:
        dic={'label':enf,'value':enf}
        enf_options.append(dic)
    return(enf_options)

@app.callback(
    Output(component_id='enf3_dropdown',component_property='options'),
    [Input(component_id='enf2_dropdown',component_property='value')]
)
def update_enf3dropdown_value(enf2_dropdown):
    ind=data_enf.index(enf2_dropdown)
    new_data_enf=[]
    for i in range(ind+1,len(data_enf)):
        new_data_enf.append(data_enf[i])
    enf_options=[]
    for enf in new_data_enf:
        dic={'label':enf,'value':enf}
        enf_options.append(dic)
    return(enf_options)

@app.callback(
    Output(component_id='enf_graph',component_property='figure'),
    [Input(component_id='enf1_dropdown',component_property='value'),
    Input(component_id='enf2_dropdown',component_property='value'),
    Input(component_id='enf3_dropdown',component_property='value')]
)
def update_enf_graph(enf1_dropdown,enf2_dropdown,enf3_dropdown):
    value1=data['Enfermedades'].value_counts()[enf1_dropdown]
    value2=data['Enfermedades'].value_counts()[enf2_dropdown]
    value3=data['Enfermedades'].value_counts()[enf3_dropdown]

    if enf1_dropdown+'+'+enf2_dropdown in data.Enfermedades.values:
        value1_2=data['Enfermedades'].value_counts()[enf1_dropdown +'+'+ enf2_dropdown]
        if enf1_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
            value1_3=data['Enfermedades'].value_counts()[enf1_dropdown +'+'+ enf3_dropdown]
            if enf2_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
                value2_3=data['Enfermedades'].value_counts()[enf2_dropdown +'+'+ enf3_dropdown]
                if enf1_dropdown+'+'+enf2_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
                    value1_2_3=data['Enfermedades'].value_counts()[enf1_dropdown +'+'+ enf2_dropdown+'+'+ enf3_dropdown]
                    position1=[0.5,1,2.5,3]
                    position2=[2,1,4,3]
                    position3=[1.5,0,3.5,2]
                    xposition_text=[1.5,2.25,3.2,1.9,2.25,2.7,2.5]
                    yposition_text=[2,2.25,2,1.25,1.75,1.25,0.5]
                    text_list=[value1,value1_2,value2,value1_3,value1_2_3,value2_3,value3]
                    x_name=[1,3.5,3.9]
                    y_name=[3.1,3.1,0.5]
                else:
                    position1=[0.5,1,2.5,3]
                    position2=[2.25,1,4.25,3]
                    position3=[1.5,-0.5,3.5,1.5]
                    xposition_text=[1.5,2.35,3.2,1.9,2.8,2.5]
                    yposition_text=[2,2,2,1.2,1.25,0.5]
                    text_list=[value1,value1_2,value2,value1_3,value2_3,value3]
                    x_name=[1,3.5,2.5]
                    y_name=[3.1,3.1,-0.7]
                
            else:
                position1=[0.5,2,2.5,4]
                position2=[2,2,4,4]
                position3=[0.5,0.5,2.5,2.5]
                xposition_text=[1.5,2.25,3,1.5,1.5]
                yposition_text=[3,3,3,2.2,1.3]
                text_list=[value1,value1_2,value2,value1_3,value3]
                x_name=[1,3.5,3]
                y_name=[4.1,4.1,1.3]
        else:
            if enf2_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
                value2_3=data['Enfermedades'].value_counts()[enf2_dropdown +'+'+ enf3_dropdown]
                position1=[0.5,2,2.5,4]
                position2=[2,2,4,4]
                position3=[2,0.5,4,2.5]
                xposition_text=[1.5,2.25,3,3,3]
                yposition_text=[3,3,3,2.2,1.3]
                text_list=[value1,value1_2,value2,value2_3,value3]
                x_name=[1,3.5,1.5]
                y_name=[4.1,4.1,1.3]
            else:
                position1=[0.5,2,2.5,4]
                position2=[2,2,4,4]
                position3=[1.25,0,3.25,2]
                xposition_text=[1.5,2.25,3,2.25]
                yposition_text=[3,3,3,1]
                text_list=[value1,value1_2,value2,value3]
                x_name=[1,3.5,3.6]
                y_name=[4.1,4.1,1]
    else:
        if enf1_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
            value1_3=data['Enfermedades'].value_counts()[enf1_dropdown +'+'+ enf3_dropdown]
            if enf2_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
                value2_3=data['Enfermedades'].value_counts()[enf2_dropdown +'+'+ enf3_dropdown]
                position1=[0,0,2,2]
                position2=[3,0,5,2]
                position3=[1.5,0,3.5,2]
                xposition_text=[1,1.7,2.5,3.3,4]
                yposition_text=[1,1,1,1,1]
                text_list=[value1,value1_3,value3,value2_3,value2]
                x_name=[1,2.5,4]
                y_name=[2.2,-0.5,2.2]
            else:
                position1=[0.5,2,2.5,4]
                position2=[2.75,2,4.75,4]
                position3=[0.5,0.5,2.5,2.5]
                xposition_text=[1.5,3.75,1.5,1.5]
                yposition_text=[3,3,2.2,1.3]
                text_list=[value1,value2,value1_3,value3]
                x_name=[1.4,3.7,3.2]
                y_name=[4.1,4.1,1.3]
        else:
            if enf2_dropdown+'+'+enf3_dropdown in data.Enfermedades.values:
                value2_3=data['Enfermedades'].value_counts()[enf2_dropdown +'+'+ enf3_dropdown]
                position1=[0.5,2,2.5,4]
                position2=[2.75,2,4.75,4]
                position3=[2.75,0.5,4.75,2.5]
                xposition_text=[1.5,3.75,3.75,3.75]
                yposition_text=[3,3,2.2,1.3]
                text_list=[value1,value2,value2_3,value3]
                x_name=[1.5,3.75,1.9]
                y_name=[4.1,4.1,1.3]
            else:
                position1=[0.5,2,2.5,4]
                position2=[2.75,2,4.75,4]
                position3=[1.75,0,3.75,2]
                xposition_text=[1.5,3.75,2.75]
                yposition_text=[3,3,1]
                text_list=[value1,value2,value3]
                x_name=[1.5,3.75,2.75]
                y_name=[4.2,4.2,-0.2]



    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xposition_text,
        y=yposition_text,
        text=text_list,
        mode="text",
        textfont=dict(
            color="black",
            size=18,
        )
    ))
    fig.add_annotation(
        x=x_name[0],
        y=y_name[0],
        text=enf1_dropdown)
    fig.add_annotation(
        x=x_name[1],
        y=y_name[1],
        text=enf2_dropdown)
    fig.add_annotation(
        x=x_name[2],
        y=y_name[2],
        text=enf3_dropdown)
    fig.update_annotations(dict(
        xref="x",
        yref="y",
        showarrow=False,
        font=dict(
            color="black",
            size=14,
        )
    ))
    fig.update_xaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )
    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )
    # Add circles
    fig.add_shape(
        type="circle",
        fillcolor="#FFAB92",
        x0=position1[0],
        y0=position1[1],
        x1=position1[2],
        y1=position1[3],
        line_color="#FF8358"
    )
    fig.add_shape(
        type="circle",
        fillcolor="#6FCFF0",
        x0=position2[0],
        y0=position2[1],
        x1=position2[2],
        y1=position2[3],
        line_color="#3BBAF0"
    )
    fig.add_shape(
        type="circle",
        fillcolor="#69F5B8",
        x0=position3[0],
        y0=position3[1],
        x1=position3[2],
        y1=position3[3],
        line_color="#33F59A"
    )
    fig.update_shapes(dict(
        opacity=0.7,
        xref="x",
        yref="y",
        layer="below"
    ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        height=500
    )
    return(fig)


if __name__ == '__main__':
    app.run_server(debug=False)

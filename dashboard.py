import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_colorscales
import pandas as pd
from dash.dependencies import Input, Output, State
from plotly.graph_objs import Bar, Layout, Scatter
#from unidecode import unidecode
from datetime import datetime

app = dash.Dash(__name__)
server = app.server

df_contract = pd.read_csv("./informe-contratos-agosto.csv", encoding = "latin-1", sep=";")
df_group_contract_type = df_contract.groupby("CLASE CONTRATO").count()["VIGENCIA"]

def parse_date(x):
	try:
		return datetime.strptime(x, "%d-%b-%y")
	except:
		return pd.NaT

df_contract["FECHA SUSCRIPCIÓN CONTRATO"] = df_contract["FECHA SUSCRIPCIÓN CONTRATO"].apply(parse_date)
df_group_date = df_contract.groupby("FECHA SUSCRIPCIÓN CONTRATO").count()['VIGENCIA']

normalize_string = lambda x:x

dropdown_options = list(pd.Series(df_group_contract_type.index).apply(lambda x:{'label':x,'value':normalize_string(x)}))

# Plotly Graph

data_ct = [Bar(
	x=df_group_contract_type.index,
	y=df_group_contract_type
)]

layout_ct = Layout(
	title='Tipos de contrato',
	xaxis=dict(
		title='Tipo de contrato'
	),
	yaxis=dict(
		title='Cantidad de contratos',
		range=[0, 50]
	)
)

fig_ct = dict( data=data_ct, layout=layout_ct )

# Plotly Graph

data_date = [Scatter(x=df_group_date.index, y=df_group_date)]
print(df_group_date)

layout_date = Layout(
    title='Cantidad de contratos a lo largo del tiempo',
    xaxis=dict(
        title='Fecha'
    ),
    yaxis=dict(
        title='Cantidad de contratos'
    )
)

fig_date = dict( data=data_date, layout=layout_date )

app.layout = html.Div(children=[

	# HTML Div

	html.Div([
		html.Div([
			html.H4(children='Análisis de datos de contratación pública en Bogotá'),
			html.P('El proceso de contratación pública debe ser sometido a una evaluación constante con el propósito de garantizar la transparencia en el manejo de recursos públicos. En el siguiente tablero de control puede estudiar la dinámica de la contratación por tipo de contrato y a lo largo del tiempo.')
		])

	], style={'margin':20} ),

	# Filter

	dcc.Dropdown(
		options=dropdown_options,
		value=[dropdown_options[0]['value']],
		multi=True,
		id='contract-types'
	),

	html.Div([
		html.Div([
			dcc.Graph(
				id = 'contract-type-bars',
				figure = fig_ct
			)
		], className='six columns'),
		#]),
		html.Div([
			dcc.Graph(
				id = 'time-series',
				figure = fig_date
			)
		], className='six columns')
		#])
	], style={'margin':20} ),

	# Plotly graph

	# dcc.Graph(
	# 		id = 'contract-type-bars',
	# 		figure = fig
	# )
])

app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/EQZeaW.css'})

@app.callback(
	Output('contract-type-bars', 'figure'),
	[Input('contract-types','value')])
def update_map_title(contract_type):
	df_filtered = df_contract.loc[df_contract["CLASE CONTRATO"].isin(contract_type)]
	df_group_contract_type_filtered = df_filtered.groupby("CLASE CONTRATO").count()["VIGENCIA"]
	data = [Bar(
		x=df_group_contract_type_filtered.index,
		y=df_group_contract_type_filtered
	)]

	layout = Layout(
		title='Tipos de contrato',
		xaxis=dict(
			title='Tipo de contrato'
		),
		yaxis=dict(
			title='Cantidad de contratos',
			range=[0, 50]
		)
	)

	fig = dict( data=data, layout=layout )
	return fig

@app.callback(
	Output('time-series', 'figure'),
	[Input('contract-types','value')])
def update_map_title(contract_type):
	df_filtered = df_contract.loc[df_contract["CLASE CONTRATO"].isin(contract_type)]
	df_group_date_filtered = df_filtered.groupby("FECHA SUSCRIPCIÓN CONTRATO").count()['VIGENCIA']

	data_date = [Scatter(x=df_group_date_filtered.index, y=df_group_date_filtered)]

	layout_date = Layout(
	    title='Cantidad de contratos a lo largo del tiempo',
	    xaxis=dict(
	        title='Fecha'
	    ),
	    yaxis=dict(
	        title='Cantidad de contratos'
	    )
	)

	fig = dict( data=data_date, layout=layout_date )

	return fig

if __name__ == '__main__':
	app.run_server(host="0.0.0.0")
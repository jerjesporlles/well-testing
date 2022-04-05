import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt

@st.cache
def cargar_archivo(archivo_excel):
	try:
		df = pd.read_excel(archivo_excel)	
	except:
		st.sidebar.error("Archivo no admitido ") # Rojo
	return df 

def ingreso_datos():
	col1,col2,col3 = st.beta_columns(3)
	with col1 :
		phi = st.number_input('Input phi',min_value=0.0000, max_value=None, value=0.048,  step=0.0010 )
		rw = st.number_input('Input rw',min_value=0.0000, max_value=None, value=0.2917,  step=0.0100 )
	with col2 :
		h = st.number_input('Input h',min_value=0.00, max_value=None, value=65.00,  step=1.00 )
		Bo = st.number_input('Input Bo',min_value=0.0000, max_value=None, value=1.8235,  step=0.1000 )		
	with col3 :
		visc = st.number_input('Input visc',min_value=0.0000, max_value=None, value=0.3620,  step=0.0010 )
		Ct = st.number_input('Input Ct',min_value=0.00, max_value=None, value=24.5,  step=1.0 )
	return phi,rw,h,Bo,visc, Ct/1000000

def ingreso_datos_buildup():

	col1,col2 = st.beta_columns(2)
	with col1 :
		qo = st.number_input('Input qo',min_value=0.00, max_value=None, value=3224.00,  step=1.00 )
		tp = st.number_input('Input tp',min_value=0.00, max_value=None, value=56.00,  step=1.00 )
	with col2 :
		pwf = st.number_input('Input Pwf(t=0)', min_value=0.00, max_value=None, value=11348.00,  step=1.00 )
	return qo,pwf, tp

def Buildup_Test_Sequence():
	st.sidebar.info("Bienvenido al módulo Buildup Test Sequence") #Amarillo
	
	archivo_excel = st.sidebar.file_uploader("Cargar archivo excel" , type=['.xls', '.xlsx'], key=None)
	if archivo_excel is None:
		st.sidebar.warning("Suba un archivo con extencion .xls o .xlsx") #Amarillo
	else:
		df = cargar_archivo(archivo_excel)
		with st.beta_expander('Datos Cargados'):
			st.write(df)

		with st.beta_expander('Ingreso de datos'):
			phi,rw,h,Bo,visc, Ct = ingreso_datos()
			st.write('Validacion de datos ingresados')
			col1,col2,col3 = st.beta_columns(3)
			with col1 :
				st.write('Phi:{}'.format(phi))
				st.write('rw:{}ft'.format(rw))
			with col2 :
				st.write('h:{}ft'.format(h))
				st.write('Bo:{}RB/STB'.format(Bo))
			with col3 :
				st.write('Visc:{}cP'.format(visc))
				st.write('Ct:{}psi-1'.format(Ct))
		with st.beta_expander('Buildup Test Sequence'):
			qo,pwf, tp = ingreso_datos_buildup()

		with st.beta_expander('Cartesian analysis '):
			col5, col6, col7 = st.beta_columns(3)
			with col5:
				df_cartesian_analysis = df[['∆t, hr','pws, psia']]
				st.write(df_cartesian_analysis)

			with col6 :
				t1 = st.number_input('Ingrese el tiempo 1 de la base de datos',min_value=0.00, max_value=None, value=0.25,  step=0.1)
				t2 = st.number_input('Ingrese el tiempo 2 de la base de datos',min_value=0.00, max_value=None, value=0.75,  step=0.1)
			with col7 :
				p1 = st.number_input('Ingrese la presión 1 de la base de datos',min_value=0.00, max_value=None, value=10095.00,  step=1.0)
				p2 = st.number_input('Ingrese la presión 2 de la base de datos',min_value=0.00, max_value=None, value=10451.00,  step=1.0)

		with st.beta_expander('Pressure drop at the start of the test, pi(t=0)'):
			col8, col9, col10 = st.beta_columns(3)
			with col8 :
				dP = st.number_input('Ingrese dP',min_value=0.00, max_value=None, value=11249.24,  step=1.00)
				m =abs((p2-p1)/(t2-t1))
				st.write('m:', m )
			with col9 :

				st.write('wellbore storage coefficient')
				cs= (qo*Bo)/(24*m)
				st.write('Cs:', cs )
			with col10 :

				st.write('Dimensionless wellbore storage coefficient')
				cd= (5.615*cs)/(2*3.1416*phi*Ct*h*rw**2)
				st.write('Cd:', cd )

		with st.beta_expander('Gráficos Drawdown'):
			col1, col2 = st.beta_columns(2)

			with col1:
				lista_columnas = df.columns
				select_columna = st.selectbox('Elija la columna de presión', options= lista_columnas)
				try: 
					df_filtrada= df[ ['∆t, hr', select_columna]]
					st.write(df_filtrada)
				except:
					st.warning('Elija una columna diferente a t, hr')
			with col2:
				grafico_drawdown , ax = plt.subplots(figsize=(3,5))
				ax.plot(df_filtrada['∆t, hr'], df_filtrada[select_columna] )
				ax.set_ylabel(select_columna)
				ax.set_xlabel('t, hr')
				ax.grid()
				st.pyplot(grafico_drawdown)

		with st.beta_expander('Pressure Drawdown Test Sequence  Gráficos comninados '):
			df_limitado = df[1:]
			st.write(df_limitado)

			fig_combinada , ax = plt.subplots()
			ax.plot(df_limitado['∆t, hr'], df_limitado['(tp +∆t) /∆t'],marker = '^',label="(tp +∆t) /∆t")
			ax.plot(df_limitado['∆t, hr'], df_limitado['pws, psia'],marker = '^',label="pws, psia")
			ax.plot(df_limitado['∆t, hr'], df_limitado['∆p, psi'], marker = 'o',label="∆p, psi")
			ax.plot(df_limitado['∆t, hr'], df_limitado["∆p' (∆t), psi"], marker = 'x',label="∆p' (∆t), psi" )
			ax.plot(df_limitado['∆t, hr'], df_limitado["∆p' (∆te), psi"], marker = '.',label="∆p' (∆te), psi" )
			ax.legend(loc="best")
			ax.set_xlabel('∆t, hr')
			plt.yscale('log')
			plt.xscale('log')
			plt.grid(True, which="both", ls="-")
			st.pyplot(fig_combinada)

		with st.beta_expander('Pressure Drawdown Test Sequence '):
		
			col3 , col4 = st.beta_columns(2)

			with col3:
				grafico_drawdown2 , ax = plt.subplots(figsize=(3,5))
				ax.plot(df_limitado['∆t, hr'], df_limitado['pws, psia'] , marker = 'x')
				plt.xscale('log')
				plt.xlim(0.1, 1000)
				ax.set_ylabel('pwf, psia')
				ax.set_xlabel('∆t, hr')
				ax.set_ylabel('pws, psia')
				ax.grid()
				st.pyplot(grafico_drawdown2)

			with col4:
				grafico_drawdown3 , ax = plt.subplots(figsize=(3,5))
				ax.plot(df_limitado['∆t, hr'], df_limitado['pws, psia'] , marker = 'x')
				plt.xscale('log')
				plt.xlim(0.1, 1000)
				ax.invert_xaxis()
				ax.set_ylabel('pws, psia')
				ax.set_xlabel('∆t, hr')
				ax.set_ylabel('pws, psia')
				ax.grid()
				st.pyplot(grafico_drawdown3)


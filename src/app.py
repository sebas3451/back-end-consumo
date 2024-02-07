from flask import Flask, request,jsonify,redirect,url_for,session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes.routes_api import routes_api
from models.model import EstSum, Estado,TipoUbicacion, Consumo, Mercado, Territorio,TipoTension,NomMunic,NomDepto,NomProv
from utils.db import db
from config import DATABASE_CONNECTION_URI, SECRET_KEY
import pandas as pd
import csv
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)

#datos para conectar con la db

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
SQLAlchemy(app)
CORS(app, supports_credentials=True)
jwt = JWTManager(app)


# RUTAS PROTEGIDAS
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'usuario' or password != 'contraseña':
        return jsonify({"error": "Credenciales inválidas"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print('CARGANDO ARCHIVO.....')
        if 'file' not in request.files:
            return 'No file part in the request', 400
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file', 400
        
        # Leer el contenido del archivo CSV y cargarlo en un DataFrame de Pandas
        df = pd.read_csv(file, sep=';', lineterminator='\n', encoding='ISO-8859-1')
        
        
        # Verificar si la columna 'est_sum' está presente en el DataFrame
        if 'EST_SUM' not in df.columns:
            return 'Columna "EST_SUM" no encontrada en el archivo CSV', 400
        
        
        df.fillna('Sin información', inplace=True)
        df.dropna(inplace=True)
        
        df_clean_estado = df.dropna(subset=['ESTADO'])
        df_clean_territorio = df.dropna(subset=['TERRITORIO'])
        df_clean_nom_munic = df.dropna(subset=['NOM_MUNIC'])
        df_clean_nom_dept = df.dropna(subset=['NOM_DEPTO'])
        df_clean_nom_prov = df.dropna(subset=['NOM_PROV'])
        df_clean_tipo_ubicacion = df.dropna(subset=['TIPO_UBICACION'])
        
        # Mostrar los valores de la columna 'est_sum' en la consola
        est_sum_column = df['EST_SUM'].unique()
        estado_column = df_clean_estado['ESTADO'].unique()
        mercado_column = df['MERCADO'].unique()
        territorio_column = df_clean_territorio['TERRITORIO'].unique()
        tipo_tension_column = df['TIPO_TENSION'].unique()
        nom_munic_column = df_clean_nom_munic['NOM_MUNIC'].unique()
        nom_depto_column = df_clean_nom_dept['NOM_DEPTO'].unique()
        nom_prov_column = df_clean_nom_prov['NOM_PROV'].unique()
        tipo_ubicacion_column = df_clean_tipo_ubicacion['TIPO_UBICACION'].unique()
        
        for value in est_sum_column:
            existing_instance = EstSum.query.filter_by(nombre=value).first()
            if existing_instance is None:
                est_sum_instance = EstSum(nombre=value)
                db.session.add(est_sum_instance) 
                db.session.commit()
                
        for value in estado_column:
            existing_instance = Estado.query.filter_by(nombre=value).first()
            if existing_instance is None:
                estado_instance = Estado(nombre=value)
                db.session.add(estado_instance) 
                db.session.commit()
                
        for value in mercado_column:
            existing_instance = Mercado.query.filter_by(nombre=value).first()
            if existing_instance is None:
                mercado_instance = Mercado(nombre=value)
                db.session.add(mercado_instance) 
                db.session.commit()
                
        for value in territorio_column:
            existing_instance = Territorio.query.filter_by(nombre=value).first()
            if existing_instance is None:
                territorio_instance = Territorio(nombre=value)
                db.session.add(territorio_instance) 
                db.session.commit()
        
        for value in tipo_tension_column:
            existing_instance = TipoTension.query.filter_by(nombre=value).first()
            if existing_instance is None:
                territorio_instance = TipoTension(nombre=value)
                db.session.add(territorio_instance) 
                db.session.commit()
                
        for value in nom_munic_column:
            existing_instance = NomMunic.query.filter_by(nombre=value).first()
            if existing_instance is None:
                territorio_instance = NomMunic(nombre=value)
                db.session.add(territorio_instance) 
                db.session.commit()

        for value in nom_depto_column:
            existing_instance = NomDepto.query.filter_by(nombre=value).first()
            if existing_instance is None:
                territorio_instance = NomDepto(nombre=value)
                db.session.add(territorio_instance) 
                db.session.commit()
                
        for value in nom_prov_column:
            existing_instance = NomProv.query.filter_by(nombre=value).first()
            if existing_instance is None:
                territorio_instance = NomProv(nombre=value)
                db.session.add(territorio_instance) 
                db.session.commit()
        
        for value in tipo_ubicacion_column:
            existing_instance = TipoUbicacion.query.filter_by(nombre=value).first()
            if existing_instance is None:
                territorio_instance = TipoUbicacion(nombre=value)
                db.session.add(territorio_instance) 
                db.session.commit()
        contador = 0        
        for index, row in df.iterrows():
            print('fila num: ', contador)
            contador = contador + 1
            est_num_id = EstSum.query.filter_by(nombre=row['EST_SUM']).first().id
            estado_id = Estado.query.filter_by(nombre=row['ESTADO']).first().id
            mercado_id = Mercado.query.filter_by(nombre=row['MERCADO']).first().id
            territorio_id = Territorio.query.filter_by(nombre=row['TERRITORIO']).first().id
            tipo_tension_id = TipoTension.query.filter_by(nombre=row['TIPO_TENSION']).first().id
            nom_munic_id = NomMunic.query.filter_by(nombre=row['NOM_MUNIC']).first().id
            nom_depto_id = NomDepto.query.filter_by(nombre=row['NOM_DEPTO']).first().id
            nom_prov_id = NomProv.query.filter_by(nombre=row['NOM_PROV']).first().id
            consumo = Consumo(
                id_est_sum=est_num_id,
                id_estado=estado_id,
                id_mercado=mercado_id,
                id_territorio=territorio_id,
                id_tipo_tension=tipo_tension_id,
                id_nom_munic=nom_munic_id,
                id_nom_depto=nom_depto_id,
                id_nom_prov=nom_prov_id,
                periodo_analisis=row['PERIODO_ANALISIS'],
                periodo_ejecucion=row['PERIODO_EJECUCION'],
                nis_rad=row['NIS_RAD'],
                nic=row['NIC'],
                codigo_sic=row['CODIGO_SIC'],
                nif=row['NIF'],
                nombre=row['NOMBRE'],
                zona=row['ZONA'],
                desc_cnae=row['DESC_CNAE'],
                f_alta=row['F_ALTA'],
                f_baja=row['F_BAJA'],
                co_asignacion=row['CO_ASIGNACION'],
                tipo_suministro=row['TIPO_SUMINISTRO'],
                tipo_asoc=row['TIPO_ASOC'],
                tarifa=row['TARIFA'],
                descripcion_tarifa=row['DESCRIPCION_TARIFA'],
                num_apa=row['NUM_APA'],
                f_inst=row['F_INST'],
                f_lvto=row['F_LVTO'],
                tipo_fase=row['TIPO_FASE'],
                codigo_marca=row['CODIGO_MARCA'],
                cod_local=row['COD_LOCAL'],
                nom_local=row['NOM_LOCAL'],
                tipo_ubicacion=row['TIPO_UBICACION'],
                direccion=row['DIRECCION'],
                nombre_salmt=row['NOMBRE_SALMT'],
                multifamiliar=row['MULTIFAMILIAR'],
                ruta=row['RUTA'],
                num_itin=row['NUM_ITIN'],
                lectura_activa=row['LECTURA_Activa'],
                lectura_activa_f_pico=row['LECTURA_Activa F.Pico'],
                lectura_activa_pico=row['LECTURA_Activa Pico'],
                lectura_reactiva=row['LECTURA_Reactiva'],
                nivel_tension=row['NIVEL_TENSION'],
                meses_en_altasinfact_pendconexion=row['MESES_EN_ALTASINFACT_PENDCONEXION'],
                rango_meses_en_altasinfact_pendconexion=row['RANGO_MESES_EN_ALTASINFACT_PENDCONEXION'],
                segmento=row['SEGMENTO'],
                anomfact=row['ANOMFACT'],
                tipo_anl_mes_anterior=row['TIPO_ANL_MES_ANTERIOR'],
                ultima_anl=row['ULTIMA_ANL'],
                periodo_ultima_anl=row['PERIODO_ULTIMA_ANL'],
                est_202212=row['EST_202212'],
                est_202301=row['EST_202301'],
                est_202302=row['EST_202302'],
                est_202303=row['EST_202303'],
                est_202304=row['EST_202304'],
                est_202305=row['EST_202305'],
                est_202306=row['EST_202306'],
                est_202307=row['EST_202307'],
                est_202308=row['EST_202308'],
                est_202309=row['EST_202309'],
                est_202310=row['EST_202310'],
                est_202311=row['EST_202311'],
                est_202312=row['EST_202312'],
                csmo_201801=row['CSMO_201801'],
                csmo_201802=row['CSMO_201802'],
                csmo_201803=row['CSMO_201803'],
                csmo_201804=row['CSMO_201804'],
                csmo_201805=row['CSMO_201805'],
                csmo_201806=row['CSMO_201806'],
                csmo_201807=row['CSMO_201807'],
                csmo_201808=row['CSMO_201808'],
                csmo_201809=row['CSMO_201809'],
                csmo_201810=row['CSMO_201810'],
                csmo_201811=row['CSMO_201811'],
                csmo_201812=row['CSMO_201812'],
                csmo_201901=row['CSMO_201901'],
                csmo_201902=row['CSMO_201902'],
                csmo_201903=row['CSMO_201903'],
                csmo_201904=row['CSMO_201904'],
                csmo_201905=row['CSMO_201905'],
                csmo_201906=row['CSMO_201906'],
                csmo_201907=row['CSMO_201907'],
                csmo_201908=row['CSMO_201908'],
                csmo_201909=row['CSMO_201909'],
                csmo_201910=row['CSMO_201910'],
                csmo_201911=row['CSMO_201911'],
                csmo_201912=row['CSMO_201912'],
                csmo_202001=row['CSMO_202001'],
                csmo_202002=row['CSMO_202002'],
                csmo_202003=row['CSMO_202003'],
                csmo_202004=row['CSMO_202004'],
                csmo_202005=row['CSMO_202005'],
                csmo_202006=row['CSMO_202006'],
                csmo_202007=row['CSMO_202007'],
                csmo_202008=row['CSMO_202008'],
                csmo_202009=row['CSMO_202009'],
                csmo_202010=row['CSMO_202010'],
                csmo_202011=row['CSMO_202011'],
                csmo_202012=row['CSMO_202012'],
                csmo_202101=row['CSMO_202101'],
                csmo_202102=row['CSMO_202102'],
                csmo_202103=row['CSMO_202103'],
                csmo_202104=row['CSMO_202104'],
                csmo_202105=row['CSMO_202105'],
                csmo_202106=row['CSMO_202106'],
                csmo_202107=row['CSMO_202107'],
                csmo_202108=row['CSMO_202108'],
                csmo_202109=row['CSMO_202109'],
                csmo_202110=row['CSMO_202110'],
                csmo_202111=row['CSMO_202111'],
                csmo_202112=row['CSMO_202112'],
                csmo_202201=row['CSMO_202201'],
                csmo_202202=row['CSMO_202202'],
                csmo_202203=row['CSMO_202203'],
                csmo_202204=row['CSMO_202204'],
                csmo_202205=row['CSMO_202205'],
                csmo_202206=row['CSMO_202206'],
                csmo_202207=row['CSMO_202207'],
                csmo_202208=row['CSMO_202208'],
                csmo_202209=row['CSMO_202209'],
                csmo_202210=row['CSMO_202210'],
                csmo_202211=row['CSMO_202211'],
                csmo_202212=row['CSMO_202212'],
                csmo_202301=row['CSMO_202301'],
                csmo_202302=row['CSMO_202302'],
                csmo_202303=row['CSMO_202303'],
                csmo_202304=row['CSMO_202304'],
                csmo_202305=row['CSMO_202305'],
                csmo_202306=row['CSMO_202306'],
                csmo_202307=row['CSMO_202307'],
                csmo_202308=row['CSMO_202308'],
                csmo_202309=row['CSMO_202309'],
                csmo_202310=row['CSMO_202310'],
                csmo_202311=row['CSMO_202311'],
                csmo_202312=row['CSMO_202312'],
                dias_real=row['DIAS_REAL'],
                dias_plan=row['DIAS_PLAN'],
                cant_os=row['Cant O/S'],
                cant_irr=row['Cant IRR'],
                ult_f_rev=row['ULT_F_REV'],
                ult_rev_res=row['ULT_REV_RES'],
                nuevo_sum=row['NUEVO_SUM'],
                antg_medidor=row['ANTG_MEDIDOR'],
                asoc_pd_hj=row['ASOC_PD_HJ'],
                fact_util=row['FACT_UTIL'],
                csmo_proyectado=row['CSMO_PROYECTADO'],
                desv_abs=row['DESV_ABS'],
                mean_5perc=row['MEAN_5perc'],
                csmo_estc=row['CSMO_ESTC'],
                csmo_proy_agenda=row['CSMO_PROY_AGENDA'],
                csmo_norm_202201=row['CSMO_NORM_202201'],
                csmo_norm_202202=row['CSMO_NORM_202202'],
                csmo_norm_202203=row['CSMO_NORM_202203'],
                csmo_norm_202204=row['CSMO_NORM_202204'],
                csmo_norm_202205=row['CSMO_NORM_202205'],
                csmo_norm_202206=row['CSMO_NORM_202206'],
                csmo_norm_202207=row['CSMO_NORM_202207'],
                csmo_norm_202208=row['CSMO_NORM_202208'],
                csmo_norm_202209=row['CSMO_NORM_202209'],
                csmo_norm_202210=row['CSMO_NORM_202210'],
                csmo_norm_202211=row['CSMO_NORM_202211'],
                csmo_norm_202212=row['CSMO_NORM_202212'],
                csmo_norm_202303=row['CSMO_NORM_202303'],
                csmo_norm_202304=row['CSMO_NORM_202304'],
                csmo_norm_202305=row['CSMO_NORM_202305'],
                csmo_norm_202306=row['CSMO_NORM_202306'],
                csmo_norm_202307=row['CSMO_NORM_202307'],
                csmo_norm_202308=row['CSMO_NORM_202308'],
                csmo_norm_202309=row['CSMO_NORM_202309'],
                csmo_norm_202310=row['CSMO_NORM_202310'],
                csmo_norm_202311=row['CSMO_NORM_202311'], 
            )
        db.session.add(consumo) 
        db.session.commit()
        print('Datos cargados')
        return dict(success = True, total_registros = contador), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_json', methods=['POST'])
def upload_json_file():
    datos_json = request.get_json()
    try:
        for dato in datos_json:
            nuevo_consumo = Consumo(**dato)
            db.session.add(nuevo_consumo)
        db.session.commit()
        return dict(success = True, mensaje = "Datos insertados"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





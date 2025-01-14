#  Copyright (c) 2020 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#       openECOE-API is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       openECOE-API is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

# Creates a worker that handle jobs in ``default`` queue.
from app.jobs import rq
from flask import current_app
import os
import pandas as pd
from app.model import db
import json
import datetime


@rq.job(timeout=300)
def export_csv(identidad, ecoe="", organization=""):
    from app.statistics.Csv import introducir_key_id
    rq.set_task_progress(0)

    try:
        conexion = db.engine

        #df_organization = pd.read_sql("SELECT * FROM shift", organization)
        cadena_parametros = ""
        if organization != "":
            cadena_parametros = "_org_" + organization
            df_organization = pd.read_sql_query("SELECT * FROM organization WHERE id = " + organization, conexion)
        else:
            df_organization = pd.read_sql_table("organization", conexion)
        #df_ecoe = pd.read_sql("SELECT * FROM shift", ecoe)
        if ecoe != "":
            cadena_parametros = "_ecoe_" + ecoe
            df_ecoe_original = pd.read_sql("SELECT id, name, id_organization, id_coordinator, status FROM ecoe WHERE id = " + ecoe, conexion)
        else:
            df_ecoe_original = pd.read_sql_table("ecoe", conexion)
        rq.set_task_progress(1)
        df_ecoe_organization = pd.merge(left=df_ecoe_original.rename(columns = {'id':'id_ecoe','name':'ecoe_name',
        'status':'ecoe_status'}),
        right=df_organization.rename(columns = {'id':'id_organization',
        'name':'organization_name'}), on=['id_organization'])

        df_ecoe = pd.merge(left=df_ecoe_organization,
        right=pd.read_sql_table("user", conexion).loc[:,['id','name','surname','email']].rename(columns = {
        'id':'id_coordinator', 'name':'coordinator_name','surname':'coordinator_surname','email':'coordinator_email'}),
         on=['id_coordinator'])
        rq.set_task_progress(5)        
        #df_planner = pd.read_sql("SELECT * FROM planner", conexion)
        df_planner_shift = pd.merge(left=pd.read_sql_table("planner", conexion).rename(columns = {'id':'id_planner'}), 
        right=pd.read_sql_table("shift", conexion).rename(columns = {'id':'id_shift','time_start':'shift_time_start'}),
         on='id_shift')
        df_planner = pd.merge(left=df_planner_shift, right=pd.read_sql_table("round", conexion)
        .rename(columns = {'id':'id_round','description':'round_description'}), on=['id_round','id_ecoe'])
        rq.set_task_progress(10)
        #df_student = pd.read_sql("SELECT * FROM student", conexion)
        df_student = pd.merge(left=df_planner, right=pd.read_sql_table("student", conexion).rename(
        columns = {'id':'id_student','name':'student_name','surnames':'student_surnames','dni':'student_dni','planner_order':'student_planner_order'}),
         on=['id_planner','id_ecoe'])
        rq.set_task_progress(20)
        #df_question = pd.read_sql("SELECT * FROM question", conexion)
        #df_question_original = pd.read_sql("SELECT * FROM question", conexion)   
        df_question_original = pd.read_sql_table("question", conexion)  
        #Quita las comillas excesivas que envolvian cada diccionario sin causar errores
        listadict = df_question_original.loc[:,"question_schema"].values.tolist()
        listadict = list(map(json.loads, listadict))
        serie_ids = df_question_original.loc[:,["id"]]
        listadict = introducir_key_id(listadict, serie_ids, "id_question")
        pddict = pd.json_normalize(listadict, errors='ignore').rename(columns = {'reference':'question_reference','description':'question_description'})
        rq.set_task_progress(40)
        df_question_normalizada = pd.merge(left=pd.read_sql("SELECT * FROM question", conexion).rename(columns = {'id':'id_question','order':'question_order',
        'max_points':'question_max_points'}), right=pddict, on='id_question')[['id_question','id_area','question_order','id_block','id_station','question_max_points',
        'question_reference','question_description']]
        rq.set_task_progress(50)
        #df_area = pd.read_sql("SELECT * FROM area", conexion)
        df_question_area = pd.merge(left=df_question_normalizada, right=pd.read_sql_table("area", conexion).rename(columns = {'id':'id_area','name':'area_name',
        'code':'area_code'}), on='id_area')

        #df_station = pd.read_sql("SELECT * FROM station", conexion)
        df_station_manager = pd.merge(
        left=pd.read_sql_table("station", conexion).rename(columns = {
        'id':'id_station','name':'station_name', 'code':'area_code', 'order':'station_order'}),
        right=pd.read_sql_table("user", conexion).loc[:,['id','name','surname','email']].rename(columns={
        'id':'id_manager','name':'manager_name','surname':'manager_surname','email':'manager_email'}), on='id_manager')
        rq.set_task_progress(55)
        df_station = pd.merge(
        left=df_station_manager,
        right=df_station_manager.loc[:,['id_station','station_name']].rename(columns={'id_station':'id_parent_station',
        'station_name':'station_parent_station_name'}), on='id_parent_station', 
        how="left")
        rq.set_task_progress(60)
        df_question_area_station = pd.merge(left=df_question_area, right=df_station, on=['id_station','id_ecoe'])
        
        df_question = pd.merge(left=df_question_area_station, right=pd.read_sql_table("block", conexion).loc[:,['id','name','order']].rename(
        columns={'id':'id_block','name':'block_name','order':'block_order'}), on=['id_block'])
        rq.set_task_progress(65)
        #df_answer = pd.read_sql("SELECT * FROM answer", conexion)   
        
        df_answer_original = pd.read_sql_table("answer", conexion)
        listadict2 = df_answer_original.loc[:,"answer_schema"].values.tolist()
        listadict2 = list(map(json.loads, listadict2))
        serie_ids2 = df_answer_original.loc[:,["id"]]
        listadict2 = introducir_key_id(listadict2, serie_ids2, "id_answer")
        pddict2 = pd.json_normalize(listadict2, errors='ignore')
        rq.set_task_progress(80)
        df_answer_normalizada = pd.merge(left=pd.read_sql_table("answer", conexion).rename(columns = {'id':'id_answer'}), 
        right=pddict2, on='id_answer')[['id_answer','id_student','id_question','answer_schema','points','id_station',
        'type']].rename(columns = {'type':'answer_type'})
        
        df_answer_student = pd.merge(left=df_answer_normalizada.rename(columns = {'points':'answer_points'}),
        right=df_student, on='id_student')
        """
        df_answer_student = pd.merge(left=pd.read_sql_table("answer", conexion).rename(columns = {'points':'answer_points'}),
        right=df_student, on='id_student')
        """
        df_answer_student_question = pd.merge(left=df_answer_student,
        right=df_question, on=['id_question','id_station','id_ecoe']).rename(columns = {'id':'id_answer'})
        
        df_answer = pd.merge(left=df_answer_student_question,
        right=df_ecoe, on=['id_ecoe']).rename(columns = {'id':'id_answer'})
        rq.set_task_progress(90)
        #Formateo para que los datos sean mas legibles
        df_answer = df_answer.reindex(columns=['organization_name',
        'ecoe_name', 'ecoe_status',
        'round_code', 'round_description',
        'shift_code', 'shift_time_start',

        'block_name', 'block_order',
        'question_order', 'question_reference', 'question_description',
        'area_name', 'area_code',
        'answer_schema','answer_type',
        'answer_points','question_max_points',
        
        'student_name','student_surnames', 'student_dni', 'student_planner_order',
        
        'station_name', 'station_order','station_parent_station_name',
        'manager_name', 'manager_surname','manager_email',
        'coordinator_name', 'coordinator_surname', 'coordinator_email',
        'id_answer', 'id_student','id_question', 'id_station', 'id_planner', 'id_shift', 'id_round',
        'id_ecoe', 'id_area', 'id_block', 'id_parent_station', 'id_manager','id_organization','id_coordinator'])
        
        filenamebase = "opendata"
        filenameextension = ".csv"

        fecha_creacion ="_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        #identidad = auth.read_identity_from_flask_login().id
        rq.set_task_progress(95)        
        filename = filenamebase + cadena_parametros + "_" + identidad + fecha_creacion + filenameextension
        filenamezip = filenamebase + cadena_parametros + "_" + identidad + fecha_creacion + ".zip"
        
            
        _archiveroute = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        absolutefilepath = os.path.join(_archiveroute, filenamezip)
        rq.set_task_progress(99)
        compression_options = dict(method='zip',archive_name=filename)
        df_answer.to_csv(absolutefilepath,index=False,encoding='utf-8',compression=compression_options)

        rq.finish_job(file="%s" % filenamezip)
        return filenamezip
        
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

    

    

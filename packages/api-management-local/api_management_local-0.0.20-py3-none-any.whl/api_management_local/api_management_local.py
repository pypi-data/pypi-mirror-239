from dotenv import load_dotenv
import json
import os
from circles_local_database_python.connector import Connector
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from src.api_call import APICallsLocal
from url_local.url_circlez import UrlCirclez
from url_local import action_name_enum, entity_name_enum, component_name_enum
from user_context_remote.user_context import UserContext
from src.api_limit import (DEVELOPER_EMAIL,
                               API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                               API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME, APILimitsLocal)
import requests
import http
BRAND_NAME = os.getenv('BRAND_NAME')
ENVIORNMENT_NAME = os.getenv('ENVIRONMENT_NAME')
AUTHENTICATION_API_VERSION = 1
LIMIT_REACHED = 1
LIMIT_NOT_REACHED = 0
url_circlez = UrlCirclez()
authentication_login_validate_jwt_url = url_circlez.endpoint_url(
            brand_name=BRAND_NAME,
            environment_name=ENVIORNMENT_NAME,
            component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
            entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
            version=AUTHENTICATION_API_VERSION,
            action_name=action_name_enum.ActionName.VALIDATE_JWT.value
        )
api_management_local_python_code = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
load_dotenv()
logger=Logger.create_logger(object=api_management_local_python_code)
class APIManagmentLocal( GenericCRUD):
    def __init__(self) -> None:
        pass
    
    def get_actual_by_api_type_id_last_x_hours(api_type_id: int, last_x_hours: int, unit: str) -> int:
        logger.start(object={'api_type_id': str(api_type_id), 'last_x_hours': str(last_x_hours), 'unit': unit})
        connection = Connector.connect("api_call")
        cursor = connection.cursor() 
        try:
            query = """
                SELECT COUNT(*)
                FROM api_call_view
                WHERE api_type_id = %s
                AND TIMESTAMPDIFF(%s, created_timestamp, NOW()) <= %s
                AND http_status_code = %s
            """        
            cursor.execute(query, (api_type_id, unit, last_x_hours, http.HTTPStatus.OK))
            actual_succ_count = cursor.fetchone()[0]
            logger.end(object={'actual_succ_count': actual_succ_count})         
            return actual_succ_count
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            

    
    @staticmethod
    def  _get_json_with_only_sagnificant_fields_by_api_type_id( json1:json, api_type_id:int)-> json:
        logger.start(object={'json1':str(json1),'api_type_id':str(api_type_id)})
        connection = Connector.connect("api_type")
        try:
            cursor = connection.cursor()
            query = f"SELECT field_name FROM api_type.api_type_field_view WHERE api_type_id = %s"
            cursor.execute(query, (api_type_id,))
            significant_fields = [row[0] for row in cursor.fetchall()]
            data = json.loads(json1)
            filtered_data = {key: data[key] for key in significant_fields if key in data}
            filtered_json = json.dumps(filtered_data)
            logger.end(object={'filtered_json':str(filtered_json)})
            return filtered_json
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            
     
     
     
    
    def check_limit  (api_type_id:int, last_x_hours: int, unit: str)->int:
        logger.start(object={'api_type_id':str(api_type_id),'last_x_hours': str(last_x_hours), 'unit': unit})
        api_succ=APIManagmentLocal.get_actual_by_api_type_id_last_x_hours(api_type_id=api_type_id,last_x_hours=last_x_hours,unit=unit)
        api_type_id1=str(api_type_id)
        api_limit=APILimitsLocal()
        limits=api_limit.get_limits_by_api_type_id(api_type_id=api_type_id1)
        api_limit=limits[0][0]
        
        if api_succ <api_limit:
            return 1      
        elif limits[0]<=api_succ and limits[1]>api_succ:
            return 0
        else:
            return -1            


        
        
     
     
    @staticmethod
    def try_to_call_api(api_type_id:int, endpoint:str, outgoing_body:str, outgoing_header:str, last_x_hours: int, unit: str)->str:
        logger.start(object={'api_type_id':str(api_type_id),'endpoint':str(endpoint),'outgoing_body':str(outgoing_body),'outgoing_header':str(outgoing_header),'last_x_hours': str(last_x_hours), 'unit': unit})
        check=APIManagmentLocal.check_limit (api_type_id=api_type_id,last_x_hours=last_x_hours,unit=unit)
        connection = Connector.connect("api_call")
        cursor = connection.cursor()
        try:
                query=f"SELECT http_status_code, response_body FROM api_call.api_call_view WHERE api_type_id= %s"
                cursor.execute(query, (api_type_id,))
                arr =cursor.fetchone()
                if arr[0]==http.HTTPStatus.OK:
                    return arr[1]
                if check==1:
                      user=UserContext.login()
                      data = {"jwtToken":f"Bearer ${user.get_user_JWT()} "}
                      outgoing_body_significant_fields_hash = hash(APIManagmentLocal._get_json_with_only_sagnificant_fields_by_api_type_id(json1=json.dumps(data), api_type_id=str(api_type_id)))         
                      output = requests.post(url=endpoint, data=json.dumps(outgoing_body, separators=(",", ":")), headers=outgoing_header)
                      status=output.status_code
                      incoming_message = output.content.decode('utf-8')
                      response_body=output.json()
                      res=json.dumps(response_body)
                      data1 = (api_type_id,endpoint, outgoing_header, outgoing_body,str(outgoing_body_significant_fields_hash),incoming_message,status,res )
                      APICall1=APICallsLocal()
                      APICall1._insert_api_call_tuple(data1)
                      logger.end()
                      return response_body                         
                elif check==0:
                      user=UserContext.login()
                      output = requests.post(url=authentication_login_validate_jwt_url, data=json.dumps(data, separators=(",", ":")), headers=outgoing_header)
                      logger.warn("you passed the soft limit")
                      logger.end()
                else:
                    logger.error("you passed the hard limit")
                    logger.end()

                  
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            

    def  delete_api(api_type_id:int, last_x_hours: int, unit: str,data:str):
        logger.start(object={'api_type_id':str(api_type_id),'last_x_hours': str(last_x_hours), 'unit': unit})
        try:
            check_limit =APIManagmentLocal.check_limit (api_type_id=api_type_id,last_x_hours=last_x_hours,unit=unit)
            data_j=json.loads(data)    
            
            if check_limit == LIMIT_REACHED:     
                requests.delete(data=data_j)
                logger.end()
            elif check_limit == LIMIT_NOT_REACHED:
                logger.warn("you passed the soft limit")
                logger.end()
            else:
                logger.error("you passed the hard limit")
                logger.end()          
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            
    
    def  get_api(api_type_id:int, last_x_hours: int, unit: str,data:str):
        logger.start(object={'api_type_id':str(api_type_id),'last_x_hours': str(last_x_hours), 'unit': unit})
        try:
            check_limit =APIManagmentLocal.check_limit (api_type_id=api_type_id,last_x_hours=last_x_hours,unit=unit)
            data_j=json.loads(data)    
            if check_limit ==LIMIT_REACHED:
                requests.get(data=data_j)
                logger.end()
            elif check_limit ==LIMIT_NOT_REACHED:
                logger.warn("you passed the soft limit")
                logger.end()
            else:
                logger.error("you passed the hard limit")
                logger.end()          
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            
        
    def  put_api(api_type_id:int, last_x_hours: int, unit: str,data:str):
        logger.start(object={'api_type_id':str(api_type_id),'last_x_hours': str(last_x_hours), 'unit': unit})
        try:
            check_limit =APIManagmentLocal.check_limit (api_type_id=api_type_id,last_x_hours=last_x_hours,unit=unit)
            data_j=json.loads(data)    
            if check_limit ==LIMIT_REACHED:
                requests.put(data=data_j)
                logger.end()
            elif check_limit ==LIMIT_NOT_REACHED:
                logger.warn("you passed the soft limit")
                logger.end()
            else:
                logger.error("you passed the hard limit")
                logger.end()          
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            
                        
          
               




        
        
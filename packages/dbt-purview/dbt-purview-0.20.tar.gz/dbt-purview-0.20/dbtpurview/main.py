import click
import json
import requests
from airflow.models import Variable
from airflow.hooks.base import BaseHook
import os

@click.command()
@click.option('--env', default='databricks')
@click.option('--dwhcid', default='jaffle_shop_databricks_connection')
@click.option('--azpurview', default='azure_purview')
@click.option('--path', default='/tmp/')
def dbtpurview(env,dwhcid,azpurview,path):

   azpurview_conn =  BaseHook.get_connection(str(azpurview))
   extras_dict_purview = json.loads(azpurview_conn.get_extra())
   tenantId = str(extras_dict_purview['extra__azure__tenantId'])
   resource = str(extras_dict_purview['resource'])
   clientId = str(azpurview_conn.login)
   secret = str(azpurview_conn.password)



   if(env == "databricks"):
        conn = BaseHook.get_connection(str(dwhcid))
        host = str(conn.host)
        print("host : "+host)
        schema = str(conn.schema)
        print("schema: "+schema)


   if(env == "snowflake"):
         snowflake_conn = BaseHook.get_connection(str(dwhcid))
         e1xtras_dict = json.loads(snowflake_conn.get_extra())
         host = str(e1xtras_dict['account'])
         database = str(e1xtras_dict['database'])
         schema = str(snowflake_conn.schema)
         warehouse = str(e1xtras_dict['warehouse'])

   file = open(path + "/manifest.json")
   data = json.load(file)
   child_map = data.get("parent_map", {})
   print(child_map)

   filtered_model_list = []
   for i in child_map:
        if(i.split(".")[0] != "test"):
               filtered_model_list.append(i)
   
   model_list = {}
   for i in filtered_model_list:
        model_list[i] = i.split(".")[::-1][0]
   
   
   nodes = data.get("nodes", {})
   model_meterialized = {}
   for i in filtered_model_list:
      if(nodes.get(i) != None):
         if(nodes.get(i).get("config").get("materialized") != 'view'):
            model_meterialized[i] = 'table'
         else:
            model_meterialized[i] = nodes.get(i).get("config").get("materialized")

   qualified_model_name = {}
   for i in filtered_model_list:
       qualified_model_name[i] = prepare_qualified_name(env, database, schema, host, model_list.get(i),model_meterialized.get(i))

   url = f"https://login.microsoftonline.com/{tenantId}/oauth2/token"
   reqeust = {
       "grant_type":"client_credentials",
       "client_id":clientId,
       "client_secret":secret,
       "resource":resource,
       "scope":f"{clientId}/.default"
   }
   response = post(url,reqeust)
   access_token = response.get("access_token")
   create_custom_assest_type(access_token,resource)
   model_guid = {}
   for i in filtered_model_list:
      if(model_meterialized.get(i) == "view"):
         url = f"https://{resource}/datamap/api/atlas/v2/entity/uniqueAttribute/type/hive_view?attr:qualifiedName={qualified_model_name.get(i)}"
      else:
         url = f"https://{resource}/datamap/api/atlas/v2/entity/uniqueAttribute/type/hive_table?attr:qualifiedName={qualified_model_name.get(i)}"

      header = {
          "Authorization": "Bearer "+access_token
      }  
      response = get(url,header)
      model_guid[i] = response.get("entity").get("guid")

#    # print(filtered_model_list)
   for child in filtered_model_list:
      if(child.split(".")[0] != "source"):
         child_id = model_guid.get(child)
         parent_ids = []
         for parent in child_map.get(child):
            print(parent)
            if(parent.split(".")[0] != "test"):
               parent_ids.append(model_guid.get(parent))
         
         input_string = []
         for i in parent_ids:
            input_string.append({
                              "guid": i
                           })
         data = {
                  "entity": {
                     "typeName":"dbt_model",
                     "attributes":{
                           "qualifiedName" : "dbt_"+child,
                           "name" : "dbt_"+child,
                           "inputs" : input_string,
                           "outputs" : [{
                              "guid":child_id
                           }],
                           "raw_query" : nodes.get(child).get("raw_code"),
                           "complie_query" : nodes.get(child).get("compiled_code"),
                           "tag" : nodes.get(child).get("tags")
                     },
                     "status": "ACTIVE"
                  },
                  "referredEntities":{}
               }
         data_json = json.dumps(data)

         header = {
            "Authorization": "Bearer "+access_token,
            "Content-Type": "application/json"
         }
         response = post_with_header(f"https://{resource}/datamap/api/atlas/v2/entity",header,data_json)
            

   file.close()

def post(url,data):   
   response = requests.post(url, data=data)
   if response.status_code == 200:
      result = response.json() 
   else:
      raise Exception(f"API request failed with status code: {response.status_code}")
   
   return result

def post_with_header(url,headers,data):   
   response = requests.post(url, headers=headers, data=data)
   if response.status_code == 200:
      result = response.json()
   else:
      print(response.json())
      raise Exception(f"API request failed with status code: {response.status_code}")
   
   return result

def get(url,header):   
   response = requests.get(url,headers=header)
   if response.status_code == 200:
      result = response.json() 
   else:
      raise Exception(f"API request failed with status code: {response.status_code}")
   
   return result

def prepare_qualified_name(env, database, schema, host, model_name,type):
   if(env == "databricks"):
       qualified_name = schema+"."+model_name+"@"+host
       return qualified_name
   if(env == "snowflake"):
       qualified_name = "snowflake://"+host+"/databases/"+database+"/schemas/"+schema+"/"+type+"/"+model_name
       return qualified_name
   
def create_custom_assest_type(access_token,resource):
   header = {
         "Authorization": "Bearer "+access_token
         }
   response = requests.get(f"https://{resource}/datamap/api/atlas/v2/types/entitydef/name/dbt_model",headers=header)
   if response.status_code != 200:
      url = f"https://{resource}/datamap/api/atlas/v2/types/typedefs"
      data = {
            "entityDefs": [
               {
                     "superTypes": [
                        "Process"
                     ],
                     "name": "dbt_model",
                     "attributeDefs": [
                        {
                           "name": "raw_query",
                           "typeName": "string",
                           "isOptional": "false",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "compile_query",
                           "typeName": "string",
                           "isOptional": "false",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        },
                        {
                           "name": "tag",
                           "typeName": "string",
                           "isOptional": "false",
                           "cardinality": "SINGLE",
                           "valuesMinCount": 1,
                           "valuesMaxCount": 1,
                           "isUnique": "false",
                           "isIndexable": "false",
                           "includeInNotification": "false"
                        }
                     ]
               }
            ]
         }
      data_json = json.dumps(data)
      header = {
            "Authorization": "Bearer "+access_token,
            "Content-Type": "application/json"
         }
      response = post_with_header(url,header,data_json)

if __name__ == '__main__':
   dbtpurview()   
   
   


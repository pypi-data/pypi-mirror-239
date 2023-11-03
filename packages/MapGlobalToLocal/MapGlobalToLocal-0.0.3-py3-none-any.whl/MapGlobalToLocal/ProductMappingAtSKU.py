from pyspark.sql import SparkSession
import pandas as pd
from databricks.sdk.runtime import *
spark = SparkSession.builder.appName("abc").getOrCreate()

class InvalidObjectAtSKULevelError(Exception):
  def __init__(self,message = 'Invalid Region name entered, suggested regions mapped at SKU Level: Fusion, Cordillera, Sirius, U2K2, SiriusVanguard'):
    self.message = message
    super().__init__(self.message)

class InvalidEnvironmentironmentEnteredError(Exception):
  def __init__(self,message = 'Invalid environment entered, suggested environments: PROD, UAT, DEV'):
    self.message = message
    super().__init__(self.message)

def GetMaterialMappedAtSKULevel(environment,region):

  if environment.casefold() == 'PROD'.casefold():
    adls = '80049'
  elif environment.casefold() == 'UAT'.casefold():
    adls = '80158'
  elif environment.casefold() == 'DEV'.casefold():
    adls = '80046'
  else:
    raise InvalidEnvironmentironmentEnteredError()

  df_mounts = dbutils.fs.mounts()
  df_pd = pd.DataFrame(df_mounts)

  df_filtered = df_pd[df_pd['source'].str.contains(f".{adls}.*/BusinessDataLake/SC/$")]
  mntpoint = df_filtered['mountPoint'].iloc[0]
  
  path_global = mntpoint + "/Hierarchies/GlobalProductHierarchyLatest/Processed_Parquet/Global/"
  df_bdl_global = spark.read.format("delta").load(path_global)
  df_bdl_global.createOrReplaceTempView('vw_bdl_hgpl')

  
  if region.casefold() == 'Sirius'.casefold():
    regionID = "E"
    path = "dbfs:" + mntpoint + "/Hierarchies/HierarchySiriusLocalProduct/Processed_Parquet/Sirius"

  elif region.casefold() == 'U2K2'.casefold():
    regionID = "R"
    path = "dbfs:" + mntpoint + "/Hierarchies/HierarchyU2K2LocalProduct/Processed_Parquet/U2K2"
  
  elif region.casefold() == 'Cordillera'.casefold():
    regionID = "A"
    path = "dbfs:" + mntpoint + "/Hierarchies/HierarchyCordilleraLocalProduct/Processed_Parquet/"

  elif region.casefold() == 'Fusion'.casefold():
    regionID = "I"
    path = "dbfs:" + mntpoint + "/Hierarchies/HierarchyFusionLocalProduct/Processed_Parquet/Fusion"

  elif region.casefold() == 'SiriusVanguard'.casefold():
    regionID = "E"
    path = "dbfs:" + mntpoint + "/Hierarchies/HierarchySiriusVanguardProduct/Processed_Parquet"
  
  else:
    raise InvalidObjectAtSKULevelError()
  
  data_local = spark.read.format("delta").load(path)
  data_local.createOrReplaceTempView('vw_udl_local')
    
  df = spark.sql(f"""Select B.RegionID as RegionID, A.SKUCODE as GlobalSKUCode, A.ProductName as GlobalSKUDescription, B.MaterialNumber as LocalMaterialCode,B.MaterialDescription as LocalMaterialDescription,  B.* except(RegionID, MaterialNumber, MaterialDescription)
                  from vw_bdl_hgpl as A inner join vw_udl_local as B  
                  ON REPLACE(LTRIM(REPLACE(A.SKUCODE,'0',' ')),' ','0') = REPLACE(LTRIM(REPLACE(B.MaterialNumber,'0',' ')),' ','0') 
                  Where A.SKURegionID = '{regionID}'""")
  return df

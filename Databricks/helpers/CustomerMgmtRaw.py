# Databricks notebook source
# MAGIC %md
# MAGIC # CustomerMgmt is NOT a required table, but it's source XML file is used as source data for multiple downstream tables
# MAGIC * Downstream tables include historical Customer and Account Data
# MAGIC * Parse the XML once and store it as a source for both historical Customer and Account Data

# COMMAND ----------

# MAGIC %md
# MAGIC # Setup

# COMMAND ----------

import json

# with open("../../tools/traditional_config.json", "r") as json_conf:
#     table_conf = json.load(json_conf)["views"]["CustomerMgmt"]
table_conf = {
    "path": "Batch1",
    "filename": "CustomerMgmt.xml",
    "rowTag": "TPCDI:Action"
}
catalog = "main"

user_name = (
    spark.sql("select current_user()").collect()[0][0].split("@")[0].replace(".", "_")
)

dbutils.widgets.text("wh_db", f"{user_name}_TPCDI", "Root name of Target Warehouse")
dbutils.widgets.text("staging_db", "dbtpcdi_stg")
dbutils.widgets.text(
    "tpcdi_directory", "/Volumes/tpcdi/tpcdi_raw_data/tpcdi_volume/", "Directory where Raw Files are located"
)
dbutils.widgets.text("scale_factor", "10", "Scale factor")

# COMMAND ----------

# wh_db = f"{dbutils.widgets.get('wh_db')}_wh"
# staging_db = f"{dbutils.widgets.get('wh_db')}_stage"
wh_db = f"{dbutils.widgets.get('wh_db')}"
staging_db = f"{dbutils.widgets.get('staging_db')}"
scale_factor = dbutils.widgets.get("scale_factor")
tpcdi_directory = dbutils.widgets.get("tpcdi_directory")
files_directory = f"{tpcdi_directory}sf={scale_factor}"

# COMMAND ----------

# DBTITLE 1,Read the XML file and create a temp view on the raw data as all string values
spark.read.format("xml").options(rowTag=table_conf["rowTag"], inferSchema=False).load(
    f"""{files_directory}/{table_conf['path']}/{table_conf['filename']}"""
).createOrReplaceTempView("v_CustomerMgmt")

# COMMAND ----------

spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog}.{staging_db}")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     cast(Customer._C_ID as BIGINT) customerid,
# MAGIC     cast(Customer.Account._CA_ID as BIGINT) accountid,
# MAGIC     cast(Customer.Account.CA_B_ID as BIGINT) brokerid,
# MAGIC     nullif(Customer._C_TAX_ID, '') taxid,
# MAGIC     nullif(Customer.Account.CA_NAME, '') accountdesc,
# MAGIC     cast(Customer.Account._CA_TAX_ST as TINYINT) taxstatus,
# MAGIC     decode(_ActionType,
# MAGIC       "NEW","Active",
# MAGIC       "ADDACCT","Active",
# MAGIC       "UPDACCT","Active",
# MAGIC       "UPDCUST","Active",
# MAGIC       "CLOSEACCT","Inactive",
# MAGIC       "INACT","Inactive") status,
# MAGIC     nullif(Customer.Name.C_L_NAME, '') lastname,
# MAGIC     nullif(Customer.Name.C_F_NAME, '') firstname,
# MAGIC     nullif(Customer.Name.C_M_NAME, '') middleinitial,
# MAGIC     nullif(upper(Customer._C_GNDR), '') gender,
# MAGIC     try_cast(Customer._C_TIER as TINYINT) tier
# MAGIC     ,
# MAGIC     cast(Customer._C_DOB as DATE) dob,
# MAGIC     nullif(Customer.Address.C_ADLINE1, '') addressline1,
# MAGIC     nullif(Customer.Address.C_ADLINE2, '') addressline2,
# MAGIC     nullif(Customer.Address.C_ZIPCODE, '') postalcode,
# MAGIC     nullif(Customer.Address.C_CITY, '') city,
# MAGIC     nullif(Customer.Address.C_STATE_PROV, '') stateprov,
# MAGIC     nullif(Customer.Address.C_CTRY, '') country,
# MAGIC     nvl2(
# MAGIC       nullif(Customer.ContactInfo.C_PHONE_1.C_LOCAL, ''),
# MAGIC       concat(
# MAGIC           nvl2(nullif(Customer.ContactInfo.C_PHONE_1.C_CTRY_CODE, ''), '+' || Customer.ContactInfo.C_PHONE_1.C_CTRY_CODE || ' ', ''),
# MAGIC           nvl2(nullif(Customer.ContactInfo.C_PHONE_1.C_AREA_CODE, ''), '(' || Customer.ContactInfo.C_PHONE_1.C_AREA_CODE || ') ', ''),
# MAGIC           Customer.ContactInfo.C_PHONE_1.C_LOCAL,
# MAGIC           nvl(Customer.ContactInfo.C_PHONE_1.C_EXT, '')),
# MAGIC       cast(null as string)) phone1,
# MAGIC     nvl2(
# MAGIC       nullif(Customer.ContactInfo.C_PHONE_2.C_LOCAL, ''),
# MAGIC       concat(
# MAGIC           nvl2(nullif(Customer.ContactInfo.C_PHONE_2.C_CTRY_CODE, ''), '+' || Customer.ContactInfo.C_PHONE_2.C_CTRY_CODE || ' ', ''),
# MAGIC           nvl2(nullif(Customer.ContactInfo.C_PHONE_2.C_AREA_CODE, ''), '(' || Customer.ContactInfo.C_PHONE_2.C_AREA_CODE || ') ', ''),
# MAGIC           Customer.ContactInfo.C_PHONE_2.C_LOCAL,
# MAGIC           nvl(Customer.ContactInfo.C_PHONE_2.C_EXT, '')),
# MAGIC       cast(null as string)) phone2,
# MAGIC     nvl2(
# MAGIC       nullif(Customer.ContactInfo.C_PHONE_3.C_LOCAL, ''),
# MAGIC       concat(
# MAGIC           nvl2(nullif(Customer.ContactInfo.C_PHONE_3.C_CTRY_CODE, ''), '+' || Customer.ContactInfo.C_PHONE_3.C_CTRY_CODE || ' ', ''),
# MAGIC           nvl2(nullif(Customer.ContactInfo.C_PHONE_3.C_AREA_CODE, ''), '(' || Customer.ContactInfo.C_PHONE_3.C_AREA_CODE || ') ', ''),
# MAGIC           Customer.ContactInfo.C_PHONE_3.C_LOCAL,
# MAGIC           nvl(Customer.ContactInfo.C_PHONE_3.C_EXT, '')),
# MAGIC       cast(null as string)) phone3,
# MAGIC     nullif(Customer.ContactInfo.C_PRIM_EMAIL, '') email1,
# MAGIC     nullif(Customer.ContactInfo.C_ALT_EMAIL, '') email2,
# MAGIC     nullif(Customer.TaxInfo.C_LCL_TX_ID, '') lcl_tx_id,
# MAGIC     nullif(Customer.TaxInfo.C_NAT_TX_ID, '') nat_tx_id,
# MAGIC     to_timestamp(_ActionTS) update_ts,
# MAGIC     _ActionType ActionType
# MAGIC   FROM v_CustomerMgmt

# COMMAND ----------

# DBTITLE 1,Now insert into CustomerMgmt table with nested values parsed and data types applied
spark.sql(
    f"""
  CREATE TABLE IF NOT EXISTS {catalog}.{staging_db}.CustomerMgmt PARTITIONED BY (ActionType) TBLPROPERTIES (
    --delta.tuneFileSizesForRewrites = true,
    delta.autoOptimize.optimizeWrite = false
  ) AS SELECT
    cast(Customer._C_ID as BIGINT) customerid,
    cast(Customer.Account._CA_ID as BIGINT) accountid,
    cast(Customer.Account.CA_B_ID as BIGINT) brokerid,
    nullif(Customer._C_TAX_ID, '') taxid,
    nullif(Customer.Account.CA_NAME, '') accountdesc,
    try_cast(Customer.Account._CA_TAX_ST as TINYINT) taxstatus,
    decode(_ActionType,
      "NEW","Active",
      "ADDACCT","Active",
      "UPDACCT","Active",
      "UPDCUST","Active",
      "CLOSEACCT","Inactive",
      "INACT","Inactive") status,
    nullif(Customer.Name.C_L_NAME, '') lastname,
    nullif(Customer.Name.C_F_NAME, '') firstname,
    nullif(Customer.Name.C_M_NAME, '') middleinitial,
    nullif(upper(Customer._C_GNDR), '') gender,
    try_cast(Customer._C_TIER as TINYINT) tier,
    cast(Customer._C_DOB as DATE) dob,
    nullif(Customer.Address.C_ADLINE1, '') addressline1,
    nullif(Customer.Address.C_ADLINE2, '') addressline2,
    nullif(Customer.Address.C_ZIPCODE, '') postalcode,
    nullif(Customer.Address.C_CITY, '') city,
    nullif(Customer.Address.C_STATE_PROV, '') stateprov,
    nullif(Customer.Address.C_CTRY, '') country,
    nvl2(
      nullif(Customer.ContactInfo.C_PHONE_1.C_LOCAL, ''),
      concat(
          nvl2(nullif(Customer.ContactInfo.C_PHONE_1.C_CTRY_CODE, ''), '+' || Customer.ContactInfo.C_PHONE_1.C_CTRY_CODE || ' ', ''),
          nvl2(nullif(Customer.ContactInfo.C_PHONE_1.C_AREA_CODE, ''), '(' || Customer.ContactInfo.C_PHONE_1.C_AREA_CODE || ') ', ''),
          Customer.ContactInfo.C_PHONE_1.C_LOCAL,
          nvl(Customer.ContactInfo.C_PHONE_1.C_EXT, '')),
      cast(null as string)) phone1,
    nvl2(
      nullif(Customer.ContactInfo.C_PHONE_2.C_LOCAL, ''),
      concat(
          nvl2(nullif(Customer.ContactInfo.C_PHONE_2.C_CTRY_CODE, ''), '+' || Customer.ContactInfo.C_PHONE_2.C_CTRY_CODE || ' ', ''),
          nvl2(nullif(Customer.ContactInfo.C_PHONE_2.C_AREA_CODE, ''), '(' || Customer.ContactInfo.C_PHONE_2.C_AREA_CODE || ') ', ''),
          Customer.ContactInfo.C_PHONE_2.C_LOCAL,
          nvl(Customer.ContactInfo.C_PHONE_2.C_EXT, '')),
      cast(null as string)) phone2,
    nvl2(
      nullif(Customer.ContactInfo.C_PHONE_3.C_LOCAL, ''),
      concat(
          nvl2(nullif(Customer.ContactInfo.C_PHONE_3.C_CTRY_CODE, ''), '+' || Customer.ContactInfo.C_PHONE_3.C_CTRY_CODE || ' ', ''),
          nvl2(nullif(Customer.ContactInfo.C_PHONE_3.C_AREA_CODE, ''), '(' || Customer.ContactInfo.C_PHONE_3.C_AREA_CODE || ') ', ''),
          Customer.ContactInfo.C_PHONE_3.C_LOCAL,
          nvl(Customer.ContactInfo.C_PHONE_3.C_EXT, '')),
      cast(null as string)) phone3,
    nullif(Customer.ContactInfo.C_PRIM_EMAIL, '') email1,
    nullif(Customer.ContactInfo.C_ALT_EMAIL, '') email2,
    nullif(Customer.TaxInfo.C_LCL_TX_ID, '') lcl_tx_id,
    nullif(Customer.TaxInfo.C_NAT_TX_ID, '') nat_tx_id,
    to_timestamp(_ActionTS) update_ts,
    _ActionType ActionType
  FROM v_CustomerMgmt
"""
)

# COMMAND ----------

spark.sql(f"ANALYZE TABLE {catalog}.{staging_db}.CustomerMgmt COMPUTE STATISTICS FOR ALL COLUMNS")
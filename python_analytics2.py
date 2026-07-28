# -----------------------------------------------------------------------------
# LOAD SQL VIEWS INTO PANDAS DATAFRAMES
# -----------------------------------------------------------------------------
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

USER = 'root'
PASSWORD = 'ankur'  
HOST = 'localhost'
PORT = '3306'
DATABASE = 'sql_analytics2' 
 
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

#importing tables from SQL
sql_query1 = 'select * from v_payment_rates;'
sql_query2 = 'select * from v_delivery_status;'

df_payment = pd.read_sql(sql_query1, con=engine)
df_delivery = pd.read_sql(sql_query2, con=engine)

# Fixing the sender and receiver country columns
df_payment['sender_country'] = df_payment['sender_country'].str.strip().str.upper()
df_payment['receiver_country'] = df_payment['receiver_country'].str.strip().str.upper()

# Fixing the amount sent column
df_payment['amount_sent'] = pd.to_numeric(df_payment['amount_sent'], errors='coerce')
df_payment['amount_sent'] = df_payment['amount_sent'].abs()

# Fixing the fee charged column
df_payment['fee_charged'] = df_payment['fee_charged'].str.replace('$','')
df_payment['fee_charged'] = pd.to_numeric(df_payment['fee_charged'], errors='coerce')
df_payment['fee_charged'] = df_payment['fee_charged'].abs()

# Fixing the currency pair column
df_payment['currency_pair'] = df_payment['currency_pair'].str.replace('-','/')
df_payment['currency_pair'] = df_payment['currency_pair'].str.replace('_','/')
df_payment['currency_pair'] = df_payment['currency_pair'].str.strip().str.upper()
df_payment['currency_pair'] = df_payment['currency_pair'].fillna('No Record')

# Fixing the exchange rate column
df_payment['exchange_rate'] = pd.to_numeric(df_payment['exchange_rate'], errors='coerce')
df_payment['exchange_rate'] = df_payment['exchange_rate'].abs()

# Fixing the date column
df_payment['date'] = pd.to_datetime(df_payment['date'], dayfirst=False, errors='coerce').dt.strftime("%Y-%m-%d")

# Fixing the status column
df_delivery['status'] = df_delivery['status'].str.strip().str.title()
df_delivery['status'] = df_delivery['status'].fillna('No Record')

# Fixing the delivery_time_hours column
df_delivery['delivery_time_hours'] = pd.to_numeric(df_delivery['delivery_time_hours'], errors='coerce')
df_delivery['delivery_time_hours'] = df_delivery['delivery_time_hours'].abs()

# Fixing the failure_reason column
df_delivery.loc[(df_delivery['status'] == 'Failed') & (df_delivery['failure_reason'].isna()),'failure_reason'] = 'No Record' 

# Merged the DataFrames into one Merged DataFrame
merged_df = pd.merge(df_payment, df_delivery, on='payment_id', how='left')

# All the transactions that do not have complete records have been flaged here
# Applying condition to classify data
conditions = [
    merged_df['amount_sent'].isna() | merged_df['fee_charged'].isna(),
    merged_df['exchange_rate'].isna() | (merged_df['currency_pair'] == 'No Record'),
    (merged_df['status'] == 'Completed') & merged_df['delivery_time_hours'].isna(),
    (merged_df['status'] == 'No Record') | merged_df['status'].isna()
]
label = [
    'Missing Financials',
    'Missing Rate & Pair',
    'Missing Delivery Time',
    'Missing Status'
]
merged_df['audit_status'] = np.select(conditions, label, default='Passed')

# Exclude the Passed Transaction to get Failed Data
failed_records = merged_df[merged_df['audit_status'] != 'Passed']

# Report 1 Operational_Failure........................................................................
# Grouping the data by audit_status
Operational_Failure = failed_records.groupby('audit_status').agg(

    Transaction_Volume = ('payment_id','count'),
    Total_Impacted_Amount = ('amount_sent','sum'), 
    Fee_at_risk = ('fee_charged', 'sum')

).reset_index()
# Added the Financial Impact % column
total_bank_amount = merged_df['amount_sent'].sum()
Operational_Failure['Financial_Impact'] = ((Operational_Failure['Total_Impacted_Amount'] / total_bank_amount) * 100).round(2)
Operational_Failure['Financial_Impact'] = Operational_Failure['Financial_Impact'].map('{}%'.format)

Operational_Failure.to_excel('Operational_Failure.xlsx',index=False)
print('Operational_Failure.xlsx Exported Successfully')
#....................................................................................................

# Report 2 FX_Corridor...............................................................................
Passed_records = merged_df[merged_df['audit_status'] == 'Passed']

FX_Corridor = Passed_records.groupby('currency_pair').agg(

    Total_Fee_Revenue = ('fee_charged', 'sum'),
    Total_Amount_Sent = ('amount_sent', 'sum'),
    Avg_Delivery_Hours = ('delivery_time_hours', 'mean'),
    Top_Sender_Country = ('sender_country', lambda x: x.mode()[0]),  
).reset_index()
# Keep only valid currency pairs for the report
FX_Corridor = FX_Corridor[FX_Corridor['currency_pair'] != 'No Record']
# Round the Avg_Delivery_Hours
FX_Corridor['Avg_Delivery_Hours'] = FX_Corridor['Avg_Delivery_Hours'].round(2)
# Calculating % of Amount per pair
FX_Corridor['Amount_Share_(%)'] = ((FX_Corridor['Total_Amount_Sent']/FX_Corridor['Total_Amount_Sent'].sum())*100).round(1)
FX_Corridor['Amount_Share_(%)'] = FX_Corridor['Amount_Share_(%)'].map('{}%'.format)

FX_Corridor.to_excel('FX_Corridor.xlsx',index=False)
print('FX_Corridor.xlsx Exported Successfully')
#....................................................................................................

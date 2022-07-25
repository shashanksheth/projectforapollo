import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import create_engine as ce

# read in the file
df = pd.read_csv('firm_trades.csv',header=None)

# separate the 3 tables
order_df = df.loc[df[0]=="ORDER"]
route_df = df.loc[df[0]=="ROUTE"]
fill_df = df.loc[df[0]=="FILL"]

# discard reduntant columns
order_df = order_df.dropna(axis=1,how='all')
route_df = route_df.dropna(axis=1,how='all')
fill_df = fill_df.dropna(axis=1,how='all')

# save the header row
order_header = order_df.iloc[0]
route_header = route_df.iloc[0]
fill_header = fill_df.iloc[0]

# save the rest of the tables
order_df = order_df[1:].copy()
route_df = route_df[1:].copy()
fill_df = fill_df[1:].copy()

# add header row
order_df.columns = order_header
route_df.columns = route_header
fill_df.columns = fill_header

# order_df formatting
order_df = order_df.astype({"Order Number": int, "Amount": float, "Filled Amount": float})

# route_df formatting
route_df = route_df.astype({"Order Number": int, "Route Number": int, "Routed Amount": float, "Route Filled Amount": float, "Route Avg Price": float, "Route Comm Amount": float, "Route Comm Rate": float})

# fill_df formatting
fill_df = fill_df.astype({"Order Number": int, "Route Number": int, "Fill Amount": float, "Fill Price": float, "Exec Seq Num": int, "Prev Exec Seq Num": float})
fill_df = fill_df.astype({"Prev Exec Seq Num": int})

# create db engine
trades_db = ce('sqlite:///trades.sqlite')

# load dataframes
order_df.to_sql('orders',trades_db, index=False, if_exists='replace')
route_df.to_sql('routes',trades_db, index=False, if_exists='replace')
fill_df.to_sql('fills',trades_db, index=False, if_exists='replace')

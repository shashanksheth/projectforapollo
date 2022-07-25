import sqlalchemy
from datetime import datetime, timezone

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trades.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return (
        f"Welcome to the Trades API<br/><br/>"
        f"You can get <b/>detailed information</b> for trades using the following routes:<br/>"
        f"1. By entering an Order ID: /api/info/byorder/&ltorder_id&gt<br/>"
        f"2. By entering a Ticker: /api/info/byticker/&ltticker&gt<br/>"
        f"3. By entering a Date Range containing Start and End Dates using the YYYY-MM-DD format:/api/info/bydaterange/&ltstart_date&gt/&ltend_date&gt<br/><br/>"
        f"You can get <b/>summary statistics</b> for trades using the following routes:<br/>"
        f"1. By entering an Order ID: /api/summary/byorder/&ltorder_id&gt<br/>"
        f"2. By entering a Ticker: /api/summary/byticker/&ltticker&gt<br/>"
        f"3. By entering a Date Range containing Start and End Dates using the YYYY-MM-DD format: /api/summary/bydaterange/&ltstart_date&gt/&ltend_date&gt<br/><br/>"
    )

@app.route("/api/info/byorder/<order_id>")
def orderinfo(order_id):
    final_dict={}
    order_query = f"""SELECT `Order Number`, Ticker, Side, Amount, "20" ||  substr(`Create Date`,7,4) || "-" || substr( `Create Date`,1,2) || "-" || substr( `Create Date`,4,2) || "T" ||`Create Time`, `Security Name`, `Filled Amount` FROM orders WHERE `Order Number`={order_id};"""
    order_results = db.session.execute(order_query)
    for row in order_results:
        final_dict["order_id"]=row[0]
        final_dict["ticker"]=row[1]
        final_dict["side"]=row[2]
        final_dict["amount"]=int(round(row[3],0))
        final_dict["create_date_time"]=row[4]+str(datetime.now().astimezone())[-6::]
        final_dict["security_name"]=row[5]
        final_dict["filled_amount"]=int(round(row[6],0))
    
    fill_query = f"""SELECT `Fill Price`, `Fill Amount`, "20" ||  substr(`Fill As Of Date`,7,4) || "-" || substr( `Fill As Of Date`,1,2) || "-" || substr( `Fill As Of Date`,4,2) || "T" ||`Fill As Of Time` FROM fills WHERE `Order Number`={order_id};"""
    fill_results = db.session.execute(fill_query)
    fill_list = []
    
    for row in fill_results:
        fill_dict={}
        fill_dict["fill_price"]=round(row[0],2)
        fill_dict["fill_amount"]=int(round(row[1],0))
        fill_dict["fill_as_of_date_time"]=row[2]+str(datetime.now().astimezone())[-6::]
        fill_list.append(fill_dict)
    
    final_dict["fills"]=fill_list
    
    return jsonify(final_dict)

@app.route("/api/info/byticker/<ticker>")
def tickerinfo(ticker):
    final_dict={}
    order_query = f"""SELECT `Order Number`, Ticker, Side, Amount, "20" ||  substr(`Create Date`,7,4) || "-" || substr( `Create Date`,1,2) || "-" || substr( `Create Date`,4,2) || "T" ||`Create Time`, `Security Name`, `Filled Amount` FROM orders WHERE Ticker="{ticker}";"""
    order_results = db.session.execute(order_query)
    for row in order_results:
        final_dict["order_id"]=row[0]
        final_dict["ticker"]=row[1]
        final_dict["side"]=row[2]
        final_dict["amount"]=int(round(row[3],0))
        final_dict["create_date_time"]=row[4]+str(datetime.now().astimezone())[-6::]
        final_dict["security_name"]=row[5]
        final_dict["filled_amount"]=int(round(row[6],0))
    
    fill_query = f"""SELECT `Fill Price`, `Fill Amount`, "20" ||  substr(`Fill As Of Date`,7,4) || "-" || substr( `Fill As Of Date`,1,2) || "-" || substr( `Fill As Of Date`,4,2) || "T" ||`Fill As Of Time` FROM fills WHERE Ticker="{ticker}";"""
    fill_results = db.session.execute(fill_query)
    fill_list = []
    
    for row in fill_results:
        fill_dict={}
        fill_dict["fill_price"]=round(row[0],2)
        fill_dict["fill_amount"]=int(round(row[1],0))
        fill_dict["fill_as_of_date_time"]=row[2]+str(datetime.now().astimezone())[-6::]
        fill_list.append(fill_dict)
    
    final_dict["fills"]=fill_list
    
    return jsonify(final_dict)

@app.route("/api/info/bydaterange/<start_date>/<end_date>")
def daterangeinfo(start_date,end_date):
    start_date_reformat = start_date[5:7] + "/" + start_date[8:10] + "/" + start_date[2:4]
    end_date_reformat = end_date[5:7] + "/" + end_date[8:10] + "/" + end_date[2:4]
    final_list=[]
    order_query = f"""SELECT `Order Number`, Ticker, Side, Amount, "20" ||  substr(`Create Date`,7,4) || "-" || substr( `Create Date`,1,2) || "-" || substr( `Create Date`,4,2) || "T" ||`Create Time`, `Security Name`, `Filled Amount` FROM orders WHERE `Create Date` >= "{start_date_reformat}" AND `Create Date` <= "{end_date_reformat}";"""
    order_results = db.session.execute(order_query)
    for row in order_results:
        final_dict={}
        final_dict["order_id"]=row[0]
        final_dict["ticker"]=row[1]
        final_dict["side"]=row[2]
        final_dict["amount"]=int(round(row[3],0))
        final_dict["create_date_time"]=row[4]+str(datetime.now().astimezone())[-6::]
        final_dict["security_name"]=row[5]
        final_dict["filled_amount"]=int(round(row[6],0))
        
        fill_query = f"""SELECT `Fill Price`, `Fill Amount`, "20" ||  substr(`Fill As Of Date`,7,4) || "-" || substr( `Fill As Of Date`,1,2) || "-" || substr( `Fill As Of Date`,4,2) || "T" ||`Fill As Of Time` FROM fills WHERE `Order Number`={final_dict["order_id"]};"""
        fill_results = db.session.execute(fill_query)
        fill_list = []
        
        for row in fill_results:
            fill_dict={}
            fill_dict["fill_price"]=round(row[0],2)
            fill_dict["fill_amount"]=int(round(row[1],0))
            fill_dict["fill_as_of_date_time"]=row[2]+str(datetime.now().astimezone())[-6::]
            fill_list.append(fill_dict)
            
        final_dict["fills"]=fill_list
        final_list.append(final_dict)
    
    return jsonify(final_list)

@app.route("/api/summary/byorder/<order_id>")
def ordersummary(order_id):
    final_dict={}
    order_query = f"""SELECT `Order Number`, Ticker, avg(`Fill Price`),(AVG(`Fill Price`*`Fill Price`) - AVG(`Fill Price`)*AVG(`Fill Price`)), CASE WHEN `Route Status`="Part-filled" THEN NULL ELSE (strftime('%s', max(`Fill As Of Time`)) - strftime('%s', min(`Route Time`))) END FROM fills WHERE `ORDER NUMBER`={order_id};"""
    order_results = db.session.execute(order_query)
    for row in order_results:
        final_dict["order_id"]=row[0]
        final_dict["ticker"]=row[1]
        final_dict["average_price"]=row[2]
        final_dict["std_price"]=row[3] ** 0.5
        final_dict["fill_duration"]=row[4]
    
    return jsonify(final_dict)

@app.route("/api/summary/byticker/<ticker>")
def tickersummary(ticker):
    final_dict={}
    order_query = f"""SELECT `Order Number`, Ticker, avg(`Fill Price`), (AVG(`Fill Price`*`Fill Price`) - AVG(`Fill Price`)*AVG(`Fill Price`)), CASE WHEN `Route Status`="Part-filled" THEN NULL ELSE (strftime('%s', max(`Fill As Of Time`)) - strftime('%s', min(`Route Time`))) END FROM fills WHERE Ticker="{ticker}";"""
    order_results = db.session.execute(order_query)
    for row in order_results:
        final_dict["order_id"]=row[0]
        final_dict["ticker"]=row[1]
        final_dict["average_price"]=row[2]
        final_dict["std_price"]=row[3] ** 0.5
        final_dict["fill_duration"]=row[4]
    
    return jsonify(final_dict)

@app.route("/api/summary/bydaterange/<start_date>/<end_date>")
def daterangesummary(start_date,end_date):
    start_date_reformat = start_date[5:7] + "/" + start_date[8:10] + "/" + start_date[2:4]
    end_date_reformat = end_date[5:7] + "/" + end_date[8:10] + "/" + end_date[2:4]
    final_list=[]
    order_query = f"""SELECT `Order Number`, Ticker, `Create Date` FROM orders WHERE `Create Date` >= "{start_date_reformat}" AND `Create Date` <= "{end_date_reformat}";"""
    order_results = db.session.execute(order_query)
    for row in order_results:
        final_dict={}
        final_dict["order_id"]=row[0]
        final_dict["ticker"]=row[0]
        
        fills_query = f"""SELECT avg(`Fill Price`),(AVG(`Fill Price`*`Fill Price`) - AVG(`Fill Price`)*AVG(`Fill Price`)), CASE WHEN `Route Status`="Part-filled" THEN NULL ELSE (strftime('%s', max(`Fill As Of Time`)) - strftime('%s', min(`Route Time`))) END FROM fills WHERE `Order Number`={final_dict["order_id"]};"""
        fill_results = db.session.execute(fills_query)
        
        for row in fill_results:
            final_dict["average_price"]=row[0]
            final_dict["std_price"]=row[1] ** 0.5
            final_dict["fill_duration"]=row[2]
        
        final_list.append(final_dict)
    
    return jsonify(final_list)

if __name__ == '__main__':
    app.run(debug=True)
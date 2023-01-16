from config import db_config, imsi_from
import mysql.connector

hostname = db_config["HOST"]
user = db_config["USERNAME"]
password = db_config["PASSWORD"]
database = db_config["DATABASE"]
port = db_config["PORT"]


def mysql_connection():
    try:
        mysql_conn = mysql.connector.connect(host=hostname, user=user,
                                             database=database, password=password,
                                             port=port)
        print("connection created successfully...", mysql_conn)

        return mysql_conn

    except Exception as e:
        print("mysql connection error".format(e))


def sql_query_fetch(query):
    try:
        db = mysql_connection()
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()[0]
        for i in data:
            print(i)
        cursor.close()
        db.close()
        return data

    except Exception as e:
        print("Error : {} ".format(e))
        return None


def sql_query_fetch_data(query):
    try:
        db = mysql_connection()
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        for i in data:
            print(i)
        cursor.close()
        db.close()
        return data

    except Exception as e:
        print("Error : {} ".format(e))
        return None


# imsi = imsi_from["imsi_from"]
#
# q_transaction_id = f'select request_id from goup_notification_url where data ->> "$.imsi" like {imsi};'
# p = sql_query_fetch(q_transaction_id)
# print(p)

def srv():
    query = 'select data ->> "$.RequestParameters" FROM gconnect_stc_cmp_third_party_db.goup_notification_url ' \
            'where request_id = "GC20221221150102869_36426"; '

    datas = sql_query_fetch(query)
    print(datas)
    import re

    # Extract the key-value pairs using a regular expression
    pattern = re.compile(r'name:(.*?)#@#@#value:(.*?)#@#@#')
    matches = pattern.findall(str(datas))

    # Loop through the matches and print the key-value pairs
    for match in matches:
        name = match[0]
        value = match[1]
        value = value.replace('}', '')
        s = f'<ins:Parameter name="{name}" value="{value}"/>'
        print(s)



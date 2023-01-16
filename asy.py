from config import imsi_from, api_urls, db_config
import requests
from test import sql_query_fetch, sql_query_fetch_data
from xml.etree.ElementTree import Element, SubElement, tostring


class Activation:
    def __init__(self):
        pass

    # def fpms():
    #     payload = f"""
    #     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    #     xmlns:fpm="http://fpmicroservice.stc.com">
    #    <soapenv:Header/>
    #    <soapenv:Body>
    #       <fpm:performSIMOperation>
    #          <details>
    #             <actionType>Activation</actionType>
    #             <transactionId>{transaction_id_fetch}</transactionId>
    #
    #             <sim>
    #                <msisdn>{msisdn_fetch}</msisdn>
    #                <imsi>{imsi}</imsi>
    #             </sim>
    #          </details>
    #       </fpm:performSIMOperation>
    #    </soapenv:Body>
    # </soapenv:Envelope>
    # """
    #
    #     headers = {
    #         'Content-Type': 'text/xml; charset=utf-8',
    #         # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    #         # Chrome/102.0.0.0 Safari/537.36',
    #         'Authorization': 'Basic c3RjX2FkbWluOmdsb2JldG91Y2g='
    #     }
    #
    #     response = requests.request("POST", fpms_url, headers=headers, data=payload)
    #
    #     print(response.text)
    #     print(response)

    def fpms(self):
        imsi = imsi_from['imsi_from']
        str_results = [str(x) for x in imsi]

        fpms_url = api_urls["fpms_api_url"]

        q_transaction_id = 'select distinct(data->> "$.msisdn") as imsi ,request_id from goup_notification_url where data ->> "$.imsi" in ({}) and api_group_name="Activation" group by data ->> "$.msisdn"  order by id desc;'.format(
            ",".join([str(i) for i in str_results]))
        print("query : ", q_transaction_id)

        transaction_id = sql_query_fetch_data(q_transaction_id)

        for i in transaction_id:
            print('transaction_id : ', i[1])
            print('msisdn : ', i[0].decode())

        headers = {
            "Content-Type": "text/xml;charset=utf-8",
            "Authorization": "Basic c3RjX2FkbWluOmdsb2JldG91Y2g=",
            "SoapAction": ""
        }

        for i in transaction_id:
            payload = f"""<?xml version="1.0" encoding="utf-8"?>
                                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                                xmlns:per="http://permission.fingerprint.webservice.stc.comarch.com/">
                               <soapenv:Header/>
                               <soapenv:Body>
                                  <per:setOperationStatus>
                                     <transactionId>{i[1]}</transactionId>
                                     <operationResult>
                                        <result>
                                           <decission>YES</decission>
                                           <msisdn>{i[0].decode()}</msisdn>
                                        </result>
                                     </operationResult>
                                  </per:setOperationStatus>
                               </soapenv:Body>
                            </soapenv:Envelope>"""

            print(payload)
            response = requests.request("POST",
                                        fpms_url,
                                        headers=headers, data=payload)
            print(response.text)
            print(response.status_code)

    def sim_provisioning(self):
        imsi = imsi_from['imsi_from']
        str_results = [str(x) for x in imsi]

        provisioning_url = api_urls["sim_provisioning_url"]

        query2 = 'select  data ->> "$.RequestParameters" ,request_id FROM gconnect_stc_cmp_third_party_db.goup_notification_url where data ->> "$.imsi" in ({}) and api_group_name="Activation" group by data ->> "$.msisdn" order by id desc;'.format(
            ",".join([str(i) for i in str_results]))

        print('query : \n', query2)
        datas = sql_query_fetch_data(query2)

        for x in datas:
            print('transaction_id : ', x[1])
            import re

            # Extract the key-value pairs using a regular expression
            pattern = re.compile(r'name:(.*?)#@#@#value:(.*?)#@#@#')
            matches = pattern.findall(str(x[0].decode()))

            string_list = []
            # Loop through the matches and print the key-value pairs
            for match in matches:
                name = match[0]
                value = match[1]
                value = value.replace('}', '')
                s = f'<ins:Parameter name="{name}" value="{value}"/>'
                string_list.append(s)
            params = "\n".join(string_list)

            # Loop through the matches and print the key-value pairs
            payload = """
                        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ins="http://soa.comptel.com/2011/02/instantlink">
           <soap:Header>
              <wsse:Security soap:mustUnderstand="true" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                 <wsse:UsernameToken wsu:Id="SOAI_req_SOAI" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:Username>stcuser</wsse:Username>
                    <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">***************</wsse:Password>
                 </wsse:UsernameToken>
              </wsse:Security>
           </soap:Header>
           <soap:Body>
              <ins:CreateRequest>
                 <ins:RequestHeader>
                    <ins:NeType>ILGSM</ins:NeType>
                      <ins:OrderNo>{}</ins:OrderNo>
                            <ins:Priority>3</ins:Priority>
                                <ins:ReqUser>stcuser</ins:ReqUser>
                 </ins:RequestHeader>
                 <ins:RequestParameters>
                  {}
                 </ins:RequestParameters>
              </ins:CreateRequest>
           </soap:Body>
        </soap:Envelope>
        """

            headers = {
                "Content-Type": "text/xml; charset=utf-8",
                "SoapAction": ""
            }

            response = requests.request("POST", provisioning_url, headers=headers,
                                        data=payload.format(x[1], params))
            print("Request Parameters : \n", payload.format(x[1], params))
            print(response)


a = Activation()
a.sim_provisioning()

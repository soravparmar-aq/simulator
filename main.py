from config import imsi_from, msisdn_from, api_urls, db_config
import requests
from test import sql_query_fetch


class Activation:
    def __init__(self):
        pass

    imsi = imsi_from['imsi_from']

    fpms_url = api_urls["fpms_api_url"]
    provisioning_url = api_urls["sim_provisioning_url"]

    q_transaction_id = f'select request_id from goup_notification_url where data ->> "$.imsi" like {imsi} order by request_id desc; '
    q_msisdn = f'select data ->> "$.msisdn" as msisdn from goup_notification_url where data ->> "$.imsi" like {imsi} order by request_id desc; '

    transaction_id = sql_query_fetch(q_transaction_id)
    msisdn = sql_query_fetch(q_msisdn)

    transaction_id_fetch = ''.join(transaction_id)
    print("transaction_id : ", transaction_id_fetch)

    msisdn_fetch = ''.join(msisdn)
    # msisdn_fetch = p.decode('utf-8')

    print('MSISDN : ', msisdn_fetch)

    print('IMSI : ', imsi)

    # try:
    #     client = SoapClient(wsdl=fpms_url, ns="web", trace=True)
    #     client['AuthHeaderElement'] = {"Authorization": "Basic c3RjX2FkbWluOmdsb2JldG91Y2g=", "Content-Type": "text/xml; charset=utf-8"}
    #     list_of_services = [service for service in client.services]
    #     print(list_of_services)
    #
    # except Exception as e:
    #     print(e)

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
        headers = {
            "Content-Type": "text/xml;charset=utf-8",
            "Authorization": "Basic c3RjX2FkbWluOmdsb2JldG91Y2g=",
            "SoapAction": ""
        }

        payload = f"""<?xml version="1.0" encoding="utf-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:per="http://permission.fingerprint.webservice.stc.comarch.com/">
               <soapenv:Header/>
               <soapenv:Body>
                  <per:setOperationStatus>
                     <transactionId>{self.transaction_id_fetch}</transactionId>
                     <operationResult>
                        <result>
                           <decission>YES</decission>
                           <msisdn>{self.msisdn_fetch}</msisdn>
                        </result>
                     </operationResult>
                  </per:setOperationStatus>
               </soapenv:Body>
            </soapenv:Envelope>"""

        response = requests.request("POST",
                                    self.fpms_url,
                                    headers=headers, data=payload)
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:

            query = f'select data ->> "$.RequestParameters" FROM gconnect_stc_cmp_third_party_db.goup_notification_url where ' \
                    f'request_id = "{self.transaction_id_fetch}";'

            datas = sql_query_fetch(query)
            print(datas)
            import re

            # Extract the key-value pairs using a regular expression
            pattern = re.compile(r'name:(.*?)#@#@#value:(.*?)#@#@#')
            matches = pattern.findall(str(datas))

            string_list = []
            # Loop through the matches and print the key-value pairs
            for match in matches:
                name = match[0]
                value = match[1]
                value = value.replace('}', '')
                s = f'<ins:Parameter name="{name}" value="{value}"/>'
                string_list.append(s)
            x = "\n".join(string_list)

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

            response = requests.request("POST", self.provisioning_url, headers=headers,
                                        data=payload.format(self.transaction_id_fetch, x))
            print("Request Parameters : \n", payload.format(self.transaction_id_fetch, x))
            print(response)


a = Activation()
a.fpms()

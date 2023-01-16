import json

from test import sql_query_fetch, srv

srv()



# for i in datas:
#     print("fetch Parameters : \n", str(i))
#
# file1 = open('sql_query_result.txt', 'w')
# file1.write(str(i))
# file1.close()
#
# f2 = open('sql_query_result.txt', 'rt')
#
# data = str(i)
# data = data.replace('#@#@#', ',')
# data = data.replace('Parameter', "'Parameter'")
# data = data.replace('name:', "'name':'")
# data = data.replace('value:', "'value':'")
# data = data.replace(',', "',")
# data = data.replace("}'", "}'")
# data = data.replace("',{", ",{")
# data = data.replace("},", "'},")
# data = data.replace("}]", "'}]")
# f2.close()
#
#
# def get_value(name):
#     z1 = f"{data}"
#
#     b = eval(z1)
#
#     for item in b['Parameter']:
#         if item[f'name'] == name:
#             return item['value']
#
#
# n = ['SO1_ACTIONCODE', 'SO1_TECHNICALPRODUCT', 'SO1_SUBS_PROFILE', 'SO1_PROFILEID']
#
#
# so1_action_code = 'SO1_ACTIONCODE'
# value = get_value(so1_action_code)
# print("SO1_ACTIONCODE :", value)
#
# so1_technical_product = 'SO1_TECHNICALPRODUCT'
# v2 = get_value(so1_technical_product)
# print("SO1_TECHNICALPRODUCT :", v2)

# so1_subs_profile = 'SO1_SUBS_PROFILE'
# v3 = get_value(so1_subs_profile)
# print('SO1_SUBS_PROFILE : ', v3)

# so1_profile_id = 'SO1_PROFILEID'
# v4 = get_value(so1_profile_id)
# print('SO1_PROFILEID : ', v4)


# query = """
# SELECT IF(data->>'$.RequestParameters' LIKE '%name:SO1_SUBS_PROFILE#@#@#value:%',
#     SUBSTRING_INDEX(SUBSTRING_INDEX(data->>'$.RequestParameters', 'name:SO1_SUBS_PROFILE#@#@#value:', -1), '}', 1),
#     NULL) AS SO1_SUBS_PROFILE,
# IF(data->>'$.RequestParameters' LIKE '%name:SO1_TECHNICALPRODUCT#@#@#value:%',
#     SUBSTRING_INDEX(SUBSTRING_INDEX(data->>'$.RequestParameters', 'name:SO1_TECHNICALPRODUCT#@#@#value:', -1), '}', 1),
#     NULL) AS SO1_TECHNICALPRODUCT,
# IF(data->>'$.RequestParameters' LIKE '%name:SO1_PROFILEID#@#@#value:%',
#     SUBSTRING_INDEX(SUBSTRING_INDEX(data->>'$.RequestParameters', 'name:SO1_PROFILEID#@#@#value:', -1), '}', 1),
#     NULL) AS SO1_PROFILEID,
# IF(data->>'$.RequestParameters' LIKE '%name:SO1_ACTIONCODE#@#@#value:%',
#     SUBSTRING_INDEX(SUBSTRING_INDEX(data->>'$.RequestParameters', 'name:SO1_ACTIONCODE#@#@#value:', -1), '}', 1),
#     NULL) AS SO1_ACTIONCODE
# FROM gconnect_stc_cmp_third_party_db.goup_notification_url
# where request_id = 'GC20221221150102869_36426';
# """
#
# s = sql_query_fetch(query)
# SO1_SUBS_PROFILE = s[0]
# SO1_TECHNICALPRODUCT = s[1]
# SO1_PROFILEID = s[2]
# SO1_ACTIONCODE = s[3]
#
# s1 = [SO1_ACTIONCODE, SO1_PROFILEID, SO1_TECHNICALPRODUCT, SO1_SUBS_PROFILE]
#
# for i in s1:
#     s2 = f'<ins:Parameter name="SO1_PROFILEID" value="{i}"/>'
#     print(s2)

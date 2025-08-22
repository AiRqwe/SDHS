import requests
import jsonpath
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiRequest:




    def login_api(self):
        
        url="http://172.160.2.160:8084/auth/user/login"
        header={"accept":"application/json, text/plain, */*",
        "content-type":"application/json;charset=UTF-8"}
        json={"username":"jtdiaodu",
        "password":"Sdhs@123456a",
        "captcha":"1","uuid":"b3f07254-2bfa-4434-8208-198c3ed78819",
        "appId":"its_portal"}
        logger.info(f"请求URL: {url}")
        logger.info(f"请求头: {header}")
        logger.info(f"请求体: {json}")
        result=requests.post(url,headers=header,json=json)
        logger.info(f"响应内容: {result.json()}")
        values=jsonpath.JSONPath('$..access_token').parse(result.json())
        ApiRequest.token=values[0]
        logger.info(f"获取的token: {ApiRequest.token}")
    def query_api(self):
        url="http://172.160.2.160:8084/emergency/event/dispatch/list"
        header={"accept":"application/json, text/plain, */*",
            "Authorization":f"Bearer {ApiRequest.token}",
            "Content-Type":"application/json;charset=UTF-8"
        }
        json={"page":1,"limit":10,
        "eventType":"","deptId":"6cc569437d354990b11f48d9864bc70a",
        "startDate":"2025-03-01 00:00:00","endTime":"2025-03-06 23:59:59",
        "eventSource":"","warningStatus":"1,2",
        "importantEvent":"3","ifForwardClearance":""
        }
        logger.info(f"请求URL: {url}")
        logger.info(f"请求头: {header}")
        logger.info(f"请求体: {json}")
        qu_result=requests.post(url,headers=header,json=json)
        logger.info(f"响应内容: {qu_result.json()}")

if __name__ == '__main__':
    api_request = ApiRequest()
    print("-------------------登录接口-----------------")
    api_request.login_api()
    print("-------------------查询接口-----------------")
    api_request.query_api()

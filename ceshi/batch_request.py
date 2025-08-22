import json
import pandas as pd
import requests
import time
import logging
from typing import List, Dict

class BatchRequest:
    def __init__(self, excel_path: str, output_path: str):
        self.excel_path = excel_path
        self.output_path = output_path
        self.results = []
        
        # 配置日志
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # 文件日志
        file_handler = logging.FileHandler('batch_request.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # 控制台日志
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def load_data(self) -> List[Dict]:
        """加载Excel数据"""
        try:
            df = pd.read_excel(self.excel_path, usecols=['login_name'], nrows=5)
            
            return df.to_dict('records')
        except KeyError as e:
            self.logger.error(f"Excel表格缺少必要列: {e}")
            return []

    def send_request(self, params: Dict) -> Dict:
        """发送单个请求（需根据实际接口修改）"""
        try:
            # 示例请求配置，需替换实际接口参数
            response = requests.post(
                url='http://172.160.1.168:8600/uniteuser/sys/user/listPage',
                headers={
                    'Accept': 'application/json',
                    'x_ticket': '602cfce9420e4d15ab39f690ea6e83d3_1:c8b149725e064053a09fb77244ebf488',
                    'Cookie':"JSESSIONID=ea0b5c59-e346-430e-b0da-cb3094726205"
                },
                files=[(k, (None, str(v))) for k, v in params.items()],
                timeout=10
            )
            response_data = response.json()
            self.logger.info(f"完整响应内容：{json.dumps(response_data, ensure_ascii=False)}")
            return {
                'status_code': response.status_code,
                'response': response_data,
                'success': response.status_code == 200,
                'id': response_data.get('data', {}).get('list', [{}])[0].get('id', None)
            }
            
        except Exception as e:
            self.logger.error(f"请求失败: {e}", exc_info=True)
            return {'error': str(e)}

    def send_put_request(self, user_id):
        """发送PUT请求更新用户信息"""
        """查看用户信息接口"""
        try:
            put_url = f'http://172.160.1.168:8600/uniteuser/sys/user/users/{user_id}'
            response = requests.put(
                url=put_url,
                headers={
                    'Accept': 'application/json',
                    'x_ticket': '602cfce9420e4d15ab39f690ea6e83d3_1:c8b149725e064053a09fb77244ebf488',
                    'Cookie': "JSESSIONID=ea0b5c59-e346-430e-b0da-cb3094726205"
                },
                timeout=10
            )
            return response.json()

        except Exception as e:
            self.logger.error(f"PUT请求失败: {e}", exc_info=True)
            return {'error': str(e)}
            
    def process(self, delay: float = 1.0):
        """处理批量请求"""
        data = self.load_data()
        if not data:
            self.logger.error("加载的数据为空，请检查Excel文件格式和内容")
            return
        self.logger.info(f"成功加载{len(data)}条待处理数据，示例第一条数据: {data[0]}")
    
        for index, row in enumerate(data):
            self.logger.info(f"正在处理第 {index+1}/{len(data)} 条数据")
            if index == 5:  # 测试时仅处理前两条
              break
        
            request_params = {
                "page": 1,
                "size": 10,
                "onlyShowCurrentUnitUsers": "false",
                "name": row.get('login_name'),
        }
            self.logger.info(f"请求参数: {request_params}")
        
            result = self.send_request(request_params)
            self.logger.debug(f"接口原始响应: {json.dumps(result, ensure_ascii=False)}")
        
        # 记录结果
            record = {
                'original_data': row,
                'request_params': request_params,
                'response': result,
                'ids': [item.get('id') for item in result.get('response', {}).get('data', {}).get('list', []) if item.get('id')]
            }
            
            # 当获取到有效IDs时发送PUT请求
            for user_id in record['ids']:
                put_response = self.send_put_request(user_id)
                self.logger.info(f"PUT请求完整响应: {json.dumps(put_response, ensure_ascii=False)}")
                record.setdefault('put_responses', []).append(put_response)
                self.logger.info(f"用户{user_id}更新响应：{put_response}")
            self.results.append(record)
            time.sleep(delay)

        # 提取并保存结果
        result_list = []
        for r in self.results:
            response_data = r['response'].get('response', {})
            # data = response_data.get('data', {})
            items = response_data.get('data', {}).get('list', [])
            
            if not items:
                continue
        
            for item in items:
                # 创建字典存储ID和mobile的对应关系
                id_mobile_map = {}
                if r.get('put_responses'):
                    for put_resp in r['put_responses']:
                        if put_resp.get('data') and put_resp['data'].get('mobile') and put_resp['data'].get('id'):
                            id_mobile_map[put_resp['data']['id']] = put_resp['data']['mobile']
                
                # 获取当前item的mobile
                current_mobile = id_mobile_map.get(item.get('id', ''), '未找到')
                
                result_list.append({
                    'login_name': r['original_data'].get('login_name', ''),
                    'loginName': item.get('loginName', '未找到'),
                    'deptName': item.get('deptName', '未找到'),
                    '用户ID': item.get('id', '未获取'),
                    'PUT响应状态': r.get('put_responses', [{}])[0].get('code', '未执行') if r.get('put_responses') else '未执行',
                    'result': '添加成功' if response_data.get('message') == 'SUCCESS' else '系统中有账号',
                    'mobile': current_mobile
                })
    
            if result_list:
                result_df = pd.DataFrame(result_list)
                result_df.to_excel(self.output_path, index=False)
                self.logger.info(f"结果已保存至 {self.output_path}")
            else:
                self.logger.warning("无有效数据可保存")
if __name__ == "__main__":
    # 使用示例
    processor = BatchRequest(
        excel_path='C:/Users/jieho/Desktop/input.xlsx',
        output_path='C:/Users/jieho/Desktop/output.xlsx'
    )
    processor.process(delay=1.0)
import re
import requests
import json
from typing import List, Dict
import pandas as pd

class DocumentParser:
    def __init__(self, document_path: str, api_key: str = "your_api_key"):
        self.document_path = document_path
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"

    def parse(self) -> Dict[str, List[str]]:
        """解析需求文档，返回结构化数据"""
        
        with open(self.document_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 调用AI大模型进行文档解析
        ai_result = self._call_ai(content)
            
            # 保留原有正则解析作为基础
        base_result = self._parse_with_regex(content)
            
            # 合并AI解析和正则解析结果
        return self._merge_results(ai_result, base_result)

            # 解析功能模块
        modules = re.findall(r'## (.*?)\n', content)
            
            # 解析验证点
        verification_points = re.findall(r'### (.*?)\n', content)
            
            # 解析前置条件
        preconditions = re.findall(r'前置条件：(.*?)\n', content)
            
            # 解析测试步骤
        test_steps = re.findall(r'测试步骤：(.*?)\n', content)
            
            # 解析预期结果
        expected_results = re.findall(r'预期结果：(.*?)\n', content)
            
        return {
                '功能模块': modules,
                '验证点': verification_points,
                '前置条件': preconditions,
                '测试步骤': test_steps,
                '预期结果': expected_results
            }

    def _call_ai(self, content: str) -> Dict:
        """调用AI大模型API进行文档解析"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-code-13b",
            "messages": [
                {
                    "role": "user",
                    "content": f"请解析以下需求文档，返回结构化数据：\n{content}"
                }
            ],
            "temperature": 0.3
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return json.loads(response.json()['choices'][0]['message']['content'])
        except Exception as e:
            print(f"调用AI大模型失败: {e}")
            return {}

    def _parse_with_regex(self, content: str) -> Dict:
        """使用正则表达式进行基础解析"""
        modules = re.findall(r'## (.*?)\n', content)
        verification_points = re.findall(r'### (.*?)\n', content)
        preconditions = re.findall(r'前置条件：(.*?)\n', content)
        test_steps = re.findall(r'测试步骤：(.*?)\n', content)
        expected_results = re.findall(r'预期结果：(.*?)\n', content)
        return {
            '功能模块': modules,
            '验证点': verification_points,
            '前置条件': preconditions,
            '测试步骤': test_steps,
            '预期结果': expected_results
        }

    def _merge_results(self, ai_result: Dict, base_result: Dict) -> Dict:
        """合并AI解析和正则解析结果"""
        merged = {}
        for key in base_result.keys():
            merged[key] = list(set(base_result[key] + ai_result.get(key, [])))
        return merged
       


class TestCaseGenerator:
    def __init__(self, parsed_data: Dict[str, List[str]]):
        self.parsed_data = parsed_data

    def generate_test_cases(self) -> List[Dict[str, str]]:
        """根据解析后的数据生成测试用例"""
        test_cases = []
        try:
            for i in range(len(self.parsed_data['功能模块'])):
                test_case = {
                    '功能模块': self.parsed_data['功能模块'][i],
                    '验证点': self.parsed_data['验证点'][i],
                    '前置条件': self.parsed_data['前置条件'][i],
                    '测试步骤': self.parsed_data['测试步骤'][i],
                    '预期结果': self.parsed_data['预期结果'][i]
                }
                test_cases.append(test_case)
            return test_cases
        except Exception as e:
            print(f"生成测试用例时出错: {e}")
            return []


class ExcelExporter:
    def __init__(self, test_cases: List[Dict[str, str]]):
        self.test_cases = test_cases

    def export(self, output_path: str):
        """将测试用例导出到Excel文件"""
        df = pd.DataFrame(self.test_cases)
        df.to_excel(output_path, index=False)


class TestFramework:
    def __init__(self, document_path: str):
        self.document_path = document_path

    def run(self, output_path: str):
        """运行整个测试框架流程"""
        parser = DocumentParser(self.document_path)
        parsed_data = parser.parse()

        generator = TestCaseGenerator(parsed_data)
        test_cases = generator.generate_test_cases()

        exporter = ExcelExporter(test_cases)
        exporter.export(output_path)
import ast
import requests
import json
from typing import List, Dict, Optional


class CodeAnalyzer:
    """代码分析框架核心类"""

    def __init__(self, deepseek_api_key: str):
        self.rules = []
        self.deepseek_api_key = deepseek_api_key
        self.base_url = "https://api.deepseek.com/v1"

    def add_rule(self, rule):
        """添加自定义检测规则"""
        self.rules.append(rule)

    def _parse_code(self, code: str) -> ast.Module:
        """使用AST解析代码结构"""
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"语法错误: {e}")

    def _apply_rules(self, tree: ast.Module) -> List[Dict]:
        """应用自定义规则检测"""
        findings = []
        for rule in self.rules:
            inspector = rule()
            inspector.visit(tree)
            findings.extend(inspector.get_findings())
        return findings

    def _call_deepseek(self, code: str) -> Dict:
        """调用DeepSeek API进行深度分析"""
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-code-13b",
            "messages": [
                {
                    "role": "user",
                    "content": f"请分析以下代码的安全漏洞和代码质量问题，用JSON格式返回结果：\n{code}"
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
            return {"error": str(e)}

    def analyze(self, code: str) -> Dict:
        """执行完整分析流程"""
        # 基础分析
        try:
            tree = self._parse_code(code)
            rule_findings = self._apply_rules(tree)
        except Exception as e:
            rule_findings = [{"type": "ERROR", "message": str(e)}]

        # 大模型分析
        ai_analysis = self._call_deepseek(code)

        return {
            "static_analysis": rule_findings,
            "ai_analysis": ai_analysis
        }


# 示例检测规则（可扩展）
class HardcodedPasswordRule(ast.NodeVisitor):
    """检测硬编码密码规则"""

    def __init__(self):
        self.findings = []
        self.password_keywords = ['password', 'passwd', 'pwd']

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.lower() in self.password_keywords:
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    self.findings.append({
                        "severity": "HIGH",
                        "type": "硬编码密码",
                        "line": node.lineno,
                        "message": "发现潜在的硬编码密码"
                    })

    def get_findings(self):
        return self.findings


# 使用示例
if __name__ == "__main__":
    # 初始化分析器
    analyzer = CodeAnalyzer(deepseek_api_key="sk-b4bd5e98959a45b799c7491f64666ee2")
    analyzer.add_rule(HardcodedPasswordRule)

    # 待检测代码
    test_code = """
    db_config = {
        'user': 'admin',
        'password': '123456',  # 硬编码密码
        'host': 'localhost'
    }
    """

    # 执行分析
    results = analyzer.analyze(test_code)

    # 输出结果
    print("静态分析结果：")
    for finding in results['static_analysis']:
        print(f"[Line {finding['line']}] {finding['message']}")

    print("\nAI分析结果：")
    print(json.dumps(results['ai_analysis'], indent=2, ensure_ascii=False))
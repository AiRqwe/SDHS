import requests




class AddUser:

    def __init__(self,url,head,data):
        self.url=url
        self.head=head
        self.data=data

    def qurey(self):
        url="https://szpt.nmgjtjt.com:19000/sys/user/page?deptId=&username=18804940902&page=1&limit=10"
        head={
            "Accept":"application/json",
            "authorization":"Bearer 8c8ab0d6-a9ad-4a1e-b1ff-70696b35ab38",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"

     }
        try:
            self.response = requests.post(url=url, headers=head, data=None)
            self.response.raise_for_status()
            return self.response.json()
        except requests.exceptions.RequestException as e:
            print(f"\033[31m请求失败: {e}\033[0m")
            return None

    def get_user_details(self):
        try:
            result = self.response.json()
            print(f"完整响应内容：{result}")  # 添加响应日志
            data = result.get('data', {})
            if not data:
                raise ValueError("响应中缺少data字段")
            record_list = data.get('record', [])
            if not isinstance(record_list, list):
                raise ValueError(f"record字段类型错误，应为列表，实际为{type(record_list)}")
            if not isinstance(record_list, list) or len(record_list) == 0:
                print(record_list)
                raise ValueError("响应中的record列表为空，可能用户不存在")
            if not (user_id := record_list[0].get('id')):
                raise ValueError("响应中未找到用户ID")
            
            new_url = f"{self.url.rstrip('/')}/{user_id}"
            response = requests.get(new_url, headers=self.head)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"\033[31m用户详情获取失败: {e}\033[0m")
            return None




if __name__=="__main__":
       url="https://szpt.nmgjtjt.com:19000/sys/user"
       head={
            "Accept":"application/json",
            "authorization":"Bearer 8c8ab0d6-a9ad-4a1e-b1ff-70696b35ab38",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"

     }
       qw = AddUser(url, head, data=None)
       if (result := qw.qurey()) is not None:
                print("\033[32m初始请求成功:\033[0m", result)
       if (details := qw.get_user_details()) is not None:
                print("\033[34m用户详细信息:\033[0m", details)


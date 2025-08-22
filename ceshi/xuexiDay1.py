

# name='王鑫'
# age="15"
# hight="1.80"

# print(f"姓名:{name},年龄:{age},身高:{hight}")
# name=input('请输入你的姓名：')
# print(f"你好，{name }")
# num=42
# text='文字'
# num2=2.3
# flag=True
# print(f"num类型是{type(num)}")
# print(f"text类型是{type(text)}")
# print(f"text类型是{type(num2)}")
# print(f"text类型是{type(flag)}")

# a=53
# b=12
# print(f"a+b={a+b}")
# print(f"a*b={a*b}")
# print(f"a/b={a/b}")
# print(f"a//b={a//b}")
# print(f"a%b={a%b}")
# print(f"a**b={a**b}")
# txt="trererr,rewtwtwtret"
#
# print(f"原字符串：{txt}")
# print(f"大写：{txt.upper()}")
# print(f"转小写：{txt.lower()}")
# print(f"字符长度：{len(txt)}")
# print(f"替换：{txt.replace("trererr,rewtwtwtret","python,xuexi")}")


# print(f"第一行\n第二行")
# print(f"制表符:质保\t分隔")
# text="python pythongramming"
#
# print(f"前6个字符",{text[:6]})
# print(f"前11个字符",{text[7:]})
# print(f"中间字符",{text[7:10]})
# print(f"每隔一个字符",{text[::2]})
# print(f"反转字符",{text[::-1]})

# try:
#     age=int(input("请输入年龄："))
#     hight=float(input("请输入身高："))
#     print(f"年龄为{age}，身高为{hight}米")
# except ValueError:
#     print("输入格式错误")
# text='hello word'
# print(f"hello in text{'hello'in text}")
# print(f"python in text{'python'not in text}")

# num=[1,2,3,4,5,6,7]
#
# print(f"2 in text{2 in num}")
# print(f"10 in text{10 in num}")\
# a=[1,2,3]
# b=[1,2,3]
# c=a
# print(f"a等于c:{a==c}")
# print(f"a等于b:{a is b}")
# print(f"a等于c:{a is c}")

def sip_1232():
    try:
        num1=float(input(f"请输入数字："))
        op=input(f"请输入+ — * /：" )
        num2 = float(input(f"请输入数字："))
        if op == '+':
             result=num1 + num2

        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                print(f"除数不能为零！")
                return
        else:
            print(f"错误的运算符")
            return
        print(f"结果：{num1}{op}{num2}={result}")

    except ValueError:
        print(f"请输入有效数字")



if __name__ == '__main__':
    sip_1232()



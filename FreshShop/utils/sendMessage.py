#coding:utf-8
import requests

url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"

account = ""    #用户
password = ""   #密码
mobile = ""  #手机号
content = "您的验证码是：20191220。请不要把验证码泄露给其他人。"  #短信内容

#定义请求的头部
headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
}

#定义请求的数据
data = {
    "account": account,
    "password": password,
    "mobile": mobile,
    "content": content,
}
#发起数据
response = requests.post(url,headers = headers,data=data)
    #url 请求的地址
    #headers 请求头部
    #data 请求的数据

print(response.content.decode())

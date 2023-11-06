from DDCCore.APICore import APICore

if __name__ == '__main__':
    sdk = APICore("https://api.xxxxx.com", "Your API Key")
    data = sdk.高级查询_姓名_省市县_性别_年龄范围查询("杨晓霞", "江苏省", "女", 18, 25)
    print(data)

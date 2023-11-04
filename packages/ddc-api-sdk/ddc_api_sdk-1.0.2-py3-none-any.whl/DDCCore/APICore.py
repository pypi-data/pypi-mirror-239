import time

import requests


class APICore:
    def __init__(self, APIHost: str, APISecretKey: str, Version: str = "v1"):
        """
        初始化SDK
        :param APIHost: API地址
        :param APISecretKey: API认证密钥
        :param Version: API版本, 默认v1
        """
        self.APIHost = APIHost
        self.APISecretKey = APISecretKey
        self.Version = Version
        self.Client = requests.Session()
        self.BashURl = f"{self.APIHost}/api/{self.Version}"
        self.Client.headers = {'User-Agent': "DingDangSDK Request Client"}
        self.PostUrl = self.BashURl
        self.Response = None

    def check_response(self):
        if self.Response.status_code == 200:
            result = self.Response.json()
            if result["code"] == 500 and result["message"] == "API Key Not Found":
                return dict(code=result["code"], message="API不存在", time=result['time'], data=None)
            elif result["code"] == 500 and result["message"] == "API Key Insufficient Balance":
                return dict(code=result["code"], message="API密钥次数已用完", time=result['time'], data=None)
            elif result["code"] == 500 and result["message"] == "API Key Status Is Block":
                return dict(code=result["code"], message="API密钥被禁用", time=result['time'], data=None)
            else:
                return result
        elif self.Response.status_code == 429:
            return dict(code=self.Response.status_code, message="请求速度太快", time=int(time.time()), data=None)
        elif self.Response.status_code == 403:
            return dict(code=self.Response.status_code, message="IP地址未授权", time=int(time.time()), data=None)
        else:
            return dict(code=self.Response.status_code, message="未知服务器错误", time=int(time.time()), data=None)

    def request_error(self, err):
        return dict(code=500, message=f"请求失败: {err.args}, {self.APISecretKey}", time=int(time.time()), data=None)

    def request_api(self, data: dict):
        try:
            self.Response = self.Client.post(self.PostUrl, data=data)
            return self.check_response()
        except Exception as err:
            return self.request_error(err)

    def 默认查询(self, query: str):
        """
        默认查询，可以查询任何关键词
        :param query:
        :return: JSON
        """
        if 2 > len(query) < 20:
            raise RuntimeError('关键词长度错误,必须大于1,小于20')
        data = dict(auth_secret=self.APISecretKey, query=query)
        self.PostUrl = f"{self.BashURl}/5500C1337F79BEC6.php"
        return self.request_api(data)

    def 高级查询_精确姓名_省市县(self, name: str, province: str):
        """
        姓名-地区搜索
        :param name: 精确姓名
        :param province: 省市县,如河南省郑州市
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(province) >= 50:
            raise RuntimeError('地区参数长度错误')
        data = dict(auth_secret=self.APISecretKey, name=name, province=province)
        self.PostUrl = f"{self.BashURl}/6825576C29BE17B3.php"
        return self.request_api(data)

    def 高级查询_姓名_省市县_性别_年龄范围查询(self, name: str, province: str, sex: str, startAge: int, endAge: int):
        """
        姓名-省市县-性别-年龄范围查询
        :param name: 精确姓名
        :param province: 省市县,如河南省郑州市
        :param sex: 性别,男或者女
        :param startAge: 开始年龄 18
        :param endAge: 结束年龄 30
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(province) >= 50:
            raise RuntimeError('地区参数长度错误')
        if sex != "男" and sex != "女":
            raise RuntimeError('性别参数错误,必须为"男"或者"女"')
        if startAge <= 1:
            raise RuntimeError('开始年龄必须大于1')
        if endAge >= 100:
            raise RuntimeError('结束年龄必须大于100')
        if startAge > endAge:
            raise RuntimeError('开始年龄不能大于结束年龄')
        data = dict(auth_secret=self.APISecretKey, name=name, province=province, sex=sex, startAge=startAge,
                    endAge=endAge)
        self.PostUrl = f"{self.BashURl}/477B937628A5555D.php"
        return self.request_api(data)

    def 高级查询_姓名_省市县_性别(self, name: str, province: str, sex: str):
        """
        姓名-省市县-性别查询
        :param name: 精确姓名
        :param province: 省市县,如河南省郑州市
        :param sex: 性别,男或者女
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(province) >= 50:
            raise RuntimeError('地区参数长度错误')
        if sex != "男" and sex != "女":
            raise RuntimeError('性别参数错误,必须为"男"或者"女"')
        data = dict(auth_secret=self.APISecretKey, name=name, province=province, sex=sex)
        self.PostUrl = f"{self.BashURl}/65B4A9BE43F2A8CB.php"
        return self.request_api(data)

    def 高级查询_姓名_省市县_年龄范围查询(self, name: str, province: str, startAge: int, endAge: int):
        """
        姓名-省市县-年龄范围查询
        :param name: 精确姓名
        :param province: 省市县,如河南省郑州市
        :param startAge: 开始年龄 18
        :param endAge: 结束年龄 30
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(province) >= 50:
            raise RuntimeError('地区参数长度错误')
        if startAge <= 1:
            raise RuntimeError('开始年龄必须大于1')
        if endAge >= 100:
            raise RuntimeError('结束年龄必须大于100')
        if startAge > endAge:
            raise RuntimeError('开始年龄不能大于结束年龄')
        data = dict(auth_secret=self.APISecretKey, name=name, province=province, startAge=startAge,
                    endAge=endAge)
        self.PostUrl = f"{self.BashURl}/A033EBC91A698419.php"
        return self.request_api(data)

    def 高级查询_模糊姓名查询(self, wildcardName: str):
        """
        模糊姓名查询
        :param wildcardName: 模糊姓名, 张xx 张x xx雪
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('模糊姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName)
        self.PostUrl = f"{self.BashURl}/63028169E057AC78.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_性别_生日范围查询(self, wildcardName: str, province: str, sex: str, startBirthday: int,
                                            endAgeBirthday: int):
        """
        姓名-省市县-性别-年龄范围查询
        :param wildcardName: 模糊姓名
        :param province: 省市县,如河南省郑州市
        :param sex: 性别,男或者女
        :param startBirthday: 开始生日(8位数字) 19000000
        :param endAgeBirthday: 结束生日(8位数字) 20999999
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if len(province) >= 50:
            raise RuntimeError('地区参数长度错误')
        if sex != "男" and sex != "女":
            raise RuntimeError('性别参数错误,必须为"男"或者"女"')
        if startBirthday > endAgeBirthday:
            raise RuntimeError('开始年龄不能大于结束年龄')
        data = dict(auth_secret=self.APISecretKey, name=wildcardName, province=province, sex=sex,
                    startAge=startBirthday,
                    endAge=endAgeBirthday)
        self.PostUrl = f"{self.BashURl}/D13F8553B30CBE01.php"
        return self.request_api(data)

    def 高级查询_姓名_模糊身份证查询(self, name: str, wildcardIDcard: str):
        """
        姓名-模糊身份证查询
        :param name: 精确姓名
        :param wildcardIDcard: 模糊18位身份证
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardIDcard:
            raise RuntimeError('模糊身份证参数必须包含x')
        if len(wildcardIDcard) != 18:
            raise RuntimeError('模糊18位身份证必须是18位')
        data = dict(auth_secret=self.APISecretKey, name=name, wildcardIDcard=wildcardIDcard)
        self.PostUrl = f"{self.BashURl}/09B219F8177F9B68.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_模糊身份证查询(self, wildcardName: str, wildcardIDcard: str):
        """
        模糊姓名-模糊身份证查询
        :param wildcardName: 模糊姓名
        :param wildcardIDcard: 模糊身份证
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if "x" not in wildcardIDcard:
            raise RuntimeError('模糊身份证参数必须包含x')
        if len(wildcardIDcard) != 18:
            raise RuntimeError('模糊18位身份证必须是18位')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, wildcardIDcard=wildcardIDcard)
        self.PostUrl = f"{self.BashURl}/09B219F8177F9B68.php"
        return self.request_api(data)

    def 高级查询_精确姓名_身份证后四位查询(self, name: str, idcard: str):
        """
        姓名和身份证后四位搜索
        :param name: 精确姓名
        :param idcard: 身份证后四位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(idcard) != 4:
            raise RuntimeError('身份证后四位必须为4位字符串')
        data = dict(auth_secret=self.APISecretKey, name=name, end_four=idcard)
        self.PostUrl = f"{self.BashURl}/AF5F2A9EF703E427.php"
        return self.request_api(data)

    # =====================

    def 高级查询_精确姓名_手机号前3位(self, name: str, mobilePrefix: str):
        """
        姓名-手机号前3位查询
        :param name: 精确姓名
        :param mobilePrefix: 手机号前3位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(mobilePrefix) != 3:
            raise RuntimeError('手机号参数必须是3位')
        if not mobilePrefix.isdigit():
            raise RuntimeError('手机号参数必须是数字')
        data = dict(auth_secret=self.APISecretKey, name=name, mobilePrefix=mobilePrefix)
        self.PostUrl = f"{self.BashURl}/A6CB1D9EA4BB29EA.php"
        return self.request_api(data)

    def 高级查询_精确姓名_手机号后4位(self, name: str, mobileSuffix: str):
        """
        姓名-手机号后4位查询
        :param name: 精确姓名
        :param mobileSuffix: 手机号后四位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(mobileSuffix) != 4:
            raise RuntimeError('手机号参数必须是4位')
        if not mobileSuffix.isdigit():
            raise RuntimeError('手机号参数必须是数字')
        data = dict(auth_secret=self.APISecretKey, name=name, mobileSuffix=mobileSuffix)
        self.PostUrl = f"{self.BashURl}/448DA50144B70064.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_手机号前3位(self, wildcardName: str, mobilePrefix: str):
        """
        模糊姓名-手机号前3位查询
        :param wildcardName: 模糊姓名
        :param mobilePrefix: 手机号前3位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if len(mobilePrefix) != 3:
            raise RuntimeError('手机号参数必须是3位')
        if not mobilePrefix.isdigit():
            raise RuntimeError('手机号参数必须是数字')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, mobilePrefix=mobilePrefix)
        self.PostUrl = f"{self.BashURl}/92E9244750001D39.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_手机号后4位(self, wildcardName: str, mobileSuffix: str):
        """
        模糊姓名-手机号后4位查询
        :param wildcardName: 模糊姓名
        :param mobileSuffix: 手机号后四位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if len(mobileSuffix) != 4:
            raise RuntimeError('手机号参数必须是4位')
        if not mobileSuffix.isdigit():
            raise RuntimeError('手机号参数必须是数字')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, mobileSuffix=mobileSuffix)
        self.PostUrl = f"{self.BashURl}/12317AA0341AF956.php"
        return self.request_api(data)

    def 高级查询_精确姓名_模糊手机号前3位(self, name: str, wildcardMobilePrefix: str):
        """
        姓名-模糊手机号前3位查询
        :param name: 精确姓名
        :param wildcardMobilePrefix: 模糊手机号前3位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(wildcardMobilePrefix) != 3:
            raise RuntimeError('手机号参数必须是3位')
        if "x" not in wildcardMobilePrefix:
            raise RuntimeError('模糊手机号参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, name=name, wildcardMobilePrefix=wildcardMobilePrefix)
        self.PostUrl = f"{self.BashURl}/0F22A86FF729A059.php"
        return self.request_api(data)

    def 高级查询_精确姓名_模糊手机号后4位(self, name: str, wildcardMobileSuffix: str):
        """
        姓名-模糊手机号后4位查询
        :param name: 精确姓名
        :param wildcardMobileSuffix: 模糊手机号后四位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(wildcardMobileSuffix) != 4:
            raise RuntimeError('手机号参数必须是4位')
        if "x" not in wildcardMobileSuffix:
            raise RuntimeError('模糊手机号参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, name=name, wildcardMobileSuffix=wildcardMobileSuffix)
        self.PostUrl = f"{self.BashURl}/3574EF7792D53B67.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_模糊手机号前3位(self, wildcardName: str, wildcardMobilePrefix: str):
        """
        模糊姓名-模糊手机号前3位查询
        :param wildcardName: 模糊姓名
        :param wildcardMobilePrefix: 模糊手机号前3位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if len(wildcardMobilePrefix) != 3:
            raise RuntimeError('手机号参数必须是3位')
        if "x" not in wildcardMobilePrefix:
            raise RuntimeError('模糊手机号参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, wildcardMobilePrefix=wildcardMobilePrefix)
        self.PostUrl = f"{self.BashURl}/5AE30CBA83152548.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_模糊手机号后4位(self, wildcardName: str, wildcardMobileSuffix: str):
        """
        模糊姓名-模糊手机号后4位查询
        :param wildcardName: 模糊姓名
        :param wildcardMobileSuffix: 模糊手机号后四位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if len(wildcardMobileSuffix) != 4:
            raise RuntimeError('手机号参数必须是4位')
        if "x" not in wildcardMobileSuffix:
            raise RuntimeError('模糊手机号参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, wildcardMobileSuffix=wildcardMobileSuffix)
        self.PostUrl = f"{self.BashURl}/1DC25E0155A2CC12.php"
        return self.request_api(data)

    def 高级查询_精确姓名_精确手机号前3位_精确后4位查询(self, name: str, mobilePrefix: str, mobileSuffix: str):
        """
        精准姓名-精准手机号前3位和后4位查询
        :param name: 精准姓名
        :param mobilePrefix: 手机号后四位
        :param mobileSuffix: 手机号后四位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(mobileSuffix) != 3:
            raise RuntimeError('手机号前3位参数必须是3位')
        if len(mobileSuffix) != 4:
            raise RuntimeError('手机号后4位参数必须是4位')
        if not mobilePrefix.isdigit() or not mobileSuffix.isdigit():
            raise RuntimeError('手机号前3位和后4位参数必须是是数字字符')
        data = dict(auth_secret=self.APISecretKey, name=name, mobilePrefix=mobilePrefix, mobileSuffix=mobileSuffix)
        self.PostUrl = f"{self.BashURl}/81D6124D13B31606.php"
        return self.request_api(data)

    def 高级查询_精确姓名_手机号前3位_模糊后4位查询(self, name: str, mobilePrefix: str, wildcardMobileSuffix: str):
        """
        精准姓名-精准手机号前3位-模糊后4位查询
        :param name: 精准姓名
        :param mobilePrefix: 手机号后四位
        :param wildcardMobileSuffix: 模糊手机号后四位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(wildcardMobileSuffix) != 3:
            raise RuntimeError('手机号前3位参数必须是3位')
        if len(wildcardMobileSuffix) != 4:
            raise RuntimeError('手机号后4位参数必须是4位')
        if "x" not in wildcardMobileSuffix:
            raise RuntimeError('模糊手机号后4位参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, name=name, mobilePrefix=mobilePrefix,
                    wildcardMobileSuffix=wildcardMobileSuffix)
        self.PostUrl = f"{self.BashURl}/DADD36A5EFA9C351.php"
        return self.request_api(data)

    def 高级查询_精确姓名_模糊手机号前3位_模糊后4位查询(self, name: str, wildcardMobilePrefix: str,
                                                        wildcardMobileSuffix: str):
        """
        精准姓名-模糊手机号前3位-模糊后4位查询
        :param name: 精准姓名
        :param wildcardMobilePrefix: 模糊手机号后四位
        :param wildcardMobileSuffix: 模糊手机号后四位
        :return: JSON
        """
        if 2 > len(name) < 20:
            raise RuntimeError('精确姓名参数长度错误')
        if len(wildcardMobileSuffix) != 3:
            raise RuntimeError('手机号前3位参数必须是3位')
        if len(wildcardMobileSuffix) != 4:
            raise RuntimeError('手机号后4位参数必须是4位')
        if "x" not in wildcardMobilePrefix:
            raise RuntimeError('模糊手机号前3位参数必须包含x')
        if "x" not in wildcardMobileSuffix:
            raise RuntimeError('模糊手机号后4位参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, name=name, wildcardMobilePrefix=wildcardMobilePrefix,
                    wildcardMobileSuffix=wildcardMobileSuffix)
        self.PostUrl = f"{self.BashURl}/2BC85B614C15DBBB.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_模糊手机号前3位_模糊后4位查询(self, wildcardName: str, wildcardMobilePrefix: str,
                                                        wildcardMobileSuffix: str):
        """
        模糊姓名-模糊手机号前3位-模糊后4位查询
        :param wildcardName: 模糊姓名
        :param wildcardMobilePrefix: 模糊手机号后四位
        :param wildcardMobileSuffix: 模糊手机号后四位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('模糊姓名参数长度错误')
        if len(wildcardMobileSuffix) != 3:
            raise RuntimeError('手机号前3位参数必须是3位')
        if len(wildcardMobileSuffix) != 4:
            raise RuntimeError('手机号后4位参数必须是4位')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if "x" not in wildcardMobilePrefix:
            raise RuntimeError('模糊手机号前3位参数必须包含x')
        if "x" not in wildcardMobileSuffix:
            raise RuntimeError('模糊手机号后4位参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, wildcardMobilePrefix=wildcardMobilePrefix,
                    wildcardMobileSuffix=wildcardMobileSuffix)
        self.PostUrl = f"{self.BashURl}/EB909B2B51F9B8ED.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_模糊手机号前3位_精准后4位查询(self, wildcardName: str, wildcardMobilePrefix: str,
                                                        mobileSuffix: str):
        """
        模糊姓名-模糊手机号前3位-精准后4位查询
        :param wildcardName: 模糊姓名
        :param wildcardMobilePrefix: 模糊手机号后四位
        :param mobileSuffix: 精准手机号后四位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('模糊姓名参数长度错误')
        if len(mobileSuffix) != 3:
            raise RuntimeError('手机号前3位参数必须是3位')
        if len(mobileSuffix) != 4:
            raise RuntimeError('手机号后4位参数必须是4位')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        if "x" not in wildcardMobilePrefix:
            raise RuntimeError('模糊手机号前3位参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, wildcardMobilePrefix=wildcardMobilePrefix,
                    mobileSuffix=mobileSuffix)
        self.PostUrl = f"{self.BashURl}/3AE3DB8E4741A0D3.php"
        return self.request_api(data)

    def 高级查询_模糊姓名_精准手机号前3位_精准后4位查询(self, wildcardName: str, mobilePrefix: str, mobileSuffix: str):
        """
        模糊姓名-精准手机号前3位-精准后4位查询
        :param wildcardName: 模糊姓名
        :param mobilePrefix: 精准手机号后四位
        :param mobileSuffix: 精准手机号后四位
        :return: JSON
        """
        if 2 > len(wildcardName) < 20:
            raise RuntimeError('模糊姓名参数长度错误')
        if len(mobileSuffix) != 3:
            raise RuntimeError('手机号前3位参数必须是3位')
        if len(mobileSuffix) != 4:
            raise RuntimeError('手机号后4位参数必须是4位')
        if "x" not in wildcardName:
            raise RuntimeError('模糊姓名参数必须包含x')
        data = dict(auth_secret=self.APISecretKey, wildcardName=wildcardName, mobilePrefix=mobilePrefix,
                    mobileSuffix=mobileSuffix)
        self.PostUrl = f"{self.BashURl}/96F2E894538019AD.php"
        return self.request_api(data)

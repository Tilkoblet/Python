# -*- coding: utf-8 -*-
'''
건강보험공단 인증결과 데이터 모델
'''
class BaseModel():
    Status = None
    Message = None

    def __init__(self):
        pass

class AuthResponse(BaseModel):
    AuthCode = None;

    def __init__(self):
        pass


class RSApublicKey(BaseModel):
    PublicKey = None    #API키에 매칭되는 RSA공개키
    ApiKey = None   #전달한 API키(검증)용

    def __init__(self):
        pass
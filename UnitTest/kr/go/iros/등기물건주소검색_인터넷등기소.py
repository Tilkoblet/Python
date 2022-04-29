import os, json, base64
import requests
from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES


apiHost = 'https://api.tilko.net/'
apiKey  = ''


# RSA 암호화 함수(RSA 공개키로 AES키 암호화)
def rsaEncrypt(publicKey, aesKey):
    rsa             = RSA.importKey(base64.b64decode(publicKey))
    cipher          = PKCS1_v1_5.new(rsa.publickey())
    aesCipherKey	= cipher.encrypt(aesKey)
    return aesCipherKey


# RSA 공개키(Public Key) 조회 함수
def getPublicKey():
    headers     = {'Content-Type': 'application/json'}
    response    = requests.get(apiHost + "/api/Auth/GetPublicKey?APIkey=" + apiKey, headers=headers)
    return response.json()['PublicKey']


# RSA Public Key 조회
rsaPublicKey    = getPublicKey()
print(f"rsaPublicKey: {rsaPublicKey}")


# AES Secret Key 및 IV 생성
aesKey          = os.urandom(16)
aesIv           = ('\x00' * 16).encode('utf-8')


# AES Key를 RSA Public Key로 암호화
aesCipherKey    = base64.b64encode(rsaEncrypt(rsaPublicKey, aesKey))
print(f"aesCipherKey: {aesCipherKey}")


# API URL 설정
# HELP: https://tilko.net/Help/Api/POST-api-apiVersion-Iros-RISUConfirmSimpleC
url         = apiHost + "api/v1.0/Iros/RISUConfirmSimpleC";


# API 요청 파라미터 설정
options     = {
    "headers": {
        "Content-Type"          : "application/json",
        "API-KEY"               : apiKey,
        "ENC-KEY"               : aesCipherKey
    },
    
    "json": {
        "Address": "__VALUE__",
        "Sangtae": "__VALUE__",
        "KindClsFlag": "__VALUE__",
        "Region": "__VALUE__",
        "Page": "__VALUE__"
    },
}


# API 호출
res         = requests.post(url, headers=options['headers'], json=options['json'])
print(f"res: {res.json()}")




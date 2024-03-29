import os, json, base64
import requests
from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
import random
from datetime import datetime


apiHost = 'https://api.tilko.net/'
apiKey  = 'API_KEY'


# AES 암호화 함수
def aesEncrypt(key, iv, plainText):
    def pad(text):
        text_length     = len(text)
        amount_to_pad   = AES.block_size - (text_length % AES.block_size)

        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
            
        pad     = chr(amount_to_pad)

        result  = None
        try:
            result  = text + str(pad * amount_to_pad).encode('utf-8')
        except Exception as e:
            result  = text + str(pad * amount_to_pad)

        return result
    
    if type(plainText) == str:
        plainText = plainText.encode('utf-8')
    
    plainText   = pad(plainText)
    cipher      = AES.new(key, AES.MODE_CBC, iv)
    
    if(type(plainText) == bytes):
        return base64.b64encode(cipher.encrypt(plainText)).decode('utf-8')
    else:
        return base64.b64encode(cipher.encrypt(plainText.encode('utf-8'))).decode('utf-8')


# RSA 암호화 함수(RSA 공개키로 AES키 암호화)
def rsaEncrypt(publicKey, aesKey):
    rsa             = RSA.importKey(base64.b64decode(publicKey))
    cipher          = PKCS1_v1_5.new(rsa.publickey())
    aesCipherKey	= cipher.encrypt(aesKey)
    return aesCipherKey


# RSA 공개키(Public Key) 조회 함수
def getPublicKey():
    headers     = {'Content-Type': 'application/json'}
    response    = requests.get(apiHost + "/api/Auth/GetPublicKey?APIkey=" + apiKey, headers=headers, verify=False)
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
# HELP: https://tilko.net/Help/Api/POST-api-apiVersion-HometaxGeneral-UTEETBAA01
url         = apiHost + "api/v1.0/HometaxGeneral/UTEETBAA01";


# 인증서 경로 설정
certPath    = "C:/Users/user01/AppData/LocalLow/NPKI/yessign/USER/user01/";
certFile    = certPath + "signCert.der";
keyFile     = certPath + "signPri.key";

today       = datetime.strftime(datetime.today(), '%Y%m%d')

# API 요청 파라미터 설정
pummok      = [
    {
        "PubDate": "__VALUE__",
        "Item": "__VALUE__",
        "Spec": "__VALUE__",
        "Qty": "__VALUE__",
        "UnitPrice": "__VALUE__",
        "SplAmount": "__VALUE__",
        "TaxAmount": "__VALUE__",
        "Remark": "__VALUE__",
    },
]

options     = {
    "headers": {
        "Content-Type"          : "application/json",
        "API-KEY"               : apiKey,
        "ENC-KEY"               : aesCipherKey
    },
    
    "json": {
        "CertFile": aesEncrypt(aesKey, aesIv, open(certFile, "rb").read()),
        "KeyFile": aesEncrypt(aesKey, aesIv, open(keyFile, "rb").read()),
        "CertPassword": aesEncrypt(aesKey, aesIv, "__VALUE__"),
        "Pummok": json.dumps(pummok, ensure_ascii=False),
        "EtxivClsfCd": "__VALUE__",
        "EtxivKndCd": "__VALUE__",
        "EtxivDmnrClsfCd": "__VALUE__",
        "RecApeClCd": "__VALUE__",
        "WriteDate": "__VALUE__",
        "SplrMpbNo": "__VALUE__",
        "SplrUpte": "__VALUE__",
        "SplrJongMok": "__VALUE__",
        "SplrEmail": "__VALUE__",
        "SplrTnmNm": "__VALUE__",
        "SplrRprsfNm": "__VALUE__",
        "DmnrBusinessNo": aesEncrypt(aesKey, aesIv, "__VALUE__"),
        "DmnrMpbNo": "__VALUE__",
        "DmnrCmpName": "__VALUE__",
        "DmnrPrsdntName": "__VALUE__",
        "DmnrAddress": "__VALUE__",
        "DmnrUpte": "__VALUE__",
        "DmnrJongMok": "__VALUE__",
        "DmnrEmail": "__VALUE__",
        "Remark": "__VALUE__",
    },
}


# API 호출
res         = requests.post(url, headers=options['headers'], json=options['json'], verify=False)
print(f"res: {res.json()}")



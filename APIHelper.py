# -*- coding: utf-8 -*-
from AES import AESCipher
import requests, base64, json, os



class APIHelper():
	_pubUrl = "https://api.tilko.net/api/Auth/GetPublicKey?APIkey={}";
	_paymentUrl = "https://api.tilko.net/api/v1.0/Nhis/jpaca00101/geongangboheom";
	_myDrugUrl = "https://api.tilko.net/api/v1.0/Hira/hiraa050300000100";
	_aes = None
	_apiKey = None;

	def __init__(self, apiKey):
		self._apiKey = apiKey
		#AES초기화
		#self._aes = AESCipher(str('\x00' * 16), '\x00' * 16)
		self._aes = AESCipher(os.urandom(16), ('\x00' * 16).encode('utf-8'))
		#self._aes = AESCipher(str('\x00' * 16), '\x00' * 16)

	#get AES plain Key
	def getAesPlainKey(self):
		return self._aes.key

	#RSA공개키 요청 API호출
	def getRSAPubKey(self):
		headers = {'Content-Type':'application/json'}
		response = requests.request("GET", self._pubUrl.format(self._apiKey), headers=headers)
		return response.text.encode('utf8')

	#건강보험료납부내역 API 호출
	def getPaymentList(self, aesCipherKey, certFilePath, keyFilePath, indetityNumber, certPassword, year, startMonth, endMonth):
		with open(certFilePath, "rb") as in_file:
			_certPlainBytes = in_file.read()
		with open(keyFilePath, "rb") as in_file:
			_keyPlainBytes = in_file.read()

		payload = {
			'CertFile':base64.b64encode(self._aes.encrypt(_certPlainBytes)).decode("UTF-8"),
			'KeyFile':base64.b64encode(self._aes.encrypt(_keyPlainBytes)).decode("UTF-8"),
			'IdentityNumber':base64.b64encode(self._aes.encrypt(indetityNumber)).decode("UTF-8"),
			'CertPassword':base64.b64encode(self._aes.encrypt(certPassword)).decode("UTF-8"),
			'Year':year,
			'StartMonth':startMonth,
			'EndMonth':endMonth,
		}
		headers = {
			'Content-Type': 'application/json; charset=utf-8',
			'API-Key': self._apiKey,
  			'ENC-Key': base64.b64encode(aesCipherKey),
		}


		response = requests.request("POST", self._paymentUrl, headers=headers, data=json.dumps(payload))
		return response.text.encode('utf8')

	#내가 먹는 약 API 호출
	def getMYDrug(self, aesCipherKey, certFilePath, keyFilePath, indetityNumber, certPassword, phoneNumber):
		with open(certFilePath, "rb") as in_file:
			_certPlainBytes = in_file.read()
		with open(keyFilePath, "rb") as in_file:
			_keyPlainBytes = in_file.read()

		payload = {
			'CertFile':base64.b64encode(self._aes.encrypt(_certPlainBytes)).decode("UTF-8"),
			'KeyFile':base64.b64encode(self._aes.encrypt(_keyPlainBytes)).decode("UTF-8"),
			'IdentityNumber':base64.b64encode(self._aes.encrypt(indetityNumber)).decode("UTF-8"),
			'CertPassword':base64.b64encode(self._aes.encrypt(certPassword)).decode("UTF-8"),
			'CellphoneNumber':base64.b64encode(self._aes.encrypt(phoneNumber)).decode("UTF-8"),
			'TelecomCompany':'0'
		}
		headers = {
			'Content-Type': 'application/json; charset=utf-8',
			'API-Key': self._apiKey,
  			'ENC-Key': base64.b64encode(aesCipherKey),
		}


		response = requests.request("POST", self._myDrugUrl, headers=headers, data=json.dumps(payload))
		return response.text.encode('utf8')
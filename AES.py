# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES

#AES 암호화 클래스 (AES-CBC-PKC7padding)
class AESCipher:
	class InvalidBlockSizeError(Exception):
		"""Raised for invalid block sizes"""
		pass

	def __init__(self, key, iv):
		self.key = key
		self.iv =iv

	def __pad(self, text):
		text_length = len(text)
		amount_to_pad = AES.block_size - (text_length % AES.block_size)
		if amount_to_pad == 0:
			amount_to_pad = AES.block_size
		pad = chr(amount_to_pad)

		result = None
		try:
			result = text + str(pad * amount_to_pad).encode("UTF-8")
		except Exception as e:
			result = text + str(pad * amount_to_pad)

		return result

	def __unpad(self, text):
		pad = ord(text[-1])
		return text[:-pad]

	def encrypt( self, raw ):
		raw = self.__pad(raw)
		cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
		if(type(raw) == bytes):
			return cipher.encrypt(raw)
		else:
			return cipher.encrypt(raw.encode('utf-8'))

	def decrypt( self, enc ):
		#enc = base64.b64decode(enc)
		cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
		return self.__unpad(cipher.decrypt(enc).decode("utf-8"))

if __name__=="__main__":
	e = AESCipher('\x00' * 16, '\x00' * 16)

	secret_data = "test"
	enc_str = e.encrypt(secret_data)
	print('enc_str: {}'.format(base64.b64encode(enc_str)))
	dec_str = e.decrypt(enc_str)
	print('dec str: {}'.format(dec_str))
from classes.handlers.log_handler import LogHandler

from cryptography.fernet import Fernet
import sys


class EncryptionHandler():
    
    
    
    def generate_encryption_key(self):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        key = Fernet.generate_key()
        LogHandler.info_log(self, function_name, 'key: ', key)
        return key
    
    
    def encrypt(self, param, enc_key):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        encrypt_key = enc_key
        raw_param = bytes(param, 'utf-8')
        LogHandler.debug_log(self, function_name, 'raw_param: ', raw_param)
        cipher_suite = Fernet(encrypt_key)
        ciphered_text = cipher_suite.encrypt(raw_param)
        LogHandler.debug_log(self, function_name, 'crypted_param: ', ciphered_text)
        return ciphered_text
    
    
    def decrypt(self, enc_key, cryp_param):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')
        key = bytes(enc_key, 'utf-8')
        LogHandler.debug_log(self, function_name, 'key: ', key)
        cipher_suite = Fernet(key)
        ciphered_text = bytes(cryp_param)
        byte_text = (cipher_suite.decrypt(ciphered_text))
        unciphered_text = byte_text.decode("utf-8") 
        LogHandler.debug_log(self, function_name, 'raw_param: ', unciphered_text)
        return unciphered_text
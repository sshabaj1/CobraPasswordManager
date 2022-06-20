from classes.handlers.log_handler import LogHandler
from classes.utilities.static_variables import StaticVariables

import sys
import secrets
import string

class OtpHandler():

    def create_otp(self, char_len):
        function_name = sys._getframe().f_code.co_name
        LogHandler.info_log(self, function_name, '', '')

        alphabet = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(alphabet) for i in range(char_len))

        LogHandler.info_log(self, function_name, 'OTP created: ', otp)

        return otp

    
import json
import requests
from requests.adapters import HTTPAdapter, Retry
from custom_logger import CustomLogger
import traceback

logger = CustomLogger()


class ProtectoVault:
    def __init__(self, auth_token, default_url="https://trial-test.thedpoforum.com/api/vault/"):
        self.auth_token = auth_token
        self.default_url = default_url
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
           'Authorization': auth_token}

    def mask(self, data):
        # Implement data masking logic here
        # This method will take data as input and mask it using the authkey and possibly the base URL.
        try:
            input_data = list()
            input_data.append({"value": "{}".format(data)})
            logger.info(f"input_data:{input_data}")
            result = self.service_call(input_data, "mask", "mask")["data"]
            return result
        except Exception as e :
            logger.error(f"Error in mask: {traceback.format_exc()}")

    def unmask(self, masked_data):
        # Implement data unmasking logic here
        # This method will take masked data and unmask it using the authkey and possibly the base URL.
        try:
            input_data = list()
            input_data.append({"token_value": "{}".format(masked_data)})
            logger.info(f"input_data:{input_data}")
            unmask_result = self.service_call(input_data, "unmask", "unmask")["data"]
            return unmask_result
        except Exception as e:
            logger.error(f"Error in unmask: {traceback.format_exc()}")

    def service_call(self,data, key, path):
        r = self.submit_request({key: data}, path)
        rc = r.status_code
        return r.json()

    def submit_request(self,input_data, hs):
        session = self.get_session()
        d = json.dumps(input_data)
        r = session.put("{}{}".format(self.default_url, hs), data=json.dumps(input_data), headers=self.headers)
        return r

    def get_session(self):
        s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.2,
                        status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        s.mount(self.default_url, adapter)
        return s

#
# obj = ProtectoVault("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZXIiOiJQcm90ZWN0byIsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjMtMTItMDIiLCJwZXJtaXNzaW9ucyI6WyJyZWFkIiwid3JpdGUiXSwidXNlcl9uYW1lIjoibml2ZXRoYXJwa0BnbWFpbC5jb20iLCJkYl9uYW1lIjoicHJvdGVjdG9fZ21haWxfbm1pcHJ6YXQiLCJoYXNoZWRfcGFzc3dvcmQiOiJkNDUyNTUxODViMWM5Yjg2NWIwZWQ4NTZkZDc0Mzk1M2RhZTdhNTUwZDUwMmU5ZWQ0ZDRlYWJiMjNlMTNkNDU4In0.2Na7lwWmZjb20ew9jyW1henSOHfm8nYSlAxVdaW_t20")
# masked_res = obj.mask("Gina lives in the U.S.A")
# print(masked_res)
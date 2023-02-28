import requests
from requests_ntlm import HttpNtlmAuth
import json

class SharePointConnector:

    def __init__(self, username, password, domain, site_url, auth_cert):
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__site_url = site_url
        self.__cert = auth_cert
        login_user = self.__domain + "\\" + self.__username
        user_auth = HttpNtlmAuth(login_user, self.__password)
        self.__auth = user_auth

    def download_file(self, sharepoint_file_path, download_path):
        headers = {
            'Accept': 'application/json;odata=verbose',
            'content-type': 'application/json;odata=verbose',
            'odata': 'verbose',
            'X-RequestForceAuthentication': 'true'
        }
        try:
            actual_file = requests.get(
                sharepoint_file_path, auth=self.__auth, headers =headers, verify=self.__cert
            ).content
            with open(download_path, "wb") as fp:
                fp.write(actual_file)
        except Exception as ex:
            print("Failed Downloading;error:{}".format(ex))

    def get_folder_contents(self, base_url, folder_url):
        sharepoint_files = []
        headers = {
            'Accept': 'application/json;odata=verbose',
            'content-type': 'application/json;odata=verbose',
            'odata': 'verbose',
            'X-RequestForceAuthentication': 'true'
        }
        complete_url = base_url + folder_url
        response = requests.get(complete_url, auth=self.__auth, headers=headers, verify=self.__cert).json()
        for file in response["d"]["results"]:
            sharepoint_files.append(file.get("FileRef"))
        return sharepoint_files

    def get_folder_contents_complete(self, base_url, folder_url):
        sharepoint_files_complete = []
        headers = {
            'Accept': 'application/json;odata=verbose',
            'content-type': 'application/json;odata=verbose',
            'odata': 'verbose',
            'X-RequestForceAuthentication': 'true'
        }
        complete_url = base_url + folder_url
        response = requests.get(complete_url, auth=self.__auth, headers=headers, verify=self.__cert).json()
        for file in response["d"]["results"]:
            sharepoint_files_complete.append(file.get("FileRef"))
        next_path = response["d"].get("__next")
        while next_path:
            response_next = requests.get(
                next_path, auth=self.__auth, headers=headers, verify=False
            ).json()
            for files in response_next["d"]["results"]:
                sharepoint_files_complete.append(files.get("FileRef"))
            next_path = response_next["d"].get("__next")
        return sharepoint_files_complete

    def get_custom_list(self, base_url, list_url):
        headers = {
            'Accept': 'application/json;odata=verbose',
            'content-type': 'application/json;odata=verbose',
            'odata': 'verbose',
            'X-RequestForceAuthentication': 'true'
        }
        complete_url = base_url + list_url
        response = requests.get(complete_url, auth=self.__auth, headers=headers, verify=self.__cert)
        if response.status_code == requests.codes.ok:  # Value of requests.codes.ok is 200
            data = json.loads(response.text)
            return data['d']
        else:
            return None

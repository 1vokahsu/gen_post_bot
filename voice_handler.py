import datetime
import os
import time
from asyncio import log

import requests
from config.config import config


async def voice_trans(file_name: str):
    headers = {"keyId": config.KeyId, "keySecret": config.KeySecret}
    create_url = "https://api.speechflow.io/asr/file/v1/create?lang=ru"
    query_url = "https://api.speechflow.io/asr/file/v1/query?taskId="
    files = {"file": open(file_name, "rb")}

    try:
        response = requests.post(create_url, headers=headers, files=files)
        print(f'{datetime.datetime.now()} - [INFO] POST request status code : {response.status_code}')
        if response.status_code == 200:
            create_result = response.json()
            query_url += create_result["taskId"] + "&resultType=4"
            while True:
                try:
                    response = requests.get(query_url, headers=headers)
                    print(f'{datetime.datetime.now()} - [OK] GET request status code : {response.status_code}')
                    if response.status_code == 200:
                        query_result = response.json()
                        if query_result["code"] == 11000:
                            if query_result["result"]:
                                result = query_result["result"].replace("\n\n", " ")
                                print(f'{datetime.datetime.now()} - [OK] result POST request : {result}')
                                os.remove(file_name)
                                print(f'{datetime.datetime.now()} - [OK] remove file: {file_name}')
                                return result
                            break
                        elif query_result["code"] == 11001:
                            time.sleep(3)
                            continue
                        else:
                            print(f'{datetime.datetime.now()} - [ERROR] query_result: {query_result["code"]}')
                            break
                    else:
                        print(f'{datetime.datetime.now()} - [ERROR] POST request status code : {response.status_code}')
                        break
                except Exception as ex:
                    print(f'{datetime.datetime.now()} - [ERROR] {ex}')
                    return None
            return None
        else:
            print(f'{datetime.datetime.now()} - [ERROR] POST request status code : {response.status_code}')
            return None
    except Exception as ex:
        print(f'{datetime.datetime.now()} - [ERROR] {ex}')
        return None


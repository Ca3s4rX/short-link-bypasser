from httpx import Client
from bs4 import BeautifulSoup
from time import sleep
from sys import argv, exit

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Cookie": "",
}

websites = {
    "linkjust.com": {
        "second_url": "https://linkjust.com/links/go",
        "referer": "https://forexrw7.com/",
        "delay": 5,
        "requsts_number": 2,
    }
}

###################### Helper Functions ######################

def http2(
    url, method="GET", headers={}, body_data={}, params={}, is_json=False, timeout=30
):
    # headers, body_data, params always passed as a dictionary
    # httpx converts params to url-encoded string
    # httpx converts body_data (if is_json=False) to url encoded string then add header "Content-Type: application/x-www-form-urlencoded"
    # httpx converts data (if it is json) to json string then add header "Content-Type: application/json"

    json = body_data if is_json else None
    data = body_data if not is_json else None

    try:
        # Sending Request
        with Client(http2=True, verify=False, timeout=timeout) as client:
            response = client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json,
                data=data,
                params=params,
            )

            # IP Address
            try:
                ip_address = response.ext.get("network_stream").get_extra_info(
                    "peername"
                )[0]
            except Exception:
                ip_address = None

            # Response Body
            res_body = (
                response.json()
                if "json" in response.headers.get("Content-Type", "").lower()
                else response.text
            )

            # Return structured response
            return {
                "ip": ip_address,
                "status_code": response.status_code,
                "request_headers": response.request.headers,
                "response_headers": response.headers,
                "response_body": res_body,
            }

    except Exception as e:
        print(f"[INF] HTTP2 Error: {e}")
        return False


def get_host(url):
    return url.split("//")[1].split("/")[0]

############################ END ############################

def print_table():
    data = [
        "Requirements ==> pip install httpx[http2] beautifulsoup4",
        "Usage ==> python short_link_bypasser.py https://linkjust.com/1KEvtFiwr"
    ]

    # Find the longest line for table width
    max_len = max(len(line) for line in data)

    # Table border top & bottom
    table_border = "+" + "-" * (max_len + 2) + "+"
    
    # Print Table
    print(table_border)
    for line in data: print(f"| {line.ljust(max_len)} |")
    print(table_border)

def config_message(host):
    obj = websites[host]
    data = [
        ("Host", host),
        ("Number of Requests", obj["requsts_number"]),
        ("Delay", obj["delay"]),
        ("Referer", obj["referer"]),
    ]

    title = " CONFIGS "  # Table title

    # Find max column widths
    col1_width = max(len(row[0]) for row in data)
    col2_width = max(len(str(row[1])) for row in data)
    total_width = col1_width + col2_width + 5  # 5 = borders and spaces

    # Print top border and title
    print("\n"+"+" + "-" * total_width + "+")
    print("|" + title.center(total_width) + "|")
    print("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+")

    # Print data rows
    for key, value in data:
        print(f"| {key.ljust(col1_width)} | {str(value).ljust(col2_width)} |")

    # Bottom border
    print("+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+"+"\n")
    
def first_request(url, host):
    global headers
    headers["Referer"] = websites[host]["referer"]
    print(f"[*] First Request ==> ", end="")
    response = http2(url, headers=headers)
    try:
        status_code = response["status_code"]
        print(f"{status_code}, ", end="")
        if status_code == 200:
            
            # Get cookies from response headers: Set-Cookie
            cookies = [ value for (key, value) in response["response_headers"].items() if key.lower() == "set-cookie"][0]
            csrf_token = cookies.split("csrfToken=")[1].split(";")[0]
            end_point = f"ref{url.split('/')[-1]}"
            
            # Set Cookies to further requests
            headers["Cookie"] += f"AppSession={cookies.split('AppSession=')[1].split(';')[0]}; "
            headers["Cookie"] += f"csrfToken={csrf_token}; "
            headers["Cookie"] += f"{end_point}={cookies.split(f'{end_point}=')[1].split(';')[0]}; "
            
            # Parsing the reponse
            soup = BeautifulSoup(response["response_body"], "html.parser")
            
            # Get Hidden Input: ad_form_data
            input_tag = soup.find("input", {"name": "ad_form_data"})
            if input_tag: ad_form_data = input_tag.get("value")
            
            # Get Hidden Input: _Token[fields]
            input_tag = soup.find("input", {"name": "_Token[fields]"})
            if input_tag: token_field = input_tag.get("value")

            print("done")
            return {
                "csrf_token": csrf_token,
                "ad_form_data": ad_form_data,
                "token_field": token_field,
            }
        else:
            print(f"error")
            return {}
    except Exception as e:
        print(f"error")
        return {}

def second_request(data, host):
    global headers
    url = websites[host]["second_url"]
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers["X-Requested-With"] = "XMLHttpRequest"
    data = {
        "_method": "POST",
        "_csrfToken": data["csrf_token"],
        "ad_form_data": data["ad_form_data"],
        "_Token[fields]": data["token_field"],
        "_Token[unlocked]": "adcopy_challenge|adcopy_response|g-recaptcha-response|h-captcha-response",
    }

    print("[*] Second Request ==> ", end="")
    response = http2(url, method="POST", headers=headers, body_data=data)
    if response:
        status_code = response["status_code"]
        print(f"{status_code}, ", end="")
        try:
            print("done")
            print(f"\n[=] Final URL: {response['response_body']['url']}")
        except Exception as e:
            print(f"error: {e}")

def bypasser(url):
    host = get_host(url)
    if host not in websites:
        print(
            f"\n[=] ERROR: Configurations Not Contain '{host}' website, You need to add it :)"
        )
        return
    config_message(host)
    print("Logs:\n======")
    data = first_request(url, host)
    if data:
        delay = websites[host]["delay"]
        print(f"[*] Sleeping {delay} seconds ...")
        sleep(delay)
        second_request(data, host)

if __name__ == "__main__":
    if len(argv) == 1:
        print_table()
        exit()
    url = argv[1]
    bypasser(url)

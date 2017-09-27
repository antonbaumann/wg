import requests

payload = {
    'monopoly_visited': 'true',
    'cities': 'M%C3%BCnchen',
    'email': '',
    # 'g-recaptcha-response': '03AJzQf7OcYsqp1YuSh3Ny3xhbz1mcbr98FpqjAHAd2RcBgxs5JAckWajz2-EIwIn-9x6KmBNyB4tyYSeoKlmnT_B7snXgzr3piT9cHbYXUbdDQhzaWNuSb-3uHn9kh0530361VDg-5sz3-7KIyvAfbr67j-tpiEtj-8Pz7wy9UHVYRq3hSy82VX-qmjVWlkm8m-DLovBl1dYxXEqLXrBaJU2gGwUOamzR-DgYhtRNCkyuYJ7c6koewQPG5z31Z44aB1QYS8C6daZHxfwEEe4gYdJFfn8sWUqLit95XRbX5HWqwfS7YQaJBe3RiG-DZmYtQbBKC88VqFvzG_fA3rPnUW7TT9A03dIT_g',
}

header = {
    'host': 'www.monopoly-wahl-2017.de',
    'connection': 'keep-alive',
    'content-length': '426',
    'accept': '*/*',
    'origin': 'http://www.monopoly-wahl-2017.de',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'referer': 'http://www.monopoly-wahl-2017.de/',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4'
}

html = requests.post('http://www.monopoly-wahl-2017.de/participation.php', data=payload, headers=header)
print(html)
print(html.json())

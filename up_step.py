from exp10it import send_http_package
import time
my_mobile_phone = "c%2FsnL7kqiQthH6f3l5gprJUJExm%2BDgQI527Qe96WPjQfrbkGkon41fPw5Qx2lqwiiCHNNRMSOi5U%0A%2F3%2FoTSmelDaM5Ctj5osYyUNj8ATxOnUeXHkAdzL1uqV6jmEsJsZ%2F%2Bk571GR20NJk5FlH1BUq1gmZ%0AuEtjiN1wDyMqcLUOICg%3D%0A"
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
package = '''POST /elis_smp_eco_dmz/ecology/elis.eco.web.healthPedomeSTQ.visit HTTP/1.1
Host: elis-smp-eco.pingan.com.cn
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Cookie: llll
Connection: close
Accept: */*
User-Agent: PALifeApp/4.9.0 (iPhone; iOS 8.1.1; Scale/2.00)
Accept-Language: zh-Hans;q=1
Content-Length: 1659
X-Tingyun-Id: s8-utloiNb8;c=2;r=2140640508

appId=10001&appVersion=4.9.0&bundleIdentifier=com.pingan.pars&chS=PKXwVPYlgXk06HHPubC3akmiPpMgR6KsaQ%2Bt4M2jJjUc/s2OgG7aQTgPykBKi0EvAjCdb0t20uoASkeT97M21wbV56lWmnIvlrExdB2Jhfe7OXMJ0M77Whx0fAO8%2BOKi9NNTftTzTVijKT/kObVQUfqH1GQCob7KtrUN8nJxn/8%3D&channelType=01&cv=490&deviceId=h902704274530537c4335a514f5821f5a&deviceToken=2a2d999d889bdb302dd0c6087afe269b797f4fabf298404009545f8f19723fd4&jsonFlag=Y&mobilePhone=''' + my_mobile_phone + '''&osType=01&osVersion=8.1.1&pedometerList=%5B%0A%20%20%7B%0A%20%20%20%20%22iWatch%22%20%3A%20%220%22%2C%0A%20%20%20%20%22iPhone%22%20%3A%20%220%22%2C%0A%20%20%20%20%22pedometerNum%22%20%3A%20%2218785%22%2C%0A%20%20%20%20%22BMP%22%20%3A%20%220%22%2C%0A%20%20%20%20%22pedometerDate%22%20%3A%20%222017-11-05%22%0A%20%20%7D%2C%0A%20%20%7B%0A%20%20%20%20%22iWatch%22%20%3A%20%220%22%2C%0A%20%20%20%20%22iPhone%22%20%3A%20%220%22%2C%0A%20%20%20%20%22pedometerNum%22%20%3A%20%2218785%22%2C%0A%20%20%20%20%22BMP%22%20%3A%20%220%22%2C%0A%20%20%20%20%22pedometerDate%22%20%3A%20%22''' + today + '''%22%0A%20%20%7D%0A%5D&raiseFlag=Y&securityToken=PgWj8SWYg4gTTuvpXtzIgdytMLxirQKKk3AxwlZt6HKj8lAThU0Kr7HKjwI8aMAqUuCxiM2E6LkpZU6plCDIymd7pbVzY1IChD%2BCBEJkQwjGLlOvEw1RyvITrdfvJebgrC5C/EZgCDAmu36IO1Ztsw%3D%3D&timeset=YXCZD7hNQ9JLA363HFt5Ip5v%2BhbUlBNqvJCz496nlYe8rt2Ykad9AKQPr1aP6YnXdIYxidOamBlTUqLBShKL9JZowpkmd6Rd1PQAFoDhrEAR8feIPSy/laVJOJ/HaOEZtCvzG2nkssSW3YervLbSd81pKiKWcxLA4wsLHPp%2Bm7g%3D&token=2a2d999d889bdb302dd0c6087afe269b797f4fabf298404009545f8f19723fd4&uid=836832654629371904'''

a = send_http_package(package, "https")
print(a)

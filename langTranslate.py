from urllib.parse import quote
import http.client
import json
from pprint import pprint
import pandas as pd


def callApi(text):
    conn = http.client.HTTPSConnection("www.bing.com")
    payload = (
        "fromLang=hi&text="
        + quote(text)
        + "&to=gu&token=OgldDPOQ3chHI82_I4hOsj1NZKB87oCD&key=1684755912622&tryFetchingGenderDebiasedTranslations=true"
    )
    headers = {
        "authority": "www.bing.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "MUID=2D4CD444D4756F992C5CC6FBD5736E55; MUIDB=2D4CD444D4756F992C5CC6FBD5736E55; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=31571E29AD89413AB4F00AB5E6609B0E&dmnchg=1; _UR=QS=0&TQS=0; MicrosoftApplicationsTelemetryDeviceId=8fc7b032-c4ae-41ac-bc1d-d3e839f21f90; ANON=A=AA851CD34D498F9611C183B3FFFFFFFF&E=1c59&W=1; NAP=V=1.9&E=1bff&C=Vhd2xW4mP9q-vJ1QJenUuEx8Tz8R5eqmQ_B0cqcQABVtWGnVlTKP_g&W=1; PPLState=1; KievRPSSecAuth=FACCBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACJAP4+IMTuvRQATu5dI2PJ5tTPvrToRGD85kNsGrI6MuhOpjHYgm1S4HA7TsOwsxbBP2jJ0AXXF2rxxcRdulwCIVXuun+/11iOspQlyQqsbvlVNiN74osbM5r359VisMhWsyyGEfn3WojlQRHy1dwOz5VT3yo3yAsuS1qnFgoGPROnU6qI3xmGWXoWyrLouIMtF1OlXxhcOAJS6hElpfBj41AB+gR+NmGWWwwHTfrRjpPRvXvZKVbab6bcMw8hN/eEdj7oXc9hZ5OQCZ+SP/G/dMz9LwvmYT/s/RPDmzVo4ivJrPldfteDOdiQiZwVbgL2SN1A9UmO3F8JNUaxNxI/8G2bOmlXeRsNMi0qKp/CfNomAFj0I3drECjp2cO5ZP6LA/DMW1aQDM0rUgXKmx7SFjqGi/s97KivOSX7xgV9NfQEmKehs93VpgKFanD1kPl+kpiCzAHy7u7r2NZxIt82/1FiHsDG0v8LsM7uUfSOtfIz5TFsZnw6cQ35UfX2j5cvJkVAqAoxF4Lbg16ANeqhJDN3yCAMTbwMLEdkSQFrUtp+t6lY19gwzoASyixovXco1CrU51hFa/8gxZk5rbCAUISGl7w+rYOkpDzMLE/aBwC5EJdorKH1OwQNGHgSim0oTYNwd8H0KjG2QPLEre55rE4S17LH74pwartWDo71cG5qiAJls2/mIg11qcnAMLfc9/hPp/PS8Ac3LgNFQhhha84fUmdZrpNe/kccc0r6+CGsIBeLzSZQuz9AnRcRwovYFYTsAhM9yC/BVNVV32xVUF7PMqOJgeu0vSzTGVCGn0Qxuqavn9f4A/eQlTo2JKF5oJbbbYGlXzkEP5HiTplT22Zhw583RIkRj1q7bLy5PemLqxKI29QlA9LWxPMRxL4byMI0kFVe1azqJ4j3KJsZnlL+O4GLBGCbyPQUvrA7mqIzSL29s5WXk0kCnL53CD9Q3RS3wCxJ4Mo7gOIKFBOaN4o7kfB1zDIHRRcYriPgE+AJaw6agzyryhiQUYctmCG+5CZyuODph/Vw0mlOFsWKAD7YYicugh3nKN2eDYZZSkMVXKmLIs/P4MAinibtxAirbYuzpTYcjaCLBTyr7vwOSFoGabomMaEqbAXzIUfTvz7DbjbpoVi/VPfNhtR44HdsE3BtidG2RhZvYrOaMvUsqcvB7c0XYjC4c5X5XAU9pXnYxx2ASah4IGk38xDSLuBNYuPUJTwIp6NEcMSdPbqL87EwLQFVKQA0q2nHQR3UL93CnhYvO3svw5N+KWkThUFx4qLm6DbOg/llgS8uU4Hk0MIoxJXqdqG85sY9znexvajqL1PcWpc2Kq8Jtr/Z9gtr0cMic8Lbrd/a8j5Gkn4AjFnjct+U5w+8fUhSDpFmZW7nD6E+PYxKN57TB65kPB7X8pAUn2Tt9WgQbCtwDVJHauHRaXn7AKwBWE9Guk5ruLWAoQ8tsYfMqvCxQA9Xfh+rtVqTz5XQEAl9kEWbIRUzQ=; _U=19T0b6SmqAONvuvgLKd2sTPa2RfDlFS7WujY7MZf1ksq2MlxPjcXqp7t0mjXLbATgoXeL28JrEJ8soflgCyIiWFU4VPZfDHy3YtrfqRDcJqI5bGImTv_xYKgSHAlZVqXimrVRg72MHVK6eI1ok2V8_1GLV1qlC7MkGNJtoKZpAm7yhboOWOGzoYM8395beQXjF7rALVub_Fi28wKPpqtUdq61NkBTjoNPMmkk2JbOUQc; WLS=C=6475ba49b577bb30&N=Praveen; WLID=wY1t46ZkGSMCD1eUdd+akk5DuGREk355SUzvmLq0ndkSVBpC0KtSp0OSIi6v9WrjstCKY0fCbOi2hmQoBg1FZvDR5lnHlRpwG30f/gJUGCM=; _EDGE_S=SID=29C6D9871DC96506211BCA921CCF64B3&mkt=en-in; USRLOC=HS=1&ELOC=LAT=28.466588973999023|LON=77.03330993652344|N=Gurugram%2C%20Haryana|ELT=6|; _tarLang=default=hi; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJoaSJd; btstkn=I3H2XxRLvmOaLrwK9YPsNL%252BBwLnSV3dsPTy4HDB35SeP1l1syNQLST8PsaNTMWctl7PGZRskjYZxRdc5EZ6DdbjsfjZyb3U3Zwm8FP6ELUo%253D; SUID=A; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNS0xOVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6NH0=; ipv6=hit=1684495949976&t=6; ai_session=F0NJycktRR66VsRZ6Xd/6J|1684492350430|1684492350430; _SS=SID=29C6D9871DC96506211BCA921CCF64B3&R=66&RB=66&GB=0&RG=0&RP=63; _RwBf=ilt=1&ihpd=1&ispd=0&rc=66&rb=66&gb=0&rg=0&pc=63&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=2&l=2023-05-19T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=4003&s=2023-05-06T05:48:26.4158786+00:00&ts=2023-05-19T10:32:36.6288962+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&mta=0&e=HNpegEz4D5SZ8dYdMNm9enMJa4ythhWVz3ls0-SG3wb-79NGoo-Y33LX5-Y1SGfd54XRk0-PtSO-W3MLzTMeCQ&A=AA851CD34D498F9611C183B3FFFFFFFF; SRCHUSR=DOB=20230518&T=1684492349000&POEX=W&TPC=1684492361000; SRCHHPGUSR=SRCHLANG=en&BRW=XW&BRH=S&CW=1536&CH=182&SCW=1519&SCH=3992&DPR=1.3&UTC=330&DM=1&PV=15.0.0&HV=1684492362&WTS=63820024488&PRVCW=1536&PRVCH=746; _clck=14iozgq|2|fbq|0|1233; _clsk=3pkqo3|1684492366169|1|0|g.clarity.ms/collect; MUID=2DBA8972BFB360AE060B9A67BE4161F4; SRCHD=AF=NOFORM; SRCHHPGUSR=SRCHLANG=en&PV=15.0.0; SRCHUID=V=2&GUID=6E9B2E95F86C462FA555CC47882C585E&dmnchg=1; SRCHUSR=DOB=20230518; _EDGE_V=1; btstkn=iNi637%252Bhgz8JPOglSWXkpNEHPYGN6lVuMkFQX131Bvl7AogdSKvC5mbyJJ%252BMmOraJRt4gz%252F1kh0W6W6u951iuIMYA9tHrnZQZpn1vV5kBrA%253D; MUIDB=2D4CD444D4756F992C5CC6FBD5736E55",
        "origin": "https://www.bing.com",
        "referer": "https://www.bing.com/search?q=translator+english+to+hindi&qs=FT&pq=transl&sk=AS1&sc=10-6&cvid=EDB98ED42E25423FB705A262A7D8EFE3&FORM=QBLH&sp=2&ghc=1&lq=0",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"113.0.5672.127"',
        "sec-ch-ua-full-version-list": '"Google Chrome";v="113.0.5672.127", "Chromium";v="113.0.5672.127", "Not-A.Brand";v="24.0.0.0"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    conn.request(
        "POST",
        "/ttranslatev3?null=null&IG=9667FA6586F849EE806DD926D32017D8&IID=SERP.5697",
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


if __name__ == '__main__':
    df = pd.read_csv("data/hi-en.csv")

    inputs = df['hindi'].tolist()
    outputs = []
    i = 0
    for input in inputs:
        txt = [input]
        result = callApi(input)
        text = result[0]["translations"][0]["text"]
        txt.append(text)
        outputs.append(text)
        i = i+1
        print(i)

    df['gujrati'] = outputs
    df.to_csv("hi-gu.csv",index=False)

    pprint()
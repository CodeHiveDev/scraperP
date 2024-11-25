import requests

url = "https://shopee.com.br/api/v4/pdp/get_pc"
params = {
    "item_id": "23792034643",
    "shop_id": "1048234848",
    "tz_offset_minutes": "-180",
    "detail_level": "0"
}

headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "af-ac-enc-dat": "d5d18b69abb788bc",
    "af-ac-enc-sz-token": "4K7V7MAMcDT5gSkfsxuuwg==|aOVJ0iVGsqSenoK0mYPyLo8wj2gMtb9Ss4e+5/dVOnjiIQDQxceadKYOM+61u0SeVu16UXetlejJyNC/+VY=|6UEzwZ4B0cLy1tpg|08|3",
    "content-type": "application/json",
    "cookie": "_gcl_au=1.1.50375326.1729730103; _fbp=fb.2.1729730102659.135137240485149106; SPC_F=yITqdXnJYBifphrVWjkwEHXl1nTH3xWi; REC_T_ID=cee786d4-919f-11ef-b32e-b686b94bb589; _QPWSDCXHZQA=66b42365-397a-4206-fae8-4f5d201107c8; REC7iLP4Q=5ccd926a-0a43-466a-b9e0-e1140b6c1fde; blueID=eef65ef9-e802-4013-9537-566d955a4862; _ga_TP7597R910=GS1.1.1729730114.1.0.1729730114.60.0.0; SPC_CLIENTID=eUlUcWRYbkpZQmlmpetlrpwvyqrjajiv; SPC_U=1403043122; SPC_R_T_IV=Sk5sNTl5QUtORWthV0dyag==; SPC_T_ID=ixIjyd//gom+1Ic/TQMTgxOWsp4g05pxd0dSB2W3kHpSNq69NChC3Zn2LSg7Q7TlUoBBwpL8HgPvpYww6b4kTwvLvdxQHMPW0hgNKGgE878XWCw4JdSbQ6G3GxmdQlqn2TQsiWNCnPwlKD2wvt0jl2b/JuFYRw7OySMAN5t1LLA=; SPC_T_IV=Sk5sNTl5QUtORWthV0dyag==; SPC_R_T_ID=ixIjyd//gom+1Ic/TQMTgxOWsp4g05pxd0dSB2W3kHpSNq69NChC3Zn2LSg7Q7TlUoBBwpL8HgPvpYww6b4kTwvLvdxQHMPW0hgNKGgE878XWCw4JdSbQ6G3GxmdQlqn2TQsiWNCnPwlKD2wvt0jl2b/JuFYRw7OySMAN5t1LLA=; SPC_SI=F3w0ZwAAAABtMWpzb0xpcVYFCgAAAAAAY1lvMHlzSFo=; _gid=GA1.3.36296461.1731530863; SPC_EC=.R1pUNkRURGJGdG9BcHBLYmL64tI0JMByCWy5XGz6Obq08R7I//fqjuryRlgaQmREQiwjLucMc9QPwP8/oE1N3OUJwSIii9Ry29KpasdgkN9yAvq6mc+uvRbQJ0JQ+n8bW6A1E/Mg3C8NvMrzq/DZf9qWZM3iimqivHGt9bcCLd04z76Ax/58IQ1IIG29zwVT+OYRoSDxGZw5kCbhgzXslGbBV0XyfTG7GVGH7RgPiMo3TGpJBCzzI8f2Hn4X5GEi; SPC_ST=.R1pUNkRURGJGdG9BcHBLYmL64tI0JMByCWy5XGz6Obq08R7I//fqjuryRlgaQmREQiwjLucMc9QPwP8/oE1N3OUJwSIii9Ry29KpasdgkN9yAvq6mc+uvRbQJ0JQ+n8bW6A1E/Mg3C8NvMrzq/DZf9qWZM3iimqivHGt9bcCLd04z76Ax/58IQ1IIG29zwVT+OYRoSDxGZw5kCbhgzXslGbBV0XyfTG7GVGH7RgPiMo3TGpJBCzzI8f2Hn4X5GEi; __LOCALE__null=BR; csrftoken=4g6ak6wERpjq6rtiiDCuIow0ybUbwfFh; _sapid=64c364028fdf7465619ea8007b8f2473844f20bdf69c866a81720a5c; SPC_SEC_SI=v1-N2NISG00bDd0TFdTNWlpY0MYDa/YSKeoNXNlt/D2mLR4fDjP0ovDDPfOcDBD5f5DHpbwtyRtC9Hc9XolhIPqYlReUxLpwxG2/IgeTiDWuSg=; SPC_CDS_CHAT=76235155-d080-4a88-81c0-8bec344c8731; AC_CERT_D=U2FsdGVkX18saIG7wdnrMXklPw7/vW27ZiHuipd3Wak0KFWINoWoPcOSjpT85whtlA3roBHEr2RNs4REckJzrkxBjLp4kUzNnND05PoCb47LQriQOppyDgSGTJHMrp3T/AgbO4MfWX37ufKn1LOgVBi9V08467NhvuBayyRt1fP+Tg6G1PB6wVCviah3D6uXCepZuG/Dfcm2ClLidfWCVSg6EO1NB/pUAHiLtFJuYTFAoVvqTQU/98e19n/R2Jnyv8a9XBl5h71/0Gv+q80wiJCdBatGc7XByezDabKhR68C1bzOXgbe95UpbIZmAdjzb3HZxJm+7tlb6Q9Xw7RHc1oVf83CrqlBj8mxBlkj8a2o2wUFogRQCXMgKLs0KIRtuCwdFir83qzQKC70w6pEb2+AKh/Heu/FKyBqJwhodrydz5NUEosEjN1sc20fiM/wK5fMGa80plE54X5PmSGB46bPnpvAKp0lMPCHavZTU7b2pTZc2b0q9CPr+lDhaPZkropmfsuEb6//HkLNEat/WdNUJxb/h7f6lXOD7dy0Jrdx/ZLWeeJ3XVACZ0+wMMtGWkywLlwpHzdPoxv79lalUtckYKn7ajoAOsht+mOVYdVswzxXttVRMD6PxG8Rbu+MsifXw38v+otZnzA5+KVg6/MEvdHO444UOL6IZ8B00EYdNq1asSqMkKitc63qPpYdnC+CMufMxyYV+G5orrccZx0FjXvArwEL72L9fZCESfhnn8oxRYEKPT9myvknsa1ovLcHmeR2n+D7x1ysVTF1KqcfRplFDfKoGvvsoqUUWsCMpiZf9j1V1qPQ1W5XYvoOw646MNs6YcoAw4TOaYFxFSz2gaOpqsbxcIRU+P/J25+RLF7PRgbgkn1hKT3TY3O2mWrrup/GZF2N/NhkFVtXDVLc+UmyYuxPmeI2uXIVophcaagZ/ICyqmty7UnPoZBoawVKXG4bdWJsAziNSX5li1BRNfdoP7gB66VRdremRmS6qIPb2VidEuyZleG9adVFP1ae5rZsahzGcUIxAb1lRtT8TJb4LajlTJLP3tTwL58bfr8FNjHg9hsplZmg0Cdz6KrFTPvUaKKIqlYOIMWLtg==",
    "referer": "https://shopee.com.br/Homem-Aranha-Brinquedo-Infantil-Lan%C3%A7ador-De-Teia-dardos-Para-Crian%C3%A7as-Spiderman-Marvel's-The-Avengers-Cartoon-i.1048234848.23792034643?sp_atk=1662b56f-6beb-4470-83bc-d714972a1f21&xptdk=1662b56f-6beb-4470-83bc-d714972a1f21",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sz-token": "4K7V7MAMcDT5gSkfsxuuwg==|aOVJ0iVGsqSenoK0mYPyLo8wj2gMtb9Ss4e+5/dVOnjiIQDQxceadKYOM+61u0SeVu16UXetlejJyNC/+VY=|6UEzwZ4B0cLy1tpg|08|3",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "x-api-source": "pc",
    "x-csrftoken": "4g6ak6wERpjq6rtiiDCuIow0ybUbwfFh",
    "x-sap-ri": "9d7b3667feaeddc4b80b993f0501093b47a7c9023dbf039a20ab",
    "x-sap-sec": "2NM8SizsYAyiyVXyzAjyzWpyIAg3zDNynAi6zXry/AgszTXyMAg8z1rytRidzTjy2Ai0zDXyR5gezUXy0Ai9z8AyU5jhzXNymAi4zWXyZAgTzVbygRifz9RyyRijz9ryURgyz9byWRgxzujyfAgizUwybAiizFuy85iyzuNyg5gozuXywAjYz8uyxRgYzWpyzAjyzAirieKM02jyzAgTzRjyH9Eh8zjyiQ7pxhXaIiRJCAjyNTF4z5jyzAjyg8+zUbDxstl1FAbyzAjyz9P4ZWDDKEPwgVXlzAiGgGeczAjyUbZi23jyRmKYwnAyfkjmzAjyEcwqztO8kHNlzAjkzRjyHAwyzAjyznjUY/HGptnuhkA6tVjyzVnsY99XWrXyzAjyzAiNiuLBUfNlzAjyzV+teAjyzAjyznLGeZZyiAwyzFrlzAjyzAgAQ6sPejjlzAjnJYt8ZP+fC5XyzAiYt+2s2Rjyzuv7DN6SHg0RrOGJJnNpvDd0HjYFCLS2Rz5h4K1ZZQVej4OocApWtCVDSP5JOeLMEZefWlNSLNPcBqJ/AB8/H11RVgDVbRS4NST/OjWe54O+rsVt/tkN80ADV9GihZl35JRmt3oCGlYKB4FMzbT1GQbzUhE+KQlGzVpqK6VbpSqCpLYtOW78ZLeYaYXsVhE001Mz+E7riPEZTi6g8dAMYUPFzcZ0fiICI7UG9xxxoZQxH+jazDbzzAfo6YIKChKk+4LC9qB69Tig6UEvUAKx3I2NSMm2K9QYbXsCl5rBvsEX76PcsVPMr7o7OWxZETo506CM5NbryZyYPq29heZqOTWpxym+vbHXC8hGKXi2jsLWJy2zfUWtUMt+tj0+dAkIryoKimm+SgbwnggKmGFpv2BISUtIqmm2rSrhnXpoAGqFBfaA+iv9n0KrAq1HKj33TZfdbNZuKeq6+JpMeEeoReIptKeZdTBH8pfyTEtR/nciPOeRg3LrmCQk66veEmqYqEgspvqJGItJ27DQ7PLWHDg9banUuzV9AOWeRAqJpFV0CcJ6Hhy7iIpJnqOqnPArYx1b8AfwgkYibnIIC6qfotFOKxO25fELVxUTTApL8WfMNA2w1oEPFWonbT40/I8iqK91bR3n2U0CPrImzAXyzAjz7j01mAjyznUSCthaRDIsz5jyzvRkzAjwzAjyJiucT5brZilZXQ4tzAjyzAuyzAgniloqyQRyzA5yzAgalOr1XMA6z7XZCz0izAjyGAjyzu4Du96yYD1D5RiPl5zkwiDw9c2w9QNPXuriZRpiYDiF5+wMl5X41z8uXF2ZlIu5zwa8a92fVlwmzAjyzFXyzAfGXOAYyD1QXquluA5mxla1IiXsmiaB1XJtycaVlIwsXpSDbApyzAjygzjyz1eNEpebZP8+/FMdh3SsFzfviD9NKFCpLhAyzAjyzAjymAjyzn7BjMNOzA1dmAjyzDbS1lTNYDArzAjyzn==",
    "x-shopee-language": "pt-BR",
    "x-sz-sdk-version": "1.12.5"
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.json())

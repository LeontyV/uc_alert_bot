#! /usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import request
from urllib.error import HTTPError, URLError
from datetime import datetime as dt
import OpenSSL

#Global
CRLs = {
	'ca_2018': 'http://www.ca.rkomi.ru/ra/cdp/cit-gov2018.crl',
	'udc_2018': 'http://www.udc.rkomi.ru/certsrv/cit-gov2018.crl',
	'ca_2017': 'http://www.ca.rkomi.ru/ra/cdp/cit-gov2017.crl',
	'udc_2017': 'http://www.udc.rkomi.ru/certsrv/cit-gov2017.crl',
	'udc_2018_gost2012': 'http://www.udc.rkomi.ru/certsrv/cit-gov2018_gost12.crl',
	'ca_2018_gost2012': 'http://www.ca.rkomi.ru/ra/cdp/cit-gov2018_gost12.crl',
	'ca_cit-gov2019.crl': 'http://www.ca.rkomi.ru/ra/cdp/cit-gov2019.crl',
	'udc_cit-gov2019.crl': 'http://www.udc.rkomi.ru/certsrv/cit-gov2019.crl',
	'ca_cit-gov2020.crl': 'http://www.ca.rkomi.ru/ra/cdp/cit-gov2020.crl',
	'udc_cit-gov2020.crl': 'http://www.udc.rkomi.ru/certsrv/cit-gov2020.crl'
}
status_crl = {
	'ca_2018': '',
	'udc_2018': '',
	'ca_2017': '',
	'udc_2017': '',
	'udc_2018_gost2012': '',
	'ca_2018_gost2012': '',
	'ca_cit-gov2019.crl': '',
	'udc_cit-gov2019.crl': '',
	'ca_cit-gov2020.crl': '',
	'udc_cit-gov2020.crl': ''
}


async def check_crl(strline):	#проверяем период действия СОС
	url_to_check = CRLs[strline]
	try:
		crl = request.urlopen(url_to_check).read()
		crl_object = OpenSSL.crypto.load_crl(OpenSSL.crypto.FILETYPE_ASN1, crl)
		ccrl_object = crl_object.to_cryptography()
		tmp = (ccrl_object.next_update - dt.now()).total_seconds() // 60
		if (tmp < 90):
			status_crl[strline] = 'ALERT! Осталось ' + str(tmp) + ' минут.\n' + url_to_check
		else:
			status_crl[strline] = 'ok! осталось ' + str(tmp) + ' минут.\n'  + url_to_check
	except HTTPError:
		print(f'Ошибка 404. Файл {url_to_check} не найден!!!')
		status_crl[strline] = f'Ошибка 404. Файл {url_to_check} не найден!!!'
		return
	except TimeoutError:
		print(f'Ошибка таймаута. [WinError 10060] Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного отклика уже подключенного компьютера')
	except URLError:
		print(f'URLError - не скачивается ссылка: {url_to_check}')
	except OpenSSL.crypto.Error:
		print("('asn1 encoding routines', 'ASN1_get_object', 'header too long')")
		status_crl[strline] = f"ALERT! Ошибка декодирования CRL {url_to_check}"
		return



async def crl_to_tlgrm():
	for strline in CRLs:
		await check_crl(strline)
	return status_crl
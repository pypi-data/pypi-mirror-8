#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from . import csp
from .certutils import Attributes, CertValidity, KeyUsage, EKU,\
    CertExtensions, SubjectAltName, CertificatePolicies, PKCS7Msg, \
    CertExtension, CertificateInfo, autopem, set_q_defaults

import platform
from binascii import hexlify, unhexlify
from .filetimes import filetime_from_dec
from datetime import datetime, timedelta
from binascii import b2a_qp, a2b_qp
import sys
import time
from functools import wraps
if sys.version_info >= (3,):
    unicode = str
    ord = lambda x: x
else:
    unicode = unicode


# Обертка для функций, которые могут не сработать из-за длительного простоя
# туннеля, при работе с криптопровайдером внешнего хранилища. Максимальный
# таймаут = 0.25 + 0.5 + 1.0 = 1.75 секунд
def retry(f, timeout=0.25, num_tries=4):
    @wraps(f)
    def wrapper(*args, **nargs):
        sleep_time = timeout
        for tr in range(num_tries):
            try:
                return f(*args, **nargs)
            except Exception:
                if tr == num_tries - 1:
                    raise
                time.sleep(sleep_time)
                sleep_time *= 2

    return wrapper


def _to_hex(s):
    return unicode(b2a_qp(s), 'ascii').replace('=', '\\x')


def _from_hex(s):
    if isinstance(s, bytes):
        s = unicode(s, 'ascii')
    return a2b_qp(s.replace('\\x', '='))


def gen_key(cont, local=True, silent=False, provider=None):
    '''
    Создание контейнера и двух пар ключей в нем

    :cont: Имя контейнера (строка)
    :local: Если True, контейнер создается в локальном хранилище по умолчанию
    :silent: Если True, включает режим без диалоговых окон. Без аппаратного датчика случайных
        чисел в таком режиме контейнер создать невозможно!
        По умолчанию silent=False
    :provider: Если не None, флаг local игнорируется и криптопровайдер
        выбирается принудительно
    :returns: True, если операция успешна

    '''
    silent_flag = csp.CRYPT_SILENT if silent else 0
    if provider is None:
        provider = str("Crypto-Pro HSM CSP") if not local else None
    cont = _from_hex(cont)

    try:
        ctx = csp.Crypt(cont, csp.PROV_GOST_2001_DH, silent_flag, provider)
    except (ValueError, SystemError):

        if platform.system() == 'Linux' and provider is None:
            cont = b'\\\\.\\HDIMAGE\\' + cont

        ctx = csp.Crypt(cont, csp.PROV_GOST_2001_DH, csp.CRYPT_NEWKEYSET |
                        silent_flag, provider)

    ctx.set_password(str(''), csp.AT_KEYEXCHANGE)
    ctx.set_password(str(''), csp.AT_SIGNATURE)
    try:
        key = ctx.get_key()
    except ValueError:
        key = ctx.create_key(csp.CRYPT_EXPORTABLE, csp.AT_SIGNATURE)

    assert key, 'NULL signature key'

    try:
        ekey = ctx.get_key(csp.AT_KEYEXCHANGE)
    except ValueError:
        ekey = ctx.create_key(csp.CRYPT_EXPORTABLE, csp.AT_KEYEXCHANGE)

    assert ekey, 'NULL exchange key'
    return True


def remove_key(cont, local=True, provider=None):
    '''
    Удаление контейнера

    :cont: Имя контейнера
    :local: Если True, контейнер удаляется в локальном хранилище по умолчанию
    :provider: Если не None, флаг local игнорируется и криптопровайдер
        выбирается принудительно
    :returns: True, если операция успешна

    '''
    cont = _from_hex(cont)
    if provider is None:
        provider = str("Crypto-Pro HSM CSP") if not local else None
    csp.Crypt.remove(cont, csp.PROV_GOST_2001_DH, provider)
    return True


def create_request(cont, params, local=True, provider=None, insert_zeroes=False):
    """Создание запроса на сертификат

    :cont: Имя контейнера
    :params: Параметры запроса в виде словаря следующего вида:
        {
        'Attributes' : список пар [('OID', 'значение'), ...],
        'CertificatePolicies' : список вида [(OID, [(квалификатор, значение), ...]), ... ]
            OID - идент-р политики
            квалификатор - OID
            значение - произвольная байтовая строка
        'ValidFrom' : Дата начала действия (объект `datetime`),
        'ValidTo' : Дата окончания действия (объект `datetime`),
        'EKU' : список OIDов,
        'SubjectAltName' : список вида [(тип, значение), (тип, значение), ]
            где значение в зависимости от типа:
                'otherName' : ('OID', 'байтовая строка')
                'ediPartyName' : ('строка', 'строка') или 'строка'
                'x400Address' : 'байтовая строка'
                'directoryName' : [('OID', 'строка'), ...]
                'dNSName' : строка
                'uniformResourceIdentifier' : строка
                'iPAddress' : строка
                'registeredID' : строка
        'KeyUsage' : список строк ['digitalSignature', 'nonRepudiation', ...]
        'RawExtensions' : список троек [('OID', 'байтовая строка', bool(CriticalFlag)), ...]
            предназначен для добавления в запрос произвольных расширений,
            закодированных в DER-кодировку внешними средставми
        }
    :local: Если True, работа идет с локальным хранилищем
    :provider: Если не None, флаг local игнорируется и криптопровайдер
        выбирается принудительно
    :insert_zeroes: Если True, в запрос добавляются нулевые значения для ИНН, ОГРН
    :returns: байтовая строка с запросом в DER-кодировке

    """

    if provider is None:
        provider = str("Crypto-Pro HSM CSP") if not local else None
    cont = _from_hex(cont)
    ctx = csp.Crypt(cont, csp.PROV_GOST_2001_DH, 0, provider)
    req = csp.CertRequest(ctx, )
    set_q_defaults(params, insert_zeroes)
    req.set_subject(Attributes(params.get('Attributes', [])).encode())
    validity = CertValidity(params.get('ValidFrom', datetime.now()),
                            params.get('ValidTo', datetime.now() + timedelta(days=365)))
    eku = EKU(params.get('EKU', []))
    usage = KeyUsage(params.get('KeyUsage', []))
    all_exts = [usage, eku]
    altname = params.get('SubjectAltName', [])
    if len(altname):
        all_exts.append(SubjectAltName(altname))
    pols = params.get('CertificatePolicies', [])
    if len(pols):
        all_exts.append(CertificatePolicies(pols))
    for (oid, data, crit) in params.get('RawExtensions', []):
        all_exts.append(CertExtension(str(oid), data, bool(crit)))
    ext_attr = CertExtensions(all_exts)
    validity.add_to(req)
    ext_attr.add_to(req)
    return req.get_data()


def bind_cert_to_key(cont, cert, local=True, provider=None):
    """Привязка сертификата к закрытому ключу в контейнере

    :cont: Имя контейнера
    :cert: Сертификат в байтовой строке
    :local: Если True, работа идет с локальным хранилищем
    :provider: Если не None, флаг local игнорируется и криптопровайдер
        выбирается принудительно
    :returns: отпечаток сертификата в виде строки

    """
    if provider is None:
        provider = str("Crypto-Pro HSM CSP") if not local else None
    cert = autopem(cert)
    cont = _from_hex(cont)
    ctx = csp.Crypt(cont, csp.PROV_GOST_2001_DH, 0, provider)
    newc = csp.Cert(cert)
    newc.bind(ctx)
    cs = csp.CertStore(ctx, b"MY")
    cs.add_cert(newc)
    return hexlify(newc.thumbprint())


def get_certificate(thumb=None, name=None):
    """Поиск сертификатов по отпечатку

    :thumb: отпечаток, возвращенный функцией `bind_cert_to_key`
    :name: имя субъекта для поиска (передается вместо параметра :thumb:)
    :returns: сертификат в байтовой строке

    """
    assert thumb or name and not (thumb and name), 'Only one thumb or name allowed'
    cs = csp.CertStore(None, b"MY")
    if thumb is not None:
        res = list(cs.find_by_thumb(unhexlify(thumb)))
    else:
        res = list(cs.find_by_name(bytes(name)))
    assert len(res), 'Cert not found'
    cert = res[0]
    return cert.extract()


@retry
def sign(thumb, data, include_data):
    """Подписывание данных сертификатом

    :thumb: отпечаток сертификата, которым будем подписывать
    :data: бинарные данные, байтовая строка
    :include_data: булев флаг, если True -- данные прицепляются вместе с подписью
    :returns: данные и/или подпись в виде байтовой строки

    """
    cs = csp.CertStore(None, b"MY")
    store_lst = list(cs.find_by_thumb(unhexlify(thumb)))
    assert len(store_lst), 'Unable to find signing cert in system store'
    signcert = store_lst[0]
    mess = csp.CryptMsg()
    sign_data = mess.sign_data(data, signcert, not(include_data))
    return sign_data


@retry
def sign_and_encrypt(thumb, certs, data):
    """Подписывание данных сертификатом

    :thumb: отпечаток сертификата, которым будем подписывать
    :certs: список сертификатов получателей
    :data: байтовая строка с данными
    :returns: данные и подпись, зашифрованные и закодированные в байтовую строку

    """
    certs = [autopem(c) for c in certs]
    cs = csp.CertStore(None, b"MY")
    store_lst = list(cs.find_by_thumb(unhexlify(thumb)))
    assert len(store_lst), 'Unable to find signing cert in system store'
    signcert = store_lst[0]
    mess = csp.CryptMsg()
    for c in certs:
        cert = csp.Cert(c)
        mess.add_recipient(cert)
    sign_data = mess.sign_data(data, signcert)
    encrypted = mess.encrypt_data(sign_data)
    return encrypted


@retry
def check_signature(cert, sig, data):
    """Проверка подписи под данными

    :cert: сертификат в байтовой строке или `None`
    :data: бинарные данные в байтовой строке
    :sig: данные подписи в байтовой строке
    :local: Если True, работа идет с локальным хранилищем
    :returns: True или False

    Если :cert: передан как None, осуществляется проверка всех подписантов в
    подписи, с использованием сертификатов, которые содержатся в самой подписи.
    Иначе проверяется только подписант, соответствующий переданному сертификату.

    """
    sign = csp.Signature(sig)
    if cert is None:
        return all(sign.verify_data(data, i) for i in range(sign.num_signers()))
    cert = autopem(cert)
    cert = csp.Cert(cert)
    icert = csp.CertInfo(cert)
    cissuer = icert.issuer()
    cserial = icert.serial()
    for i in range(sign.num_signers()):
        isign = csp.CertInfo(sign, i)
        if (cissuer == isign.issuer() and
                cserial == isign.serial()):
            return sign.verify_data(data, i)
    return False


@retry
def encrypt(certs, data):
    """Шифрование данных на сертификатах получателей

    :certs: список сертификатов в байтовых строках
    :data: данные в байтовой строке
    :returns: шифрованные данные в байтовой строке

    """
    bin_data = data
    certs = [autopem(c) for c in certs]
    msg = csp.CryptMsg()
    for c in certs:
        cert = csp.Cert(c)
        msg.add_recipient(cert)
    encrypted = msg.encrypt_data(bin_data)
    return encrypted


@retry
def decrypt(data, thumb):
    """Дешифрование данных из сообщения

    :thumb: отпечаток сертификата для расшифровки
    :data: данные в байтовой строке
    :returns: шифрованные данные в байтовой строке

    """
    cs = csp.CertStore(None, b"MY")
    certs = list(cs.find_by_thumb(unhexlify(thumb)))
    assert len(certs), 'Certificate for thumbprint not found'
    bin_data = data
    msg = csp.CryptMsg(bin_data)
    msg.decrypt_by_cert(certs[0])
    return msg.get_data()


def pkcs7_info(data):
    """Информация о сообщении в формате PKCS7

    :data: данные в байтовой строке
    :returns: словарь с информацией следующего вида:
    {
        'Content': '....', # байтовая строка
        'Certificates': [сертификат, сертификат, ...], # байтовые строки
        'SignerInfos': [ { 'SerialNumber': 'строка', 'Issuer': [(OID, 'строка'), ... ] }, ... ],
        'ContentType': 'signedData' # один из ('data', 'signedData',
                                    #   'envelopedData', 'signedAndEnvelopedData', 'digestedData',
                                    #   'encryptedData')
        'RecipientInfos': [ { 'SerialNumber': 'строка', 'Issuer': [(OID, строка), ...] }, ... ],
    }


    """
    msg = csp.CryptMsg(data)
    res = PKCS7Msg(data).abstract()
    res['Content'] = msg.get_data()
    res['Certificates'] = list(x.extract() for x in csp.CertStore(msg))
    return res


def cert_subject_id(cert):
    """Функция получения Subject Key Id сертификата.

    :cert: сертификат в base64, или в бинарнике
    :returns: Строку из шестнадцатиричных цифр.

    """
    cert = autopem(cert)
    cert = csp.Cert(cert)
    return hexlify(cert.subject_id())


def cert_info(cert):
    """Информация о сертификате

    :cert: сертификат в base64
    :returns: словарь с информацией следующего вида:
    {
        'Version' : целое число,
        'ValidFrom' : ДатаНачала (тип datetime),
        'ValidTo' : ДатаОкончания (тип datetime),
        'Issuer': [(OID, строка), ...],
        'UseToSign': булев флаг,
        'UseToEncrypt' : булев флаг,
        'Thumbprint': строка,
        'SerialNumber': СерийныйНомер,
        'Subject': [(OID, строка), ...],
        'Extensions': [OID, OID, ...]
    }

    """
    cert = autopem(cert)
    infoasn = CertificateInfo(cert)
    cert = csp.Cert(cert)
    info = csp.CertInfo(cert)
    res = dict(
        Version=info.version(),
        ValidFrom=filetime_from_dec(info.not_before()),
        ValidTo=filetime_from_dec(info.not_after()),
        Issuer=Attributes.load(info.issuer(False)).decode(),
        Thumbprint=hexlify(cert.thumbprint()),
        UseToSign=bool(info.usage() & csp.CERT_DIGITAL_SIGNATURE_KEY_USAGE),
        UseToEncrypt=bool(info.usage() & csp.CERT_DATA_ENCIPHERMENT_KEY_USAGE),
        SerialNumber=':'.join(hex(ord(x))[2:] for x in reversed(info.serial())),
        Subject=Attributes.load(info.name(False)).decode(),
        Extensions=infoasn.EKU(),
    )
    return res


class Hash(object):

    """Хэш по ГОСТ 3411, имитирующий интерфейс дайджестов из `hashlib`.

    ВАЖНО: после первого вызова digest() или hexdigest(), к хэшу больше нельзя
    добавлять данные (ограничения CryptoAPI 2.0)

    Пример использования:
    > data = os.urandom(10000)
    > h = GOSTR3411(data)
    > print(h.DIGEST_URI)
    > print(h.hexdigest())

    """

    DIGEST_URI = "http://www.w3.org/2001/04/xmldsig-more#gostr3411"

    def _init_hash(self, data, key=None):
        self._hash = (csp.Hash(self._ctx, data, key)
                      if data else csp.Hash(self._ctx, key))

    def __init__(self, data=None):
        '''
        Инициализация хэша. Если присутствует параметр `data`, в него
        подгружаются начальные данные.

        '''
        self._ctx = csp.Crypt(
            b'',
            csp.PROV_GOST_2001_DH,
            csp.CRYPT_VERIFYCONTEXT,
            None
        )
        self._init_hash(data)

    def update(self, data):
        '''
        Добавление данных в хэш.

        '''
        self._hash.update(data)

    def digest(self):
        '''
        Возвращает дайджест данных и закрывает хэш от дальнейших обновлений.

        '''
        return self._hash.digest()

    def _derive_key(self):
        '''
        Возвращает ключевой объект для использования в HMAC

        '''
        return self._hash.derive_key()

    def hexdigest(self):
        '''
        Возвращает шестнадцатиричное представление хэша.

        '''
        return hexlify(self.digest())

    def verify(self, cert, signature):
        '''
        Проверка подписи, полученной из экземпляра класса `SignedHash`.

        :cert: Сертификат с открытым ключом подписанта в PEM или DER
        :signature: Бинарные данные подписи
        :returns: True или False

        '''
        cert = csp.Cert(autopem(cert))
        return self._hash.verify(cert, signature)


class HMAC(Hash):

    '''
    Вычисление HMAC в соответствии с ГОСТ 3411-94

    Пример использования:
    > data = os.urandom(10000)
    > key = b'some secret password'
    > mac = HMAC(key, data)
    или
    > mac = HMAC(key)
    > mac.update(data)

    > print(mac.hexdigest())

    '''

    def __init__(self, key, data=None):
        '''
        Инициализация HMAC-а. Помимо параметров базового класса, получает `key`
        -- байтовую строку с секретом

        '''
        _keyhash = Hash(key)
        _key = _keyhash._derive_key()

        self._ctx = _keyhash._ctx
        self._init_hash(data, _key)


class SignedHash(Hash):

    '''
    Хэш ГОСТ 3411 с возможностью подписывания. Требует наличия в хранилище
    сертификата, привязанного к контейнеру закрытого ключа.

    Пример использования:
    > data = os.urandom(10000)
    > digest = SignedHash('0123456789ABCDEF123456789ABCD')
    > print(digest.SIGNATURE_URI)
    > digest.update(data)
    > sig = digest.sign()
    > print(sig.encode('base64').rstrip())

    Для проверки подписи не требуется закрытый ключ, поэтому может
    использоваться базовый класс:
    > new_digest = Hash(data)

    > cert = open('cert.pem').read()
    или
    > cert = get_certificate('0123456789ABCDEF123456789ABCD')

    > res = new_digest.verify(cert, sig)
    > print(res)

    '''

    SIGNATURE_URI = "http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411"

    def __init__(self, thumb, data=None):
        '''
        Инициализация хэша. Помимо параметров базового класса, получает `thumb`
        -- отпечаток

        '''
        cs = csp.CertStore(None, b"MY")
        store_lst = list(cs.find_by_thumb(unhexlify(thumb)))
        assert len(store_lst), 'Unable to find signing cert in system store'
        self._ctx = csp.Crypt(store_lst[0])
        self._init_hash(data)

    def sign(self):
        '''
        Возвращает подпись хэша данных и закрывает хэш от дальнейших обновлений.

        '''
        return self._hash.sign()

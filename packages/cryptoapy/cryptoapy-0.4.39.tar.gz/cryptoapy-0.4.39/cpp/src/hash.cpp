#include "hash.hpp"
#include "context.hpp"
#include "cert.hpp"

void Hash::init(Crypt *ctx) throw(CSPException)
{
    parent = ctx;
    parent->ref();
    if(!CryptCreateHash(
        parent->hprov,
        CALG_GR3411, 
        0, 
        0, 
        &hhash)) 
    {
        throw CSPException("Hash::init() failed");
    }
}

/**
 * \~english
 * Create hash from initial data
 *
 * * ctx -- `csp.Crypt`, used for hashing, signing and verifying
 * * STRING, LENGTH -- initial binary data.
 * 
 * \~russian
 * Создание хэша из начальных данных
 *
 * * ctx -- Экземпляр `csp.Crypt` для хэширования, подписывания и проверки * подписи
 * * STRING, LENGTH -- начальные данные.
 *
 */
Hash::Hash(Crypt *ctx, BYTE *STRING, DWORD LENGTH) throw(CSPException)
{
    init(ctx);
    this->update(STRING, LENGTH);
}

Hash::Hash(Crypt *ctx) throw(CSPException)
{
    init(ctx);
}

Hash::~Hash() throw(CSPException)
{
    if (hhash && !CryptDestroyHash(hhash)) {
        throw CSPException("~Hash: Couldn't release handle");
    }
    parent->unref();
}

void Hash::digest(BYTE **s, DWORD *slen) throw(CSPException) 
{
    DWORD n = sizeof(DWORD);
    if (!CryptGetHashParam(hhash, HP_HASHSIZE, (PBYTE)slen, &n, 0)) {
        throw CSPException("Hash.digest(): Couldn't determine hash size");
    }
    *s = (BYTE*)malloc(*slen);
    if (!CryptGetHashParam(hhash, HP_HASHVAL, *s, slen, 0)) {
        DWORD err = GetLastError();
        free((void *)*s);
        throw CSPException("Hash.digest(): Couldn't get hash value", err);
    }
}

void Hash::update(BYTE *STRING, DWORD LENGTH) throw(CSPException)
{
    if(!CryptHashData(
        hhash, 
        STRING, 
        LENGTH, 
        0)) 
    {
        throw CSPException("Hash::update() failed");
    }
}

void Hash::sign(BYTE **s, DWORD *slen, DWORD dwKeyspec) throw(CSPException) 
{
    if(!CryptSignHash(
        hhash, 
        dwKeyspec, 
        NULL, 
        0, 
        NULL, 
        slen)) 
    {
        throw CSPException("Hash.sign(): Couldn't determine signature size");
    }

    *s = (BYTE*)malloc(*slen);

    if (!CryptSignHash(
        hhash, 
        dwKeyspec, 
        NULL, 
        0, 
        *s, 
        slen)) 
    {
        DWORD err = GetLastError();
        free((void *)*s);
        throw CSPException("Hash.sign(): Couldn't get signature value", err);
    }
}

/**
 * \~russian
 * Проверка подписи под данными, полученной путем вызова `Hash::sign`
 *
 * * `cert` -- сертификат с открытым ключом для проверки
 * * `STRING`, `LENGTH` -- подпись в виде бинарной строки
 *
 * На момент вызова данные должны быть загружены в хэш путем начальной
 * инициализации или вызовом `Hash::update()`.
 * \~english
 * Test Test Test
 *
 */
bool Hash::verify(Cert *cert, BYTE *STRING, DWORD LENGTH) throw (CSPException)
{
    HCRYPTKEY hPubKey = NULL;
    // Get the public key from the certificate
    if (!CryptImportPublicKeyInfo(
        parent->hprov, 
        MY_ENC_TYPE,
        &cert->pcert->pCertInfo->SubjectPublicKeyInfo,
        &hPubKey))
    {
        throw CSPException("Hash.verify(): Couldn't get certificate public key handle");
    }

    if (!CryptVerifySignature(
            hhash, 
            STRING, 
            LENGTH, 
            hPubKey,
            NULL, 
            0
        ))
    {
        DWORD err = GetLastError();
        if (err == NTE_BAD_SIGNATURE) {
            return false;
        }
        throw CSPException("Hash.verify(): error verifying hash", err);
    }
    return true;
}

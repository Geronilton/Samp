import crcmod
import qrcode
from io import BytesIO

def Payload(nome, chavepix, valor, cidade, txtId):
    valor = valor.replace(',', '.')

    merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{len(chavepix):02}{chavepix}'
    transactionAmount_tam = f'{len(valor):02}{float(valor):.2f}'
    addDataField_tam = f'05{len(txtId):02}{txtId}'

    payloadFormat = '000201'
    merchantAccount = f'26{len(merchantAccount_tam):02}{merchantAccount_tam}'
    merchantCategCode = '52040000'
    transactionCurrency = '5303986'
    transactionAmount = f'54{transactionAmount_tam}'
    countryCode = '5802BR'
    merchantName = f'59{len(nome):02}{nome}'
    merchantCity = f'60{len(cidade):02}{cidade}'
    addDataField = f'62{len(addDataField_tam):02}{addDataField_tam}'
    crc16 = '6304'

    payload = gerarPayload(payloadFormat, merchantAccount, merchantCategCode, transactionCurrency, transactionAmount, countryCode, merchantName, merchantCity, addDataField, crc16)

    # Gera QR code em memória
    img_buffer = BytesIO()
    qr_img = qrcode.make(payload)
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return payload, img_buffer

def gerarPayload(*args):
    payload = ''.join(args)
    return gerarCrc16(payload)

def gerarCrc16(payload):
    crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    crc = hex(crc16(payload.encode('utf-8'))).replace('0x', '').upper().zfill(4)
    return f'{payload}{crc}'

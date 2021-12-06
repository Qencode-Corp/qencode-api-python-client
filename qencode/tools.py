#
from const import *
import datetime
import hashlib
import hmac
import requests
from requests.utils import quote
import xml.etree.cElementTree as et
import uuid


def generate_aws_signed_url(
    region, bucket, object_key, access_key, secret_key, expiration, endpoint=None
):

    # request elements
    http_method = 'GET'
    endpoint = endpoint if endpoint else 's3.amazonaws.com'
    host = bucket + '.' + endpoint
    endpoint = 'https://' + host

    # hashing methods
    def hash(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    # region is a wildcard value that takes the place of the AWS region value
    # as COS doen't use regions like AWS, this parameter can accept any string
    def createSignatureKey(key, datestamp, region, service):
        keyDate = hash(('AWS4' + key).encode('utf-8'), datestamp)
        keyRegion = hash(keyDate, region)
        keyService = hash(keyRegion, service)
        keySigning = hash(keyService, 'aws4_request')
        return keySigning

    # assemble the standardized request
    time = datetime.datetime.utcnow()
    timestamp = time.strftime('%Y%m%dT%H%M%SZ')
    datestamp = time.strftime('%Y%m%d')

    standardized_querystring = (
        'X-Amz-Algorithm=AWS4-HMAC-SHA256'
        + '&X-Amz-Credential='
        + access_key
        + '/'
        + datestamp
        + '/'
        + region
        + '/s3/aws4_request'
        + '&X-Amz-Date='
        + timestamp
        + '&X-Amz-Expires='
        + str(expiration)
        + '&X-Amz-SignedHeaders=host'
    )
    standardized_querystring_url_encoded = quote(standardized_querystring, safe='&=')

    standardized_resource = '/' + object_key
    standardized_resource_url_encoded = quote(standardized_resource, safe='&')

    payload_hash = 'UNSIGNED-PAYLOAD'
    standardized_headers = 'host:' + host
    signed_headers = 'host'

    standardized_request = (
        http_method
        + '\n'
        + standardized_resource
        + '\n'
        + standardized_querystring_url_encoded
        + '\n'
        + standardized_headers
        + '\n'
        + '\n'
        + signed_headers
        + '\n'
        + payload_hash
    ).encode('utf-8')

    # assemble string-to-sign
    hashing_algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + 's3' + '/' + 'aws4_request'
    sts = (
        hashing_algorithm
        + '\n'
        + timestamp
        + '\n'
        + credential_scope
        + '\n'
        + hashlib.sha256(standardized_request).hexdigest()
    )

    # generate the signature
    signature_key = createSignatureKey(secret_key, datestamp, region, 's3')
    signature = hmac.new(
        signature_key, (sts).encode('utf-8'), hashlib.sha256
    ).hexdigest()

    # create and send the request
    # the 'requests' package autmatically adds the required 'host' header
    request_url = (
        endpoint
        + '/'
        + object_key
        + '?'
        + standardized_querystring_url_encoded
        + '&X-Amz-Signature='
        + signature
    )

    def hex_hash(key, msg):
        return hmac.new(b'key', msg.encode('utf-8'), hashlib.sha256).hexdigest()

    def createHexSignatureKey(key, datestamp, region, service):
        keyDate = hex_hash(('AWS4' + key).encode('utf-8'), datestamp)
        keyRegion = hex_hash(keyDate, region)
        keyService = hex_hash(keyRegion, service)
        keySigning = hex_hash(keyService, 'aws4_request')
        return keySigning

    signature_key_hex = createHexSignatureKey(secret_key, datestamp, region, 's3')

    # print(request_url)
    return request_url


def fps_drm(username, password, uid=None):
    asset_id = uid if uid else uuid.uuid4()
    url = FPS_DRM_KEYGENERATOR_URI_TEMPLATE % (asset_id, username, password)
    response = requests.post(url, {})
    tree = et.ElementTree(et.fromstring(response.content))
    root = tree.getroot()
    kid = root[0][0].get('kid')
    iv = root[0][0].get('explicitIV')
    key = root[0][0][0][0][0].text
    key_hex = key.decode('base64').encode('hex')
    iv_hex = iv.decode('base64').encode('hex')
    key_url = DRM_KEY_URL_TEMPLATE % kid
    payload = dict(AssetID=asset_id)
    data = dict(key=key_hex, iv=iv_hex, key_url=key_url)
    return data, payload


def cenc_drm(username, password, uid=None):
    asset_id = uid if uid else uuid.uuid4()
    url = CENC_DRM_KEYGENERATOR_URI_TEMPLATE % (asset_id, username, password)
    response = requests.post(url, {})
    tree = et.ElementTree(et.fromstring(response.content))
    root = tree.getroot()
    key_id = root[0][0].get('kid')
    key = root[0][0][0][0][0].text
    pssh = root[1][0][0].text
    key_id_hex = key_id.replace('-', '')
    key_hex = key.decode('base64').encode('hex')
    key_url = DRM_KEY_URL_TEMPLATE % key_id
    payload = dict(AssetID=asset_id)
    data = dict(key=key_hex, key_id=key_id_hex, pssh=pssh, key_url=key_url)
    return data, payload

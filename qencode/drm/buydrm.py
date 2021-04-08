from lxml import etree
from signxml import XMLSigner
import os

NSMAP = {
    'cpix': 'urn:dashif:org:cpix',
    'xenc': 'http://www.w3.org/2001/04/xmlenc#',
    'pskc': 'urn:ietf:params:xml:ns:keyprov:pskc',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

SYSTEM_ID_PLAYREADY = '9a04f079-9840-4286-ab92-e65be0885f95'
SYSTEM_ID_WIDEVINE = 'edef8ba9-79d6-4ace-a3c8-27dcd51d21ed'
SYSTEM_ID_FAIRPLAY = '94ce86fb-07ff-4f43-adb8-93d2fa968ca2'

def create_cpix_user_request(
  key_ids, media_id, user_private_key_path, user_public_cert_path,
  use_playready=False, use_widevine=False, use_fairplay=False,
  nsmap=None
):
    document_public_cert_path = os.path.dirname(__file__) + '/keys/buydrm_qencode_public_cert.pem'
    """Creates CPIX request XML signed end user

    Arguments:
        key_ids {list} -- List of Key IDs and corresponding track quality types. The list is of
        the following format - { 'kid': [string in GUID/UUID format], 'track_type': [string track type]}.

        media_id {string} -- Some random name for your asset which is shown in KeyOS console and reports.

        nsmap {list} -- List of namespaces.

    Returns:
        string -- CPIX request XML signed end user
    """
    nsmap = nsmap if nsmap is not None else NSMAP

    # Own private key and end user's private key used to sign the document
    end_user_private_key = open(user_private_key_path, 'rb').read()

    # Own public certificate and end user's public certificate to include into the CPIX request
    end_user_public_cert = open(user_public_cert_path, 'rb').read()
    document_public_cert = open(document_public_cert_path, 'rb').read()

    root = etree.Element('{%s}CPIX' % nsmap['cpix'], name=media_id, nsmap=nsmap)
    root.set('{%s}schemaLocation' % nsmap['xsi'], 'urn:dashif:org:cpix cpix.xsd')

    # Delivery data list
    delivery_data_list = etree.SubElement(root, '{%s}DeliveryDataList' % nsmap['cpix'])
    delivery_data = etree.SubElement(delivery_data_list, '{%s}DeliveryData' % nsmap['cpix'])
    delivery_key = etree.SubElement(delivery_data, '{%s}DeliveryKey' % nsmap['cpix'])

    # The public certificate of a partner. This certificate's public key will be used
    # to encrypt Document Key which will later be used to encrypt Contnet Keys.
    x509_data = etree.SubElement(delivery_key, '{%s}X509Data' % nsmap['ds'])
    x509_cert = etree.SubElement(x509_data, '{%s}X509Certificate' % nsmap['ds'])
    x509_cert.text = document_public_cert.replace('-----BEGIN CERTIFICATE-----', '').replace('-----END CERTIFICATE-----', '').replace('\n', '')

    # Content key list
    content_key_list = etree.SubElement(root, '{%s}ContentKeyList' % nsmap['cpix'])

    # Content key usage rules
    content_key_usage_list = etree.SubElement(
        root, '{%s}ContentKeyUsageRuleList' % nsmap['cpix']
    )

    # DRM systems list
    drm_system_list = etree.SubElement(root, '{%s}DRMSystemList' % nsmap['cpix'])

    for data in key_ids:
        etree.SubElement(
            content_key_list, '{%s}ContentKey' % nsmap['cpix'], kid=data['kid']
        )
        if use_playready:
            etree.SubElement(
                drm_system_list, '{%s}DRMSystem' % nsmap['cpix'], kid=data['kid'],
                systemId=SYSTEM_ID_PLAYREADY
            )
        if use_widevine:
            etree.SubElement(
                drm_system_list, '{%s}DRMSystem' % nsmap['cpix'], kid=data['kid'],
                systemId=SYSTEM_ID_WIDEVINE
            )
        if use_fairplay:
            etree.SubElement(
                drm_system_list, '{%s}DRMSystem' % nsmap['cpix'], kid=data['kid'],
                systemId=SYSTEM_ID_FAIRPLAY
            )

        etree.SubElement(
            content_key_usage_list, '{%s}ContentKeyUsageRule' % nsmap['cpix'],
            kid=data['kid'], intendedTrackType=data['track_type']
        )

    # Signing document with end user's data
    end_user_signed_root = XMLSigner(
        c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315',
        signature_algorithm='rsa-sha256', digest_algorithm='sha512'
    ).sign(root, key=end_user_private_key, cert=end_user_public_cert)
    x509_sign_cert = end_user_signed_root.xpath(
        '//ds:X509Certificate', namespaces=nsmap
    )[1]
    x509_sign_cert.text = x509_sign_cert.text.replace('\n', '')
#
    return etree.tostring(end_user_signed_root).decode('utf-8')


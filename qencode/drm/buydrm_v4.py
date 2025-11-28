# for python2.7
import os
from lxml import etree
from signxml import XMLSigner, XMLVerifier
#
import const

def create_cpix_user_request(
    key_ids, media_id,
    content_id, commonEncryptionScheme,
    private_key, public_cert, delivery_public_cert=None,
    use_playready=False, use_widevine=False, use_fairplay=False,
    nsmap=const.NSMAP
  ):
  if delivery_public_cert is None:
    delivery_public_cert_path = (os.path.dirname(__file__) + '/keys/qencode-public_cert.pem')
    delivery_public_cert = open(delivery_public_cert_path, 'rb').read()

  root = etree.Element('{%s}CPIX' % nsmap['cpix'],
    name=media_id, contentId=content_id, nsmap=nsmap)
  root.set('{%s}schemaLocation' % nsmap['xsi'],
    'urn:dashif:org:cpix cpix.xsd')

  delivery_data_list = etree.SubElement(root, '{%s}DeliveryDataList' % nsmap['cpix'])
  delivery_data = etree.SubElement(delivery_data_list,'{%s}DeliveryData' % nsmap['cpix'])
  delivery_key = etree.SubElement(delivery_data, '{%s}DeliveryKey' % nsmap['cpix'])

  x509_data = etree.SubElement(delivery_key, '{%s}X509Data' % nsmap['ds'])
  x509_cert = etree.SubElement(x509_data, '{%s}X509Certificate' % nsmap['ds'])
  x509_cert.text = delivery_public_cert.replace(
    '-----BEGIN CERTIFICATE-----', ''
  ).replace(
    '-----END CERTIFICATE-----', ''
  ).replace('\n', '')

  content_key_list = etree.SubElement(root,
    '{%s}ContentKeyList' % nsmap['cpix'])
  content_key_usage_list = etree.SubElement(root,
    '{%s}ContentKeyUsageRuleList' % nsmap['cpix'])
  drm_system_list = etree.SubElement(root,
    '{%s}DRMSystemList' % nsmap['cpix'])

  for data in key_ids:
    if commonEncryptionScheme == 'default':
      etree.SubElement(content_key_list, '{%s}ContentKey' % nsmap['cpix'], kid=data['kid'])
    else:
      etree.SubElement(content_key_list, '{%s}ContentKey' % nsmap['cpix'], kid=data['kid'],
        commonEncryptionScheme=commonEncryptionScheme)

    if use_playready:
      etree.SubElement(drm_system_list, '{%s}DRMSystem' % nsmap['cpix'], kid=data['kid'],
        systemId=const.SYSTEM_ID_PLAYREADY)

    if use_widevine:
      etree.SubElement(drm_system_list, '{%s}DRMSystem' % nsmap['cpix'], kid=data['kid'],
        systemId=const.SYSTEM_ID_WIDEVINE)

    if use_fairplay:
      etree.SubElement(drm_system_list, '{%s}DRMSystem' % nsmap['cpix'], kid=data['kid'],
        systemId=const.SYSTEM_ID_FAIRPLAY)

    etree.SubElement(content_key_usage_list,
      '{%s}ContentKeyUsageRule' % nsmap['cpix'],
      kid=data['kid'],
      intendedTrackType=data['track_type'])

  signed_root = XMLSigner(
    c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315',
    signature_algorithm='rsa-sha256',
    digest_algorithm='sha512'
  ).sign(root, key=private_key, cert=public_cert)

  xml_text = etree.tostring(signed_root, encoding='utf-8')

  return xml_text

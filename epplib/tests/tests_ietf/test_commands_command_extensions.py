from typing import Any, Dict, Mapping, cast
from unittest.mock import patch
from xml.etree.ElementTree import QName, fromstring
from lxml.builder import ElementMaker
from lxml import etree
from epplib import commands
from epplib.commands import CreateDomain
from epplib.commands.command_extensions import CreateDomainSecDNSExtension, UpdateDomainSecDNSExtension
from epplib.commands.info import InfoDomain
from epplib.commands.update import UpdateDomain
from epplib.tests.tests_ietf.constants import NAMESPACE, SCHEMA_LOCATION, SCHEMA
from epplib.tests.utils import EM, XMLTestCase, make_epp_root
from epplib.models.common import DSData, DomainAuthInfo, SecDNSKeyData
keyDataDict={'flags':257,
                    'protocol':3,
                    'alg':1,
                    'pubKey':'AQPJ////4Q=='}
dsDataDict={
            'keyTag':12345,
            'alg':3,
            'digestType':1,
            'digest':'49FD46E6C4B45C55D4AC',
            'keyData':SecDNSKeyData(**keyDataDict)
            }
paramsWithDsData:Mapping[str, Any] = {
        'maxSigLife': 3215,
        'dsData':DSData(**dsDataDict)
    }
paramsWithKeyData:Mapping[str, Any] = {
        'maxSigLife': 3215,
        'keyData':SecDNSKeyData(**keyDataDict)
    }


@patch('epplib.commands.create.NAMESPACE', NAMESPACE)
@patch('epplib.commands.create.SCHEMA_LOCATION', SCHEMA_LOCATION)
@patch('epplib.models.common.DomainAuthInfo.namespace', NAMESPACE.NIC_DOMAIN)
@patch('epplib.constants', NAMESPACE)
@patch('epplib.constants.SCHEMA_LOCATION', SCHEMA_LOCATION)
class TestCreateDomainSecDNS(XMLTestCase):
    command_params: Dict[str, Any] = {
        'name': 'thisdomain.cz',
        'registrant': 'CID-MYOWN',
        'auth_info': DomainAuthInfo(pw='2fooBAR123fooBaz'),
    }
    # keyDataDict={'flags':257,
    #                 'protocol':3,
    #                 'alg':1,
    #                 'pubKey':'AQPJ////4Q=='}
    # dsDataDict={
    #         'keyTag':12345,
    #         'alg':3,
    #         'digestType':1,
    #         'digest':'49FD46E6C4B45C55D4AC',
    #         'keyData':SecDNSKeyData(**keyDataDict)
    #         }
    # paramsWithDsData:Mapping[str, Any] = {
    #     'maxSigLife': 3215,
    #     'dsData':DSData(**dsDataDict)
    # }
    # paramsWithKeyData:Mapping[str, Any] = {
    #     'maxSigLife': 3215,
    #     'keyData':SecDNSKeyData(**keyDataDict)
    # }

    def test_data_with_dsData(self):
        extension = CreateDomainSecDNSExtension(**paramsWithDsData)
        EM = ElementMaker(namespace=NAMESPACE.SEC_DNS,nsmap={"secDNS":NAMESPACE.SEC_DNS})
        
        expected = EM.create(
            EM.maxSigLife(str(paramsWithDsData['maxSigLife'])),
            EM.dsData(
                EM.keyTag(str(dsDataDict['keyTag'])),
                EM.alg(str(dsDataDict['alg'])),
                EM.digestType(str(dsDataDict['digestType'])),
                EM.digest(dsDataDict['digest']),
                EM.keyData(
                            EM.flags(str(keyDataDict['flags'])),
                            EM.protocol(str(keyDataDict['protocol'])),
                            EM.alg(str(keyDataDict['alg'])),
                            EM.pubKey(str(keyDataDict['pubKey']))
                           )
            )
        )

        self.assertXMLEqual(extension.get_payload(), expected)
    
    def test_data_with_keyData(self):
        extension = CreateDomainSecDNSExtension(**paramsWithKeyData)
        
        EM = ElementMaker(namespace=NAMESPACE.SEC_DNS,nsmap={"secDNS":NAMESPACE.SEC_DNS})
        expected = EM.create(
            EM.maxSigLife(str(paramsWithDsData['maxSigLife'])),
            EM.keyData(
                    EM.flags(str(keyDataDict['flags'])),
                    EM.protocol(str(keyDataDict['protocol'])),
                    EM.alg(str(keyDataDict['alg'])),
                    EM.pubKey(str(keyDataDict['pubKey']))
                    )
            
        )
    

        self.assertXMLEqual(extension.get_payload(), expected)
        
    def test_valid(self):
        extension = CreateDomainSecDNSExtension(**paramsWithDsData)
        request = CreateDomain(**self.command_params)
        cast(commands, request).add_extension(extension)
        xml = request.xml(tr_id='tr_id_123')
        parser = etree.XMLParser(no_network=True, resolve_entities=False)
        parsed = etree.fromstring(xml, parser=parser)  

        if parsed.getroottree().docinfo.doctype:
            print("error")
        print("~~~~~*******")
        print()
        r=CreateDomain(**self.command_params)
        cast(CreateDomain,request).add_extension(extension)
        xml=request.xml(tr_id="123")
        print(xml)
        self.assertRequestValid(CreateDomain, self.command_params, extension=extension,schema=SCHEMA)


@patch('epplib.commands.update.NAMESPACE', NAMESPACE)
@patch('epplib.commands.update.SCHEMA_LOCATION', SCHEMA_LOCATION)
@patch('epplib.models.common.DomainAuthInfo.namespace', NAMESPACE.NIC_DOMAIN)
class TestUpdateDomainSecDnsExtension(XMLTestCase):
    addKeyData={'flags':250,
                    'protocol':2,
                    'alg':0,
                    'pubKey':'AQPJ//213245//='}
    addDsData={
            'keyTag':1234,
            'alg':1,
            'digestType':3,
            'digest':'49FD46E6C4BSDFLASDHK',
            'keyData':SecDNSKeyData(**addKeyData)
            }
    updateParams={"maxSigLife":1222,
                  "remDsData":paramsWithDsData['dsData'],
                  "dsData":DSData(**addDsData)}
    updateParamsKeyData={"remKeyData":paramsWithKeyData['keyData'],
                  "keyData":SecDNSKeyData(**addKeyData)}
    
    def setUp(self) -> None:
        """Setup params."""
        self.params = {'name': 'mydoma.in', 'auth_info': DomainAuthInfo(pw='2fooBAR123fooBaz')}

    def test_valid(self):
        self.assertRequestValid(UpdateDomain, self.params, schema=SCHEMA)

    def test_data_with_dsData(self):
        extension = UpdateDomainSecDNSExtension(**self.updateParams)
        EM = ElementMaker(namespace=NAMESPACE.SEC_DNS,nsmap={"secDNS":NAMESPACE.SEC_DNS})
        
        expected = EM.update(
          
            EM.rem(EM.dsData(
                EM.keyTag(str(dsDataDict['keyTag'])),
                EM.alg(str(dsDataDict['alg'])),
                EM.digestType(str(dsDataDict['digestType'])),
                EM.digest(dsDataDict['digest']),
                EM.keyData(
                            EM.flags(str(keyDataDict['flags'])),
                            EM.protocol(str(keyDataDict['protocol'])),
                            EM.alg(str(keyDataDict['alg'])),
                            EM.pubKey(str(keyDataDict['pubKey']))
                           )
            )),
            EM.add(EM.dsData(
                EM.keyTag(str(self.addDsData['keyTag'])),
                EM.alg(str(self.addDsData['alg'])),
                EM.digestType(str(self.addDsData['digestType'])),
                EM.digest(self.addDsData['digest']),
                EM.keyData(
                        EM.flags(str(self.addKeyData['flags'])),
                        EM.protocol(str(self.addKeyData['protocol'])),
                        EM.alg(str(self.addKeyData['alg'])),
                        EM.pubKey(str(self.addKeyData['pubKey']))
                        )
            )),  
            EM.chg( EM.maxSigLife(str(self.updateParams['maxSigLife'])))
        )

        # print("****EXPECTED****")
        # print(etree.tostring(expected, pretty_print=False))
        # print("********")
        # print("\n\n\n\n****actual****")
        # print(etree.tostring(extension.get_payload(), pretty_print=False))
        # print("********")
        self.assertXMLEqual(extension.get_payload(), expected)
    
    def test_data_with_removeAll(self):
        extension = UpdateDomainSecDNSExtension(remAllDsKeyData=True)
        EM = ElementMaker(namespace=NAMESPACE.SEC_DNS,nsmap={"secDNS":NAMESPACE.SEC_DNS})
        
        expected = EM.update(
            EM.rem(
                EM.all("true"))  
        )
        self.assertXMLEqual(extension.get_payload(), expected)
    
    def test_data_with_keydata(self):

        extension = UpdateDomainSecDNSExtension(**self.updateParamsKeyData)
        
        EM = ElementMaker(namespace=NAMESPACE.SEC_DNS,nsmap={"secDNS":NAMESPACE.SEC_DNS})
        expected = EM.update(

            EM.rem(
                EM.keyData(
                    EM.flags(str(keyDataDict['flags'])),
                    EM.protocol(str(keyDataDict['protocol'])),
                    EM.alg(str(keyDataDict['alg'])),
                    EM.pubKey(str(keyDataDict['pubKey']))
                    )
            ),
            EM.add(      
                EM.flags(str(self.addKeyData['flags'])),
                EM.protocol(str(self.addKeyData['protocol'])),
                EM.alg(str(self.addKeyData['alg'])),
                EM.pubKey(str(self.addKeyData['pubKey']))
            )
            
        )
        print("****EXPECTED****")
        print(etree.tostring(expected, pretty_print=False))
        print("********")
        print("\n\n\n\n****actual****")
        print(etree.tostring(extension.get_payload(), pretty_print=False))
        print("********")
        self.assertXMLEqual(extension.get_payload(), expected)
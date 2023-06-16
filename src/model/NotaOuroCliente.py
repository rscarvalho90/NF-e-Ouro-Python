import base64
import gzip
from typing import Tuple

import requests_pkcs12 as requests
import signxml
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding
from cryptography.x509 import Certificate
from lxml import etree as et
from requests import Response
from signxml import XMLSigner, XMLVerifier

from src.enum.AmbienteEnum import AmbienteEnum


class NotaOuroCliente:
    """Classe que representa um cliente de envio e consulta da NF-e Ouro."""

    __ambiente = AmbienteEnum.HOMOLOGACAO
    __path_certificado = None
    __senha_certificado = None

    def __init__(self, ambiente: AmbienteEnum, path_certificado: str, senha_certificado: str):
        """
        :param ambiente: Ambiente em que o serviço será executado.
        :param path_certificado: Local, na estação de execução do serviço, em que encontra-se o certificado para assinatura do XML.
        :param senha_certificado: Senha do arquivo do certificado.
        """
        self.__ambiente = ambiente
        self.__path_certificado = path_certificado
        self.__senha_certificado = senha_certificado

    def envia_dao(self, xml_path: str) -> Response:
        """
        Envia um XML contendo uma DAO (Declaração de Aquisição de Ouro ativo financeiro).

        :param xml_path: Path (local, caminho) do arquivo XML a ser enviado.

        :returns: Response - Resposta do servidor à requisição.
        """

        xml_assinado, certificado = self.__assina_xml(xml_path)

        # Compacta o XML assinado para o formato gzip e o converte em base64
        xml_assinado_base64_gzip = base64.b64encode(gzip.compress(bytes(xml_assinado, 'utf8'))).decode('utf8')

        # Converte o certificado a ser utilizado em base64 para a requisição
        certificado_base_64 = base64.b64encode(certificado.public_bytes(Encoding.PEM)).decode('utf8')

        # Cria a requisição para o serviço
        ip = self.__get_ip()

        cabecalhos = {'X-SSL-Client-Cert': certificado_base_64,
                      'X-ARR-ClientCert': certificado_base_64,
                      'X-Forwarded-For': ip,
                      'Content-Type': 'application/json'
                      }
        json_requisicao = {'XmlGzipDao': xml_assinado_base64_gzip}

        resposta = requests.post(self.__ambiente.value + '/nfeouro',
                                 json=json_requisicao,
                                 headers=cabecalhos,
                                 pkcs12_filename=self.__path_certificado,
                                 pkcs12_password=self.__senha_certificado)

        return resposta

    def consulta_por_nsu(self, nsu_recepcao: int) -> Response:
        """
        Consulta um XML contendo uma NF-e Ouro e seu DAO (Declaração de Aquisição de Ouro ativo financeiro).

        :param nsu_recepcao: NSU da NF-e Ouro.

        :returns: Response - Resposta do servidor à requisição.
        """

        # Importa um certificado tipo A1
        with open(self.__path_certificado, 'rb') as arquivo_io:
            chave_privada, certificado, certificados_adicionais = pkcs12.load_key_and_certificates(arquivo_io.read(),
                                                                                                   bytes(
                                                                                                       self.__senha_certificado,
                                                                                                       'utf8'))
        arquivo_io.close()

        # Converte o certificado a ser utilizado em base64 para a requisição
        certificado_base_64 = base64.b64encode(certificado.public_bytes(Encoding.PEM)).decode('utf8')

        # Cria a requisição para o serviço
        ip = self.__get_ip()

        cabecalhos = {'X-SSL-Client-Cert': certificado_base_64,
                      'X-ARR-ClientCert': certificado_base_64,
                      'X-Forwarded-For': ip,
                      'Content-Type': 'application/json'
                      }

        resposta = requests.get(self.__ambiente.value + '/nsu/' + str(nsu_recepcao) + '/nfeouro',
                                headers=cabecalhos,
                                pkcs12_filename=self.__path_certificado,
                                pkcs12_password=self.__senha_certificado)

        return resposta

    def consulta_por_chave(self, chave_acesso: str) -> Response:
        """
        Consulta um XML contendo uma NF-e Ouro e seu DAO (Declaração de Aquisição de Ouro ativo financeiro).

        :param chave_acesso: Chave de acesso da NF-e Ouro.

        :returns: Response - Resposta do servidor à requisição.
        """

        # Importa um certificado tipo A1
        with open(self.__path_certificado, 'rb') as arquivo_io:
            chave_privada, certificado, certificados_adicionais = pkcs12.load_key_and_certificates(arquivo_io.read(),
                                                                                                   bytes(
                                                                                                       self.__senha_certificado,
                                                                                                       'utf8'))
        arquivo_io.close()

        # Converte o certificado a ser utilizado em base64 para a requisição
        certificado_base_64 = base64.b64encode(certificado.public_bytes(Encoding.PEM)).decode('utf8')

        # Cria a requisição para o serviço
        ip = self.__get_ip()

        cabecalhos = {'X-SSL-Client-Cert': certificado_base_64,
                      'X-ARR-ClientCert': certificado_base_64,
                      'X-Forwarded-For': ip,
                      'Content-Type': 'application/json'
                      }

        resposta = requests.get(self.__ambiente.value + '/nfeouro/'+chave_acesso,
                      headers=cabecalhos,
                      pkcs12_filename=self.__path_certificado,
                      pkcs12_password=self.__senha_certificado)

        return resposta

    def __assina_xml(self, xml_path: str) -> Tuple[str, Certificate]:
        """
        Assina um XML com certificado do tipo A1.

        :param xml_path: Path (local, caminho) do arquivo XML a ser assinado

        :returns:  Retorna uma :py:class:`Tuple[str, Certificate]` contendo o XML assinado e o certificado que o assinou.
        """

        # Importa um certificado tipo A1
        with open(self.__path_certificado, 'rb') as arquivo_io:
            chave_privada, certificado, certificados_adicionais = pkcs12.load_key_and_certificates(arquivo_io.read(),
                                                                                                   bytes(
                                                                                                       self.__senha_certificado,
                                                                                                       'utf8'))
        arquivo_io.close()

        with open(xml_path, 'rb') as xml_io:
            xml_str = xml_io.read().decode('utf8')
        xml_io.close()

        assinador = XMLSigner(method=signxml.methods.enveloped,
                              c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315',
                              signature_algorithm='rsa-sha1',
                              digest_algorithm='sha1')
        ns = {None: assinador.namespaces['ds']}
        assinador.namespaces = ns

        cert = self.__configura_certificado(certificado.public_bytes(Encoding.PEM).decode('utf8'))

        # Remove todas as quebras de linha do XML inserido, antes da assinatura
        xml_str = self.__configura_xml(xml_str)
        xml_root = et.fromstring(xml_str.encode('utf-8'))

        reference_uri = xml_root.find('./*').attrib['Id']

        xml_assinado_element = assinador.sign(xml_root.find('.//{http://www.sped.fazenda.gov.br/nfeouro}infDAO'),
                                              id_attribute='Id',
                                              cert=cert,
                                              key=chave_privada,
                                              reference_uri=reference_uri)
        xml_assinatura = et.tostring(
            xml_assinado_element.findall('.//{http://www.w3.org/2000/09/xmldsig#}Signature')[0]). \
            decode('utf8').replace('\n', '')
        xml_root.append(et.fromstring(bytes(xml_assinatura, 'utf8')))
        xml_assinado = self.__finaliza_xml(et.tostring(xml_root).decode('utf8'))

        verify = XMLVerifier().verify(et.fromstring(bytes(xml_assinado, 'utf8')), x509_cert=cert).signed_xml

        return xml_assinado, certificado

    def __configura_certificado(self, certificado_txt: str) -> str:
        """
        Configura um certificado em formato de texto para que cada linha tenha 64 caracteres.

        :param certificado_txt: Certificado em formato texto.

        :returns: Certificado configurado em formato texto
        """

        certificado_txt = certificado_txt.replace('\n', '')
        certificado_txt = certificado_txt.replace('-----BEGIN CERTIFICATE-----', '')
        certificado_txt = certificado_txt.replace('-----END CERTIFICATE-----', '')

        linhas_certificado = ['-----BEGIN CERTIFICATE-----\n']
        for i in range(0, len(certificado_txt), 64):
            linhas_certificado.append(certificado_txt[i:i + 64] + '\n')
        linhas_certificado.append('-----END CERTIFICATE-----\n')

        certificado_txt = ''.join(linhas_certificado)

        return certificado_txt

    def __configura_xml(self, xml_txt: str) -> str:
        """
        Configura o XML a ser assinado.

        :param xml_txt: Represtentação em formato string do XML a ser configurado.

        :returns: XML configurado em formato texto
        """

        xml_txt = xml_txt.replace('\r', '')
        xml_txt = xml_txt.replace('\n', '')
        xml_txt = xml_txt.replace('\t', '')

        return xml_txt

    def __finaliza_xml(self, xml_txt: str) -> str:
        """
        Finaliza o XML para que seja enviado ao serviço de recepção de DAOs.

        :param xml_txt: Represtentação em formato string do XML a ser finalizado.

        :returns: XML finalizado em formato texto
        """

        xml_txt = '<?xml version=\'1.0\' encoding=\'utf-8\'?>' + xml_txt

        return xml_txt

    def __get_ip(self):
        return requests.get('https://api.myip.com').json()['ip']

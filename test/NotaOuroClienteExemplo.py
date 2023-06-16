import unittest

from src.enum.AmbienteEnum import AmbienteEnum
from src.model.NotaOuroCliente import NotaOuroCliente


class NotaOuroClienteExemplo(unittest.TestCase):

    __senha_certificado = 'senha1'
    __ambiente = AmbienteEnum.HOMOLOGACAO
    __certificado = '../res/certificados_homologacao/Cert_03763656000154.p12'

    def testa_envio_dao(self):
        nfeourocliente = NotaOuroCliente(ambiente=self.__ambiente,
                                         path_certificado=self.__certificado,
                                         senha_certificado=self.__senha_certificado)
        resposta = nfeourocliente.envia_dao(xml_path='exemplos/primeiraAquisicao_04.xml')
        print(resposta.json())

    def testa_consulta_por_chave(self):
        nfeourocliente = NotaOuroCliente(ambiente=self.__ambiente,
                                         path_certificado=self.__certificado,
                                         senha_certificado=self.__senha_certificado)
        resposta = nfeourocliente.consulta_por_chave(chave_acesso='3106200037636560001540010001770000000106')
        print(resposta.json())

    def testa_consulta_por_nsu(self):
        nfeourocliente = NotaOuroCliente(ambiente=self.__ambiente,
                                         path_certificado=self.__certificado,
                                         senha_certificado=self.__senha_certificado)
        resposta = nfeourocliente.consulta_por_nsu(nsu_recepcao=10)
        print(resposta.json())

from enum import Enum


class AmbienteEnum(Enum):
    """Lista de servidores por ambiente."""

    HOMOLOGACAO = 'https://hom-nfoe.estaleiro.serpro.gov.br/API'
    PRODUCAO = 'https://nfeouro.rfb.gov.br/API'

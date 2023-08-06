***************************************************************
.gov.br: Pacote de Portlets
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
==========

Este pacote provê a instalação de produto com pacote de portlets multimídia seguindo padrão de estilização do Portal Padrão.

Requisitos
==========

Este pacote foi desenvolvido especificadamente para o Portal Padrão, dessa forma, para uso sem erros de funcionalidades e estilização é indicado que seja utilizado como complemento ao Portal Padrão.


Estado deste pacote
===================

O **brasil.gov.portlets** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis. 

O estado atual dos testes pode ser visto nas imagens a seguir:

.. image:: https://secure.travis-ci.org/plonegovbr/brasil.gov.portlets.png?branch=master
    :target: http://travis-ci.org/plonegovbr/brasil.gov.portlets

.. image:: https://coveralls.io/repos/plonegovbr/brasil.gov.portlets/badge.png?branch=master
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.portlets


Instalação
==========

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.portlets`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.portlets

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**.gov.br: Busca Multiportlets: Instalação do Pacote**.
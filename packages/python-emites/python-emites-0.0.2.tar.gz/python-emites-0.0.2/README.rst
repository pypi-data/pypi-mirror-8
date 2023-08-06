=============
python-emites
=============

Sobre o Emites
--------------

O Emites é uma aplicação para emissão de notas fiscais eletrônicas de serviço sob demanda.
Esta biblioteca implementa um cliente para a `versão 1 de sua API <http://myfreecomm.github.io/emites/v1/index.html>`_

.. image:: https://travis-ci.org/myfreecomm/python-emites.png?branch=master
        :target: https://travis-ci.org/myfreecomm/python-emites

Instalação
----------

.. code-block:: sh

    pip install python-emites


Exemplo de utilização
---------------------

.. code-block:: python

    from emites_api.main import Emites

    api_client = Emites(
        host='https://sandbox.emites.com.br',
        token='DD00027F4A76E4B79209ACBFBC72F68E'
    )

    # Cadastrar um emitente
    emitter_data = {
        'email': 'financeiro@python-emites.test',
        'cnpj': '91762868000184',
        'fancy_name': 'Empresa de Testes',
        'social_reason': 'Empresa de Testes Ltda ME',
        'state_inscription': 'ISENTO',
        'city_inscription': '00000000',
        'state': 'RJ',
        'city': 'Rio de Janeiro',
        'neighborhood': 'Centro',
        'street_type': 'RUA',
        'street': 'dos testes',
        'number': 42,
        'zip_code': '20011020',
        'phone': '21000000000',
        'certificate': **<certificado da empresa codificado em base-64>**,
        'password': **<senha do certificado>**,
    }
    new_emitter = api_client.emitters.create(**emitter_data)

    # Cadastrar um tomador
    taker_data = {
        'cnpj': '91762868000184',
        'fancy_name': 'Empresa de Testes',
        'social_reason': 'Empresa de Testes Ltda ME',
        'city_inscription': '00000000',
        'state_inscription': 'ISENTO',
        'address': {
            'state': 'RJ',
            'city_code': 3304557,
            'city': 'Rio de Janeiro',
            'street_type': 'RUA',
            'street': 'dos testes',
            'number': 42,
            'neighborhood_type': 'COM',
            'neighborhood': 'Centro',
            'zip_code': '20011020',
            'country_code': '01058',
            'country': 'Brasil',
            'country_abbreviation': 'BR',
        },
        'contact': {
            'phone': '21000000000',
            'email': 'financeiro@python-emites.test',
        }
    }
    new_taker = api_client.takers.create(**taker_data)

    # Cadastrar um modelo de valores e serviço
    service_values_data = {
        'emitter_id': new_emitter.id,
        'name': u'Desenvolvimento de programas de computador',
        'city_code': 3304557,
        'service_item_code': '0105',
        'city_tax_code': '010501',
        'cnae_code': '6201-5',
        'iss_percentage': '5.00',
    }
    new_service_values = api_client.service_values.create(**service_values_data)

    # Emitir uma nota fiscal de serviço
    nfse_data = {
        'emitter_id': new_emitter.id,
        'taker_id': new_taker.id,
        'serie': 'TESTE',
        'emission_date': '2014-11-12T18:16:56Z',
        'service_values': {
            'id': new_service_values.id,
            'service_amount': '99.99',
            'deduction_amount': '0.00',
            'discount_conditioning_amount': '0.00',
            'calculation_base': '99.99',
            'nfse_liquid_amount': '99.99',
            'description': u'Testes da api do emites',
        }
    }
    new_nfse = api_client.nfse.create(**nfse_data)

    # Adicionar uma nota fiscal de serviço a um novo lote
    second_nfse_data = {
        'batch_name': u'Notas do dia 12 de Novembro de 2014',
        'emitter_id': new_emitter.id,
        'taker_id': new_taker.id,
        'serie': 'TESTE',
        'emission_date': '2014-11-12T18:20:18Z',
        'service_values': {
            'id': new_service_values.id,
            'service_amount': '99.99',
            'deduction_amount': '0.00',
            'discount_conditioning_amount': '0.00',
            'calculation_base': '99.99',
            'nfse_liquid_amount': '99.99',
            'description': u'Cliente python para a api do emites',
        }
    }
    second_nfse = api_client.nfse.create(**second_nfse_data)

    # Obter lote
    new_batch = api_client.batches.all(name=second_nfse_data['batch_name'])[0]

    # Adicionar nova nfse ao lote
    third_nfse_data = {
        'batch_id': new_batch.id,
        'emitter_id': new_emitter.id,
        'taker_id': new_taker.id,
        'serie': 'TESTE',
        'emission_date': '2014-11-12T18:22:34Z',
        'service_values': {
            'id': new_service_values.id,
            'service_amount': '99.99',
            'deduction_amount': '0.00',
            'discount_conditioning_amount': '0.00',
            'calculation_base': '99.99',
            'nfse_liquid_amount': '99.99',
            'description': u'Teste da manipulação de lotes',
        }
    }
    third_nfse = api_client.nfse.create(**third_nfse_data)

    # Enviar lote
    new_batch.send()

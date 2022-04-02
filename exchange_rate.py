import requests

def get_exchange_rates(currency, date):
    api_url = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=\'{}\'&@dataCotacao=\'{}\'&$top=10&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim'

    response = requests.get(api_url.format(currency, date))

    return response.json()['value']

print(get_exchange_rates('USD', '04-01-2022'))
print(get_exchange_rates('USD', '04-02-2022'))

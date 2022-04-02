import requests
import datetime as dt

def get_exchange_rates(currency, date):
    api_url = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=\'{}\'&@dataCotacao=\'{}\'&$top=10&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim'

    response = requests.get(api_url.format(currency, date))

    return response.json()['value']

def get_latest_report(currency):
    date = dt.date.today()
    rates = get_exchange_rates(currency, date.strftime('%m-%d-%Y'))

    while not rates:
        date -= dt.timedelta(days=1)
        rates = get_exchange_rates(currency, date.strftime('%m-%d-%Y'))

    return rates

def format_money(money):
    return 'R$ ' + str(round(money, 2)).replace('.', ',').ljust(4, '0')

print(format_money(get_latest_report('USD')[0]['cotacaoCompra']))
print(format_money(get_latest_report('EUR')[0]['cotacaoCompra']))

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

def format_date(datetime):
    date = dt.date.fromisoformat(datetime[:10])

    return date.strftime('%d/%m/%Y')

def format_report_item(item):
    str_item = '\n\n' + item['tipoBoletim']
    str_item += ' - ' + item['dataHoraCotacao'][11:16]
    str_item += '\nCotação de Compra: ' + format_money(item['cotacaoCompra'])
    str_item += '\nCotação de Venda: ' + format_money(item['cotacaoVenda'])

    return str_item

currencies = {}
currencies['DKK'] = {'Unicode': '\U0001F1E9\U0001F1EF', 'Name': 'Coroa Dinamarquesa'}
currencies['NOK'] = {'Unicode': '\U0001F1F3\U0001F1F4', 'Name': 'Coroa Norueguesa'}
currencies['SEK'] = {'Unicode': '\U0001F1F8\U0001F1EA', 'Name': 'Coroa Sueca'}
currencies['USD'] = {'Unicode': '\U0001F1FA\U0001F1F8', 'Name': 'Dólar Americano'}
currencies['AUD'] = {'Unicode': '\U0001F1E6\U0001F1FA', 'Name': 'Dólar Australiano'}
currencies['CAD'] = {'Unicode': '\U0001F1E8\U0001F1E6', 'Name': 'Dólar Canadense'}
currencies['EUR'] = {'Unicode': '\U0001F1EA\U0001F1FA', 'Name': 'Euro'}
currencies['CHF'] = {'Unicode': '\U0001F1E8\U0001F1ED', 'Name': 'Franco Suíço'}
currencies['JPY'] = {'Unicode': '\U0001F1EF\U0001F1F5', 'Name': 'Iene'}
currencies['GBP'] = {'Unicode': '\U0001F1EC\U0001F1E7', 'Name': 'Libra Esterlina'}

for i in currencies.keys():
    print(currencies[i]['Name'])
    print(get_latest_report(i))

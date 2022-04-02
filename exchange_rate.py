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

report = get_latest_report('USD')

text = '\U0001F1FA\U0001F1F8 Dólar americano \U0001F1FA\U0001F1F8\n'
text += 'Data: ' + format_date(report[0]['dataHoraCotacao'])

for i in report:
    text += format_report_item(i)

print(text)

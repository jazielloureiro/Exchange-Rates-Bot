import json
import requests
import datetime as dt
import telebot as tb
import os
import re
import dotenv

dotenv.load_dotenv()

bot = tb.TeleBot(os.getenv('BOT_TOKEN'), threaded=False)

currencies = {}
currencies['DKK'] = {'Unicode': '\U0001F1E9\U0001F1F0', 'Name': 'Coroa Dinamarquesa'}
currencies['NOK'] = {'Unicode': '\U0001F1F3\U0001F1F4', 'Name': 'Coroa Norueguesa'}
currencies['SEK'] = {'Unicode': '\U0001F1F8\U0001F1EA', 'Name': 'Coroa Sueca'}
currencies['USD'] = {'Unicode': '\U0001F1FA\U0001F1F8', 'Name': 'Dólar Americano'}
currencies['AUD'] = {'Unicode': '\U0001F1E6\U0001F1FA', 'Name': 'Dólar Australiano'}
currencies['CAD'] = {'Unicode': '\U0001F1E8\U0001F1E6', 'Name': 'Dólar Canadense'}
currencies['EUR'] = {'Unicode': '\U0001F1EA\U0001F1FA', 'Name': 'Euro'}
currencies['CHF'] = {'Unicode': '\U0001F1E8\U0001F1ED', 'Name': 'Franco Suíço'}
currencies['JPY'] = {'Unicode': '\U0001F1EF\U0001F1F5', 'Name': 'Iene'}
currencies['GBP'] = {'Unicode': '\U0001F1EC\U0001F1E7', 'Name': 'Libra Esterlina'}

currencies_regex = '(DKK)|(NOK)|(SEK)|(USD)|(AUD)|(CAD)|(EUR)|(CHF)|(JPY)|(GBP)'

def lambda_handler(event, context):
    request_body = json.loads(event['body'])

    updates = tb.types.Update.de_json(request_body)

    try:
        bot.process_new_updates([updates])
    except Exception as e:
        print(e)

    return {
        'statusCode': 200
    }

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

def format_report(report, currency):
    str_report = '{0} {1} {0}\n'.format(currencies[currency]['Unicode'], currencies[currency]['Name'])
    str_report += 'Data: ' + format_date(report[0]['dataHoraCotacao'])

    for i in report:
        str_report += format_report_item(i)

    return str_report

@bot.message_handler(commands=['start'])
def show_start_message(message):
    keyboard = tb.types.ReplyKeyboardMarkup()

    for i in currencies.keys():
        button_label = '{0} {1} ({2}) {0}'.format(currencies[i]['Unicode'], currencies[i]['Name'], i)
        keyboard.row(tb.types.KeyboardButton(button_label))

    start_msg = 'Olá, seja bem-vindo ao Beija-flor. O bot de consulta à taxas de câmbio do Telegram. Escolha uma moeda para consultar.'

    bot.send_message(message.chat.id, start_msg, reply_markup=keyboard)

@bot.message_handler(regexp=currencies_regex)
def show_currency_report(message):
    currency = re.search(currencies_regex, message.text.upper()).group(0)

    report = get_latest_report(currency)

    bot.send_message(message.chat.id, format_report(report, currency))

@bot.message_handler(func=lambda message: True)
def show_error_message(message):
    error_msg = 'Desculpe, não consegui reconhecer a sua entrada. Tente usar o menu da próxima vez.'

    bot.send_message(message.chat.id, error_msg)

if __name__ == '__main__':
    bot.infinity_polling()

import telebot
from transitions import Machine

class Order(object):
    states = ['big_or_little','thin_or_thick','payment','checking']

    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=Order.states, initial='big_or_little')
        self.machine.add_transition(trigger='size', source='big_or_little', dest='thin_or_thick')
        self.machine.add_transition(trigger='thickness', source='thin_or_thick', dest='payment')
        self.machine.add_transition(trigger='pay', source='payment', dest='checking')
        self.machine.add_transition(trigger='confirm', source='checking', dest='big_or_little')

TOKEN = '2100387942:AAH4g9wkTGYvLKmoXa-FY8zT_bJM1Y-gw6E'
bot = telebot.TeleBot(token=TOKEN)
order = Order('user')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text in ("Начнем", "/start"):
        bot.send_message(message.from_user.id, "Какую вы хотите пиццу? Большую или маленькую?")
    elif message.text in ("Большую","Маленькую") and order.state == 'big_or_little':
        global pizza_size
        pizza_size = message.text
        order.size()
        bot.send_message(message.from_user.id, "На каком тесте Вам сделать? На толстом, На тонком")
    elif message.text in ("На толстом","На тонком") and order.state == 'thin_or_thick':
        global pizza_thickness
        pizza_thickness = message.text
        order.thickness()
        bot.send_message(message.from_user.id, "Как вы будете платить? Наличкой, Картой")
    elif order.state == 'payment' and message.text in ("Наличкой","Картой"):
        global type_of_payment
        type_of_payment = message.text
        bot.send_message(message.from_user.id,
        "Вы хотите {x} пиццу, {z} тесте, оплата - {y}?".format(x=str.lower(pizza_size), y=str.lower(type_of_payment), z=str.lower(pizza_thickness)))
        order.pay()

    elif order.state == 'checking' and message.text == "Да":
        bot.send_message(message.from_user.id, "Спасибо за заказ")
        order.confirm()
    elif order.state == 'checking' and message.text == "Нет":
        bot.send_message(message.from_user.id, "Давайте проверим. Какую вы хотите пиццу? Большую или Маленькую? ")
        order.confirm()

    elif message.text == "Помощь":
        bot.send_message(message.from_user.id, "Напиши \"Начнем\" ")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши \"Помощь\" или исправь опечатку.")


bot.polling(none_stop=True, interval=0)








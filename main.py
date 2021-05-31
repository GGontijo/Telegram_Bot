import requests
import time
import json
import os

class Telegram_Bot:
    def __init__(self):
        token = '_____YOUR_____TOKEN_____HERE_____'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Start(self):
        update_id = None
        while True:
            atualizacao = self.get_new_messages(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"].lower())
                    usuario = str(dado["message"]["from"]["username"])
                    chat_id = dado["message"]["from"]["id"]
                    firstmessage = int(
                        dado["message"]["message_id"]) == 1
                    response = self.create_response(
                        mensagem, firstmessage)

                    #DEBUG
                    #print(dado)
                    ###########
                    print(usuario, chat_id, mensagem)
                    self.responder(response, chat_id)

    # Get messages
    def get_new_messages(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Create response
    def create_response(self, mensagem, firstmessage):
        message = None
        
        if firstmessage == True or mensagem in ('/start', '/menu'):
            message = f'''        
            Hello, I'm your bot! Do whatever you want.

            You can find my creator at: https://github.com/GGontijo{os.linesep}
           
            Choose an option:{os.linesep}
                        
            /donate - Show how can you donate to this project ..{os.linesep}

            /menu - Show this menu'''

        elif mensagem == ('/donate'):
            message = ''' I'm glad you considered donate to this project, please click this link to help maintain this bot. '''

        return message

    # Send response
    def responder(self, response, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={response}'
        requests.get(link_requisicao)

bot = Telegram_Bot()
bot.Start()

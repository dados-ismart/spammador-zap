from WPP_Whatsapp import Create
import logging
import pandas as pd
import os
import sys
import re
import datetime as dt
from time import sleep
from random import randint

#verificando se a base com numeros existe
if not os.path.exists('Base_Spammador.xlsx'):
    df=pd.DataFrame({'Telefone':['+5511999999999'],'Mensagem':['Ao lado temos um telefone no formato de exemplo.']})
    df.to_excel('Base_Spammador.xlsx',index=False)
    print(f'O arquivo Base_Spammador.xlsx foi criado, preencha-o e rode novamente o programa.')
    input('Aperte qualquer tecla para sair.')
    sys.exit()


#importando base
base=pd.read_excel('Base_Spammador.xlsx')
base=base.astype(str)

logger = logging.getLogger(name="Spamador_zap")
logger.setLevel(logging.DEBUG)
print('Se o seu navegador ainda não está conectado ao whatsapp, leia o QRCode que aparecerá para conectar. Caso contrário, suas mensagens já irão para o fluxo de envio.')


# start no cliente do whatsapp
your_session_name = "Spammador"
creator = Create(
    session=your_session_name,
    headless=False,
    #catchQR=catchQR,
    #logQR=False
    )
client = creator.start()


# check state of login
if creator.state != 'CONNECTED':
    raise Exception(creator.state)
print('Conexão feita com sucesso. As mensagens serão enviadas.\n\n')
execucao_nome_log = str(dt.datetime.now().strftime('%Y-%m-%d %H-%M-%S')).replace(":", "-").replace(" ", "_") + ".xlsx"
log_numeros=[]
log_status=[]
log_hora=[]

# Expressão regular para validar números de telefone no formato +55DDDNÚMERO
telefone_regex = re.compile(r"^55\d{2}\d{8,9}$")


for phone_number in base['Telefone']:
    try:
        #verificação se o número está em formato correto:
        if not telefone_regex.match(phone_number):
            logger.error(f'Número de telefone inválido: {phone_number}')
            log_status.append('Número Inválido')
        else:
            sleep(randint(4, 8))
            message = base[base['Telefone']==phone_number]['Mensagem'].values[0]
            result = client.sendText(phone_number, message)
            logger.info(f'Mensagem enviada para: {phone_number}')
            log_status.append('Sucesso')
        log_numeros.append(phone_number)
        log_hora.append(str(dt.datetime.now().strftime('%Y-%m-%d %H-%M-%S')))

    except Exception as e:
        log_numeros.append(phone_number)
        log_status.append('Falha')
        log_hora.append(str(dt.datetime.now().strftime('%Y-%m-%d %H-%M-%S')))
        logger.error(f'Erro ao enviar mensagem para {phone_number}')
        raise e

df_log=pd.DataFrame({'Telefone':log_numeros,'Status':log_status,'Envio':log_hora})
nome_log='Registros_'+execucao_nome_log
df_log.to_excel(nome_log,index=False)
input('\n\nMensagens enviadas. Aperte qualquer tecla para sair')
sys.exit()
#for number in phone_numbers:
#  print(number)
#  result = client.sendText(number, message)
  #print(result)
#  creator.loop.run_forever()
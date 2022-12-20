import scrapy
from time import sleep
from rich import print
from varredor_celular.email_send import Emailer

email = input("Choose an email where the report will be sent: ")
print(f"The report would be sent to the email: {email}...")
sleep(5)


class BotCelularesSpider(scrapy.Spider):
    name = 'botcel'

    def start_requests(self):
        urls = ['https://telefonesimportados.netlify.app/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for elemento in response.xpath("//div[@class='single-shop-product']"):
            yield{
                'nome': elemento.xpath(".//h2//a/text()").get(),
                'preco': elemento.xpath(".//div[2]//ins/text()").get(),
                }
            
        
        numero_proxima_pagina = response.xpath("//a[@aria-label='Next']/@href").get()
        print("#"*20)
        print(numero_proxima_pagina)
        print("#"*20)
        if numero_proxima_pagina is not None:
            link_proxima_pagina = f'https://telefonesimportados.netlify.app/{numero_proxima_pagina}'
            print("#"*20)
            print(link_proxima_pagina)
            print("#"*20)
            yield scrapy.Request(url=link_proxima_pagina, callback=self.parse)

        else:    
            print("All pages have been extracted. Sending report to email...")
            sleep(3)
            print("The email has been sent!")
            sleep(3)  
                  
mail = Emailer('seuemailgmail', 'suachavegmail')
mail.definir_conteudo('Data Report', 'seuemailgmail', email, 'Anexo arquivo excel')

mail.anexar_arquivos('dados.csv')
mail.enviar_email(5)
import mercadopago
import os
import datetime
from PIL import Image
import base64

class Pagamento:
	def __init__(self):
		token_pagamento = os.getenv("TOKEN_PAGAMENTO_TESTE")
		self.sdk = mercadopago.SDK(token_pagamento)

	def criando_pagamento(self, valor, tipo_pagamento, email, descricao = ""):
		validade = datetime.datetime.now() + datetime.timedelta(days=1)
		validade = validade.strftime("%Y-%m-%dT%-H:%M:%S.000-03:00")
		email = "seusindicadores@gmail.com"
		payment_data = {
			"transaction_amount": int(valor),
			"payment_method_id": f"{tipo_pagamento}",
			"installments": 1,
			"description": f"{descricao} ",
			"date_of_expiration": f"{validade}",
			"payer": {
				"email": f"{email}"
			}
		}
		result = self.sdk.payment().create(payment_data)
		return result

	def confirmar_compra_pix(self, preco, nome_plano, tipo_plano, email):
		descricao = f"{tipo_plano} - {nome_plano}"
		payment = self.criando_pagamento(preco, "pix", email, descricao)
		print(payment)
		pix_copia_cola = payment['response']['point_of_interaction']['transaction_data']['qr_code']
		qr_code = payment['response']['point_of_interaction']['transaction_data']['qr_code_base64']
		qr_code = base64.b64decode(qr_code)
		#qr_code_img = Image.open(BytesIO(qr_code))
		#qrcode_output = qr_code_img.convert('RGB')
		return [qr_code, f'<code>{pix_copia_cola}</code>', 'HTML']
	
	def obter_pagamento(self, id_):
		request = self.sdk.payment().get(id_)
		print(request)
		return request
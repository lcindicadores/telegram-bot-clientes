import mercadopago
import os
import datetime
import base64
import uuid

class Pagamento:
	def __init__(self):
		token_pagamento = os.getenv("TOKEN_PAGAMENTO_PRODUCAO") #trocar para teste
		self.sdk = mercadopago.SDK(token_pagamento)

	def criando_pagamento(self, valor, tipo_pagamento, email, descricao = ""):
		validade = datetime.datetime.now() + datetime.timedelta(days=1)
		validade = validade.strftime("%Y-%m-%dT%-H:%M:%S.000-03:00")
		email = "seusindicadores@gmail.com"
		payment_data = {
			"transaction_amount": float(valor),
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

	def criando_pagamento2(self, tipo_pagamento, valor, email, descricao = ""):
		request_options = mercadopago.config.RequestOptions()
		idempotency_key = str(uuid.uuid4())
		request_options.custom_headers = {
			'x-idempotency-key': idempotency_key
		}
		payment_data = {
			"transaction_amount": float(valor),
			"token": "",
			"description": descricao,
			"payment_method_id": tipo_pagamento,
			"installments": 1,
			"payer": {
				"email": email,
			},
			"token": "",
			"issuer_id": None,
			"statement_descriptor": "MercadoPago",
		}

		payment_response = self.sdk.payment().create(payment_data,request_options)
		return payment_response

	def criando_pagamento3(self, valor, email, descricao = ""):
		request_options = mercadopago.config.RequestOptions()
		idempotency_key = str(uuid.uuid4())
		request_options.custom_headers = {
			'x-idempotency-key': idempotency_key
		}
		payment_data = {
			"transaction_amount": float(valor),
			"description": descricao,
			"payment_method_id": "pix",
			"payer": {
				"email": email,
				"first_name": "Test",
				"last_name": "User",
				"identification": {
					"type": "CPF",
					"number": "191191191-00"
				},
				"address": {
					"zip_code": "06233-200",
					"street_name": "Av. das Nações Unidas",
					"street_number": "3003",
					"neighborhood": "Bonfim",
					"city": "Osasco",
					"federal_unit": "SP"
				}
			}
		}	
		payment_response = self.sdk.payment().create(payment_data,request_options)
		return payment_response

	def confirmar_compra_pix(self, preco, email, descricao = ""):
		payment = self.criando_pagamento3(preco,email,descricao)
		status_response = payment['status']
		print("status: ", status_response)
		if(status_response != 200 and status_response != 201):
			return [payment]
		pix_copia_cola = payment["response"]['point_of_interaction']['transaction_data']['qr_code']
		qr_code = payment["response"]['point_of_interaction']['transaction_data']['qr_code_base64']
		qr_code = base64.b64decode(qr_code)
		#qr_code_img = Image.open(BytesIO(qr_code))
		#qrcode_output = qr_code_img.convert('RGB')
		return [qr_code, f'<code>{pix_copia_cola}</code>', 'HTML']
	
	def obter_meios_pagamento_API(self):
		response = self.sdk.payment_methods()
		return response.list_all()      
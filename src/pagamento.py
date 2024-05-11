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
'''
request_options = mercadopago.config.RequestOptions()
request_options.custom_headers = {
	'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
}

payment_data = {
	"application_fee": False,
	"binary_mode": False,
	"campaign_id": None,
	"capture": False,
	"coupon_amount": None,
	"description": "Payment for product",
	"differential_pricing_id": None,
	"external_reference": "MP0001",
	"installments": 1,
	"metadata": None,
	"payer": {
		"entity_type": "individual",
		"type": "customer",
		"email": "test_user_123@testuser.com",
		"identification": {
			"type": "CPF",
			"number": "95749019047"
		}
	},
	"payment_method_id": "master",
	"token": "ff8080814c11e237014c1ff593b57b4d",
	"transaction_amount": 58.8,
	"notification_url": "https://www.suaurl.com/notificacoes/",
	"sponsor_id": None,
	"binary_mode": False,
	"external_reference": "MP0001",
	"statement_descriptor": "MercadoPago",
	"additional_info": {
		"items": [
			{
				"id": "MLB2907679857",
				"title": "Point Mini",
				"description": "Point product for card payments via Bluetooth.",
				"picture_url": "https://http2.mlstatic.com/resources/frontend/statics/growth-sellers-landings/device-mlb-point-i_medium2x.png",
				"category_id": "electronics",
				"type": "electronics",
				"quantity": 1,
				"unit_price": 58.80,
				"event_date": "2023-12-31T09:37:52.000-04:00",
				"warranty": False,
				"category_descriptor": {
					"passenger": {},
					"route": {}
				}
			}
		],
		"payer": {
			"first_name": "Test",
			"last_name": "Test",
			"address": {
				"zip_code": "06233-200",
				"street_name": "Av das Nacoes Unidas",
				"street_number": 3003
			},
			"phone": {
				"area_code": "11",
				"number": "987654321"
			}
		},
		"shipments": {
			"width": None,
			"height": None,
			"receiver_address": {
				"street_name": "Av das Nacoes Unidas",
				"street_number": 3003,
				"zip_code": "06233200",
				"city_name": "Buzios",
				"state_name": "Rio de Janeiro"
			}
		}
	}
}

payment_response = sdk.payment().create(payment_data, request_options)
payment = payment_response["response"]
'''
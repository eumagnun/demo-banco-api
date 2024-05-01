from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import random

app = Flask(__name__)
api = Api(app)

contas = {}

class ContaBancaria(Resource):
    def get(self, numero_conta):
        """
        Obter Conta Bancária

        Recupera os dados de uma conta bancária específica.

        ---
        parameters:
          - name: numero_conta
            in: path
            description: O número da conta bancária.
            required: true
            type: integer
        responses:
          200:
            description: Conta bancária encontrada.
            schema:
              $ref: '#/definitions/ContaBancaria'
          404:
            description: Conta bancária não encontrada.
        """
        if numero_conta not in contas:
            return jsonify({'error': 'Conta bancária não encontrada'}), 404
        return jsonify(contas[numero_conta])

    def put(self, numero_conta):
        """
        Atualizar Conta Bancária

        Atualiza os dados de uma conta bancária específica.

        ---
        parameters:
          - name: numero_conta
            in: path
            description: O número da conta bancária.
            required: true
            type: integer
          - name: body
            in: body
            description: Os dados atualizados da conta bancária.
            required: true
            schema:
              $ref: '#/definitions/ContaBancaria'
        responses:
          200:
            description: Conta bancária atualizada com sucesso.
            schema:
              $ref: '#/definitions/ContaBancaria'
          400:
            description: Dados inválidos.
          404:
            description: Conta bancária não encontrada.
        """
        if numero_conta not in contas:
            return jsonify({'error': 'Conta bancária não encontrada'}), 404
        data = request.get_json()
        contas[numero_conta]['saldo'] = data['saldo']
        return jsonify(contas[numero_conta])

    def delete(self, numero_conta):
        """
        Excluir Conta Bancária

        Exclui uma conta bancária específica.

        ---
        parameters:
          - name: numero_conta
            in: path
            description: O número da conta bancária.
            required: true
            type: integer
        responses:
          200:
            description: Conta bancária excluída com sucesso.
          404:
            description: Conta bancária não encontrada.
        """
        if numero_conta not in contas:
            return jsonify({'error': 'Conta bancária não encontrada'}), 404
        del contas[numero_conta]
        return jsonify({'message': 'Conta bancária excluída com sucesso.'})

class Deposito(Resource):
    def post(self, numero_conta):
        """
        Realizar Depósito

        Realiza um depósito em uma conta bancária específica.

        ---
        parameters:
          - name: numero_conta
            in: path
            description: O número da conta bancária.
            required: true
            type: integer
          - name: body
            in: body
            description: Os dados do depósito.
            required: true
            schema:
              type: object
              properties:
                valor:
                  type: number
                  description: O valor a ser depositado.
        responses:
          200:
            description: Depósito realizado com sucesso.
            schema:
              $ref: '#/definitions/ContaBancaria'
          400:
            description: Dados inválidos.
          404:
            description: Conta bancária não encontrada.
        """
        if numero_conta not in contas:
            return jsonify({'error': 'Conta bancária não encontrada'}), 404
        data = request.get_json()
        contas[numero_conta]['saldo'] += data['valor']
        return jsonify(contas[numero_conta])

class Saque(Resource):
    def post(self, numero_conta):
        """
        Realizar Saque

        Realiza um saque em uma conta bancária específica.

        ---
        parameters:
          - name: numero_conta
            in: path
            description: O número da conta bancária.
            required: true
            type: integer
          - name: body
            in: body
            description: Os dados do saque.
            required: true
            schema:
              type: object
              properties:
                valor:
                  type: number
                  description: O valor a ser sacado.
        responses:
          200:
            description: Saque realizado com sucesso.
            schema:
              $ref: '#/definitions/ContaBancaria'
          400:
            description: Dados inválidos.
          404:
            description: Conta bancária não encontrada.
          409:
            description: Saldo insuficiente.
        """
        if numero_conta not in contas:
            return jsonify({'error': 'Conta bancária não encontrada'}), 404
        data = request.get_json()
        if contas[numero_conta]['saldo'] < data['valor']:
            return jsonify({'error': 'Saldo insuficiente'}), 409
        contas[numero_conta]['saldo'] -= data['valor']
        return jsonify(contas[numero_conta])

class Transferencia(Resource):
    def post(self):
        """
        Realizar Transferência

        Realiza uma transferência entre duas contas bancárias.

        ---
        parameters:
          - name: body
            in: body
            description: Os dados da transferência.
            required: true
            schema:
              type: object
              properties:
                numero_conta_origem:
                  type: integer
                  description: O número da conta bancária de origem.
                numero_conta_destino:
                  type: integer
                  description: O número da conta bancária de destino.
                valor:
                  type: number
                  description: O valor a ser transferido.
        responses:
          200:
            description: Transferência realizada com sucesso.
            schema:
              $ref: '#/definitions/ContaBancaria'
          400:
            description: Dados inválidos.
          404:
            description: Conta bancária de origem ou destino não encontrada.
          409:
            description: Saldo insuficiente na conta bancária de origem.
        """
        data = request.get_json()
        if data['numero_conta_origem'] not in contas or data['numero_conta_destino'] not in contas:
            return jsonify({'error': 'Conta bancária de origem ou destino não encontrada'}), 404
        if contas[data['numero_conta_origem']]['saldo'] < data['valor']:
            return jsonify({'error': 'Saldo insuficiente na conta bancária de origem'}), 409
        contas[data['numero_conta_origem']]['saldo'] -= data['valor']
        contas[data['numero_conta_destino']]['saldo'] += data['valor']
        return jsonify({'numero_conta_origem': data['numero_conta_origem'], 'numero_conta_destino': data['numero_conta_destino'], 'saldo': contas[data['numero_conta_origem']]['saldo']})

api.add_resource(ContaBancaria, '/contas/<int:numero_conta>')
api.add_resource(Deposito, '/contas/<int:numero_conta>/depositos')
api.add_resource(Saque, '/contas/<int:numero_conta>/saques')
api.add_resource(Transferencia, '/transferencias')

swaggerui_blueprint = get_swaggerui_blueprint(
    '/docs',
    '/static/swagger.json',
    config={
        'app_name': 'API Banco Demo'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

if __name__ == '__main__':
    for i in range(1, 11):
        contas[i] = {'numero_conta': i, 'saldo': random.randint(1000, 10000)}
    app.run(debug=True, host="0.0.0.0", port=8080)

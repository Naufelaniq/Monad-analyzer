from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
RPC_URL = "https://testnet-rpc.monad.xyz"

@app.route('/api')
def analyze():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "No address provided"}), 400
    
    try:
        balance = requests.post(RPC_URL, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBalance",
            "params": [address, "latest"]
        }).json().get("result", "0x0")
        
        tx_count = requests.post(RPC_URL, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getTransactionCount",
            "params": [address, "latest"]
        }).json().get("result", "0x0")
        
        return jsonify({
            "address": address,
            "balance": str(int(balance, 16)/10**18),
            "tx_count": str(int(tx_count, 16))
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

import hashlib
import json
from datetime import datetime
from web3 import Web3
from eth_account import Account
import logging

# Configurer le logging
logger = logging.getLogger(__name__)

# Simulation d'une connexion Blockchain (Ethereum / Polygon)
# Dans un cas réel, utilisez os.getenv("BLOCKCHAIN_PROVIDER_URL")
# ex: https://polygon-mumbai.g.alchemy.com/v2/...
WEB3_PROVIDER_URL = "https://rpc.ankr.com/eth_goerli" # URL publique de test
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

# Exemple d'ABI minimaliste pour un contrat de certificat (fictif)
CERTIFICATE_CONTRACT_ABI = [
    {
        "constant": False,
        "inputs": [{"name": "student", "type": "string"}, {"name": "course", "type": "string"}, {"name": "hash", "type": "string"}],
        "name": "issueCertificate",
        "outputs": [],
        "type": "function"
    }
]
# Adresse fictive
CERTIFICATE_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"

def generate_certificate_hash(student_email: str, course_title: str, completion_date: str) -> str:
    """
    Génère un hash unique pour le certificat basé sur les métadonnées.
    Utilise SHA-256.
    """
    data_string = f"{student_email}|{course_title}|{completion_date}"
    return hashlib.sha256(data_string.encode()).hexdigest()

async def issue_certificate_on_blockchain(student_email: str, course_title: str) -> dict:
    """
    Simule l'émission d'un certificat sur la Blockchain.
    Retourne les détails de la transaction (mock).
    """
    completion_date = datetime.now().isoformat()
    cert_hash = generate_certificate_hash(student_email, course_title, completion_date)
    
    logger.info(f"Preparing to issue certificate for {student_email} - Hash: {cert_hash}")

    # Vérification de la connexion Web3 (optionnelle, juste pour le debug)
    is_connected = w3.is_connected()
    logger.info(f"Web3 Connected: {is_connected}")

    # Simulation de la transaction
    # Dans un vrai scénario, on signerait une transaction ici avec une clé privée
    # transaction = contract.functions.issueCertificate(...).buildTransaction(...)
    # signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
    # tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Mock result
    mock_tx_hash = "0x" + hashlib.sha256(f"tx_{cert_hash}".encode()).hexdigest()
    
    return {
        "network": "Ethereum (Simulated)", # Ou Polygon
        "contract_address": CERTIFICATE_CONTRACT_ADDRESS,
        "transaction_hash": mock_tx_hash,
        "certificate_hash": cert_hash,
        "status": "pending", # La transaction serait en attente de minage
        "timestamp": completion_date
    }

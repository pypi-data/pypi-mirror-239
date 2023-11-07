from spectral_cli.config_manager import ConfigManager
from functools import wraps
from tqdm import tqdm
from web3 import Web3
import click
import os
import requests
# from . import CONFIG_PATH, ALCHEMY_URL, ABIS # works for pip package
from spectral_cli import CONFIG_PATH, ALCHEMY_URL, ABIS # works for direct calling
from spectral_cli.ezkl_wrapper.ezkl_wrapper import dump_model, upload_file_to_ipfs

from retrying import retry
config_manager = None
@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_from_ipfs(cid, filename, file_type = "File"):
    primary_source = "http://ipfs.io/ipfs/"
    url = primary_source + cid

    try:
        # Make the GET request to fetch the file content
        response = requests.get(url, timeout=(3,8), stream=True)
        
        # Check if the request was successful
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8K
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        # Save the content to the specified file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))
        
        progress_bar.close()
        print(f"{file_type} successfully downloaded!")
        

    except requests.ReadTimeout as e:
        print("Failed to fetch the file from the official gateway. Trying another gateway...")
        response = requests.post("http://ipfs.dev.spectral.finance:5001/api/v0/cat?arg=" + cid)
        
        # Check if the request was successful
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8K
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        
        # Save the content to the specified file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))
        
        progress_bar.close()
        print(f"{file_type} successfully fetched from the alternative gateway!")


@click.group()
def cli():
    """Modelers CLI provides tools to interact with Spectral platform and taking part in challenges."""
    pass

import requests

def get_multisig_address(address):
    """
    Fetches the MultiSig address for a given address from the API.

    :param address: The address to query.
    :return: A string with the MultiSig address or None.
    """
    url = f"https://subscription-library.dev.spectral.finance/getMultiSigAddress/{address}"
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'message' in data and data['message'] == 'No data found':
            return None
        else:
            print(data)
            print(data[0])
            return data[0]['contract_address']
    elif response.status_code == 404:
        return None

def ensure_global_config(step=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_manager = ConfigManager(CONFIG_PATH)
            config_updated = False
            if step != "training_data" and config_manager.get('global', 'api_key') is None:
                click.echo("Input your Spectral API key.")
                click.echo("To get your Spectral API key, please visit www.app.dev.spectral.finance")
                api_key = click.prompt("Spectral API key:")
                config_manager.set('global', 'api_key', api_key)
                config_updated = True
                click.echo("\n")
            if config_manager.get('global', 'alchemy_api_key') is None:
                click.echo("Input your Alchemy API key.")
                click.echo(
                    "To get your Alchemy API key, please visit https://www.alchemy.com/")
                alchemy_api_key = click.prompt("Alchemy API key:")
                config_manager.set('global', 'alchemy_api_key', alchemy_api_key)
                config_updated = True
                click.echo("\n")
            if config_manager.get('global', 'wallet_private_key') is None and config_manager.get('global', 'wallet_address') is None:
                from web3 import Web3
                from eth_account import Account
                # Initialize Web3
                w3 = Web3()
                # Generate a new account
                new_account = Account.create()

                # Extract the private key and address
                private_key = new_account._private_key.hex()
                address = new_account.address
                config_manager.set('global', 'wallet_private_key', private_key)
                config_manager.set('global', 'wallet_address', address)
                click.echo(f"A new wallet address has been generated for this machine. To see how to connect local wallet with your main wallet check our-gitbook-link.com \n")
                config_updated = True
            if step != "training_data" and config_manager.get('global', 'wallet_private_key') and config_manager.get('global', 'multisig_wallet_address') is None and not config_updated:
                multisig_wallet_address = get_multisig_address(config_manager.get('global', 'wallet_address'))
                if multisig_wallet_address:
                    config_manager.set('global', 'multisig_wallet_address', multisig_wallet_address)
                    config_updated = True
                else:
                    click.echo("Your wallet address is not connected to any multisig wallet. Please connect your wallet to multisig wallet in your Spectral account profile page. https://app.spectral.finance/profile")
                    return -1
            if config_updated:
                click.echo("Config has been updated. You can fetch training data now.")
            return func(config_manager, *args, **kwargs)
        return wrapper
    return decorator

@cli.command()
def list_challenges():
    """List all available challenges."""
    print("""Available challenges:\nCredit Scoring: 0xB79CDBC5Cd94a807CC5cc761e3eF4A6B9baC8939""")

@cli.command()
def show_wallet():
    """Shows the wallet address used by the CLI."""
    config_manager = ConfigManager(CONFIG_PATH)
    wallet_address = config_manager.get('global', 'wallet_address')
    if wallet_address:
        print(f"CLI Wallet address: {wallet_address}")
    else:
        print("CLI Wallet address is not set. Please run `spectral configure` to set it up.")

@cli.command()
@ensure_global_config("training_data")
@click.argument('challenge_id')
def fetch_training_data(config_manager, challenge_id):
    """Fetches Training Dataset."""
    competition_abi = ABIS['Competition']
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL + web3_provider_api_key))
    contract = w3.eth.contract(address=challenge_id, abi=competition_abi)
    ipfsTrainingDataset = contract.functions.ipfsTrainingDataset().call()
    filename = f"{challenge_id}_training_data.parquet"
    fetch_from_ipfs(ipfsTrainingDataset, filename, "Training dataset")

@cli.command()
@ensure_global_config()
@click.argument('challenge_id')
@click.argument('wallet_address')
def fetch_testing_data(config_manager, challenge_id, wallet_address):
    """Fetch testing dataset."""
    competition_abi = ABIS['Competition']
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL + web3_provider_api_key))
    contract = w3.eth.contract(address=challenge_id, abi=competition_abi)
    modeler_contract_address = contract.functions.modelerContract().call()
    modeler_abi = ABIS['Modeler']
    modeler_contract = w3.eth.contract(address=modeler_contract_address, abi=modeler_abi)
    modeller_challanges = modeler_contract.functions.modelerChallenges(wallet_address).call()
    if not modeller_challanges:
        print("The file with your challenge data is not available yet. Please try again in a couple of minutes.")
        return -1
    ipfs_hash = modeller_challanges[0]
    fetch_from_ipfs(ipfs_hash, f"{challenge_id}_testing_dataset.csv", "Testing dataset")
    

@cli.command()
@ensure_global_config()
@click.argument('competition_address')
@click.argument('submission_file')
def submit_inferences(config_manager, competition_address, submission_file):
    """Submit inferences to a competition."""
    ipfs_api_key = config_manager.get('global', 'api_key')
    inferences_cid = upload_file_to_ipfs(submission_file, ipfs_api_key)
    if not inferences_cid:
        print("Submission failed. Please try again.")
        return -1
    print(f"Submitting response with CID: {inferences_cid} to competition with address: {competition_address}. This may take a moment.")
    destination_wallet_address_private_key = config_manager.get('global', 'wallet_private_key')
    destination_wallet_address = config_manager.get('global', 'wallet_address')
    multisig_wallet_address = config_manager.get('global', 'multisig_wallet_address')
    competition_abi = ABIS['Competition']
    modeler_abi = ABIS['Modeler']
    modeler_address = "0xAC689722AfB9887ce61B4c1677f5cb49293A1BbC"
    validator_wallet_address="0xc001C50946AF123B8dD85171B05F43000feCfA22"
    wallet_simple_abi = ABIS['WalletSimple']
    
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    current_block = w3.eth.block_number

    current_block_timestamp = w3.eth.get_block(current_block)['timestamp']
    competition_contract = w3.eth.contract(address=competition_address, abi=competition_abi)
    modeler_contract = w3.eth.contract(address=modeler_address, abi=modeler_abi)
    multisig_contract = w3.eth.contract(address=multisig_wallet_address, abi=wallet_simple_abi)
    
    commit_function_data = {}
    contract_address = None
    commit_function_data = modeler_contract.functions.respondToChallenge(validator_wallet_address, inferences_cid).build_transaction({
        'chainId': 5,
        'gas': 300000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    })['data']
    contract_address =  modeler_address
    
    import time
    next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
    expire_time = int(time.time()) + 3600  # Current time + 1 hour
    sequence_id = next_sequence_id
    signature = '0x'  # No signature needed for a 1-2 multisig
    
    txn_details = {
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    }
    multisig_txn = multisig_contract.functions.sendMultiSig(
        contract_address,
        0,
        commit_function_data,
        expire_time,
        sequence_id,
        signature
    ).build_transaction(txn_details)
    
    private_key = destination_wallet_address_private_key
    signed_multisig_txn = w3.eth.account.sign_transaction(multisig_txn, private_key)

    try:
        multisig_txn_hash = w3.eth.send_raw_transaction(signed_multisig_txn.rawTransaction)
        multisig_txn_receipt = w3.eth.wait_for_transaction_receipt(multisig_txn_hash)
        tx_hash = multisig_txn_receipt['transactionHash']
        tx_hash = tx_hash.hex()
        status = multisig_txn_receipt['status']
        if status == 1:
            print('Your inferences have been recorded successfully!')
        else:
            print('Submitting your inferences failed')         
        print(f"You can check status of that transaction under: https://goerli.etherscan.io/tx/{str(tx_hash)}")
    except Exception as e:
        config_manager = ConfigManager(CONFIG_PATH)
        wallet_address = config_manager.get('global', 'wallet_address')
        if "insufficient funds for" in str(e):
            print("Transaction failed with error: Insufficient funds. Please make sure you have enough ETH in your wallet.")
            print(f"Your CLI wallet address is: {wallet_address}")
        else:
            print("Transaction failed with error:", str(e))

@cli.command()
@ensure_global_config()
@click.argument('model_path')
@click.argument('input_json_path')
@click.argument('competition_address')
def commit(config_manager, model_path, input_json_path, competition_address):
    """Commit to a machine learning model."""
    ipfs_api_key = config_manager.get('global', 'api_key')
    model_cid = dump_model(model_path, input_json_path, ipfs_api_key)
    if not model_cid:
        print("Uploading your commitment to IPFS failed. Please try again.")
        return -1
    print(f"Submitting model with CID: {model_cid} to competition with address: {competition_address}. This may take a moment.")
    destination_wallet_address_private_key = config_manager.get('global', 'wallet_private_key')
    destination_wallet_address = config_manager.get('global', 'wallet_address')
    multisig_wallet_address = config_manager.get('global', 'multisig_wallet_address')
    competition_abi = ABIS['Competition']
    modeler_abi = ABIS['Modeler']
    modeler_address = "0xAC689722AfB9887ce61B4c1677f5cb49293A1BbC"
    wallet_simple_abi = ABIS['WalletSimple']
    
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    current_block = w3.eth.block_number

    current_block_timestamp = w3.eth.get_block(current_block)['timestamp']
    competition_contract = w3.eth.contract(address=competition_address, abi=competition_abi)
    modeler_contract = w3.eth.contract(address=modeler_address, abi=modeler_abi)
    multisig_contract = w3.eth.contract(address=multisig_wallet_address, abi=wallet_simple_abi)
    
    commit_function_data = {}
    contract_address = None
    if modeler_contract.functions.modelers(multisig_wallet_address).call()[0] == '':
        commit_function_data = competition_contract.functions.signUpToCompetition(model_cid).build_transaction({
            'chainId': 5,
            'gas': 300000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(destination_wallet_address)
        })['data']
        contract_address = competition_address
    else:
        commit_function_data = modeler_contract.functions.updateModel(model_cid).build_transaction({
            'chainId': 5,
            'gas': 300000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(destination_wallet_address)
        })['data']
        contract_address = modeler_address
    
    import time
    next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
    expire_time = int(time.time()) + 3600  # Current time + 1 hour
    sequence_id = next_sequence_id
    signature = '0x'  # No signature needed for a 1-2 multisig
    
    txn_details = {
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    }
    multisig_txn = multisig_contract.functions.sendMultiSig(
        contract_address,
        0,
        commit_function_data,
        expire_time,
        sequence_id,
        signature
    ).build_transaction(txn_details)
    
    private_key = destination_wallet_address_private_key
    signed_multisig_txn = w3.eth.account.sign_transaction(multisig_txn, private_key)

    try:
        multisig_txn_hash = w3.eth.send_raw_transaction(signed_multisig_txn.rawTransaction)
        multisig_txn_receipt = w3.eth.wait_for_transaction_receipt(multisig_txn_hash)
        tx_hash = multisig_txn_receipt['transactionHash']
        tx_hash = tx_hash.hex()
        status = multisig_txn_receipt['status']
        if status == 1:
            print('Your submission has been recorded successfully!')
        else:
            print('Your submission failed')         
        print(f"You can check status of that transaction under: https://goerli.etherscan.io/tx/{str(tx_hash)}")
    except Exception as e:
        config_manager = ConfigManager(CONFIG_PATH)
        wallet_address = config_manager.get('global', 'wallet_address')
        if "insufficient funds for" in str(e):
            print("Transaction failed with error: Insufficient funds. Please make sure you have enough ETH in your wallet.")
            print(f"Your CLI wallet address is: {wallet_address}")
        else:
            print("Transaction failed with error:", str(e))


# @cli.command()
# @ensure_global_config()
# @click.argument('competition_address')
# @click.argument('submission_file')
# def submit_inferences(config_manager, competition_address, submission_file):
#     destination_wallet_address_private_key = config_manager.get('global', 'wallet_private_key')
#     destination_wallet_address = config_manager.get('global', 'wallet_address')
#     multisig_wallet_address = config_manager.get('global', 'multisig_wallet_address')
#     spectral_token_abi = ABIS['SpectralToken']
#     wallet_simple_abi = ABIS['WalletSimple']

#     web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
#     w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    
#     token_contract = w3.eth.contract(address=token_contract_address, abi=spectral_token_abi)
#     multisig_contract = w3.eth.contract(address=multisig_wallet_address, abi=wallet_simple_abi)

#     approve_function_data = token_contract.functions.approve(competition_contract_address, int(amount)).build_transaction({'chainId': 5,  # or whatever chain you're using
#         'gas': 30000000,
#         'gasPrice': w3.to_wei('2000', 'gwei'),
#         'nonce': w3.eth.get_transaction_count(destination_wallet_address)})['data']
#     import time
#     next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
#     expire_time = int(time.time()) + 3600  # Current time + 1 hour
#     sequence_id = next_sequence_id
#     signature = '0x'  # No signature needed for a 1-2 multisig

#     multisig_txn = multisig_contract.functions.sendMultiSig(
#         token_contract_address,
#         0,
#         approve_function_data,
#         expire_time,
#         sequence_id,
#         signature
#     ).build_transaction({
#         'chainId': 5,
#         'gas': 150000,
#         'gasPrice': w3.to_wei('100', 'gwei'),
#         'nonce': w3.eth.get_transaction_count(destination_wallet_address)
#     })
#     pass

def remove_global_config():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(CONFIG_PATH):
                os.remove(CONFIG_PATH)                
            return func(*args, **kwargs)
        return wrapper
    return decorator

@cli.command()
@remove_global_config()
@ensure_global_config()
def configure(config_manager):
    """Configure CLI."""
    pass

if __name__ == '__main__':
    cli()
    pass

from cpchain.wallet.fs import *
from cpchain.chain.trans import *
from cpchain import chain, config, root_dir
from cpchain.chain.models import OrderInfo
from cpchain.crypto import Encoder, RSACipher


def test_server_chain():
    os.chdir(root_dir)
    server_web3 = chain.default_web3
    # chain.utils.deploy_contract(config.chain.core_contract)
    buyertrans = BuyerTrans(server_web3, config.chain.core_contract)
    print(server_web3.eth.defaultAccount)
    desc_hash_base64 = 'AQkKqDxtNIRJ+1V82J5lP2/fRj/zbJ+2n0GzUF52Wsc='
    desc_hash = Encoder.str_to_base64_byte(desc_hash_base64)
    public_key = RSACipher.load_public_key()
    print('pubkey ' + str(len(public_key)))
    order_info = OrderInfo(
        desc_hash=desc_hash,
        buyer_rsa_pubkey=public_key,
        seller=buyertrans.web3.eth.defaultAccount,
        proxy=buyertrans.web3.eth.defaultAccount,
        secondary_proxy=buyertrans.web3.eth.defaultAccount,
        proxy_value=10,
        value=20,
        time_allowed=100
    )
    test_server_id = buyertrans.place_order(order_info)
    print(test_server_id)
    # buyertrans.withdraw_order(test_server_id)
    # print(buyertrans.query_order(test_server_id))
    # order_num = buyertrans.get_order_num()
    # print(order_num)
    print(buyertrans.query_order(test_server_id))


def main():
    test_server_chain()


if __name__ == '__main__':
    main()

from web3 import Web3

ZERO_ADDRESS = Web3.to_checksum_address("0x0000000000000000000000000000000000000000")

NETWORK_MAP = {
    'Arbitrum Goerli': {
        'chain_id': 421613,
        'rpc': 'https://arbitrum-goerli.publicnode.com',
        'token': 'AGOR'
    },
    'Arbitrum': {
        'chain_id': 42161,
        'rpc': 'https://arbitrum-one.publicnode.com',
        'token': 'ETH'
    },
    'BSC': {
        'chain_id': 56,
        'rpc': 'https://bsc.publicnode.com',
        'token': 'BNB'
    },
    'tBSC': {
        'chain_id': 97,
        'rpc': 'https://bsc-testnet.publicnode.com',
        'token': 'tBNB'
    },
    'Ethereum': {
        'chain_id': 1,
        'rpc': 'https://ethereum.publicnode.com',
        'token': 'ETH'
    },
    'Goerli': {
        'chain_id': 5,
        'rpc': 'https://ethereum-goerli.publicnode.com',
        'token': 'GETH'
    },
    'Sepolia': {
        'chain_id': 11155111,
        'rpc': 'https://ethereum-sepolia.publicnode.com',
        'token': 'SETH'
    },
    'Optimism': {
        'chain_id': 10,
        'rpc': 'https://optimism.publicnode.com',
        'token': 'ETH'
    },
    'Optimism Goerli': {
        'chain_id': 420,
        'rpc': 'https://optimism-goerli.publicnode.com',
        'token': 'OGOR'
    },
    'Polygon': {
        'chain_id': 137,
        'rpc': 'https://polygon-bor.publicnode.com',
        'token': 'MATIC'
    },
    'Mumbai': {
        'chain_id': 80001,
        'rpc': 'https://polygon-mumbai-bor.publicnode.com',
        'token': 'MATIC'
    },
    'zkSync': {
        'chain_id': 324,
        'rpc': 'https://zksync.drpc.org',
        'token': 'ETH'
    }
}

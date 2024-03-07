from random import choice


def get_token():
    tokens = [
        '4dacf0ee4dacf0ee4dacf0ee094eba6a9f44dac4dacf0ee28dbbdc4a23c5348e6580f16',
        '3c6237653c6237653c6237653c3f75b52b33c623c623765598813034614cd3d437eab26',
        '5d3af2135d3af2135d3af213705e2d704355d3a5d3af21338d0d7255b2cd02d20c6dbcc',
        '3851144a3851144a3851144a963b46961b338513851144a5dbb312108863782dc11d1c3',
        '9253ecc49253ecc49253ecc40f91446e96992539253ecc4f7b9c95ee00c6a45915858b4'
    ]
    return choice(tokens)


for _ in range(10):
    print(get_token())

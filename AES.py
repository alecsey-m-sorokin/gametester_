import base64
import json

from Crypto.Cipher import AES
from base64 import b64encode
from base64 import b64decode
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

BS = 16
key_ = b'29F8A13E0F12076292E17EC6F83776DA'
text = b'XHiwSgf1Vv4e8tFIhlCu+8rwnudGl4p+TqcnRkHgsdly48jNPFonKH+mcj6woT7AUYr4pJa82jlx3aB9L1SUfojw4/z7UPdR9ppnE+XliFIRq2qtTuM25BR7ZMoQWqSwAhca/GeFqMYskLtIBvJVT+GhqpH5sbXvHVr74o2VuIJaifvbZZoB103eQJc0hke16w/fLKIMOlSSJPcmgWRmTxkXGRveHF/eCO6gblA48RutV/eiGHklPyPV9Yk2iT/gWp2huHp0GhqGqzvFwBjNOAWCfRYGwGJ1yRCdtG2Oes6mcNZdYeaehFA7bGItc6s544WDPYDmG91RlGrBMRK4Wh7qq+DPCXwA/WuhxZrCoUOqS44M26UWk+BPIDShzS6iix8NY1Br2IcJzAq/KTyeN33knw2L6mXXYWF3i/SaZ3FXd+vBkhnBVK/4ywBR7He3yh58vkwI0GlqrXfFZQnx8SAS/WKRLJVOFVq6VZ3llch9VC61WtIzWaxCqhAWVWKYHmcQG9FgW0CBHV2h+aRiQKNtwsSYDoO8NwI3TtZD5nPnd2DPme4g41ZzZ6bCo2wsYr9lvlzZdgBNs8rfTD7FdUWBSoLXagW0FExZNJgIw0r5qtQVCYRUAkiNBY4rc/RrP4pn56a0+vOWPqAj+HQ4oer1f5n+VOmSpQr9W2xLXcdr6BKqjtUdYVRLv61I4tJe'

# key = b'Sixteen byte key'
# cipher = AES.new(key, AES.MODE_EAX)
# ciphertext = cipher.encrypt_and_digest(b'secret')
# print(cipher.nonce)


data = b"secret"
key = get_random_bytes(32)
print(key)
cipher = AES.new(key_, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))
iv = b64encode(cipher.iv).decode('utf-8')
print(f'iv = {iv}')
ct = b64encode(ct_bytes).decode('utf-8')
print(f'ct = {ct}')
result = json.dumps({'iv': iv, 'ciphertext': ct})
print(result)


try:
    b64 = json.loads(result)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key_, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", pt)
except ValueError and KeyError:
    print("Incorrect decryption")


iv = get_random_bytes(16)

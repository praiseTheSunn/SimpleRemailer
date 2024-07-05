# SendStrategy
- implement some "gom thu" methods 

# DecryptionStrategy
- implement some cryptography algorithms to en/decrypt while sending/receiving

# Mix Node
- each MixNode has its own private key to decrypt (client can get MixNode's public key)
- use SendStrategy to decide when enough mail to send
- use DecryptionStrategy to en/decrypt by several methods

# Email
- help send email via SMTP
- need app password to run (you can get app pw here: https://myaccount.google.com/u/3/apppasswords)
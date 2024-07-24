from pydantic import BaseModel

class EmailRequest(BaseModel):
    email: str
    subject: str
    message: str

# encrypted by symmetric key K
class Message(BaseModel):
    # encryption algorithm to decrypt encrypted_key
    encryption_algorithm: str
    encrypted_content: str # encrypted by symmetric key (k) symmetric_key
    encrypted_key: str # encrypted by RSA public key

# encrypted_content decrypted by symmetric key symmetric_key 
class Hidden(BaseModel):
    ip: str
    path_strategy: str
    flag_begin: bool
    flag_end: bool

    # encrypted by symmetric key K2 for next node
    content: str # if flag_end is true then content is EmailRequest, else content is Hidden

class KEncrypted(BaseModel):
    # symmetric key to decrypt encrypted_content of Message
    symmetric_key: str

    # encrypted by RSA public key for next node
    k_encrypted: str 

# class HeaderInfo(BaseModel):
#     encryption_algorithm: str

# class EncryptedContent(BaseModel):
#     encrypted_message: str # encrypted by symmetric key
    

# class DecryptedData:
#     def __init__(self, flag_end: bool, path_strategy: str, next_ip: str, next_node_encrypted_data: str):
#         self.flag_end = flag_end
#         self.path_strategy = path_strategy
#         self.next_ip = next_ip
#         self.next_node_encrypted_data = next_node_encrypted_data
#     # EmailRequest: EmailRequest // secret
#     flag_end: bool
#     starting_node: bool # 1 la node dau tien, 0 la node khac
#     path_strategy: str # "Random 
#     next_ip: str
#     next_node_encrypted_data: str

#     def to_dict(self):
#         return {
#             "flag_end": self.flag_end,
#             "path_strategy": self.path_strategy,
#             "next_ip": self.next_ip,
#             "next_node_encrypted_data": self.next_node_encrypted_data
#         }
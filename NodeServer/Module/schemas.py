from pydantic import BaseModel

class EmailRequest(BaseModel):
    email: str
    subject: str
    message: str

class HeaderInfo(BaseModel):
    encryption_algorithm: str

class Message(BaseModel):
    header: HeaderInfo
    content: str
    

class DecryptedData(BaseModel):
    # EmailRequest: EmailRequest // secret
    flag_end: bool
    path_strategy: str
    next_ip: str
    next_node_encrypted_data: str
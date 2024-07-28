import axios from 'axios';
import CryptoJS from 'crypto-js';
import forge from 'node-forge';

const convertJsonToBytes = (json) => {
    return new TextEncoder().encode(JSON.stringify(json));
};

const convertJsonToString = (json) => {
    return JSON.stringify(json);
};

const base64Encode = (bytes) => {
    return CryptoJS.enc.Base64.stringify(CryptoJS.lib.WordArray.create(bytes));
};

const encryptRSA = (data, publicKey) => {
    const rsa = forge.pki.publicKeyFromPem(publicKey);
    const encrypted = rsa.encrypt(data, 'RSA-OAEP', {
        md: forge.md.sha256.create(),
        mgf1: forge.mgf1.create(forge.md.sha256.create())
    });
    return forge.util.encode64(encrypted);
};


// ==================================== AES ENCRYPTION ====================================

const generateKey = (keySize = 192) => {
  if (![128, 192, 256].includes(keySize)) {
    throw new Error("Invalid key size. Choose 128, 192, or 256 bits.");
  }
  return CryptoJS.lib.WordArray.random(keySize / 8);
};

const encrypt = (key, data) => {
  const iv = CryptoJS.lib.WordArray.random(16);
  const cipherParams = CryptoJS.AES.encrypt(data, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return iv.concat(cipherParams.ciphertext).toString(CryptoJS.enc.Base64);
};

// Reference: https://medium.com/@asttle1997/encryption-in-react-react-native-and-node-js-ceee589f429f
// Function to generate AES Key
export const generateAesKey = () => {
    const aesSalt = forge.random.getBytesSync(16);
    const keyPassPhrase = forge.random.getBytesSync(16);
    const aesKey = forge.pkcs5.pbkdf2(
      keyPassPhrase,
      aesSalt,
      100, // use according to your requirement
      32 // use according to your requirement
    );
    return aesKey;
  };
  
  // Function to encrypt data using AES Key
  export const encryptData = (data, aesKey) => {
    const iv = forge.random.getBytesSync(16); // Generate a random IV
    const cipher = forge.cipher.createCipher('AES-CBC', aesKey);
    cipher.start({ iv });
    cipher.update(forge.util.createBuffer(data));
    cipher.finish();
    const encrypted = cipher.output;
  const concatenatedBytes = iv + encrypted.getBytes();
  const concatenatedBase64 = forge.util.encode64(concatenatedBytes);
  
  return concatenatedBase64;
  };


// ------------------

const sendToSendingServer = async (baseURL, email, subject, message, encryptionAlgorithm, mixPathAlgorithm, mixSendingStrategy) => {
    const http = axios.create({
        baseURL: baseURL,
        headers: {
            "Content-type": "application/json",
            'Access-Control-Allow-Origin': '*',
        }
    });

    const emailMessage = {
        email: email,
        subject: subject,
        message: message,
    };

    var emailBytes = convertJsonToBytes(emailMessage);
    emailBytes = base64Encode(emailBytes);

    const hidden = {
        ip: '',
        path_strategy: mixPathAlgorithm,
        flag_begin: true,
        flag_end: false,
        content: emailBytes,
    };

    var publicKey = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArC4HVnO3rNdGJkACwuEJ\nmaXDrkFs2Al53vqoYDVYCavOsmHmv6KoXot6aXr0onBO8YugdTIjQLJ3PE1x1WaW\n+BQi6hbP3WxmShL8/l2SUHjvIMUWJe6nkbrRUYAHmSGouhif5FLWPvUtWcFenKwN\nvnR9Rtjlbut70vLpVp3/A/R6L+VykUWQ8EpQcpg0yFlvlJbKD7e+9btAZgkUtI9j\neF2LOnA++XM2+So4Y5CO2xNAZ5nSKmEYd/zmjnfxDgabe62M1eWyKtxCXnokklfG\nWt0HYcMvFuKr4CzpdChfL5JBagRo4qEEphf0eWo0hVgp0QKBUl2x5X0olUOcVAiy\nnwIDAQAB\n-----END PUBLIC KEY-----\n'
    var symmetric_key_bytes = generateAesKey();
    var symmetric_key = forge.util.encode64(symmetric_key_bytes);
    

    console.log("Symmetric key base64:", symmetric_key);
    const encryptedKey = {
        symmetric_key : symmetric_key,
        k_encrypted : "",
    }

    var encryptedKeyStr = convertJsonToString(encryptedKey);
    var hiddenStr = convertJsonToString(hidden);

    console.log('Hidden:', hiddenStr);
    var encrypted_content = encryptData(hiddenStr, symmetric_key_bytes);
    var encrypted_key = encryptRSA(encryptedKeyStr, publicKey);

    console.log('Encrypted content:??', encrypted_content);
    console.log('Encrypted key:', encrypted_key);
    
    const encryptedMessage = {
        encryption_algorithm: "rsa_encryption",
        encrypted_content: (encrypted_content),
        encrypted_key: encrypted_key,
    };

    try {
        const response = await http.post(`/receiveEmail`, encryptedMessage);
        return response.data;
    } catch (error) {
        console.error('Error sending email:', error);
    }
};

const serverRequestService = {
    sendToSendingServer,
};

export default serverRequestService;

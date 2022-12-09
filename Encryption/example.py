from Encryption import Encrypt, DeEncrypt, Key

#Define key object
#Key has the parameters: -MINlen, -MAXlen, -AddChars (Str)
key = Key(MAXlen=50)
key.make()

Enc = Encrypt(key, "Hello world!")
print(f"{Enc}, lenght: {len(Enc)}")

DeEnc = DeEncrypt(key, Enc) #Encrypted string
print(f"{DeEnc}, lenght: {len(DeEnc)}")
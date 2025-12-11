import hashlib

def MD5():
    original = "C"
    
    # Créer un objet MD5 (équivalent à MessageDigest.getInstance("MD5"))
    md = hashlib.md5()
    
    # Mettre à jour avec les bytes de la chaîne
    md.update(original.encode())
    
    # Récupérer le digest
    digest = md.digest()
    
    # Convertir en hexadécimal (équivalent de la boucle Java)
    sb = "".join(format(b, "02x") for b in digest)
    
    print("original: " + original)
    print("digested(hex): " + sb)
    print("premier élément du digest: " + str(digest[0]))

if __name__ == "__main__":
    MD5()
from stellar_base.keypair import Keypair

def verify(te, keypair):

    if te.signatures is None or len(te.signatures) == 0:
        return False

    hash_e = te.hash_meta()
    signatures = te.signatures

    for signature in signatures:
        try:
            keypair.verify(signature=signature.signature,data=hash_e)
            return True
        except Exception as e:
            pass

    return False

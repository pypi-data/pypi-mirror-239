import argparse
import getpass
import random
import secrets
import sys
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e
from decimal import Decimal

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ArgParser(argparse.ArgumentParser):
    """
    argparse ArgumentParser internal override for custom help functionality
    """
    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        message = f" • split:\n\tpython3 \"{ sys.argv[0] }\" split -f STRING -m INT -n INT -e\n\n\t-f: Filepath to file to be split into shares.\n\t-m: Minimum number of shares needed to reconstruct the file.\n\t-n: Total number of shares to split the file into.\n\t-e: OPTIONAL - Password encrypt shares if provided.\n\n • join:\n\tpython3 \"{ sys.argv[0] }\" join -s STRING -d\n\n\t-s: REPEATABLE - Filepath to a share of the file to be reconstucted.\n\t-d: OPTIONAL - Password decrypt shares if provided."
        file.write(message+"\n")

class SSS():
    """
    Shamir's Secret Sharing
    """
    FIELD_SIZE = 10**5

    def reconstruct_secret(shares):
        """
        Combines individual shares (points on graph)
        using Lagranges interpolation.
        
        `shares` is a list of points (x, y) belonging to a
        polynomial with a constant of our key.
        """
        sums = 0
        for j, share_j in enumerate(shares):
            xj, yj = share_j
            prod = Decimal(1)
            for i, share_i in enumerate(shares):
                xi, _ = share_i
                if i != j:
                    prod *= Decimal(Decimal(xi)/(xi-xj))
            prod *= yj
            sums += Decimal(prod)
        return int(round(Decimal(sums), 0))

    def polynom(x, coefficients):
        """
        This generates a single point on the graph of given polynomial
        in `x`. The polynomial is given by the list of `coefficients`.
        """
        point = 0
        for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
            point += x ** coefficient_index * coefficient_value
        return point
        
    def coeff(t, secret):
        """
        Randomly generate a list of coefficients for a polynomial with
        degree of `t` - 1, whose constant is `secret`.
        
        For example with a 3rd degree coefficient like this:
            3x^3 + 4x^2 + 18x + 554
        
            554 is the secret, and the polynomial degree + 1 is
            how many points are needed to recover this secret.
            (in this case it's 4 points).
        """
        coeff = [random.randrange(0, SSS.FIELD_SIZE) for _ in range(t - 1)]
        coeff.append(secret)
        return coeff
        
    def generate_shares(n, m, secret):
        """
        Split given `secret` into `n` shares with minimum threshold
        of `m` shares to recover this `secret`, using SSS algorithm.
        """
        coefficients = SSS.coeff(m, secret)
        shares = []
        
        for i in range(1, n+1):
            x = random.randrange(1, SSS.FIELD_SIZE)
            shares.append((x, SSS.polynom(x, coefficients)))
        
        return shares

class OKTS():
    """
    Open Keyshare Threshold Scheme - internal functions
    """
    backend = default_backend()
    iterations = 100_000

    def str_to_int(x) -> int:
        """
        Converts a string to int using byte encoding since the SSS algorithm only works with numbers.
        """
        return int.from_bytes(str(x).encode("utf-8"), byteorder="big")

    def int_to_str(x) -> str:
        """
        Converts an integer to a string using byte decoding.
        """
        return (int(x).to_bytes(((x.bit_length() + 7) // 8), byteorder='big')).decode("utf-8")

    def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=iterations, backend=OKTS.backend)
        return b64e(kdf.derive(password))

    def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
        salt = secrets.token_bytes(16)
        key = OKTS._derive_key(password.encode(), salt, iterations)
        return b64e(
            b'%b%b%b' % (
                salt,
                iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        )

    def password_decrypt(token: bytes, password: str) -> bytes:
        decoded = b64d(token)
        salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter, 'big')
        key = OKTS._derive_key(password.encode(), salt, iterations)
        return Fernet(key).decrypt(token)
                

    def split(args):
        chunks = []
        with open(args['f'], "rb") as in_file:
            print(f" getting 8 byte chunks from '{args['f']}'")
            while True:
                chunk = in_file.read(8)
                if chunk == b'':
                    break
                else:
                    shares = SSS.generate_shares(int(args['n']), int(args['m']), OKTS.str_to_int(chunk.decode("utf-8")))
                    chunks.append(shares)
        path = '\\'.join(args['f'].split('\\')[0:-1])
        name = (args['f'].rpartition('\\')[-1]).rpartition('.')[0]
        sharefiles = []
        for chunk in chunks:
            i = 0
            for share in chunk:
                if f"{path}\\{name}{i}.share" not in sharefiles:
                    sharefiles.append(f"{path}\\{name}{i}.share")
                with open(f"{path}\\{name}{i}.share", "a") as out_file:
                    out_file.write(f"{share[0]} {share[1]}\n")
                i += 1
        for sf in sharefiles:
            if not args['e']:
                print(f" created '{sf}'")
            else:
                with open(f"{sf}", "rb") as file:
                    data = file.read()
                with open(f"{sf}", "wb") as file:
                    print(f"\n Please enter a password for {sf}")
                    print(f"  • Password should have at least one number")
                    print(f"  • Password should have at least one uppercase letter")
                    print(f"  • Password should have at least one lowercase letter")
                    print(f"  • Password should have at least one special character")
                    print(f"  • Password should have at least 8 characters or more")
                    match = False
                    while not match:
                        password = getpass.getpass(f"\n Password for '{sf}':")
                        val = OKTS.validate_password(password)
                        if len(val) > 0:
                            print(val)
                        else:
                            confirm = getpass.getpass(f" Please confirm password: ")
                            if password == confirm:
                                file.write(OKTS.password_encrypt(data, password))
                                print(f" created '{sf}'")
                                break
                            print ("\n Passwords dont match")
        print ("\n Split complete!")

    def join(args):
        shares = []
        for share_file in args['s']:
            i = 0
            if not args['d']:
                with open(share_file, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.strip() != "":
                            if share_file == args['s'][0]:
                                shares.append([])
                            shares[i].append([
                                int(line.strip().split(' ')[0]) if line.strip().split(' ')[0].isdecimal() else 0,
                                int(line.strip().split(' ')[1]) if line.strip().split(' ')[1].isdecimal() else 0,
                            ])
                            if len(shares[i]) == len(args['s']):
                                shares[i] = OKTS.int_to_str(SSS.reconstruct_secret(shares[i]))
                            i += 1
            else:
                with open(share_file, "rb") as file:
                    decrypted = False
                    while not decrypted:
                        try:
                            lines = ((OKTS.password_decrypt(file.read(), getpass.getpass(f"\n Password for '{share_file}':")).decode()).split("\r\n"))
                            decrypted = True
                        except Exception as error:
                            stacktrace = f"{sys.exc_info()}"
                            if "cryptography.fernet.InvalidToken" in stacktrace:
                                print(f"\n Invalid password")
                            else:
                                raise Exception(error)

                    for line in lines:
                        if line.strip() != "":
                            if share_file == args['s'][0]:
                                shares.append([])
                            shares[i].append([
                                int(line.strip().split(' ')[0]) if line.strip().split(' ')[0].isdecimal() else 0,
                                int(line.strip().split(' ')[1]) if line.strip().split(' ')[1].isdecimal() else 0,
                            ])
                            if len(shares[i]) == len(args['s']):
                                shares[i] = OKTS.int_to_str(SSS.reconstruct_secret(shares[i]))
                            i += 1
        print(f"\n Reconstructed Key:\n\n{''.join(shares)}")

    def validate_password(password) -> str:
        has_digit = False
        has_upper = False
        has_lower = False
        has_sym = False
        has_len = False

        for char in password:
            if ord(char) >= 48 and ord(char) <= 57:
                has_digit = True
            elif ord(char) >= 65 and ord(char) <= 90:
                has_upper = True
            elif ord(char) >= 97 and ord(char) <= 122:
                has_lower = True
            elif not str(char).isalnum():
                has_sym = True

        if not len(password) < 8:
            has_len = True
            
        if not has_digit:
            return' Password should have at least one numeral'
        if not has_upper:
            return' Password should have at least one uppercase letter'
        if not has_lower:
            return' Password should have at least one lowercase letter'
        if not has_sym:
            return' Password should have at least one special character'
        if not has_len:
            return' Password cannot be less than 8 characters'
        return ""

if (__name__ == "__main__"):
    print("\n============================================")
    print("  Open Keyshare Threshold Scheme - CLI: v0.0.1")
    print("============================================\n")

    parser = ArgParser()
    subparsers = parser.add_subparsers()

    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("-f", action="store", required=True)
    split_parser.add_argument("-m", action="store", type=int, required=True)
    split_parser.add_argument("-n", action="store", type=int, required=True)
    split_parser.add_argument("-e", action="store_true")

    join_parser = subparsers.add_parser("join")
    join_parser.add_argument("-s", action="append", required=True)
    join_parser.add_argument("-d", action="store_true")

    args = vars(parser.parse_args())

    try:
        if 'f' in args and 'm' in args and 'n' in args:
            OKTS.split(args)
        elif 's' in args:
            OKTS.join(args)
    except Exception as error:
        if "Invalid base64-encoded string" in str(error):
            print(f"\n An error occurred: File is not encrypted")
        else:
            if len(str(error)) > 0:
                print(f"\n An error occurred: {error}")
            else:
                print(f"\n An error occurred: {sys.exc_info()}")
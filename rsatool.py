import base64
from pathlib import Path
from datetime import datetime

from typing import Union
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option("--out_pubk_filename", default='public.pem', type=click.Path(), show_default=True, help='public key filename to saved in current dir')
@click.option('--out_prik_filename', default='private.pem', type=click.Path(), show_default=True, help='private key filename to saved in current dir')
@click.option("--backup", is_flag=True, show_default=True, default=True, help="backup the old public and private key if exists in current dir")
def generate(out_pubk_filename, out_prik_filename, backup):
    if backup:
        if Path(out_pubk_filename).exists():
            Path(out_pubk_filename).rename(f"{datetime.now():%Y%m%d%H%M%S%f}_old_public.pem")
        if Path(out_prik_filename).exists():
            Path(out_prik_filename).rename(f"{datetime.now():%Y%m%d%H%M%S%f}_old_private.pem")
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(out_prik_filename, 'wb') as f:
        f.write(private_key)

    public_key = key.publickey().export_key()
    with open(out_pubk_filename, 'wb') as f:
        f.write(public_key)

@cli.command()
@click.option("--input_filename", default='data', type=click.Path(), show_default=True)
@click.option('--out_filename', default='encrypted_data', type=click.Path(), show_default=True)
@click.option('--cipher', default='PKCS1_v1_5', type=click.Choice(['PKCS1_v1_5', 'PKCS1_OAEP'], case_sensitive=False), show_default=True)
def encrypt(input_filename, out_filename, cipher):
    with open(input_filename, 'rb') as input:
        data = input.read()
        with open("public.pem") as f:
            publick_key = RSA.import_key(f.read())
        
        cipher_select = {
            "PKCS1_v1_5": PKCS1_v1_5,
            "PKCS1_OAEP": PKCS1_OAEP
        }
        cipher = cipher_select[cipher].new(publick_key)
        ciphertext = cipher.encrypt(data)

        with open(out_filename, "wb") as f:
            f.write(base64.b64encode(ciphertext))


@cli.command()
@click.option("--input_filename", default='encrypted_data', type=click.Path(), show_default=True)
@click.option('--out_filename', default='decrypted_data', type=click.Path(), show_default=True)
@click.option('--cipher', default='PKCS1_v1_5', type=click.Choice(['PKCS1_v1_5', 'PKCS1_OAEP'], case_sensitive=False), show_default=True)
def decrypt(input_filename, out_filename, cipher):
    with open(input_filename, 'rb') as input:
        data = input.read().decode()
        if isinstance(data, str):
            data = data.encode()
        data = base64.b64decode(data)
        with open("private.pem") as f:
            private_key = RSA.import_key(f.read())

        cipher_select = {
            "PKCS1_v1_5": PKCS1_v1_5,
            "PKCS1_OAEP": PKCS1_OAEP
        }
        _cipher = cipher_select[cipher].new(private_key)
        if cipher == 'PKCS1_v1_5':
            args = (data, True)
        else:
            args = (data, )
        ciphertext = _cipher.decrypt(*args)

        with open(out_filename, "wb") as f:
            f.write(ciphertext)


if __name__ == '__main__':
    cli()
# RSAGenerator

A tools to generate rsa keys, encrypt and decrypt message.

[中文说明](ZH-README.md)

## Usage
1. Command `generate`: 
   Generate rsa keys, will generate `public.pem` and `private.pem` in **current dir**.
2. Command `encrypt`: 
   Encrypt message, will read `public.pem`, `data.txt` file and create `encrypted_data.txt` in **current dir**
3. Command `decrypt`: 
   Decrypt message, will read `private.pem`, `encrypted_data.txt` and create `decrypted_data.txt` file in **current dir**.
4. Option `--help`: Print help message.Include input/output filename, cipher used and etc.

### Windows
> You need download rsatool.exe from [Releases](https://github.com/MioYvo/RSAGenerator/releases) page.
Currently rsatool can only run in Windows Powershell or Windows Ternimal. No GUI.

1. Find and open your `rsatools.exe` folder ![](docs/d_folder.png).
2. Open Windows terminal or Windows PowerShell. 
   1. On Windows 11, just `right mouse click` at folder blank area.![](docs/open_t.png)
   2. You can try `shift + right mouse click` at folder's blank area and choose "open a powershell window here"![](docs/shift_open_t.png)
3. type:
    ```
    rsatools.exe
    ```

    ```
    rsatools.exe generate
    ```

    ```
    rsatools.exe encrypt
    ```

    ```
    rsatools.exe decrypt
    ```

    add `--help` will print help message. 
    Example:
    ```
    PS D:\test> .\rsatool.exe encrypt --help
    Usage: rsatool.exe encrypt [OPTIONS]

    Options:
    --input_filename PATH           [default: data]
    --out_filename PATH             [default: encrypted_data]
    --cipher [PKCS1_v1_5|PKCS1_OAEP]
                                    [default: PKCS1_v1_5]
    --help                          Show this message and exit
    ```
    ![](docs/type_in.png)



# For development
## Package codes to exe
```
pyinstaller rsatool.py -F
```




#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,re,base64,binascii,time,shutil
from hashlib import md5
from os import urandom

import ansible
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
from ansible.parsing.vault import VaultLib
from ansible.module_utils._text import to_bytes, to_text, to_native

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def print_mes(vault_dir, role_name, mes):
  out_file = open( os.path.join(os.path.dirname(vault_dir), 'tmp/roles_params/%s/%s.log' % (role_name, role_name)),'ab' )
  out_file.write("\n%s" % mes)
  out_file.close()

def print_err_mes(vault_dir, role_name, mes):
  out_file = open( os.path.join(os.path.dirname(vault_dir), 'tmp/roles_params/%s/%s.error' % (role_name, role_name)),'ab' )
  out_file.write("\n%s" % mes)
  out_file.close()

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + str.encode(password) + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def decrypt(vault_dir, in_file, password, salt_header='Salted__', key_length=32):
    bs = algorithms.AES.block_size / 8
    salt = in_file.read(bs)[len(salt_header):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    message_decrypt = decryptor.update(in_file.read()) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(message_decrypt) + unpadder.finalize()

    return plaintext

def parse_enc_parameters(vault_dir, vault_file, role_name, enc_data, fetch_keys):
    enc_params_dict = {}
    for data in enc_data.split('\n'):
        data_row = data.rstrip('\r\n')
        row = ''.join(data_row.split())
        if not re.search(r"^#(.*)", row) and row != '':
            options = data_row.split('=')
            if len(options) > 1:
                # Передаётся содержимое строки после знака '=', включая пробелы и любые другие символы, кроме "\r" или "\n"
                pass_data_key = ''.join(options[0].split())
                pass_data_row = ''.join(options[1].split())
                if len(pass_data_key) > 0:
                    offset = len(options[0]) + 1
                    if pass_data_key in fetch_keys:
                        if pass_data_key not in enc_params_dict.keys():
                            if pass_data_row.startswith('"') and pass_data_row.endswith('"') and len(pass_data_row.split('"')) > 2:
                                lsp_offset = data_row[offset:].index('"') + 1
                                rsp_offset = data_row[offset:].rindex('"')
                                if rsp_offset - lsp_offset >= 0:
                                    enc_params_dict[pass_data_key] = data_row[offset:][lsp_offset:rsp_offset]
                            else:
                                print_mes(vault_dir, role_name, "Не найдено ограничивающих символов кавычек для значения ключа \"%s\". В качестве значения ключа будет передано содержимое строки после знака '=', включая пробелы и любые другие символы, кроме \"\\r\" или \"\\n\"." % pass_data_key)
                                enc_params_dict[pass_data_key] = data_row[offset:]
                        else:
                            print_mes(vault_dir, role_name, "Обнаружено повторное вхождение для ключа, который уже был считан ранее в файле: \"%s\"." % vault_file)
    keys_not_found = []
    for key in fetch_keys:
        if key not in enc_params_dict.keys():
            keys_not_found.append(key)
    if keys_not_found:
        print_err_mes(vault_dir, role_name, "Не найдены следующие ключи из списка поиска: [%s]." % ', '.join(keys_not_found))
    else:
        print_mes(vault_dir, role_name, "Значения для ключей из списка поиска в файле: \"%s\" загружены." % vault_file)

    return enc_params_dict

def get_filter_enc_parameters(vault_pass, vault_type, vault_file, vault_dir, fetch_keys, role_name):
    enc_params_dict = {}
    print_mes(vault_dir, role_name, "Загрузка параметров по списку ключей из файла \"%s\"." % vault_file)
    if sys.version_info < (3, 0):
        vault_pass_data = bytes(vault_pass)
    else:
        vault_pass_data = bytes(vault_pass, 'utf8')

    if os.path.isfile(os.path.join(vault_dir, vault_file)):
        if vault_type == "ANSIBLE_VAULT":
            _ansible_ver = float('.'.join(ansible.__version__.split('.')[:2]))
            if _ansible_ver <= 2.3:
                vault = VaultLib(vault_pass)
            elif _ansible_ver >= 2.4:
                from ansible.constants import DEFAULT_VAULT_ID_MATCH
                from ansible.parsing.vault import VaultSecret
                vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, VaultSecret(vault_pass_data))])

            try:
                print_mes(vault_dir, role_name, "Загрузка \"%s\"." % vault_file)
                enc_data = vault.decrypt(  open( os.path.join(vault_dir, vault_file) ).read() )
                print_mes(vault_dir, role_name, "Файл \"%s\" загружен." % vault_file)
                enc_params_dict = parse_enc_parameters(vault_dir, vault_file, role_name, enc_data, fetch_keys)
                # Очистка переменных
                enc_data = 'init'
                vault_pass_data = ''
            except Exception as exc:
                print_err_mes(vault_dir, role_name, "При считывании файла \"%s\" произошла ошибка." % vault_file)
                print_err_mes(vault_dir, role_name, exc)

        elif vault_type == "OPENSSL_AES_256_CBC":
            in_file = open( os.path.join(vault_dir, vault_file),'r' )
            try:
                print_mes(vault_dir, role_name, "Загрузка \"%s\"." % vault_file)
                enc_data = decrypt(vault_dir, in_file, vault_pass_data, 'Salted__')
                print_mes(vault_dir, role_name, "Файл \"%s\" загружен." % vault_file)
                enc_params_dict = parse_enc_parameters(vault_dir, vault_file, role_name, enc_data, fetch_keys)
                # Очистка переменных
                enc_data = ''
                vault_pass_data = ''

            except Exception as exc:
                print_err_mes(vault_dir, role_name, "При считывании файла \"%s\" произошла ошибка." % vault_file)
                print_err_mes(vault_dir, role_name, exc)
            in_file.close()
        else:
          print_err_mes(vault_dir, role_name, "Формат контейнера \"%s\" не поддерживается." % vault_type)
    else:
      print_mes(vault_dir, role_name, "Файл \"%s\" не найден." % vault_file)
    return enc_params_dict

def main():
    module = AnsibleModule(

        argument_spec = dict(
            vault_pass  = dict(required=True, type='str'),
            vault_type  = dict(required=True, type='str'),
            vault_file  = dict(required=False, default='_passwords.conf', type='str'),
            vault_dir   = dict(required=True, type='str'),
            fetch_keys     = dict(required=True, type='list'),
            set_fact_var   = dict(required=True, type='str'),
            role_name   = dict(required=True, type='str')
        )
    )
    vault_pass = module.params['vault_pass']
    vault_type = module.params['vault_type']
    vault_file = module.params['vault_file']
    vault_dir = module.params['vault_dir']
    fetch_keys = module.params['fetch_keys']
    set_fact_var = module.params['set_fact_var']
    role_name = module.params['role_name']
    enc_params_dict = get_filter_enc_parameters(vault_pass, vault_type, vault_file, vault_dir, fetch_keys, role_name)

    module.exit_json(
        changed = False,
        ansible_facts = { set_fact_var: enc_params_dict}
    )

if __name__ == '__main__':
      main()

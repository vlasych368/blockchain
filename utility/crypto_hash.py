import hashlib
import json

def stringify(data):
    return json.dumps(data)

def crypto_hash(*args):
    """
    Return a sha-256 hash of the given argument.
    """
    stringifies_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringifies_args)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest() 
    '''
    sha 256 приводит строку в битный формат
    .encode() преобразовывает в 8 битный формат
    
    '''

def main():
    print(f"crypto_hash('one', 2 ,[3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash( 2 ,'one',[3]): {crypto_hash(2,'one',[3])}")

if __name__ == '__main__':
    main()
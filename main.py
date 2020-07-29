import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(f'Error fetchning:{response.status_code},check the api and try again')
    return response

def get_password_leaks_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
          return count
    return 0

def pwned_api_check(password):
    #Check password if it exist in api response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5],sha1password[5:]
    res = request_api_data(first5_char)
    print(first5_char,tail)
    return get_password_leaks_count(res,tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times...you should probably change your password!')
        else:
            print(f'{password} was not found.Carry on!')
    return 'Done!'

if __name__ == '__main__':
 sys.exit( main(sys.argv[1:]))


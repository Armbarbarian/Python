# Utils

def get_handle():
    handle = input('Enter your name: ')
    return handle

if __name__ == '__main__':
    h = get_handle()
    length = len(h)
    print('your name has', length, 'characters')

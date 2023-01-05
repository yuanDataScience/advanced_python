import io
from iso6346 import create

def get_BIC(owner, num):
    return create(owner,num)

if __name__ == "__main__":
    print(create("NIW", "3337"))


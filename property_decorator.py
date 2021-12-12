class Person():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def email(self):
        return "{}.{}@hotmail.com".format(self.first_name, self.last_name)

    @property
    def fullname(self):
        return "{}.{}".format(self.first_name, self.last_name)

    @fullname.setter
    def fullname(self, name):
        self.first_name, self.last_name = name.split(" ")

    @fullname.deleter
    def fullname(self):
        print(f"delete fullname {self.firstname} {self.lastname}")
        self.first_name = None
        self.last_name = None

if __name__ == "__main__":
    jb = Person("Jane", "Hu")
    print(jb.fullname)
    print(jb.email)

    jb.fullname = "Alice Wang"
    print(jb.fullname)
    print(jb.email)

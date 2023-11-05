def pityu_loopyear(year):
    year = int(year)
    if year % 4 != 0:
        print("Not leap year.")
        return False
    else:
        if year % 100 != 0:
            print("Leap year.")
            return True
        else:
            if year % 400 != 0:
                print("Not leap year.")
                return False
            else:
                print("Leap year.")
                return True

def hello_world():
    print("Hello World!")
import re, random

def is_email(email):
	EMAIL_PATTERN = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
	return re.fullmatch(EMAIL_PATTERN, email) is not None

def is_name(name):
    NAME_PATTERN = "[A-Za-z]+"
    return re.fullmatch(NAME_PATTERN, name) is not None

def is_phone_number(phone):
    PHONE_PATTERN =  "^((\\+?(?!0)\\d{2,3})|0)\\d{10}"
    return re.fullmatch(PHONE_PATTERN, phone) is not None

def make_code():
    return "".join(random.sample('01234567890123456789', 4))

def is_img_extension(image_name):
    PATTERN = ".+\\.(png|jpg|jpeg|gif)$"
    return re.search(PATTERN, image_name, re.IGNORECASE) is not None

if __name__ == "__main__":
    while True:
        text = input("Enter image file name: ")
        is_valid = is_img_extension(text)
        if is_valid:
            print("The %s is valid" %text)
        else:
            print("The %s is not valid" %text)
        if input("try again? ") not in ["Y", 'y', 'yes']:
            break

# INPUT

PINCODE = input("Enter your pincode : ")
PATH = "C:/Users/abhin/Desktop/chromedriver.exe"

products = []
product = ''
print("Enter item name(Enter 0 when done) : ")
while product != '0':
    # Product 
    product = input()
    products.append(product)
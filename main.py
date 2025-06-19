m_username="rahul.007"
m_password="password"
man_username=input("Enter username=>" )
man_password=input("Enter password=> ")
def discount(n):
    return lambda grand_total:grand_total-((grand_total*n)/100)
n=0
if m_password==man_password and m_username==man_username:
    print("****Welcome****\nPlease enter discount for today")
    n=int(input("Enter discount % =>"))
else:
    print("Access denied")

bil_username="admin"
bill_password="12345"
bil_username1=input("Enter biller username=> ")
bill_password1=input("Enter biller password=> ")
if bil_username==bil_username1 and bill_password==bill_password1:
    print("***Billing window activated***")
else:
    print("Access denied")
shopkart=[]
while True:
    product_name=input("Enter product name(or type done to end)=> ")
    if product_name.lower()=="done":
        break
    try:
            product_num=int(input("Enter number of product=> "))
            product_price=int(input("Product MRP => "))
            total=(product_num*product_price)
            shopkart.append((product_name,product_num,product_price,total))
    except ValueError:
        print("Enter the details correctly")
print("\nShopping Bill:")
print("-" * 40)
print(f"{'Product':<15}{'Qty':<5}{'Price':<10}{'Total':<10}")
print("-" * 40)

grand_total=0
for item in shopkart:
    print(f"{item[0]:<15}{item[1]:<5}{item[2]:<10}{item[3]:<10}")
    grand_total+=item[3]

if grand_total>=1000:
    offer = discount(n)
    discounted_price=offer(grand_total)
else:
    n=0
    offer = discount(n)
    discounted_price=offer(grand_total)
print(f"Payble amount after {n}% discount =>{discounted_price}")
print("*"*10,"Thank You Visit Again","*"*10)
from datetime import datetime
import pandas as pd

input = "0|H0STASP0|001|000660^152522^A^959000^960000^961000^0^0^0^0^0^0^0^958000^957000^956000^0^0^0^0^0^0^0^3893^7010^4960^0^0^0^0^0^0^0^12^76^51^0^0^0^0^0^0^0^15863^139^0^0^959000^259810^259810^10000^2^1.05^3184369^0^0^0^0^0^0^0^0"
data = input.split('|')[3]
print(type(data[:6]))

now = datetime.now()
print(now.strftime("%H:%M:%S"))
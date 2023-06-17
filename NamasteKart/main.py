import pandas as pd

from validations import Validate
from send_mail import Email



if __name__ =="__main__":
    
    product_master = pd.read_csv(r'NamasteKart\incoming_files\20230616\product_master.csv')
    orders = pd.read_csv(r'NamasteKart\incoming_files\20230616\orders_1.csv')  
    
    output = Validate(product_master , orders)
    output2 = Email()
    output.current_date_folder(0)
    output.validate_id()
    output.validate_total_sales()
    output.validate_order_date()
    output.check_empty_fields()
    output.vlaidate_order_city()
    output.allocate_files()
    output2.send_email()
    print('\n')
    print('________________________________SUCCESSFUL RUN________________________________')
    print('\n')

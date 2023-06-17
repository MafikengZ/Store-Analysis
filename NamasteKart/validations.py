import os
from datetime import datetime , date
import pandas as pd
import numpy as np

from dataclasses import dataclass, field
from typing import List

@dataclass
class Validate(object):
    
    products: pd.DataFrame
    order: pd.DataFrame
    reasons= []
    cities =['Mumbai', 'Bangalore']
    sub_folder:str = 'NamasteKart'
    today = datetime.now().strftime("%Y%m%d")
    
    
    def current_date_folder (self, n)->None:

        # list of the current working directories
        dir =  os.listdir(self.sub_folder)
        
        # Create a directory path to incoming_files
        path = os.path.join(self.sub_folder, dir[n])
        
        # Create a directory path with the current date as folder_name
        folder_path = os.path.join(path,  self.today)

        # Create the directory
        os.makedirs(folder_path, exist_ok=True)
        

    def append_reasons(self):
        return self.order.apply(lambda row: pd.concat([row, pd.Series([','.join(map(str, self.reasons))], index=['Reason'])]), axis=1)
       

    def validate_id(self):
         # Check if the ID in product matches the ID in orders
        self.order['Match'] = self.order['product_id'].isin(self.products['product_id'])
        
        #If there is no match on product id
        if (self.order['Match'] == False).any():
            # Append values to each row and separate by commas
            self.reasons.append('Non Matching Product IDs')
            order = self.append_reasons()
            return order
        return self.order
    
    def validate_total_sales(self):
        order = self.validate_id()
        
        if (order['Match'] == False).any():
            self.reasons.append('Total Sale not balanced')
            order = self.append_reasons()
            return order         
        order['Total Sales'] = np.sum(self.products['price'] * order['quantity'])
        return order
     

    def validate_order_date (self):
        
    # Convert the 'order_date' column to datetime
        self.order['order_date'] = pd.to_datetime(self.order['order_date'])

        # Get the current date
        current_date = pd.to_datetime(date.today())

        # Check if the 'order_date' is not in the future
        if (self.order['order_date'] > current_date).any():
            self.reasons.append('Order date in future')
            order = self.append_reasons()
            return order
        return self.validate_total_sales()

        
        
    def check_empty_fields(self):
        
        # Check if any fields are empty
        is_empty = self.order.isna().any()
        if (is_empty == True).any():
            self.reasons.append('Empty Fields')
            order = self.append_reasons()
            return order
        return self.validate_order_date()
        

    def vlaidate_order_city(self):
        
        # Check if orders are coming from Mumbai or Bangalore
        is_city = self.order['city'].isin(self.cities).all()
        
        if not is_city:
            self.reasons.append('Order not from Mumbai/Bangalore')
            order = self.append_reasons()
            return order
        return self.check_empty_fields()
    

    def allocate_files(self):
        
        column_name ="Reason"
        order = self.vlaidate_order_city()    
        order.drop(['Match'], axis=1, inplace=True)
        
        #check if column name 'Reason' exist
        if column_name in order.columns:
        
            # copy the 'orders.csv' file to rejected/success
            self.current_date_folder(1)
            order.to_csv(f"NamasteKart/rejected_files/{self.today}/errors_{self.today}.csv",index=False)
            # shutil.move(r'{}/{}'.format(source , f"errors_{self.today}.csv"), r"NamasteKart/rejected_files/{}".format(self.today))
        else:        
            self.current_date_folder(1)
            order.to_csv(f"NamasteKart/success_files/{self.today}/orders_{self.today}.csv",index=False)

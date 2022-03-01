from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class IncompleteOrders(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select 
                bangazon_api_order.id as order_id,
                auth_user.first_name || " " || auth_user.last_name as customer_name,
                sum(price) as total_paid,
                bangazon_api_paymenttype.merchant_name as payment_type,
                bangazon_api_order.created_on
            from bangazon_api_order
            join auth_user on auth_user.id == bangazon_api_order.user_id
            left join bangazon_api_paymenttype on bangazon_api_paymenttype.id == bangazon_api_order.payment_type_id
            join bangazon_api_orderproduct on bangazon_api_orderproduct.order_id == bangazon_api_order.id
            join bangazon_api_product on bangazon_api_product.id == bangazon_api_orderproduct.product_id
            where payment_type is NULL
            group by order_id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            orders = []

            for row in dataset:

                order = {
                    'order_id': row['order_id'],
                    'customer_name': row['customer_name'],
                    'total_paid': row['total_paid'],
                    'created_on': row['created_on']
                }
                
                orders.append(order)


        # The template string must match the file name of the html template
        template = 'incomplete_orders.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "incomplete_orders_list": orders
        }

        return render(request, template, context)
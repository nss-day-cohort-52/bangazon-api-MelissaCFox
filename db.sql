select * from bangazon_api_orderproduct op
join bangazon_api_order  on bangazon_api_order.id = op.order_id
where bangazon_api_order.completed_on != 'NULL'
order by product_id


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



where bangazon_api_order.completed_on is not NULL

select * from bangazon_api_order
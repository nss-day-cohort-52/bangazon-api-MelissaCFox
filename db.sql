select * from bangazon_api_orderproduct op
join bangazon_api_order  on bangazon_api_order.id = op.order_id
where bangazon_api_order.completed_on != 'NULL'
order by product_id

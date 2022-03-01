select * from bangazon_api_orderproduct op
join bangazon_api_order  on bangazon_api_order.id = op.order_id
where bangazon_api_order.completed_on != 'NULL'
order by product_id


            select 
                bangazon_api_product.name as name,
                bangazon_api_product.price as price,
                bangazon_api_store.name as store
            from bangazon_api_product
            join bangazon_api_store on bangazon_api_store.id == bangazon_api_product.store_id
            where price >= 1000

update bangazon_api_product
set price = 1001.5
where id = 1 


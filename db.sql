select
    auth_user.id as customer_id,
    auth_user.first_name || " " || auth_user.last_name as customer,
    bangazon_api_store.name as store
from bangazon_api_favorite
join bangazon_api_store  on bangazon_api_store.id = bangazon_api_favorite.store_id
join auth_user on auth_user.id = bangazon_api_favorite.customer_id



\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY SellerInventories FROM 'SellerInventories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellerinventories_id_seq',
                         (SELECT MAX(id)+1 FROM SellerInventories),
                         false);
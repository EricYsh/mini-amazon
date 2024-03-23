\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);


\COPY Categories FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.categories_id_seq',
                         (SELECT MAX(id)+1 FROM Categories),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY SellerInventories FROM 'SellerInventories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellerinventories_id_seq',
                         (SELECT MAX(id)+1 FROM SellerInventories),
                         false);

\COPY PriceHistory FROM 'PriceHistory.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.pricehistory_id_seq',
                         (SELECT MAX(id)+1 FROM PriceHistory),
                         false);

\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.carts_id_seq',
                         (SELECT MAX(id)+1 FROM Carts),
                         false);

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_id_seq',
                         (SELECT MAX(id)+1 FROM Orders),
                         false);

\COPY OrderItems FROM 'OrderItems.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orderitems_id_seq',
                         (SELECT MAX(id)+1 FROM OrderItems),
                         false);

\COPY Coupons FROM 'Coupons.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.coupons_id_seq',
                         (SELECT MAX(id)+1 FROM Coupons),
                         false);

\COPY ProductComments FROM 'ProductComments.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.productcomments_id_seq',
                         (SELECT MAX(id)+1 FROM ProductComments),
                         false);
                         
\COPY SellerComments FROM 'SellerComments.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.sellercomments_id_seq',
                         (SELECT MAX(id)+1 FROM SellerComments),
                         false);


-- the below load will not be use in our implementation

-- \COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.purchases_id_seq',
--                          (SELECT MAX(id)+1 FROM Purchases),
--                          false);

-- \COPY Wishes FROM 'Wishes.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.wishes_id_seq',
--                          (SELECT MAX(id)+1 FROM Wishes),
--                          false);

/*
ID 	VIN 				Manufacturer 	Model 				Year 	Color
0 	3K096I98581DHSNUP 	Volkswagen 		Tiguan 				2019 	Blue
1 	ZM8G7BEUQZ97IH46V 	Peugeot 		Rifter 				2019 	Red
2 	RKXVNNIHLVVZOUB4M 	Ford 			Fusion 				2018 	White
3 	HKNDGS7CU31E9Z7JW 	Toyota 			RAV4 				2018 	Silver
4 	DAM41UDN3CHU2WVF6 	Volvo 			V60 				2019 	Gray
5 	DAM41UDN3CHU2WVF6 	Volvo 			V60 Cross Country 	2019 	Gray
*/

INSERT INTO cars (VIN,manufacturer,model,year,color)
VALUES
	('3K096I98581DHSNUP','Volkswagen','Tiguan','2019','Blue'),
	('ZM8G7BEUQZ97IH46V','Peugeot','Rifter','2019','Red'),
    ('RKXVNNIHLVVZOUB4M','Ford','Fusion','2018','White'),
    ('HKNDGS7CU31E9Z7JW','Toyota','RAV4','2018','Silver'),
    ('DAM41UDN3CHU2WVF6','Volvo','V60','2019','Gray'),
    ('DAM41UDN3CHU2WVF6','Volvo','V60 Cross Country','2019','Gray');

/*
Customer ID 	Name 	Phone 	Email 	Address 	City 	State/Province 	Country 	Postal
10001 	Pablo Picasso 	+34 636 17 63 82 	- 	Paseo de la Chopera, 14 	Madrid 	Madrid 	Spain 	28045
20001 	Abraham Lincoln 	+1 305 907 7086 	- 	120 SW 8th St 	Miami 	Florida 	United States 	33130
30001 	Napoléon Bonaparte 	+33 1 79 75 40 00 	- 	40 Rue du Colisée 	Paris 	Île-de-France 	France 	75008
*/

INSERT INTO customers(customer_id,name,phone,email,address,city,state_province,country,zip_postal)
VALUES
	(10001,'Pablo Picasso','+34 636 17 63 82',null,'Paseo de la Chopera, 14','Madrid','Madrid','Spain',28045),
	(20001,'Abraham Lincoln','+1 305 907 7086',null,'120 SW 8th St','Miami','Florida','United States',33130),
	(30001,'Napoléon Bonaparte','+33 1 79 75 40 00',null,'40 Rue du Colisée','Paris','Île-de-France','France',75008);


/*
ID 	Staff ID 	Name 	Store
0 	00001 	Petey Cruiser 	Madrid
1 	00002 	Anna Sthesia 	Barcelona
2 	00003 	Paul Molive 	Berlin
3 	00004 	Gail Forcewind 	Paris
4 	00005 	Paige Turner 	Mimia
5 	00006 	Bob Frapples 	Mexico City
6 	00007 	Walter Melon 	Amsterdam
7 	00008 	Shonda Leer 	São Paulo
*/

INSERT INTO salespersons(staff_id,name,store)
VALUES	
	(00001,'Petey Cruiser','Madrid'),
	(00002,'Anna Sthesia','Barcelona'),
	(00003,'Paul Molive','Berlin'),
	(00004,'Gail Forcewind','Paris'),
	(00005,'Paige Turner','Mimia'),
	(00006,'Bob Frapples','Mexico City'),
	(00007,'Walter Melon','Amsterdam'),
	(00008,'Shonda Leer','São Paulo');
    

/*
ID 	Invoice Number 	Date 	Car 	Customer 	Sales Person
0 	852399038 	22-08-2018 	0 	1 	3
1 	731166526 	31-12-2018 	3 	0 	5
2 	271135104 	22-01-2019 	2 	2 	7
*/

INSERT INTO invoices(invoice_id,invoice_date,car,customer,salesperson)
VALUES 
	(852399038,'2018-08-22',(SELECT car_id FROM cars WHERE car_id = 1),(SELECT customer_id from customers Where customer_id = 20001),(Select staff_id from salespersons where staff_id = 3)),
	(731166526,'2018-12-31',(SELECT car_id FROM cars WHERE car_id = 4),(SELECT customer_id from customers Where customer_id = 10001),(Select staff_id from salespersons where staff_id = 5)),
	(271135104,'2019-01-22',(SELECT car_id FROM cars WHERE car_id = 3),(SELECT customer_id from customers Where customer_id = 30001),(Select staff_id from salespersons where staff_id = 7));

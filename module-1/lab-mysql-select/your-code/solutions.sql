USE lab_mysql_select;

/*
SELECT * FROM authors;
SELECT* FROM publishers;
SELECT * FROM titles;
SELECT * FROM titleauthor;
SELECT * FROM sales;
*/

/*CHALLENGE 1*/
SELECT 
	a.au_id AS author_id,
    a.au_lname AS author_last_name,
    a.au_fname AS author_first_name,
    t.title AS title,
    p.pub_name AS publisher
FROM authors AS a
INNER JOIN titleauthor AS ta 
	ON a.au_id = ta.au_id
INNER JOIN titles AS t 
	ON ta.title_id = t.title_id
INNER JOIN publishers AS p 
	ON t.pub_id = p.pub_id;

/*CHALLENGE 2*/
SELECT 
	a.au_id AS author_id,
    a.au_lname AS author_last_name,
    a.au_fname AS author_first_name,
    p.pub_name AS publisher,
    COUNT(t.title) AS title_count
FROM authors AS a
INNER JOIN titleauthor AS ta 
	ON a.au_id = ta.au_id
INNER JOIN titles AS t 
	ON ta.title_id = t.title_id
INNER JOIN publishers AS p 
	ON t.pub_id = p.pub_id
GROUP BY a.au_id;


/*CHALENGE 3*/
SELECT 
	a.au_id AS author_id,
    a.au_lname AS author_last_name,
    a.au_fname AS author_first_name,
    SUM(s.qty) AS total
FROM authors AS a
INNER JOIN titleauthor AS ta 
	ON a.au_id = ta.au_id
INNER JOIN sales AS s
	ON ta.title_id = s.title_id
GROUP BY a.au_id
ORDER BY SUM(s.qty) DESC
LIMIT 3;

/*CHALLENGE 4*/
SELECT 
	a.au_id AS author_id,
    a.au_lname AS author_last_name,
    a.au_fname AS author_first_name,
    COALESCE(SUM(s.qty), 0 ) AS total
FROM authors AS a
LEFT JOIN titleauthor AS ta 
	ON a.au_id = ta.au_id
LEFT JOIN sales AS s
	ON ta.title_id = s.title_id
GROUP BY a.au_id
ORDER BY total DESC;
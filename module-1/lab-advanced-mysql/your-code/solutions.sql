use lab_mysql_select;

/*CHALLENGE 1*/
/*Getting a table of total sales per title*/
CREATE TEMPORARY TABLE title_sales
SELECT 
	s.title_id, 
	SUM(s.qty) AS total_qty,
	t.price, 
    SUM(s.qty)*t.price AS total_sales
FROM sales AS s
INNER JOIN titles AS t
	ON s.title_id = t.title_id
GROUP BY s.title_id;
    
SELECT * FROM title_sales;

/*Total royalty per title*/
CREATE TEMPORARY TABLE title_royalty
SELECT 
	r.title_id,
    r.royalty,
    ts.total_sales,
    r.royalty*ts.total_sales/100 AS total_royalty
FROM roysched AS r
INNER JOIN title_sales AS ts
	ON r.title_id = ts.title_id
WHERE 
	ts.total_sales >= r.lorange AND
    ts.total_sales <= r.hirange;
    
SELECT * FROM title_royalty;

/*Getting royalty plus advance for each title*/
CREATE TEMPORARY TABLE total_title_earnings 
SELECT 
	t.title_id, 
	tr.total_royalty,
    t.advance 
FROM title_royalty AS tr
INNER JOIN titles AS t
	ON tr.title_id = t.title_id;

SELECT * FROM total_title_earnings;

/*Total profits per author*/
CREATE TEMPORARY TABLE author_profits
SELECT
	au_id,
    SUM((total_royalty+advance)*royaltyper/100) AS author_profit
FROM titleauthor AS ta
INNER JOIN total_title_earnings AS tte
	ON ta.title_id = tte.title_id
GROUP BY au_id
ORDER BY author_profit DESC;


/*Final Result*/
SELECT 
	a.au_id, 
    au_lname,
    au_fname,
    author_profit
FROM author_profits AS ap
INNER JOIN authors AS a
	ON ap.au_id = a.au_id
ORDER BY author_profit DESC
LIMIT 3;
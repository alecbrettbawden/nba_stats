SELECT
	PLAYER_NAME
FROM
	(SELECT 
		PLAYER_NAME,
		(MIN*GP) AS TOTAL_MIN,
		RANK() OVER(ORDER BY MIN*GP DESC) AS rankings 
	FROM 
		dbo.nba_stats) temp
WHERE
	rankings = 3

select * from dbo.nba_stats
SELECT
	*
FROM

	(SELECT
		PLAYER_NAME,
		POSITION,
		RANK() OVER(PARTITION BY POSITION ORDER BY abs(AVG_FG3_PCT - overall_avg) DESC) AS ranking,
		abs(AVG_FG3_PCT - overall_avg) as difference_from_avg
	FROM
		(SELECT
			n.PLAYER_NAME,
			p.POSITION,
			(FG3A*GP) as PT_ATTEMPTS,
			AVG(FG3_PCT) as AVG_FG3_PCT
		FROM
			dbo.nba_stats n
			join
			dbo.player_indexes p on n.PLAYER_ID = p.PERSON_ID
		GROUP BY
			n.PLAYER_NAME,
			p.POSITION,
			(FG3A*GP)
		HAVING
			(FG3A*GP) >= 20) temp
	CROSS JOIN
	(SELECT
		AVG(FG3_PCT) as overall_avg
	FROM
		dbo.nba_stats n
	WHERE
		(FG3A*GP) >= 20) avg_table) temp2
WHERE
	ranking = 1
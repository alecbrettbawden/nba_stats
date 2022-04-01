SELECT TOP 1
	TEAM_ABBREVIATION
FROM
	dbo.nba_stats
GROUP BY
	TEAM_ABBREVIATION
ORDER BY
	SUM(AST*GP) DESC
WITH team (name, total_points)
AS
(SELECT
	TEAM_ABBREVIATION,
	SUM(PTS*GP)
 FROM
	dbo.nba_stats
 GROUP BY
	TEAM_ABBREVIATION),
players (name, team, total_points, ranking)
AS
(SELECT
	*
 FROM
	(SELECT
		PLAYER_NAME,
		TEAM_ABBREVIATION,
		total_points,
		RANK() OVER(PARTITION BY TEAM_ABBREVIATION ORDER BY total_points DESC) ranking
	 FROM
		(SELECT
			PLAYER_NAME,
			TEAM_ABBREVIATION,
			SUM(PTS*GP) as total_points
		 FROM
			dbo.nba_stats
		 GROUP BY
			PLAYER_NAME,
			TEAM_ABBREVIATION) temp) temp2
 WHERE ranking = 1),
point_percentage_cte (player, team,point_percentage)
AS
 (SELECT 
	p.name,
	p.team,
	(p.total_points / t.total_points) AS point_percent
  FROM 
	players p
	JOIN
	team t ON p.team = t.name)

SELECT TOP 1
	* 
FROM 
	point_percentage_cte
ORDER BY
	point_percentage DESC

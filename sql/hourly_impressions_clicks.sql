SELECT
        toDate(created_at) AS date,
        toHour(created_at) AS hour,
        COUNTIf(event = 'impression') AS impressions,
        COUNTIf(event = 'click') AS clicks
    FROM (
        SELECT created_at, 'impression' AS event FROM impressions
        UNION ALL
        SELECT created_at, 'click' AS event FROM clicks
    )
    GROUP BY date, hour
    ORDER BY 4 desc
    limit 30
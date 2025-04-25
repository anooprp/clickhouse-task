SELECT
    c.id AS campaign_id,
    c.name AS campaign_name,
    toDate(i.created_at) AS date,
    countDistinct(i.id) AS daily_impressions,
    countDistinct(cl.id) AS daily_clicks
FROM campaign c
LEFT JOIN impressions i ON c.id = i.campaign_id
LEFT JOIN clicks cl
    ON cl.campaign_id = c.id
    AND toDate(cl.created_at) = toDate(i.created_at)
GROUP BY
    c.id,
    c.name,
    toDate(i.created_at)
ORDER BY
    c.id,
    date
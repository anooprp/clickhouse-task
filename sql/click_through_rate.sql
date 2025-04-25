SELECT
    c.id AS campaign_id,
    c.name AS campaign_name,
    a.name AS advertiser_name,
    COUNT(DISTINCT i.id) AS impressions,
    COUNT(DISTINCT cl.id) AS clicks,
    ROUND(
        CASE
            WHEN COUNT(DISTINCT i.id) = 0 THEN 0
            ELSE (COUNT(DISTINCT cl.id) * 100.0 / COUNT(DISTINCT i.id))
        END,
        2
    ) AS ctr
FROM campaign c
JOIN advertiser a ON c.advertiser_id = a.id
LEFT JOIN impressions i ON c.id = i.campaign_id
LEFT JOIN clicks cl ON c.id = cl.campaign_id
GROUP BY c.id, c.name, a.name
ORDER BY c.id
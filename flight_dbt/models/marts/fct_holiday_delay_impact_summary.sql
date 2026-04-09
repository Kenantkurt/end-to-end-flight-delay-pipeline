SELECT 
CASE 
WHEN holiday_name is not null then 1
else 0
END AS is_holiday,
COUNT(*) AS total_flights,
COUNTIF(departure_delay > 15) AS delayed_flights,
ROUND(SAFE_DIVIDE(COUNTIF(departure_delay > 15),
COUNT(*)),3) AS delay_rate
FROM {{ref('enriched_flights')}}
WHERE is_cancelled IS FALSE 
AND is_diverted IS FALSE
GROUP BY is_holiday
ORDER BY delay_rate DESC

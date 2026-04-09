SELECT 
CASE 
WHEN total_rain_mm > 0 OR total_snowfall_mm > 0 THEN 'bad_weather'
ELSE 'good_weather'
END AS weather_condition,
COUNT(*) AS total_flights,
COUNTIF(departure_delay > 15) AS delayed_flights,
ROUND(SAFE_DIVIDE(COUNTIF(departure_delay > 15),
COUNT(*)),3) AS delay_rate
FROM {{ref('enriched_flights')}}
WHERE is_cancelled IS FALSE 
AND is_diverted IS FALSE
GROUP BY weather_condition
ORDER BY delay_rate DESC
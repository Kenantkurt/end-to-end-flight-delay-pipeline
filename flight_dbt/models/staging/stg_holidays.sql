SELECT 
    DATE(date) AS date,
    holiday_name
FROM {{ source('flight_data', 'holidays') }}
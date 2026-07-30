-- ============================================================
-- Tabloları temizle (yeniden çalıştırılabilirlik için)
-- Not: FK bağımlılığı nedeniyle önce weather_data, sonra status_types
-- ============================================================
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE weather_data;
TRUNCATE TABLE status_types;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- status_types tablosuna veri yükleme
-- CSV sütun sırası: summary, precip_type, status_id
-- ============================================================
LOAD DATA LOCAL INFILE 'C:/statusTypes.csv'
INTO TABLE status_types
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(summary, precip_type, status_id);

-- ============================================================
-- weather_data tablosuna veri yükleme
-- CSV sütun sırası: formatted_date, temperature_c, apparent_temperature_c,
-- humidity, wind_speed_kmh, wind_bearing_degrees, visibility_km,
-- pressure_millibars, daily_summary, year, month, day, status_id
-- ============================================================
LOAD DATA LOCAL INFILE 'C:/lastWeatherHistory.csv'
INTO TABLE weather_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(formatted_date, temperature_c, apparent_temperature_c, humidity, wind_speed_kmh, wind_bearing_degrees, visibility_km, pressure_millibars, daily_summary, year, month, day, status_id);

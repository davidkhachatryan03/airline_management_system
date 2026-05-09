USE airline;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE routes;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO routes (flight_number, origin, destination, distance_km, duration_min) VALUES 
    ('AR1240', 'AEP', 'COR', 646, 85),
    ('AR1241', 'COR', 'AEP', 646, 85),
    ('AR1432', 'AEP', 'MDZ', 984, 110),
    ('AR1433', 'MDZ', 'AEP', 984, 110),
    ('AR1870', 'AEP', 'BRC', 1316, 140),
    ('AR1871', 'BRC', 'AEP', 1316, 140),
    ('AR2840', 'AEP', 'USH', 2380, 215),
    ('AR2841', 'USH', 'AEP', 2380, 215),
    ('AR1530', 'AEP', 'IGR', 1050, 105),
    ('AR1531', 'IGR', 'AEP', 1050, 105),
    ('LA2350', 'SCL', 'AEP', 1140, 130),
    ('LA2351', 'AEP', 'SCL', 1140, 130),
    ('LA3122', 'AEP', 'GRU', 1700, 165),
    ('LA3123', 'GRU', 'AEP', 1700, 165),
    ('LA4500', 'LIM', 'AEP', 3150, 245),
    ('LA4501', 'AEP', 'LIM', 3150, 245),
    ('AV9340', 'BOG', 'AEP', 4600, 370),
    ('AV9341', 'AEP', 'BOG', 4600, 370),
    ('AF7652', 'GIG', 'AEP', 1980, 190),
    ('AF7653', 'AEP', 'GIG', 1980, 190),
    ('AA1142', 'MIA', 'AEP', 7100, 540),
    ('AA1143', 'AEP', 'MIA', 7100, 540),
    ('IB3106', 'AEP', 'MAD', 10050, 750),
    ('IB3107', 'MAD', 'AEP', 10050, 750),
    ('LH0120', 'FRA', 'AEP', 11500, 820),
    ('LH0121', 'AEP', 'FRA', 11500, 820),
    ('AM0120', 'MEX', 'AEP', 7400, 580),
    ('AM0121', 'AEP', 'MEX', 7400, 580),
    ('AF0412', 'AEP', 'CDG', 11100, 790),
    ('AF0413', 'CDG', 'AEP', 11100, 790);
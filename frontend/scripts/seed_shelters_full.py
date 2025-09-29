# scripts/seed_shelters_full.py
import boto3, os, time
from backend.app.core.config import AWSREGION, SHELTER_TABLE

d = boto3.resource("dynamodb", region_name=AWSREGION)
table = d.Table(SHELTER_TABLE)

seed = [
{"id":"s-ondo-001","name":"Ondo Central School Shelter","address":"Ondo Town","lat":7.0966,"lng":5.1050,"capacity":250,"type":"school","contact":"+234801000001","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-002","name":"Ifon Community Center","address":"Ifon","lat":6.8578,"lng":4.9833,"capacity":150,"type":"community_center","contact":"+234801000002","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-003","name":"Akure East Shelter","address":"Akure","lat":7.2500,"lng":5.2000,"capacity":300,"type":"school","contact":"+234801000003","radius_m":600,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-004","name":"Ondo State Hospital Annex","address":"Ondo Town","lat":7.1005,"lng":5.1301,"capacity":120,"type":"clinic","contact":"+234801000004","radius_m":400,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-005","name":"Okitipupa Civic Hall","address":"Okitipupa","lat":6.8423,"lng":4.7948,"capacity":200,"type":"community_center","contact":"+234801000005","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-006","name":"Irele School Shelter","address":"Irele","lat":6.7000,"lng":4.8333,"capacity":180,"type":"school","contact":"+234801000006","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-007","name":"Owo Town Hall Shelter","address":"Owo","lat":7.2000,"lng":5.6667,"capacity":220,"type":"community_center","contact":"+234801000007","radius_m":600,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-008","name":"Idanre Safe Shelter","address":"Idanre","lat":7.1186,"lng":5.0739,"capacity":140,"type":"school","contact":"+234801000008","radius_m":400,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-009","name":"Akure North Hall","address":"Akure","lat":7.2900,"lng":5.1800,"capacity":160,"type":"community_center","contact":"+234801000009","radius_m":400,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-010","name":"Ikare-Akoko Shelter","address":"Ikare-Akoko","lat":7.4745,"lng":5.9556,"capacity":200,"type":"school","contact":"+234801000010","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-011","name":"Ese-Odo School Shelter","address":"Ese-Odo","lat":6.5556,"lng":4.7981,"capacity":130,"type":"school","contact":"+234801000011","radius_m":400,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-012","name":"Akoko North Refuge","address":"Akoko North","lat":7.6000,"lng":5.7000,"capacity":180,"type":"community_center","contact":"+234801000012","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-013","name":"Ondo East Shelter","address":"Ondo East","lat":7.0500,"lng":5.1250,"capacity":210,"type":"school","contact":"+234801000013","radius_m":500,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-014","name":"Akure Central Clinic","address":"Akure","lat":7.2560,"lng":5.1910,"capacity":100,"type":"clinic","contact":"+234801000014","radius_m":350,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-015","name":"Odigbo Relief Centre","address":"Odigbo","lat":6.9667,"lng":4.9333,"capacity":170,"type":"community_center","contact":"+234801000015","radius_m":450,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-016","name":"Igbotako Shelter","address":"Igbotako","lat":6.6200,"lng":4.7800,"capacity":120,"type":"school","contact":"+234801000016","radius_m":400,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-017","name":"Oda Shelter Hub","address":"Oda","lat":7.0200,"lng":5.1000,"capacity":150,"type":"community_center","contact":"+234801000017","radius_m":400,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-018","name":"Ikare Clinic Shelter","address":"Ikare","lat":7.4770,"lng":5.9560,"capacity":110,"type":"clinic","contact":"+234801000018","radius_m":350,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-019","name":"Ile-Oluji Relief Point","address":"Ile-Oluji","lat":7.3333,"lng":5.1333,"capacity":140,"type":"community_center","contact":"+234801000019","radius_m":450,"last_updated":"2025-09-29T00:00:00Z"},
{"id":"s-ondo-020","name":"Irele Safe School","address":"Irele","lat":6.7250,"lng":4.8450,"capacity":160,"type":"school","contact":"+234801000020","radius_m":450,"last_updated":"2025-09-29T00:00:00Z"}
]

for it in seed:
    table.put_item(Item=it)
print(f"Seeded {len(seed)} shelters to {SHELTER_TABLE}")

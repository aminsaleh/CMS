curl -X POST http://localhost:8000/courier/ -H "Content-Type: application/json" -d '{"national_id": "0123456789", "name": "amin"}'
curl -X POST http://localhost:8000/customer/ -H "Content-Type: application/json" -d '{"name": "restaurant", "type": 2}'

curl -X POST http://localhost:8000/ride/ -H "Content-Type: application/json" -d '{"ride_distance": 100, "courier_distance": 8, "customer": "restaurant", "price": 10000}'
curl -X POST http://localhost:8000/bonus/ -H "Content-Type: application/json" -d '{"courier_national_id": "0123456789", "amount": 10000}'
curl -X POST http://localhost:8000/penalty/ -H "Content-Type: application/json" -d '{"courier_national_id": "0123456789", "amount": 5000}'

curl -X GET http://localhost:8000/dailyincome/ -H "Content-Type: application/json" -d '{"national_id": "0123456789", "date": "2022/6/9"}'
curl -X GET http://localhost:8000/weekldyincome/ -H "Content-Type: application/json" -d '{"national_id": "0123456789", "from_date": "2022/6/1", "to_date": "2022/6/10"}'

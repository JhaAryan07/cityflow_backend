def test_me(client):
    response = client.get('/api/v1/me')
    assert response.status_code == 200
    assert response.json()['email'] == 'demo@cityflow.local'


def test_vehicle_crud(client):
    payload = {
        'name': 'Test Truck', 'vehicle_type': 'Truck',
        'height_m': 3.4, 'width_m': 2.4, 'length_m': 8.0, 'weight_t': 9.0,
    }
    created = client.post('/api/v1/vehicles', json=payload)
    assert created.status_code == 201
    vehicle_id = created.json()['id']
    assert client.get('/api/v1/vehicles').status_code == 200
    updated = client.patch(f'/api/v1/vehicles/{vehicle_id}', json={'name': 'Updated Truck'})
    assert updated.status_code == 200
    assert updated.json()['name'] == 'Updated Truck'
    deleted = client.delete(f'/api/v1/vehicles/{vehicle_id}')
    assert deleted.status_code == 200
    assert deleted.json()['deleted'] is True


def test_saved_route_and_preferences(client):
    saved = client.post('/api/v1/routes/saved', json={
        'name': 'Office', 'origin': 'A', 'destination': 'B', 'preference': 'fit'
    })
    assert saved.status_code == 201
    routes = client.get('/api/v1/routes/saved')
    assert routes.status_code == 200
    assert routes.json()[0]['name'] == 'Office'

    prefs = client.put('/api/v1/preferences', json={'preferred_route_type': 'emission', 'units': 'metric'})
    assert prefs.status_code == 200
    assert prefs.json()['preferred_route_type'] == 'emission'


def test_network_transit_weather_prediction_safety(client):
    network = client.get('/api/v1/network?city=delhi')
    assert network.status_code == 200
    assert network.json()['city'] == 'delhi'
    assert network.json()['traffic']
    assert network.json()['safety']

    transit = client.get('/api/v1/transit?city=delhi')
    assert transit.status_code == 200
    assert transit.json()['airports']

    weather = client.get('/api/v1/weather?city=delhi')
    assert weather.status_code == 200
    assert weather.json()['aqi'] == 112

    prediction = client.get('/api/v1/predictions/traffic?city=delhi&horizon=30')
    assert prediction.status_code == 200
    assert prediction.json()['source'] == 'MODEL_PLACEHOLDER'

    safety = client.get('/api/v1/safety?city=delhi&time_of_day=night')
    assert safety.status_code == 200
    assert safety.json()['source'] == 'MODELLED_HISTORICAL'


def test_route_validation_and_different_vehicle_output(client):
    car = {
        'origin': 'A', 'destination': 'B',
        'vehicle': {'vehicle_type': 'Car', 'height_m': 1.7, 'width_m': 1.9, 'length_m': 4.5, 'weight_t': 1.6},
        'preference': 'balanced',
    }
    truck = {
        **car,
        'vehicle': {'vehicle_type': 'Truck', 'height_m': 3.8, 'width_m': 2.5, 'length_m': 8.0, 'weight_t': 12.0},
    }
    a = client.post('/api/v1/routes/vehicle', json=car)
    b = client.post('/api/v1/routes/vehicle', json=truck)
    assert a.status_code == 200 and b.status_code == 200
    assert a.json()[0]['duration_min'] != b.json()[0]['duration_min']
    assert b.json()[0]['restrictions']

    bad = client.post('/api/v1/routes/vehicle', json={**car, 'vehicle': {**car['vehicle'], 'height_m': -1}})
    assert bad.status_code == 422


def test_transit_journey(client):
    response = client.post('/api/v1/transit/journey', json={
        'origin': 'New Delhi Railway Station',
        'destination': 'Noida International Airport',
        'mode': 'mixed',
    })
    assert response.status_code == 200
    assert response.json()[0]['legs']
    assert 'geometry' in response.json()[0]


def test_incident_create_and_authority_protection(client):
    created = client.post('/api/v1/incidents', json={
        'type': 'Obstruction', 'road': 'Test Road', 'severity': 'Low', 'impact': 'Low', 'latitude': 28.6, 'longitude': 77.2,
    })
    assert created.status_code == 201
    assert created.json()['status'] == 'REPORTED'

    forbidden = client.patch('/api/v1/incidents/i1', json={'status': 'VERIFIED'})
    assert forbidden.status_code == 403

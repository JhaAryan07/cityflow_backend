import pytest

from app.providers.mock.providers import MockRoutingProvider, MockTransitProvider


@pytest.mark.asyncio
async def test_route_differs_by_vehicle():
    provider = MockRoutingProvider()
    car = {'vehicle_type': 'Car', 'height_m': 1.7, 'width_m': 1.9, 'length_m': 4.5, 'weight_t': 1.6}
    truck = {'vehicle_type': 'Truck', 'height_m': 3.8, 'width_m': 2.5, 'length_m': 8, 'weight_t': 12}
    car_options = await provider.get_route({'vehicle': car, 'preference': 'balanced'})
    truck_options = await provider.get_route({'vehicle': truck, 'preference': 'balanced'})
    assert car_options[0]['duration_min'] != truck_options[0]['duration_min']
    assert truck_options[0]['restrictions']


@pytest.mark.asyncio
async def test_transit_modes():
    provider = MockTransitProvider()
    metro = await provider.plan_journey({'origin': 'A', 'destination': 'B', 'mode': 'metro'})
    rail = await provider.plan_journey({'origin': 'A', 'destination': 'B', 'mode': 'rail'})
    assert metro and rail and metro[0]['mode'] != rail[0]['mode']

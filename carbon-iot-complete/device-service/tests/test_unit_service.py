from app.schemas import DeviceCreate

def test_device_schema_validation():
    dc = DeviceCreate(name='s1', type='temp', location='lab')
    assert dc.name == 's1'

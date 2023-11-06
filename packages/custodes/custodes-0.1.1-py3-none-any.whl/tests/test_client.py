from custodes.client import post
import asyncio


def test_post_api():
    asyncio.run(post(service_name='test', status={'code': 0, 'message': 'OK'},
                     expire=120))

    asyncio.run(post(service_name='test', status={'code': 0, 'message': 'OK'},
                     expire=120, loop=False))

    resp = asyncio.run(post(service_name='test', status={'code': 0, 'message': 'Do not go gentle into that good night'},
                     expire=86400, sleep_period=0.1, loop=False))
    assert resp != ''

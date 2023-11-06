from custodes.server import generate_summary, _sync_status
import asyncio


def test_post():
    message1 = {
        'service_name': 'pytest',
        'status': {
            'code': 0,
            'message': 'OK'
        },
        'datetime': '2029-08-01 12:00:00',
        'ipinfo': 'ip'
    }
    message2 = {
        'service_name': 'pytest-2',
        'status': {
            'code': 1,
            'message': 'Error'
        },
        'datetime': '2021-08-01 12:00:00',
        'ipinfo': 'ip'
    }
    asyncio.run(_sync_status(str(message1).encode()))
    asyncio.run(_sync_status(str(message2).encode()))
    summary = asyncio.run(generate_summary())
    assert isinstance(summary, list)
    assert len(summary) == 2
    assert summary[0]['service_name'] == 'pytest'
    assert summary[0]['is_okay'] == True

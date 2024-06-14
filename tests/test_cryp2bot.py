"""Imoprt the cryp2bot function from the cryp2bot module and test it."""
from cryp2bot.cryp2bot import cryp2bot


def test_cryp2bot():
    """Test the cryp2bot function."""
    assert cryp2bot() is True

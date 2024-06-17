"""Imoprt the cryp2bot function from the cryp2bot module and test it."""
from cryp2bot.cryp2bot import usecryp2bot


def test_cryp2bot():
    """Test the cryp2bot function."""
    assert usecryp2bot(2, 2) == 4
    assert usecryp2bot(2, 3) == 5
    assert usecryp2bot(2, 4) == 6

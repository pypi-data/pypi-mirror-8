from colormap import get_cmap


def test_get_cmap():
    get_cmap("heat")
    get_cmap("heat_r")
    get_cmap("spectral")
    get_cmap("red_black_blue")
    try:
        get_cmap('dummy')
        assert False
    except:
        assert True

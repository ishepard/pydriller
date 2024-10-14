import mock
import pytest
from pydriller.domain.developer import Developer
from pydriller.utils.mailmap import DefaultDeveloperFactory, MailmapDeveloperFactory
from subprocess import CompletedProcess


def test_default_dev_factory():
    name, email = "Davide", "s.d@gmail.com"
    d1 = Developer(name, email)
    dev_factory = DefaultDeveloperFactory()

    d2 = dev_factory.get_developer(name, email)

    assert d1 == d2


config = {"path_to_repo": "test-repos/contentmine_mailmap"}
testdata = [
    (config, "My Name", "tarrow@users.noreply.github.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (config, "Thomas Arrow", "thomasarrow@gmail.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (config, "Sam Pablo Kuper", "sampablokuper@uclmail.net", Developer("Sam Pablo Kuper", "sampablokuper@uclmail.net")),
    (config, "Davide", "s.d@gmail.com", Developer("Davide", "s.d@gmail.com")),
]


@pytest.mark.parametrize("conf,name,email,expected", testdata)
def test_mailmap_dev_factory_wo_caching(conf, name, email, expected):
    dev_factory = MailmapDeveloperFactory(conf)

    d = dev_factory.get_developer(name, email)

    assert d == expected


dev_factory = MailmapDeveloperFactory(config)
testdata2 = [
    (dev_factory, "My Name", "tarrow@users.noreply.github.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (dev_factory, "Thomas Arrow", "thomasarrow@gmail.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (dev_factory, "My Name", "tarrow@users.noreply.github.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (dev_factory, "Thomas Arrow", "thomasarrow@gmail.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (dev_factory, "Sam Pablo Kuper", "sampablokuper@uclmail.net", Developer("Sam Pablo Kuper", "sampablokuper@uclmail.net")),
    (dev_factory, "Davide", "s.d@gmail.com", Developer("Davide", "s.d@gmail.com")),
    (dev_factory, "", "sampablokuper@uclmail.net", Developer("", "sampablokuper@uclmail.net")),
]


@pytest.mark.parametrize("dev_factory,name,email,expected", testdata2)
def test_mailmap_dev_factory_with_caching(dev_factory, name, email, expected):
    d = dev_factory.get_developer(name, email)

    assert d == expected


dev_factory = MailmapDeveloperFactory(config)
testdata3 = [
    (dev_factory, "My Name", "tarrow@users.noreply.github.com", Developer("My Name", "tarrow@users.noreply.github.com")),
    (dev_factory, "Thomas Arrow", "thomasarrow@gmail.com", Developer("Thomas Arrow", "thomasarrow@gmail.com")),
    (dev_factory, "Sam Pablo Kuper", "sampablokuper@uclmail.net", Developer("Sam Pablo Kuper", "sampablokuper@uclmail.net")),
    (dev_factory, "Davide", "s.d@gmail.com", Developer("Davide", "s.d@gmail.com")),
]


@pytest.mark.parametrize("dev_factory,name,email,expected", testdata3)
def test_mailmap_dev_factory_with_caching_raise_exception(dev_factory, name, email, expected):

    with mock.patch.object(dev_factory, "_run_check_mailmap",  side_effect=Exception("ERROR")):
        d = dev_factory.get_developer(name, email)

        assert d == expected


@pytest.mark.parametrize("dev_factory,name,email,expected", testdata3)
def test_mailmap_dev_factory_with_caching_stderr(dev_factory, name, email, expected):

    mock_result = CompletedProcess("", 123)
    mock_result.stderr = "fatal: ..."

    with mock.patch("subprocess.run",  return_value=mock_result):
        d = dev_factory.get_developer(name, email)

        assert d == expected

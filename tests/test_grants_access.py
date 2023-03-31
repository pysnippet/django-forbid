from django_forbid.access import grants_access


def test():
    # Run without any configuration, should be allowed
    assert grants_access("127.0.0.1")

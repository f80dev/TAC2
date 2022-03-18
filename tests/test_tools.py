from tools import Tools

t = Tools(subdir=".")

def test_translate():
    t.add_to_translate_dict("bonjour", "hello", "en-US")
    assert t.translate("##bonjour", "en-US", "fr-FR") == "hello"
    assert t.translate("!!bonjour", "en-US", "fr-FR") == "hello"
    assert t.translate("$$bonjour", "en-US", "fr-FR") == "bonjour"
    assert t.translate("bonjour", "en-US", "fr-FR") == "hello"
    assert t.translate("bonjour", "en-US") == "hello"


def test_speak():
    pass

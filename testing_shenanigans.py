def test_len_str():
    print(len('window["ytInitialData"] = '))


def test_extract():
    target = 'var ytInitialData = {"resp'
    print(len(target))

if __name__ == "__main__":
    test_len_str()
    test_extract()
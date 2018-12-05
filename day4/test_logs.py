from logs import Logger

def test_1():
    logger = Logger()
    input = ["[1518-11-01 00:00] Guard #10 begins shift",
             "[1518-11-01 00:05] falls asleep"]
    logger.parse(input)
    guards = logger.guard_list()
    assert logger.last().isoformat(' ','minutes') == "1518-11-01 00:05"
    assert guards == ['10']
    
def test_2():
    logger = Logger()
    input = open("test1.txt", "r")
    logger.parse(input)
    guards = logger.guard_list()
    assert logger.last().isoformat(' ','minutes') == "1518-11-05 00:55"
    assert guards == ['10','99']
    assert logger.guard_sleep(10) == 50
    assert logger.guard_sleep(99) == 30
    (long_min, freq_min) = logger.find_minute(10)
    assert long_min == 24
    (long_min, freq_min) = logger.find_minute(99)
    assert freq_min == 45
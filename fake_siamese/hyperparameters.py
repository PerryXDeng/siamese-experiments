LEARNING_RATE = 0.1
REG_CONST = 1
NUMERICAL_DELTA = 0.0001
SAMPLE_SIZE = 200
FEATURE_SIZE = 5
JOINED_NET = [3, 2, 1]
JOINED_L = len(JOINED_NET)
TWIN_NET = [FEATURE_SIZE, 4, JOINED_NET[0]]
TWIN_L = len(TWIN_NET)

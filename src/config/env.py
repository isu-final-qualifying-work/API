from environs import Env

env = Env()
env.read_env()

DICT_ENVS = {}

DICT_ENVS["BASE_IP"] = env.str("BASE_IP")
DICT_ENVS["BASE_PORT"] = env.int("BASE_PORT")

DICT_ENVS["USER_NAME"] = env.str("USER_NAME")
DICT_ENVS["USER_PASS"] = env.str("USER_PASS")

DICT_ENVS["DB_NAME"] = env.str("DB_NAME")
import sys
import create_pool

# ! Так как формула уровней в геншине еще неизвестна,
# ! пока что у каждого уровня будет определенное
# ! количество exp
rank_levels_exp = {
    1: 0,
    2: 375,
    3: 875,
    4: 1500,
    5: 2225,
    6: 3075,
    7: 4025,
    8: 5100,
    9: 6275,
    10: 7575,
    11: 9000,
    12: 10525,
    13: 12175,
    14: 13950,
    15: 15825,
    16: 17825,
    17: 20200,
    18: 22700,
    19: 25325,
    20: 28100,
    21: 30925,
    22: 34350,
    23: 38075,
    24: 42075,
    25: 46375,
    26: 50950,
    27: 55825,
    28: 60975,
    29: 66425,
    30: 72150,
    31: 78175,
    32: 84475,
    33: 91075,
    34: 97975,
    35: 105150,
    36: 112625,
    37: 120375,
    38: 128425,
    39: 136750,
    40: 145375,
    41: 155925,
    42: 167450,
    43: 179925,
    44: 193375,
    45: 207775,
    46: 223125,
    47: 239450,
    48: 256725,
    49: 274975,
    50: 294175,
    51: 320575,
    52: 349375,
    53: 380575,
    54: 414175,
    55: 450175,
    56: 682525,
    57: 941475,
    58: 1227225,
    59: 1540050,
    60: 1880175,
}


def exp_to_level(exp: int):
    # ? Уверен, что это можно было сделать лучше, сейчас
    # ? здесь вариант, сгенерированный github copilot
    for level, exp_to_level in rank_levels_exp.items():
        if exp < exp_to_level:
            return level-1
    return 60


async def give_exp(new_exp: int, user_id: int, peer_id: int):
    pool = create_pool.pool
    async with pool.acquire() as pool:
        exp = await pool.fetchrow(
            "SELECT experience FROM players WHERE user_id=$1 AND peer_id=$2",
            user_id, peer_id
        )
        if exp_to_level(exp["experience"]) < 60:
            await pool.execute(
                "UPDATE players SET experience=experience+$1 WHERE user_id=$2 AND peer_id=$3",
                new_exp, user_id, peer_id
            )

        if exp["experience"] > rank_levels_exp[60]:
            await pool.execute(
                "UPDATE players SET experience=$1 WHERE user_id=$2 AND peer_id=$3",
                rank_levels_exp[60], user_id, peer_id
            )


def get_default_header():
    python_version = sys.version_info

    return {
        "User-Agent": "Genshin-Impact-VK-Bot/{version} (Python {major}.{minor}.{micro})".format(
            version=0.1,
            major=python_version.major,
            minor=python_version.minor,
            micro=python_version.micro
        )
    }

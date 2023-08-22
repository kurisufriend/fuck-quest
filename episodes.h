#pragma once
#include <string>
#include "lib/sqlite/sqlite3.h"
#include "lib/sqleasy/sqleasy.h"
namespace episodes
{
    std::string make_episodes_for_season(sqlite3* db, int season);
    std::string make_episode_list(sqlite3* db, bool cach = true);
}
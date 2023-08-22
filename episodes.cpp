#include <iostream>
#include "episodes.h"
#include "lib/dumbstr/dumbstr.h"

std::string episodes::make_episodes_for_season(sqlite3* db, int season)
{
    std::string acc = "";
    rows eps = 
        sqleasy_q{db, dfmt({"select * from episode_assignments where number=", std::to_string(season), " order by thread asc;"})}.exec();
    foreach (eps, ep)
    {
        acc.append(dfmt({"<a href='/fq/", (*ep)["thread"], "'>", (*ep)["title"], "</a><br>"}));
    }
    return acc;
}

std::string episodes::make_episode_list(sqlite3* db, bool cach)
{
    std::string acc = "";
    static std::string cache;
    if (!(cache.empty()) && cach)
        return cache;
    rows seas = 
        sqleasy_q{db, dfmt({"select * from seasons order by number asc;"})}.exec();

    foreach (seas, sea)
    {
        acc.append(dumbfmt_file("./static/template/episode.html", {
            {"title", (*sea)["title"]},
            {"number", (*sea)["number"]},
            {"content", make_episodes_for_season(db, std::stoi((*sea)["number"]))}
        }));
    }

    cache = acc;
    return acc;
}
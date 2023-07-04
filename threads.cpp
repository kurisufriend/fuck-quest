#include "threads.h"
#include "lib/dumbstr/dumbstr.h"
#include "lib/sqleasy/sqleasy.h"
#include <string>
#include <iostream>
#include <regex>
#include <utility>

std::string threads::make_post(sqlite3* db, row data, bool reader_mode)
{
    bool is_op = data["is_op_studios"] == "1";
    int prev_op_studios_int = std::stoi(data["prev_op_studios"]);
    int prev_op = std::stoi(data["prev_op"]);
    int next_op_studios_int = std::stoi(data["next_op_studios"]);
    int op_no_int = std::stoi(data["op_no"]);
    int thread_ender = op_no_int+std::stoi(data["reply_count"]);
    std::map<std::string, std::string> nav_block = {
        {"prev_op", dumbfmt({(prev_op_studios_int >= op_no_int) ? "#" : dumbfmt({"/fq/", std::to_string(prev_op), "#"}), data["prev_op_studios"]})},
        {"next_op", dumbfmt({(next_op_studios_int <= thread_ender) ? "#" : dumbfmt({"/fq/", std::to_string(thread_ender+1), "#"}), data["next_op_studios"]})}
    };
    time_t ti = (time_t)std::stoi(data["tim"]);
    return dumbfmt_file("./static/template/post.html", {
        {"no", data["post_number"]},
        {"subject", data["subject"]},
        {"name", (data["name"] == "Anonymous" && data["trip"] != "") ? "" : data["name"]},
        {"trip", data["trip"]},
        {"posterid", (data["usr_id"] == "000000") ? "" : dumbfmt({"ID: ", data["usr_id"]})},
        {"date", ctime(&ti)},
        {"body", dumbfmt_replace("[realquoterep]", "\"", data["bod"])},

        {"markers", dumbfmt({(data["is_ghost"] == "1") ? "<img src='/imgs/prof-ghost.png' title='ghost post!'></img>" : "", (data["is_story"] == "1") ? "<img src='/imgs/prof-story.png' title='story post!'></img>" : ""})},
    
        {"nav-top", (is_op && !reader_mode) ? dumbfmt_file("./static/template/navigator.html", nav_block) : ""},
        {"nav-bottom", (is_op && !reader_mode) ? dumbfmt_file("./static/template/navigator.html", nav_block) : ""},

        {"specials", is_op ? "op-studios" : ""}
        
    });
}

std::string threads::make_thread(sqlite3* db, int op_id, bool reader_mode, bool cach)
{
    std::string acc = "";
    static std::map<std::pair<int, bool>, std::string> cache;
    if (cache.find(std::make_pair(op_id, reader_mode)) != cache.end() && cach)
        return cache.at(std::make_pair(op_id, reader_mode));
    rows posts = 
        sqleasy_q{db, dfmt({"select * from posts where op_no=", std::to_string(op_id), " order by post_number asc;"})}.exec();
    foreach (posts, post)
    {
        if (reader_mode && (*post)["is_story"] != "1") {continue;}
        acc.append(threads::make_post(db, *post, reader_mode));
    }
    cache.emplace(std::make_pair(op_id, reader_mode), acc);
    return acc;
}
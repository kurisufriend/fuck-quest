#include "threads.h"
#include "lib/dumbstr/dumbstr.h"
#include "lib/sqleasy/sqleasy.h"
#include <string>
#include <iostream>
#include <regex>

std::string threads::make_post(sqlite3* db, row data)
{
    bool is_op = data["is_op_studios"] == "1";
    int prev_op_studios_int = std::stoi(data["prev_op_studios"]);
    int next_op_studios_int = std::stoi(data["next_op_studios"]);
    int op_no_int = std::stoi(data["op_no"]);
    int thread_ender = op_no_int+std::stoi(data["reply_count"]);
    std::map<std::string, std::string> nav_block = {
        {"prev_op", dumbfmt({"#", data["prev_op_studios"]})},
        {"next_op", dumbfmt({(next_op_studios_int <= thread_ender) ? "#" : dumbfmt({"/fq/", std::to_string(thread_ender+1), "#"}), data["next_op_studios"]})}
    };
    time_t ti = (time_t)std::stoi(data["tim"]);
    return dumbfmt_file("./static/template/post.html", {
        {"no", data["post_number"]},
        {"subject", data["subject"]},
        {"name", (data["name"] == "Anonymous" && data["trip"] != "") ? "" : data["name"]},
        {"trip", data["trip"]},
        {"posterid", data["usr_id"]},
        {"date", ctime(&ti)},
        {"body", dumbfmt_replace("[realquoterep]", "\"", data["bod"])},
    
        {"nav-top", is_op ? dumbfmt_file("./static/template/navigator.html", nav_block) : ""},
        {"nav-bottom", is_op ? dumbfmt_file("./static/template/navigator.html", nav_block) : ""},

        {"specials", is_op ? "op-studios" : ""}
        
    });
}

std::string threads::make_thread(sqlite3* db, int op_id, bool cach)
{
    std::string acc = "";
    static std::map<int, std::string> cache;
    if (cache.find(op_id) != cache.end() && cach)
        return cache.at(op_id);
    rows posts = 
        sqleasy_q{db, dfmt({"select * from posts where op_no=", std::to_string(op_id), " order by post_number asc;"})}.exec();
    foreach (posts, post)
    {
        acc.append(threads::make_post(db, *post));
    }
    cache.emplace(op_id, acc);
    return acc;
}
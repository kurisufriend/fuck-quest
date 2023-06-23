#include "threads.h"
#include "lib/dumbstr/dumbstr.h"
#include "lib/sqleasy/sqleasy.h"
#include <string>
#include <iostream>
#include <regex>

std::string threads::make_post(sqlite3* db, row data)
{
    bool is_op = data["is_op_studios"] == "1";
    std::map<std::string, std::string> nav_block = {
        {"prev_op", data["prev_op_studios"]},
        {"next_op", data["next_op_studios"]}
    };
    time_t ti = (time_t)std::stoi(data["tim"]);
    return dumbfmt_file("./static/template/post.html", {
        {"no", data["post_number"]},
        {"subject", data["subject"]},
        {"name", (data["name"] == "Anonymous" && data["trip"] != "") ? "" : data["name"]},
        {"trip", data["trip"]},
        {"posterid", data["usr_id"]},
        {"date", ctime(&ti)},
        {"body", std::regex_replace(data["bod"], std::regex("\\[realquoterep\\]"), "\"")},
    
        {"nav-top", is_op ? dumbfmt_file("./static/template/navigator.html", nav_block) : ""},
        {"nav-bottom", is_op ? dumbfmt_file("./static/template/navigator.html", nav_block) : ""},

        {"specials", is_op ? "op-studios" : ""}
        
    });
}

std::string threads::make_thread(sqlite3* db, int op_id)
{
    rows posts = 
        sqleasy_q{db, dfmt({"select * from posts where op_no=", std::to_string(op_id), " order by post_number asc;"})}.exec();
    std::string acc = "";
    foreach (posts, post)
    {
        acc.append(threads::make_post(db, *post));
    }
    std::cout << acc.length() << std::endl;
    return acc;
}
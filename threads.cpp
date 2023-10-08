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
    int prev_story = std::stoi(data["prev_story"]);
    int prev_lewd = std::stoi(data["prev_lewd"]);
    
    int next_op_studios_int = std::stoi(data["next_op_studios"]);
    int next_story = std::stoi(data["next_story"]);
    int next_lewd = std::stoi(data["next_lewd"]);
    int op_no_int = std::stoi(data["op_no"]);
    int thread_ender = op_no_int+std::stoi(data["reply_count"]);
    std::map<std::string, std::string> nav_block = {
        {"prev_story", dumbfmt({(prev_story >= op_no_int) ? "#" : dumbfmt({"/fq/", std::to_string(prev_op), "#"}), data["prev_story"]})},
        {"next_story", dumbfmt({(next_story <= thread_ender) ? "#" : dumbfmt({"/fq/", std::to_string(thread_ender+1), "#"}), data["next_story"]})},

        {"prev_lewd", dumbfmt({(prev_lewd >= op_no_int) ? "#" : dumbfmt({"/fq/", std::to_string(prev_op), "#"}), data["prev_lewd"]})},
        {"next_lewd", dumbfmt({(next_lewd <= thread_ender) ? "#" : dumbfmt({"/fq/", std::to_string(thread_ender+1), "#"}), data["next_lewd"]})},

        {"prev_op", dumbfmt({(prev_op_studios_int >= op_no_int) ? "#" : dumbfmt({"/fq/", std::to_string(prev_op), "#"}), data["prev_op_studios"]})},
        {"next_op", dumbfmt({(next_op_studios_int <= thread_ender) ? "#" : dumbfmt({"/fq/", std::to_string(thread_ender+1), "#"}), data["next_op_studios"]})}
    };

    std::string upload_filename = data["picrel_name"];
    if (upload_filename != "")
    {
        int ext_idx = upload_filename.find_last_of(".");
        std::string file_ext = upload_filename.substr(ext_idx);
        upload_filename = upload_filename.substr(0, ext_idx);
        if (upload_filename.length() >= 15)
        {
            upload_filename = upload_filename.substr(0, 15).append("(...)");
        }
        upload_filename = upload_filename.append(file_ext);
    }


    time_t ti = (time_t)std::stoi(data["tim"]);
    return dumbfmt_file("./static/template/post.html", {
        {"no", data["post_number"]},
        {"subject", data["subject"]},
        {"name", (data["name"] == "Anonymous" && data["trip"] != "") ? "" : data["name"]},
        {"trip", data["trip"]},
        {"posterid", (data["usr_id"] == "000000") ? "" : dumbfmt({"ID: ", data["usr_id"]})},
        {"date", ctime(&ti)},
        {"body", dumbfmt_replace("[realquoterep]", "\"", data["bod"])},

        {"image", data["picrel"] == "" ? "" : dumbfmt_file("./static/template/image.html", {{"thumbname", data["picrel_spoiler"]=="1" ? "spoiler.png" : data["picrel"]}, {"filename", data["picrel"]}, {"uploadname", data["picrel_spoiler"]=="1" ? "Spoiler Image" : upload_filename}, {"size", is_op ? "250" : "125"}})},

        #define genericmarker(name) (data["is_" #name] == "1") ? "<img src='/imgs/prof-"#name".png' title='"#name" post!'></img>" : ""
        {"markers", dumbfmt({genericmarker(ghost), genericmarker(story), genericmarker(lewd)})},
    
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

std::pair<std::string, std::string> threads::get_prev_next_thread(sqlite3* db, int op_id, bool cach)
{
    std::string acc = "";
    static std::map<int, std::pair<std::string, std::string>> cache;
    if (cache.find(op_id) != cache.end() && cach)
        return cache.at(op_id);
    rows next = 
        sqleasy_q{db, dfmt({"select * from posts where post_number=", std::to_string(op_id), ";"})}.exec();
    rows last = 
        sqleasy_q{db, dfmt({"select * from posts where post_number=", std::to_string(op_id-1), ";"})}.exec();
    std::string prev = "";
    foreach(last, l)
        {prev = (*l)["op_no"];} // don't ask
    return std::pair<std::string, std::string>((prev == "") ? "0" : prev, std::to_string(op_id+1+std::stoi(next[0]["reply_count"])));
}
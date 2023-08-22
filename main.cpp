#include "lib/mongoose/mongoose.h"
#include "lib/sqlite/sqlite3.h"
#include "lib/dumbstr/dumbstr.h"
#include "lib/json.hpp"

#include "threads.h"
#include "episodes.h"

#include <cctype>
#include <cstdlib>
#include <iostream>
#include <map>
#include <any>
#include <string>
#include <vector>
#include <fstream>

#define XCLACKSOVERHEAD "X-Clacks-Overhead: GNU Terry Pratchett, GNU Aaron Swartz, GNU Hal Finney, GNU Norm Macdonald, GNU Gilbert Gottfried, GNU Aniki, GNU Terry Davis, GNU jstark, GNU John McAfee, GNU asshurtmacfags\n"
#define THROW404() mg_http_reply(c, 404, headers.c_str(), "the name's huwer, as in who are the fuck is you?")


typedef mg_connection connection;
typedef mg_http_message message;

sqlite3* db;

void callback(connection* c, int ev, void* ev_data, void* fn_data)
{
    if (ev == MG_EV_HTTP_MSG)
    {
        std::string headers = XCLACKSOVERHEAD;
        message* msg = (message*)ev_data;
        std::string url = msg->uri.len != 0 ? msg->uri.ptr : "/viv.png";

        if(mg_http_match_uri(msg, "/"))
        {
            headers.append("Content-Type: text/html;charset=shift_jis\n");
            mg_http_reply(c, 200, headers.c_str(),
                dumbfmt_file("./static/index.html", {
                    {"body", dumbfmt_file("./static/template/main-body.html", {})}
                }).c_str());
        }
        else if (mg_http_match_uri(msg, "/imgs/*"))
        {
            std::string stub = "./static";
            foreach(url, iter)
            {
                if (*iter == ' ') {break;}
                stub.push_back(*iter);
            }
            mg_http_serve_opts opt {};
            mg_http_serve_file(c, msg, stub.c_str(), &opt);
        }
        else if (mg_http_match_uri(msg, "/fq/*"))
        {
            std::string tid_s = msg->uri.ptr;
            std::string tid_trimmed;
            foreach(tid_s, c)
            {
                if (*c == ' ') {break;}
                tid_trimmed.push_back(*c);
            }
            tid_trimmed = tid_trimmed.substr(4);
            std::string real = "";
            std::string query = "";
            bool past = false;
            foreach(tid_trimmed, c)
            {
                if (*c == '?') {past = true;continue;}
                (past ? query : real).push_back(*c);
            }
            tid_trimmed = real;
            bool is_num = true;
            foreach(tid_trimmed, c) {is_num &= std::isdigit(*c);}
            if (tid_trimmed == "") {is_num = false;}
            if (!is_num)
            {
                THROW404();
                return;
            }
            bool reader_mode = (query == "reader_mode");
            int tid = std::stoi(tid_trimmed);
            headers.append("Content-Type: text/html;charset=shift_jis\n");
            mg_http_reply(c, 200, headers.c_str(),
                dumbfmt_file("./static/index.html", {
                    {"body", dumbfmt_file("./static/template/tview.html", {
                        {"temp", threads::make_thread(db, tid, reader_mode).c_str()},
                        {"nav", dumbfmt_file("./static/template/tnav.html",{{"query_link", reader_mode ? "?" : "?reader_mode"}})}
                    })}
                }).c_str());
        }
        else if (mg_http_match_uri(msg, "/main.css"))
        {
            mg_http_reply(c, 200, headers.c_str(),
                dumbfmt_file("./static/main.css", {}).c_str());
        }
        else if (mg_http_match_uri(msg, "/episodes"))
        {
            mg_http_reply(c, 200, headers.c_str(),
                dumbfmt_file("./static/index.html", {
                    {"body", dumbfmt_file("./static/template/episodes.html", {
                        {"episode_listing", episodes::make_episode_list(db)}
                    })}
                }).c_str());
        }
#define gimmick(inp, out)else if (mg_http_match_uri(msg, inp)) {mg_http_reply(c, 418, headers.c_str(), out);}
        gimmick("/rose", "won")
        gimmick("/421", "beep")
        gimmick("/422", "boop")
        gimmick("/CHART", "coming soon")
        else 
        {
            THROW404();
        }
    }

}

int main(int argc, char* argv[])
{
    mg_mgr mongoose;
    mg_mgr_init(&mongoose);

    bool inited = true;
    if (access("./fq.db", F_OK) == -1)
        inited = false;

    if (sqlite3_open("./fq.db", &db))
    {
        std::cout << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return -1;
    }
    //if (!inited)
        //db_schema_init(db);
    
    std::fstream f;
    f.open("./config.json");
    nlohmann::json cfg = nlohmann::json::parse(f);
    f.close();


    mg_http_listen(&mongoose, cfg["host"].get<std::string>().c_str(), callback, &mongoose);
    while (true) {mg_mgr_poll(&mongoose, 1000);}
    sqlite3_close(db);

    return 0;
}
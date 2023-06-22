#include "lib/mongoose/mongoose.h"
#include "lib/sqlite/sqlite3.h"
#include "lib/dumbstr/dumbstr.h"
#include "lib/json.hpp"

#include "threads.h"

#include <cstdlib>
#include <iostream>
#include <map>
#include <any>
#include <string>
#include <vector>
#include <fstream>

#define XCLACKSOVERHEAD "X-Clacks-Overhead: GNU Terry Pratchett, GNU Aaron Swartz, GNU Hal Finney, GNU Norm Macdonald, GNU Gilbert Gottfried, GNU Aniki, GNU Terry Davis, GNU jstark, GNU John McAfee, GNU asshurtmacfags\n"

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
            for (auto iter = url.begin(); iter < url.end(); iter++)
            {
                if (*iter == ' ') {break;}
                stub.push_back(*iter);
            }
            std::cout << stub << std::endl;
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
            std::cout << tid_trimmed.substr(4) << std::endl;
            int tid = std::stoi(tid_trimmed.substr(4));
            headers.append("Content-Type: text/html;charset=shift_jis\n");
            mg_http_reply(c, 200, headers.c_str(),
                dumbfmt_file("./static/index.html", {
                    {"body", dumbfmt_file("./static/template/tview.html", {
                        {"temp", threads::make_thread(db, tid).c_str()}
                    })}
                }).c_str());
        }
        else if (mg_http_match_uri(msg, "/main.css"))
        {
            mg_http_reply(c, 200, headers.c_str(),
                dumbfmt_file("./static/main.css", {}).c_str());
        }
#define gimmick(inp, out)else if (mg_http_match_uri(msg, inp)) {mg_http_reply(c, 418, headers.c_str(), out);}
        gimmick("/rose", "won")
        gimmick("/421", "beep")
        gimmick("/422", "boop")
        gimmick("/CHART", "coming soon")
        else 
        {
            mg_http_reply(c, 404, headers.c_str(), 
                "the name's huwer, as in who are the fuck is you?");
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
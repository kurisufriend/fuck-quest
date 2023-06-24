#include <string>
#include "lib/sqlite/sqlite3.h"
#include "lib/sqleasy/sqleasy.h"
namespace threads
{
    std::string make_thread(sqlite3* db, int op_id, bool cach = true);
    std::string make_post(sqlite3* db, row data);
}
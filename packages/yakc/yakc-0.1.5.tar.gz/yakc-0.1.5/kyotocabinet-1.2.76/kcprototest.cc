/*************************************************************************************************
 * The test cases of the prototype database
 *                                                               Copyright (C) 2009-2012 FAL Labs
 * This file is part of Kyoto Cabinet.
 * This program is free software: you can redistribute it and/or modify it under the terms of
 * the GNU General Public License as published by the Free Software Foundation, either version
 * 3 of the License, or any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program.
 * If not, see <http://www.gnu.org/licenses/>.
 *************************************************************************************************/


#include <kcprotodb.h>
#include "cmdcommon.h"


// global variables
const char* g_progname;                  // program name
uint32_t g_randseed;                     // random seed
int64_t g_memusage;                      // memory usage


// function prototypes
int main(int argc, char** argv);
static void usage();
static void dberrprint(kc::BasicDB* db, int32_t line, const char* func);
static void dbmetaprint(kc::BasicDB* db, bool verbose);
static int32_t runorder(int argc, char** argv);
static int32_t runqueue(int argc, char** argv);
static int32_t runwicked(int argc, char** argv);
static int32_t runtran(int argc, char** argv);
template <class PROTODB>
static int32_t procorder(const char* tname, int64_t rnum, int32_t thnum, bool rnd,
                         bool etc, bool tran);
template <class PROTODB>
static int32_t procqueue(const char* tname, int64_t rnum, int32_t thnum, int32_t itnum,
                         bool rnd);
template <class PROTODB>
static int32_t procwicked(const char* tname, int64_t rnum, int32_t thnum, int32_t itnum);
template <class PROTODB>
static int32_t proctran(const char* tname, int64_t rnum, int32_t thnum, int32_t itnum);


// main routine
int main(int argc, char** argv) {
  g_progname = argv[0];
  const char* ebuf = kc::getenv("KCRNDSEED");
  g_randseed = ebuf ? (uint32_t)kc::atoi(ebuf) : (uint32_t)(kc::time() * 1000);
  mysrand(g_randseed);
  g_memusage = memusage();
  kc::setstdiobin();
  if (argc < 2) usage();
  int32_t rv = 0;
  if (!std::strcmp(argv[1], "order")) {
    rv = runorder(argc, argv);
  } else if (!std::strcmp(argv[1], "queue")) {
    rv = runqueue(argc, argv);
  } else if (!std::strcmp(argv[1], "wicked")) {
    rv = runwicked(argc, argv);
  } else if (!std::strcmp(argv[1], "tran")) {
    rv = runtran(argc, argv);
  } else {
    usage();
  }
  if (rv != 0) {
    oprintf("FAILED: KCRNDSEED=%u PID=%ld", g_randseed, (long)kc::getpid());
    for (int32_t i = 0; i < argc; i++) {
      oprintf(" %s", argv[i]);
    }
    oprintf("\n\n");
  }
  return rv;
}


// print the usage and exit
static void usage() {
  eprintf("%s: test cases of the prototype database of Kyoto Cabinet\n", g_progname);
  eprintf("\n");
  eprintf("usage:\n");
  eprintf("  %s order [-tree] [-th num] [-rnd] [-etc] [-tran] rnum\n", g_progname);
  eprintf("  %s queue [-tree] [-th num] [-it num] [-rnd] rnum\n", g_progname);
  eprintf("  %s wicked [-tree] [-th num] [-it num] rnum\n", g_progname);
  eprintf("  %s tran [-tree] [-th num] [-it num] rnum\n", g_progname);
  eprintf("\n");
  std::exit(1);
}


// print the error message of a database
static void dberrprint(kc::BasicDB* db, int32_t line, const char* func) {
  const kc::BasicDB::Error& err = db->error();
  oprintf("%s: %d: %s: %s: %d: %s: %s\n",
          g_progname, line, func, db->path().c_str(), err.code(), err.name(), err.message());
}


// print members of a database
static void dbmetaprint(kc::BasicDB* db, bool verbose) {
  if (verbose) {
    std::map<std::string, std::string> status;
    status["opaque"] = "";
    if (db->status(&status)) {
      uint32_t type = kc::atoi(status["type"].c_str());
      oprintf("type: %s (%s) (type=0x%02X)\n",
              kc::BasicDB::typecname(type), kc::BasicDB::typestring(type), type);
      uint32_t rtype = kc::atoi(status["realtype"].c_str());
      if (rtype > 0 && rtype != type)
        oprintf("real type: %s (%s) (realtype=0x%02X)\n",
                kc::BasicDB::typecname(rtype), kc::BasicDB::typestring(rtype), rtype);
      oprintf("path: %s\n", status["path"].c_str());
      if (status["opaque"].size() >= 16) {
        const char* opaque = status["opaque"].c_str();
        oprintf("opaque:");
        if (std::count(opaque, opaque + 16, 0) != 16) {
          for (int32_t i = 0; i < 16; i++) {
            oprintf(" %02X", ((unsigned char*)opaque)[i]);
          }
        } else {
          oprintf(" 0");
        }
        oprintf("\n");
      }
      int64_t count = kc::atoi(status["count"].c_str());
      std::string cntstr = unitnumstr(count);
      oprintf("count: %lld (%s)\n", count, cntstr.c_str());
      int64_t size = kc::atoi(status["size"].c_str());
      std::string sizestr = unitnumstrbyte(size);
      oprintf("size: %lld (%s)\n", size, sizestr.c_str());
    }
  } else {
    oprintf("count: %lld\n", (long long)db->count());
    oprintf("size: %lld\n", (long long)db->size());
  }
  int64_t musage = memusage();
  if (musage > 0) oprintf("memory: %lld\n", (long long)(musage - g_memusage));
}


// parse arguments of order command
static int32_t runorder(int argc, char** argv) {
  bool argbrk = false;
  const char* rstr = NULL;
  bool tree = false;
  int32_t thnum = 1;
  bool rnd = false;
  bool etc = false;
  bool tran = false;
  for (int32_t i = 2; i < argc; i++) {
    if (!argbrk && argv[i][0] == '-') {
      if (!std::strcmp(argv[i], "--")) {
        argbrk = true;
      } else if (!std::strcmp(argv[i], "-tree")) {
        tree = true;
      } else if (!std::strcmp(argv[i], "-th")) {
        if (++i >= argc) usage();
        thnum = kc::atoix(argv[i]);
      } else if (!std::strcmp(argv[i], "-rnd")) {
        rnd = true;
      } else if (!std::strcmp(argv[i], "-etc")) {
        etc = true;
      } else if (!std::strcmp(argv[i], "-tran")) {
        tran = true;
      } else {
        usage();
      }
    } else if (!rstr) {
      argbrk = true;
      rstr = argv[i];
    } else {
      usage();
    }
  }
  if (!rstr) usage();
  int64_t rnum = kc::atoix(rstr);
  if (rnum < 1 || thnum < 1) usage();
  if (thnum > THREADMAX) thnum = THREADMAX;
  int32_t rv = 0;
  if (tree) {
    rv = procorder<kc::ProtoTreeDB>("Tree", rnum, thnum, rnd, etc, tran);
  } else {
    rv = procorder<kc::ProtoHashDB>("Hash", rnum, thnum, rnd, etc, tran);
  }
  return rv;
}


// parse arguments of queue command
static int32_t runqueue(int argc, char** argv) {
  bool argbrk = false;
  const char* rstr = NULL;
  bool tree = false;
  int32_t thnum = 1;
  int32_t itnum = 1;
  bool rnd = false;
  for (int32_t i = 2; i < argc; i++) {
    if (!argbrk && argv[i][0] == '-') {
      if (!std::strcmp(argv[i], "--")) {
        argbrk = true;
      } else if (!std::strcmp(argv[i], "-tree")) {
        tree = true;
      } else if (!std::strcmp(argv[i], "-th")) {
        if (++i >= argc) usage();
        thnum = kc::atoix(argv[i]);
      } else if (!std::strcmp(argv[i], "-it")) {
        if (++i >= argc) usage();
        itnum = kc::atoix(argv[i]);
      } else if (!std::strcmp(argv[i], "-rnd")) {
        rnd = true;
      } else {
        usage();
      }
    } else if (!rstr) {
      argbrk = true;
      rstr = argv[i];
    } else {
      usage();
    }
  }
  if (!rstr) usage();
  int64_t rnum = kc::atoix(rstr);
  if (rnum < 1 || thnum < 1 || itnum < 1) usage();
  if (thnum > THREADMAX) thnum = THREADMAX;
  int32_t rv = 0;
  if (tree) {
    rv = procqueue<kc::ProtoTreeDB>("Tree", rnum, thnum, itnum, rnd);
  } else {
    rv = procqueue<kc::ProtoHashDB>("Hash", rnum, thnum, itnum, rnd);
  }
  return rv;
}


// parse arguments of wicked command
static int32_t runwicked(int argc, char** argv) {
  bool argbrk = false;
  const char* rstr = NULL;
  bool tree = false;
  int32_t thnum = 1;
  int32_t itnum = 1;
  for (int32_t i = 2; i < argc; i++) {
    if (!argbrk && argv[i][0] == '-') {
      if (!std::strcmp(argv[i], "--")) {
        argbrk = true;
      } else if (!std::strcmp(argv[i], "-tree")) {
        tree = true;
      } else if (!std::strcmp(argv[i], "-th")) {
        if (++i >= argc) usage();
        thnum = kc::atoix(argv[i]);
      } else if (!std::strcmp(argv[i], "-it")) {
        if (++i >= argc) usage();
        itnum = kc::atoix(argv[i]);
      } else {
        usage();
      }
    } else if (!rstr) {
      argbrk = true;
      rstr = argv[i];
    } else {
      usage();
    }
  }
  if (!rstr) usage();
  int64_t rnum = kc::atoix(rstr);
  if (rnum < 1 || thnum < 1 || itnum < 1) usage();
  if (thnum > THREADMAX) thnum = THREADMAX;
  int32_t rv = 0;
  if (tree) {
    rv = procwicked<kc::ProtoTreeDB>("Tree", rnum, thnum, itnum);
  } else {
    rv = procwicked<kc::ProtoHashDB>("Hash", rnum, thnum, itnum);
  }
  return rv;
}


// parse arguments of tran command
static int32_t runtran(int argc, char** argv) {
  bool argbrk = false;
  const char* rstr = NULL;
  bool tree = false;
  int32_t thnum = 1;
  int32_t itnum = 1;
  for (int32_t i = 2; i < argc; i++) {
    if (!argbrk && argv[i][0] == '-') {
      if (!std::strcmp(argv[i], "--")) {
        argbrk = true;
      } else if (!std::strcmp(argv[i], "-tree")) {
        tree = true;
      } else if (!std::strcmp(argv[i], "-th")) {
        if (++i >= argc) usage();
        thnum = kc::atoix(argv[i]);
      } else if (!std::strcmp(argv[i], "-it")) {
        if (++i >= argc) usage();
        itnum = kc::atoix(argv[i]);
      } else {
        usage();
      }
    } else if (!rstr) {
      argbrk = true;
      rstr = argv[i];
    } else {
      usage();
    }
  }
  if (!rstr) usage();
  int64_t rnum = kc::atoix(rstr);
  if (rnum < 1 || thnum < 1 || itnum < 1) usage();
  if (thnum > THREADMAX) thnum = THREADMAX;
  int32_t rv = 0;
  if (tree) {
    rv = proctran<kc::ProtoTreeDB>("Tree", rnum, thnum, itnum);
  } else {
    rv = proctran<kc::ProtoHashDB>("Hash", rnum, thnum, itnum);
  }
  return rv;
}


// perform order command
template <class PROTODB>
static int32_t procorder(const char* tname, int64_t rnum, int32_t thnum, bool rnd,
                         bool etc, bool tran) {
  oprintf("<%s In-order Test>\n  seed=%u  rnum=%lld  thnum=%d  rnd=%d  etc=%d  tran=%d\n\n",
          tname, g_randseed, (long long)rnum, thnum, rnd, etc, tran);
  bool err = false;
  PROTODB db;
  oprintf("opening the database:\n");
  double stime = kc::time();
  if (!db.open("-", kc::BasicDB::OWRITER | kc::BasicDB::OCREATE | kc::BasicDB::OTRUNCATE)) {
    dberrprint(&db, __LINE__, "DB::open");
    err = true;
  }
  double etime = kc::time();
  dbmetaprint(&db, false);
  oprintf("time: %.3f\n", etime - stime);
  oprintf("setting records:\n");
  stime = kc::time();
  class ThreadSet : public kc::Thread {
   public:
    void setparams(int32_t id, kc::BasicDB* db, int64_t rnum, int32_t thnum,
                   bool rnd, bool tran) {
      id_ = id;
      db_ = db;
      rnum_ = rnum;
      thnum_ = thnum;
      err_ = false;
      rnd_ = rnd;
      tran_ = tran;
    }
    bool error() {
      return err_;
    }
    void run() {
      int64_t base = id_ * rnum_;
      int64_t range = rnum_ * thnum_;
      for (int64_t i = 1; !err_ && i <= rnum_; i++) {
        if (tran_ && !db_->begin_transaction(false)) {
          dberrprint(db_, __LINE__, "DB::begin_transaction");
          err_ = true;
        }
        char kbuf[RECBUFSIZ];
        size_t ksiz = std::sprintf(kbuf, "%08lld",
                                   (long long)(rnd_ ? myrand(range) + 1 : base + i));
        if (!db_->set(kbuf, ksiz, kbuf, ksiz)) {
          dberrprint(db_, __LINE__, "DB::set");
          err_ = true;
        }
        if (rnd_ && i % 8 == 0) {
          switch (myrand(8)) {
            case 0: {
              if (!db_->set(kbuf, ksiz, kbuf, ksiz)) {
                dberrprint(db_, __LINE__, "DB::set");
                err_ = true;
              }
              break;
            }
            case 1: {
              if (!db_->append(kbuf, ksiz, kbuf, ksiz)) {
                dberrprint(db_, __LINE__, "DB::append");
                err_ = true;
              }
              break;
            }
            case 2: {
              if (!db_->remove(kbuf, ksiz) && db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "DB::remove");
                err_ = true;
              }
              break;
            }
            case 3: {
              kc::DB::Cursor* cur = db_->cursor();
              if (cur->jump(kbuf, ksiz)) {
                switch (myrand(8)) {
                  default: {
                    size_t rsiz;
                    char* rbuf = cur->get_key(&rsiz, myrand(10) == 0);
                    if (rbuf) {
                      delete[] rbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get_key");
                      err_ = true;
                    }
                    break;
                  }
                  case 1: {
                    size_t rsiz;
                    char* rbuf = cur->get_value(&rsiz, myrand(10) == 0);
                    if (rbuf) {
                      delete[] rbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get_value");
                      err_ = true;
                    }
                    break;
                  }
                  case 2: {
                    size_t rksiz;
                    const char* rvbuf;
                    size_t rvsiz;
                    char* rkbuf = cur->get(&rksiz, &rvbuf, &rvsiz, myrand(10) == 0);
                    if (rkbuf) {
                      delete[] rkbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get");
                      err_ = true;
                    }
                    break;
                  }
                  case 3: {
                    std::string key, value;
                    if (!cur->get(&key, &value, myrand(10) == 0) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get");
                      err_ = true;
                    }
                    break;
                  }
                  case 4: {
                    if (myrand(8) == 0 && !cur->remove() &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::remove");
                      err_ = true;
                    }
                    break;
                  }
                }
              } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              }
              delete cur;
              break;
            }
            default: {
              size_t vsiz;
              char* vbuf = db_->get(kbuf, ksiz, &vsiz);
              if (vbuf) {
                delete[] vbuf;
              } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "DB::get");
                err_ = true;
              }
              break;
            }
          }
        }
        if (tran_ && !db_->end_transaction(true)) {
          dberrprint(db_, __LINE__, "DB::end_transaction");
          err_ = true;
        }
        if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
          oputchar('.');
          if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
        }
      }
    }
   private:
    int32_t id_;
    kc::BasicDB* db_;
    int64_t rnum_;
    int32_t thnum_;
    bool err_;
    bool rnd_;
    bool tran_;
  };
  ThreadSet threadsets[THREADMAX];
  if (thnum < 2) {
    threadsets[0].setparams(0, &db, rnum, thnum, rnd, tran);
    threadsets[0].run();
    if (threadsets[0].error()) err = true;
  } else {
    for (int32_t i = 0; i < thnum; i++) {
      threadsets[i].setparams(i, &db, rnum, thnum, rnd, tran);
      threadsets[i].start();
    }
    for (int32_t i = 0; i < thnum; i++) {
      threadsets[i].join();
      if (threadsets[i].error()) err = true;
    }
  }
  etime = kc::time();
  dbmetaprint(&db, false);
  oprintf("time: %.3f\n", etime - stime);
  if (etc) {
    oprintf("adding records:\n");
    stime = kc::time();
    class ThreadAdd : public kc::Thread {
     public:
      void setparams(int32_t id, kc::BasicDB* db, int64_t rnum, int32_t thnum,
                     bool rnd, bool tran) {
        id_ = id;
        db_ = db;
        rnum_ = rnum;
        thnum_ = thnum;
        err_ = false;
        rnd_ = rnd;
        tran_ = tran;
      }
      bool error() {
        return err_;
      }
      void run() {
        int64_t base = id_ * rnum_;
        int64_t range = rnum_ * thnum_;
        for (int64_t i = 1; !err_ && i <= rnum_; i++) {
          if (tran_ && !db_->begin_transaction(false)) {
            dberrprint(db_, __LINE__, "DB::begin_transaction");
            err_ = true;
          }
          char kbuf[RECBUFSIZ];
          size_t ksiz = std::sprintf(kbuf, "%08lld",
                                     (long long)(rnd_ ? myrand(range) + 1 : base + i));
          if (!db_->add(kbuf, ksiz, kbuf, ksiz) &&
              db_->error() != kc::BasicDB::Error::DUPREC) {
            dberrprint(db_, __LINE__, "DB::add");
            err_ = true;
          }
          if (tran_ && !db_->end_transaction(true)) {
            dberrprint(db_, __LINE__, "DB::end_transaction");
            err_ = true;
          }
          if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
            oputchar('.');
            if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
          }
        }
      }
     private:
      int32_t id_;
      kc::BasicDB* db_;
      int64_t rnum_;
      int32_t thnum_;
      bool err_;
      bool rnd_;
      bool tran_;
    };
    ThreadAdd threadadds[THREADMAX];
    if (thnum < 2) {
      threadadds[0].setparams(0, &db, rnum, thnum, rnd, tran);
      threadadds[0].run();
      if (threadadds[0].error()) err = true;
    } else {
      for (int32_t i = 0; i < thnum; i++) {
        threadadds[i].setparams(i, &db, rnum, thnum, rnd, tran);
        threadadds[i].start();
      }
      for (int32_t i = 0; i < thnum; i++) {
        threadadds[i].join();
        if (threadadds[i].error()) err = true;
      }
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
  }
  if (etc) {
    oprintf("appending records:\n");
    stime = kc::time();
    class ThreadAppend : public kc::Thread {
     public:
      void setparams(int32_t id, kc::BasicDB* db, int64_t rnum, int32_t thnum,
                     bool rnd, bool tran) {
        id_ = id;
        db_ = db;
        rnum_ = rnum;
        thnum_ = thnum;
        err_ = false;
        rnd_ = rnd;
        tran_ = tran;
      }
      bool error() {
        return err_;
      }
      void run() {
        int64_t base = id_ * rnum_;
        int64_t range = rnum_ * thnum_;
        for (int64_t i = 1; !err_ && i <= rnum_; i++) {
          if (tran_ && !db_->begin_transaction(false)) {
            dberrprint(db_, __LINE__, "DB::begin_transaction");
            err_ = true;
          }
          char kbuf[RECBUFSIZ];
          size_t ksiz = std::sprintf(kbuf, "%08lld",
                                     (long long)(rnd_ ? myrand(range) + 1 : base + i));
          if (!db_->append(kbuf, ksiz, kbuf, ksiz)) {
            dberrprint(db_, __LINE__, "DB::append");
            err_ = true;
          }
          if (tran_ && !db_->end_transaction(true)) {
            dberrprint(db_, __LINE__, "DB::end_transaction");
            err_ = true;
          }
          if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
            oputchar('.');
            if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
          }
        }
      }
     private:
      int32_t id_;
      kc::BasicDB* db_;
      int64_t rnum_;
      int32_t thnum_;
      bool err_;
      bool rnd_;
      bool tran_;
    };
    ThreadAppend threadappends[THREADMAX];
    if (thnum < 2) {
      threadappends[0].setparams(0, &db, rnum, thnum, rnd, tran);
      threadappends[0].run();
      if (threadappends[0].error()) err = true;
    } else {
      for (int32_t i = 0; i < thnum; i++) {
        threadappends[i].setparams(i, &db, rnum, thnum, rnd, tran);
        threadappends[i].start();
      }
      for (int32_t i = 0; i < thnum; i++) {
        threadappends[i].join();
        if (threadappends[i].error()) err = true;
      }
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
    char* opaque = db.opaque();
    if (opaque) {
      std::memcpy(opaque, "1234567890123456", 16);
      if (!db.synchronize_opaque()) {
        dberrprint(&db, __LINE__, "DB::synchronize_opaque");
        err = true;
      }
    } else {
      dberrprint(&db, __LINE__, "DB::opaque");
      err = true;
    }
  }
  oprintf("getting records:\n");
  stime = kc::time();
  class ThreadGet : public kc::Thread {
   public:
    void setparams(int32_t id, kc::BasicDB* db, int64_t rnum, int32_t thnum,
                   bool rnd, bool tran) {
      id_ = id;
      db_ = db;
      rnum_ = rnum;
      thnum_ = thnum;
      err_ = false;
      rnd_ = rnd;
      tran_ = tran;
    }
    bool error() {
      return err_;
    }
    void run() {
      int64_t base = id_ * rnum_;
      int64_t range = rnum_ * thnum_;
      for (int64_t i = 1; !err_ && i <= rnum_; i++) {
        if (tran_ && !db_->begin_transaction(false)) {
          dberrprint(db_, __LINE__, "DB::begin_transaction");
          err_ = true;
        }
        char kbuf[RECBUFSIZ];
        size_t ksiz = std::sprintf(kbuf, "%08lld",
                                   (long long)(rnd_ ? myrand(range) + 1 : base + i));
        size_t vsiz;
        char* vbuf = db_->get(kbuf, ksiz, &vsiz);
        if (vbuf) {
          if (vsiz < ksiz || std::memcmp(vbuf, kbuf, ksiz)) {
            dberrprint(db_, __LINE__, "DB::get");
            err_ = true;
          }
          delete[] vbuf;
        } else if (!rnd_ || db_->error() != kc::BasicDB::Error::NOREC) {
          dberrprint(db_, __LINE__, "DB::get");
          err_ = true;
        }
        if (rnd_ && i % 8 == 0) {
          switch (myrand(8)) {
            case 0: {
              if (!db_->set(kbuf, ksiz, kbuf, ksiz)) {
                dberrprint(db_, __LINE__, "DB::set");
                err_ = true;
              }
              break;
            }
            case 1: {
              if (!db_->append(kbuf, ksiz, kbuf, ksiz)) {
                dberrprint(db_, __LINE__, "DB::append");
                err_ = true;
              }
              break;
            }
            case 2: {
              if (!db_->remove(kbuf, ksiz) &&
                  db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "DB::remove");
                err_ = true;
              }
              break;
            }
            case 3: {
              kc::DB::Cursor* cur = db_->cursor();
              if (cur->jump(kbuf, ksiz)) {
                switch (myrand(8)) {
                  default: {
                    size_t rsiz;
                    char* rbuf = cur->get_key(&rsiz, myrand(10) == 0);
                    if (rbuf) {
                      delete[] rbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get_key");
                      err_ = true;
                    }
                    break;
                  }
                  case 1: {
                    size_t rsiz;
                    char* rbuf = cur->get_value(&rsiz, myrand(10) == 0);
                    if (rbuf) {
                      delete[] rbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get_value");
                      err_ = true;
                    }
                    break;
                  }
                  case 2: {
                    size_t rksiz;
                    const char* rvbuf;
                    size_t rvsiz;
                    char* rkbuf = cur->get(&rksiz, &rvbuf, &rvsiz, myrand(10) == 0);
                    if (rkbuf) {
                      delete[] rkbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get");
                      err_ = true;
                    }
                    break;
                  }
                  case 3: {
                    std::string key, value;
                    if (!cur->get(&key, &value, myrand(10) == 0) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get");
                      err_ = true;
                    }
                    break;
                  }
                  case 4: {
                    if (myrand(8) == 0 && !cur->remove() &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::remove");
                      err_ = true;
                    }
                    break;
                  }
                }
              } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              }
              delete cur;
              break;
            }
            default: {
              size_t vsiz;
              char* vbuf = db_->get(kbuf, ksiz, &vsiz);
              if (vbuf) {
                delete[] vbuf;
              } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "DB::get");
                err_ = true;
              }
              break;
            }
          }
        }
        if (tran_ && !db_->end_transaction(true)) {
          dberrprint(db_, __LINE__, "DB::end_transaction");
          err_ = true;
        }
        if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
          oputchar('.');
          if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
        }
      }
    }
   private:
    int32_t id_;
    kc::BasicDB* db_;
    int64_t rnum_;
    int32_t thnum_;
    bool err_;
    bool rnd_;
    bool tran_;
  };
  ThreadGet threadgets[THREADMAX];
  if (thnum < 2) {
    threadgets[0].setparams(0, &db, rnum, thnum, rnd, tran);
    threadgets[0].run();
    if (threadgets[0].error()) err = true;
  } else {
    for (int32_t i = 0; i < thnum; i++) {
      threadgets[i].setparams(i, &db, rnum, thnum, rnd, tran);
      threadgets[i].start();
    }
    for (int32_t i = 0; i < thnum; i++) {
      threadgets[i].join();
      if (threadgets[i].error()) err = true;
    }
  }
  etime = kc::time();
  dbmetaprint(&db, false);
  oprintf("time: %.3f\n", etime - stime);
  if (etc) {
    oprintf("getting records with a buffer:\n");
    stime = kc::time();
    class ThreadGetBuffer : public kc::Thread {
     public:
      void setparams(int32_t id, kc::BasicDB* db, int64_t rnum, int32_t thnum,
                     bool rnd, bool tran) {
        id_ = id;
        db_ = db;
        rnum_ = rnum;
        thnum_ = thnum;
        err_ = false;
        rnd_ = rnd;
        tran_ = tran;
      }
      bool error() {
        return err_;
      }
      void run() {
        int64_t base = id_ * rnum_;
        int64_t range = rnum_ * thnum_;
        for (int64_t i = 1; !err_ && i <= rnum_; i++) {
          if (tran_ && !db_->begin_transaction(false)) {
            dberrprint(db_, __LINE__, "DB::begin_transaction");
            err_ = true;
          }
          char kbuf[RECBUFSIZ];
          size_t ksiz = std::sprintf(kbuf, "%08lld",
                                     (long long)(rnd_ ? myrand(range) + 1 : base + i));
          char vbuf[RECBUFSIZ];
          int32_t vsiz = db_->get(kbuf, ksiz, vbuf, sizeof(vbuf));
          if (vsiz >= 0) {
            if (vsiz < (int32_t)ksiz || std::memcmp(vbuf, kbuf, ksiz)) {
              dberrprint(db_, __LINE__, "DB::get");
              err_ = true;
            }
          } else if (!rnd_ || db_->error() != kc::BasicDB::Error::NOREC) {
            dberrprint(db_, __LINE__, "DB::get");
            err_ = true;
          }
          if (tran_ && !db_->end_transaction(true)) {
            dberrprint(db_, __LINE__, "DB::end_transaction");
            err_ = true;
          }
          if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
            oputchar('.');
            if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
          }
        }
      }
     private:
      int32_t id_;
      kc::BasicDB* db_;
      int64_t rnum_;
      int32_t thnum_;
      bool err_;
      bool rnd_;
      bool tran_;
    };
    ThreadGetBuffer threadgetbuffers[THREADMAX];
    if (thnum < 2) {
      threadgetbuffers[0].setparams(0, &db, rnum, thnum, rnd, tran);
      threadgetbuffers[0].run();
      if (threadgetbuffers[0].error()) err = true;
    } else {
      for (int32_t i = 0; i < thnum; i++) {
        threadgetbuffers[i].setparams(i, &db, rnum, thnum, rnd, tran);
        threadgetbuffers[i].start();
      }
      for (int32_t i = 0; i < thnum; i++) {
        threadgetbuffers[i].join();
        if (threadgetbuffers[i].error()) err = true;
      }
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
  }
  if (etc) {
    oprintf("traversing the database by the inner iterator:\n");
    stime = kc::time();
    int64_t cnt = db.count();
    class VisitorIterator : public kc::DB::Visitor {
     public:
      explicit VisitorIterator(int64_t rnum, bool rnd) :
          rnum_(rnum), rnd_(rnd), cnt_(0), rbuf_() {
        std::memset(rbuf_, '+', sizeof(rbuf_));
      }
      int64_t cnt() {
        return cnt_;
      }
     private:
      const char* visit_full(const char* kbuf, size_t ksiz,
                             const char* vbuf, size_t vsiz, size_t* sp) {
        cnt_++;
        const char* rv = NOP;
        switch (rnd_ ? myrand(7) : cnt_ % 7) {
          case 0: {
            rv = rbuf_;
            *sp = rnd_ ? myrand(sizeof(rbuf_)) : sizeof(rbuf_) / (cnt_ % 5 + 1);
            break;
          }
          case 1: {
            rv = REMOVE;
            break;
          }
        }
        if (rnum_ > 250 && cnt_ % (rnum_ / 250) == 0) {
          oputchar('.');
          if (cnt_ == rnum_ || cnt_ % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)cnt_);
        }
        return rv;
      }
      int64_t rnum_;
      bool rnd_;
      int64_t cnt_;
      char rbuf_[RECBUFSIZ];
    } visitoriterator(rnum, rnd);
    if (tran && !db.begin_transaction(false)) {
      dberrprint(&db, __LINE__, "DB::begin_transaction");
      err = true;
    }
    if (!db.iterate(&visitoriterator, true)) {
      dberrprint(&db, __LINE__, "DB::iterate");
      err = true;
    }
    if (rnd) oprintf(" (end)\n");
    if (tran && !db.end_transaction(true)) {
      dberrprint(&db, __LINE__, "DB::end_transaction");
      err = true;
    }
    if (visitoriterator.cnt() != cnt) {
      dberrprint(&db, __LINE__, "DB::iterate");
      err = true;
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
  }
  if (etc) {
    oprintf("traversing the database by the outer cursor:\n");
    stime = kc::time();
    int64_t cnt = db.count();
    class VisitorCursor : public kc::DB::Visitor {
     public:
      explicit VisitorCursor(int64_t rnum, bool rnd) :
          rnum_(rnum), rnd_(rnd), cnt_(0), rbuf_() {
        std::memset(rbuf_, '-', sizeof(rbuf_));
      }
      int64_t cnt() {
        return cnt_;
      }
     private:
      const char* visit_full(const char* kbuf, size_t ksiz,
                             const char* vbuf, size_t vsiz, size_t* sp) {
        cnt_++;
        const char* rv = NOP;
        switch (rnd_ ? myrand(7) : cnt_ % 7) {
          case 0: {
            rv = rbuf_;
            *sp = rnd_ ? myrand(sizeof(rbuf_)) : sizeof(rbuf_) / (cnt_ % 5 + 1);
            break;
          }
          case 1: {
            rv = REMOVE;
            break;
          }
        }
        if (rnum_ > 250 && cnt_ % (rnum_ / 250) == 0) {
          oputchar('.');
          if (cnt_ == rnum_ || cnt_ % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)cnt_);
        }
        return rv;
      }
      int64_t rnum_;
      bool rnd_;
      int64_t cnt_;
      char rbuf_[RECBUFSIZ];
    } visitorcursor(rnum, rnd);
    if (tran && !db.begin_transaction(false)) {
      dberrprint(&db, __LINE__, "DB::begin_transaction");
      err = true;
    }
    typename PROTODB::Cursor cur(&db);
    if (!cur.jump() && db.error() != kc::BasicDB::Error::NOREC) {
      dberrprint(&db, __LINE__, "Cursor::jump");
      err = true;
    }
    kc::DB::Cursor* paracur = db.cursor();
    int64_t range = rnum * thnum;
    while (!err && cur.accept(&visitorcursor, true, !rnd)) {
      if (rnd) {
        char kbuf[RECBUFSIZ];
        size_t ksiz = std::sprintf(kbuf, "%08lld", (long long)myrand(range));
        switch (myrand(3)) {
          case 0: {
            if (!db.remove(kbuf, ksiz) && db.error() != kc::BasicDB::Error::NOREC) {
              dberrprint(&db, __LINE__, "DB::remove");
              err = true;
            }
            break;
          }
          case 1: {
            if (!paracur->jump(kbuf, ksiz) && db.error() != kc::BasicDB::Error::NOREC) {
              dberrprint(&db, __LINE__, "Cursor::jump");
              err = true;
            }
            break;
          }
          default: {
            if (!cur.step() && db.error() != kc::BasicDB::Error::NOREC) {
              dberrprint(&db, __LINE__, "Cursor::step");
              err = true;
            }
            break;
          }
        }
      }
    }
    if (db.error() != kc::BasicDB::Error::NOREC) {
      dberrprint(&db, __LINE__, "Cursor::accept");
      err = true;
    }
    oprintf(" (end)\n");
    delete paracur;
    if (tran && !db.end_transaction(true)) {
      dberrprint(&db, __LINE__, "DB::end_transaction");
      err = true;
    }
    if (!rnd && visitorcursor.cnt() != cnt) {
      dberrprint(&db, __LINE__, "Cursor::accept");
      err = true;
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
  }
  if (etc) {
    oprintf("synchronizing the database:\n");
    stime = kc::time();
    if (!db.synchronize(false, NULL)) {
      dberrprint(&db, __LINE__, "DB::synchronize");
      err = true;
    }
    class SyncProcessor : public kc::BasicDB::FileProcessor {
     public:
      explicit SyncProcessor(int64_t rnum, bool rnd, int64_t size) :
          rnum_(rnum), rnd_(rnd), size_(size) {}
     private:
      bool process(const std::string& path, int64_t count, int64_t size) {
        if (size != size_) return false;
        return true;
      }
      int64_t rnum_;
      bool rnd_;
      int64_t size_;
    } syncprocessor(rnum, rnd, db.size());
    if (!db.synchronize(false, &syncprocessor)) {
      dberrprint(&db, __LINE__, "DB::synchronize");
      err = true;
    }
    if (!db.occupy(rnd ? myrand(2) == 0 : true, &syncprocessor)) {
      dberrprint(&db, __LINE__, "DB::occupy");
      err = true;
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
  }
  if (etc && db.size() < (256LL << 20)) {
    oprintf("dumping records into snapshot:\n");
    stime = kc::time();
    std::ostringstream ostrm;
    if (!db.dump_snapshot(&ostrm)) {
      dberrprint(&db, __LINE__, "DB::dump_snapshot");
      err = true;
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
    oprintf("loading records from snapshot:\n");
    stime = kc::time();
    int64_t cnt = db.count();
    if (rnd && myrand(2) == 0 && !db.clear()) {
      dberrprint(&db, __LINE__, "DB::clear");
      err = true;
    }
    const std::string& str = ostrm.str();
    std::istringstream istrm(str);
    if (!db.load_snapshot(&istrm) || db.count() != cnt) {
      dberrprint(&db, __LINE__, "DB::load_snapshot");
      err = true;
    }
    etime = kc::time();
    dbmetaprint(&db, false);
    oprintf("time: %.3f\n", etime - stime);
  }
  oprintf("removing records:\n");
  stime = kc::time();
  class ThreadRemove : public kc::Thread {
   public:
    void setparams(int32_t id, kc::BasicDB* db, int64_t rnum, int32_t thnum,
                   bool rnd, bool etc, bool tran) {
      id_ = id;
      db_ = db;
      rnum_ = rnum;
      thnum_ = thnum;
      err_ = false;
      rnd_ = rnd;
      etc_ = etc;
      tran_ = tran;
    }
    bool error() {
      return err_;
    }
    void run() {
      int64_t base = id_ * rnum_;
      int64_t range = rnum_ * thnum_;
      for (int64_t i = 1; !err_ && i <= rnum_; i++) {
        if (tran_ && !db_->begin_transaction(false)) {
          dberrprint(db_, __LINE__, "DB::begin_transaction");
          err_ = true;
        }
        char kbuf[RECBUFSIZ];
        size_t ksiz = std::sprintf(kbuf, "%08lld",
                                   (long long)(rnd_ ? myrand(range) + 1 : base + i));
        if (!db_->remove(kbuf, ksiz) &&
            ((!rnd_ && !etc_) || db_->error() != kc::BasicDB::Error::NOREC)) {
          dberrprint(db_, __LINE__, "DB::remove");
          err_ = true;
        }
        if (rnd_ && i % 8 == 0) {
          switch (myrand(8)) {
            case 0: {
              if (!db_->set(kbuf, ksiz, kbuf, ksiz)) {
                dberrprint(db_, __LINE__, "DB::set");
                err_ = true;
              }
              break;
            }
            case 1: {
              if (!db_->append(kbuf, ksiz, kbuf, ksiz)) {
                dberrprint(db_, __LINE__, "DB::append");
                err_ = true;
              }
              break;
            }
            case 2: {
              if (!db_->remove(kbuf, ksiz) &&
                  db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "DB::remove");
                err_ = true;
              }
              break;
            }
            case 3: {
              kc::DB::Cursor* cur = db_->cursor();
              if (cur->jump(kbuf, ksiz)) {
                switch (myrand(8)) {
                  default: {
                    size_t rsiz;
                    char* rbuf = cur->get_key(&rsiz, myrand(10) == 0);
                    if (rbuf) {
                      delete[] rbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get_key");
                      err_ = true;
                    }
                    break;
                  }
                  case 1: {
                    size_t rsiz;
                    char* rbuf = cur->get_value(&rsiz, myrand(10) == 0);
                    if (rbuf) {
                      delete[] rbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get_value");
                      err_ = true;
                    }
                    break;
                  }
                  case 2: {
                    size_t rksiz;
                    const char* rvbuf;
                    size_t rvsiz;
                    char* rkbuf = cur->get(&rksiz, &rvbuf, &rvsiz, myrand(10) == 0);
                    if (rkbuf) {
                      delete[] rkbuf;
                    } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get");
                      err_ = true;
                    }
                    break;
                  }
                  case 3: {
                    std::string key, value;
                    if (!cur->get(&key, &value, myrand(10) == 0) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::get");
                      err_ = true;
                    }
                    break;
                  }
                  case 4: {
                    if (myrand(8) == 0 && !cur->remove() &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::remove");
                      err_ = true;
                    }
                    break;
                  }
                }
              } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              }
              delete cur;
              break;
            }
            default: {
              size_t vsiz;
              char* vbuf = db_->get(kbuf, ksiz, &vsiz);
              if (vbuf) {
                delete[] vbuf;
              } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "DB::get");
                err_ = true;
              }
              break;
            }
          }
        }
        if (tran_ && !db_->end_transaction(true)) {
          dberrprint(db_, __LINE__, "DB::end_transaction");
          err_ = true;
        }
        if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
          oputchar('.');
          if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
        }
      }
    }
   private:
    int32_t id_;
    kc::BasicDB* db_;
    int64_t rnum_;
    int32_t thnum_;
    bool err_;
    bool rnd_;
    bool etc_;
    bool tran_;
  };
  ThreadRemove threadremoves[THREADMAX];
  if (thnum < 2) {
    threadremoves[0].setparams(0, &db, rnum, thnum, rnd, etc, tran);
    threadremoves[0].run();
    if (threadremoves[0].error()) err = true;
  } else {
    for (int32_t i = 0; i < thnum; i++) {
      threadremoves[i].setparams(i, &db, rnum, thnum, rnd, etc, tran);
      threadremoves[i].start();
    }
    for (int32_t i = 0; i < thnum; i++) {
      threadremoves[i].join();
      if (threadremoves[i].error()) err = true;
    }
  }
  etime = kc::time();
  dbmetaprint(&db, true);
  oprintf("time: %.3f\n", etime - stime);
  oprintf("closing the database:\n");
  stime = kc::time();
  if (!db.close()) {
    dberrprint(&db, __LINE__, "DB::close");
    err = true;
  }
  etime = kc::time();
  oprintf("time: %.3f\n", etime - stime);
  oprintf("%s\n\n", err ? "error" : "ok");
  return err ? 1 : 0;
}


// perform queue command
template <class PROTODB>
static int32_t procqueue(const char* tname, int64_t rnum, int32_t thnum, int32_t itnum,
                         bool rnd) {
  oprintf("<%s Queue Test>\n  seed=%u  rnum=%lld  thnum=%d  itnum=%d  rnd=%d\n\n",
          tname, g_randseed, (long long)rnum, thnum, itnum, rnd);
  bool err = false;
  PROTODB db;
  for (int32_t itcnt = 1; itcnt <= itnum; itcnt++) {
    if (itnum > 1) oprintf("iteration %d:\n", itcnt);
    double stime = kc::time();
    uint32_t omode = PROTODB::OWRITER | PROTODB::OCREATE;
    if (itcnt == 1) omode |= PROTODB::OTRUNCATE;
    if (!db.open("-", omode)) {
      dberrprint(&db, __LINE__, "DB::open");
      err = true;
    }
    class ThreadQueue : public kc::Thread {
     public:
      void setparams(int32_t id, PROTODB* db, int64_t rnum, int32_t thnum, bool rnd,
                     int64_t width) {
        id_ = id;
        db_ = db;
        rnum_ = rnum;
        thnum_ = thnum;
        rnd_ = rnd;
        width_ = width;
        err_ = false;
      }
      bool error() {
        return err_;
      }
      void run() {
        kc::DB::Cursor* cur = db_->cursor();
        int64_t base = id_ * rnum_;
        int64_t range = rnum_ * thnum_;
        for (int64_t i = 1; !err_ && i <= rnum_; i++) {
          char kbuf[RECBUFSIZ];
          size_t ksiz = std::sprintf(kbuf, "%010lld", (long long)(base + i));
          if (!db_->set(kbuf, ksiz, kbuf, ksiz)) {
            dberrprint(db_, __LINE__, "DB::set");
            err_ = true;
          }
          if (rnd_) {
            if (myrand(width_ / 2) == 0) {
              if (!cur->jump() && db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              }
              ksiz = std::sprintf(kbuf, "%010lld", (long long)myrand(range) + 1);
              switch (myrand(10)) {
                case 0: {
                  if (!db_->set(kbuf, ksiz, kbuf, ksiz)) {
                    dberrprint(db_, __LINE__, "DB::set");
                    err_ = true;
                  }
                  break;
                }
                case 1: {
                  if (!db_->append(kbuf, ksiz, kbuf, ksiz)) {
                    dberrprint(db_, __LINE__, "DB::append");
                    err_ = true;
                  }
                  break;
                }
                case 2: {
                  if (!db_->remove(kbuf, ksiz) &&
                      db_->error() != kc::BasicDB::Error::NOREC) {
                    dberrprint(db_, __LINE__, "DB::remove");
                    err_ = true;
                  }
                  break;
                }
              }
              int64_t dnum = myrand(width_) + 2;
              for (int64_t j = 0; j < dnum; j++) {
                if (myrand(2) == 0) {
                  size_t rsiz;
                  char* rbuf = cur->get_key(&rsiz);
                  if (rbuf) {
                    if (myrand(10) == 0 && !db_->remove(rbuf, rsiz) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "DB::remove");
                      err_ = true;
                    }
                    if (myrand(2) == 0 && !cur->jump(rbuf, rsiz) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::jump");
                      err_ = true;
                    }
                    if (myrand(10) == 0 && !db_->remove(rbuf, rsiz) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "DB::remove");
                      err_ = true;
                    }
                    delete[] rbuf;
                  } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                    dberrprint(db_, __LINE__, "Cursor::get_key");
                    err_ = true;
                  }
                }
                if (!cur->remove() && db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "Cursor::remove");
                  err_ = true;
                }
              }
            }
          } else {
            if (i > width_) {
              if (!cur->jump() && db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              }
              if (!cur->remove() && db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::remove");
                err_ = true;
              }
            }
          }
          if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
            oputchar('.');
            if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
          }
        }
        delete cur;
      }
     private:
      int32_t id_;
      PROTODB* db_;
      int64_t rnum_;
      int32_t thnum_;
      bool rnd_;
      int64_t width_;
      bool err_;
    };
    int64_t width = rnum / 10;
    ThreadQueue threads[THREADMAX];
    if (thnum < 2) {
      threads[0].setparams(0, &db, rnum, thnum, rnd, width);
      threads[0].run();
      if (threads[0].error()) err = true;
    } else {
      for (int32_t i = 0; i < thnum; i++) {
        threads[i].setparams(i, &db, rnum, thnum, rnd, width);
        threads[i].start();
      }
      for (int32_t i = 0; i < thnum; i++) {
        threads[i].join();
        if (threads[i].error()) err = true;
      }
    }
    int64_t count = db.count();
    if (!rnd && itcnt == 1 && count != width * thnum) {
      dberrprint(&db, __LINE__, "DB::count");
      err = true;
    }
    if ((rnd ? (myrand(2) == 0) : itcnt == itnum) && count > 0) {
      kc::DB::Cursor* cur = db.cursor();
      if (!cur->jump()) {
        dberrprint(&db, __LINE__, "Cursor::jump");
        err = true;
      }
      for (int64_t i = 1; i <= count; i++) {
        if (!cur->remove()) {
          dberrprint(&db, __LINE__, "Cursor::remove");
          err = true;
        }
        if (rnum > 250 && i % (rnum / 250) == 0) {
          oputchar('.');
          if (i == rnum || i % (rnum / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
        }
      }
      if (rnd) oprintf(" (end)\n");
      delete cur;
      if (db.count() != 0) {
        dberrprint(&db, __LINE__, "DB::count");
        err = true;
      }
    }
    dbmetaprint(&db, itcnt == itnum);
    if (!db.close()) {
      dberrprint(&db, __LINE__, "DB::close");
      err = true;
    }
    oprintf("time: %.3f\n", kc::time() - stime);
  }
  oprintf("%s\n\n", err ? "error" : "ok");
  return err ? 1 : 0;
}


// perform wicked command
template <class PROTODB>
static int32_t procwicked(const char* tname, int64_t rnum, int32_t thnum, int32_t itnum) {
  oprintf("<%s Wicked Test>\n  seed=%u  rnum=%lld  thnum=%d  itnum=%d\n\n",
          tname, g_randseed, (long long)rnum, thnum, itnum);
  bool err = false;
  PROTODB db;
  for (int32_t itcnt = 1; itcnt <= itnum; itcnt++) {
    if (itnum > 1) oprintf("iteration %d:\n", itcnt);
    double stime = kc::time();
    uint32_t omode = kc::BasicDB::OWRITER | kc::BasicDB::OCREATE;
    if (itcnt == 1) omode |= kc::BasicDB::OTRUNCATE;
    if (!db.open("-", omode)) {
      dberrprint(&db, __LINE__, "DB::open");
      err = true;
    }
    class ThreadWicked : public kc::Thread {
     public:
      void setparams(int32_t id, PROTODB* db, int64_t rnum, int32_t thnum,
                     const char* lbuf) {
        id_ = id;
        db_ = db;
        rnum_ = rnum;
        thnum_ = thnum;
        lbuf_ = lbuf;
        err_ = false;
      }
      bool error() {
        return err_;
      }
      void run() {
        kc::DB::Cursor* cur = db_->cursor();
        int64_t range = rnum_ * thnum_ / 2;
        for (int64_t i = 1; !err_ && i <= rnum_; i++) {
          bool tran = myrand(100) == 0;
          if (tran) {
            if (myrand(2) == 0) {
              if (!db_->begin_transaction(myrand(rnum_) == 0)) {
                dberrprint(db_, __LINE__, "DB::begin_transaction");
                tran = false;
                err_ = true;
              }
            } else {
              if (!db_->begin_transaction_try(myrand(rnum_) == 0)) {
                if (db_->error() != kc::BasicDB::Error::LOGIC) {
                  dberrprint(db_, __LINE__, "DB::begin_transaction_try");
                  err_ = true;
                }
                tran = false;
              }
            }
          }
          char kbuf[RECBUFSIZ];
          size_t ksiz = std::sprintf(kbuf, "%lld", (long long)(myrand(range) + 1));
          if (myrand(1000) == 0) {
            ksiz = myrand(RECBUFSIZ) + 1;
            if (myrand(2) == 0) {
              for (size_t j = 0; j < ksiz; j++) {
                kbuf[j] = j;
              }
            } else {
              for (size_t j = 0; j < ksiz; j++) {
                kbuf[j] = myrand(256);
              }
            }
          }
          const char* vbuf = kbuf;
          size_t vsiz = ksiz;
          if (myrand(10) == 0) {
            vbuf = lbuf_;
            vsiz = myrand(RECBUFSIZL) / (myrand(5) + 1);
          }
          do {
            switch (myrand(10)) {
              case 0: {
                if (!db_->set(kbuf, ksiz, vbuf, vsiz)) {
                  dberrprint(db_, __LINE__, "DB::set");
                  err_ = true;
                }
                break;
              }
              case 1: {
                if (!db_->add(kbuf, ksiz, vbuf, vsiz) &&
                    db_->error() != kc::BasicDB::Error::DUPREC) {
                  dberrprint(db_, __LINE__, "DB::add");
                  err_ = true;
                }
                break;
              }
              case 2: {
                if (!db_->replace(kbuf, ksiz, vbuf, vsiz) &&
                    db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "DB::replace");
                  err_ = true;
                }
                break;
              }
              case 3: {
                if (!db_->append(kbuf, ksiz, vbuf, vsiz)) {
                  dberrprint(db_, __LINE__, "DB::append");
                  err_ = true;
                }
                break;
              }
              case 4: {
                if (myrand(2) == 0) {
                  int64_t num = myrand(rnum_);
                  int64_t orig = myrand(10) == 0 ? kc::INT64MIN : myrand(rnum_);
                  if (myrand(10) == 0) orig = orig == kc::INT64MIN ? kc::INT64MAX : -orig;
                  if (db_->increment(kbuf, ksiz, num, orig) == kc::INT64MIN &&
                      db_->error() != kc::BasicDB::Error::LOGIC) {
                    dberrprint(db_, __LINE__, "DB::increment");
                    err_ = true;
                  }
                } else {
                  double num = myrand(rnum_ * 10) / (myrand(rnum_) + 1.0);
                  double orig = myrand(10) == 0 ? -kc::inf() : myrand(rnum_);
                  if (myrand(10) == 0) orig = -orig;
                  if (kc::chknan(db_->increment_double(kbuf, ksiz, num, orig)) &&
                      db_->error() != kc::BasicDB::Error::LOGIC) {
                    dberrprint(db_, __LINE__, "DB::increment_double");
                    err_ = true;
                  }
                }
                break;
              }
              case 5: {
                if (!db_->cas(kbuf, ksiz, kbuf, ksiz, vbuf, vsiz) &&
                    db_->error() != kc::BasicDB::Error::LOGIC) {
                  dberrprint(db_, __LINE__, "DB::cas");
                  err_ = true;
                }
                break;
              }
              case 6: {
                if (!db_->remove(kbuf, ksiz) &&
                    db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "DB::remove");
                  err_ = true;
                }
                break;
              }
              case 7: {
                if (myrand(2) == 0) {
                  if (db_->check(kbuf, ksiz) < 0 && db_->error() != kc::BasicDB::Error::NOREC) {
                    dberrprint(db_, __LINE__, "DB::check");
                    err_ = true;
                  }
                } else {
                  size_t rsiz;
                  char* rbuf = db_->seize(kbuf, ksiz, &rsiz);
                  if (rbuf) {
                    delete[] rbuf;
                  } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                    dberrprint(db_, __LINE__, "DB::seize");
                    err_ = true;
                  }
                }
                break;
              }
              case 8: {
                if (myrand(10) == 0) {
                  if (myrand(4) == 0) {
                    if (!cur->jump_back(kbuf, ksiz) &&
                        db_->error() != kc::BasicDB::Error::NOIMPL &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::jump_back");
                      err_ = true;
                    }
                  } else {
                    if (!cur->jump(kbuf, ksiz) &&
                        db_->error() != kc::BasicDB::Error::NOREC) {
                      dberrprint(db_, __LINE__, "Cursor::jump");
                      err_ = true;
                    }
                  }
                } else {
                  class VisitorImpl : public kc::DB::Visitor {
                   public:
                    explicit VisitorImpl(const char* lbuf) : lbuf_(lbuf) {}
                   private:
                    const char* visit_full(const char* kbuf, size_t ksiz,
                                           const char* vbuf, size_t vsiz, size_t* sp) {
                      const char* rv = NOP;
                      switch (myrand(3)) {
                        case 0: {
                          rv = lbuf_;
                          *sp = myrand(RECBUFSIZL) / (myrand(5) + 1);
                          break;
                        }
                        case 1: {
                          rv = REMOVE;
                          break;
                        }
                      }
                      return rv;
                    }
                    const char* lbuf_;
                  } visitor(lbuf_);
                  if (!cur->accept(&visitor, true, myrand(2) == 0) &&
                      db_->error() != kc::BasicDB::Error::NOREC) {
                    dberrprint(db_, __LINE__, "Cursor::accept");
                    err_ = true;
                  }
                  if (myrand(5) > 0 && !cur->step() &&
                      db_->error() != kc::BasicDB::Error::NOREC) {
                    dberrprint(db_, __LINE__, "Cursor::step");
                    err_ = true;
                  }
                }
                break;
              }
              default: {
                size_t rsiz;
                char* rbuf = db_->get(kbuf, ksiz, &rsiz);
                if (rbuf) {
                  delete[] rbuf;
                } else if (db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "DB::get");
                  err_ = true;
                }
                break;
              }
            }
          } while (myrand(100) == 0);
          if (myrand(100) == 0) {
            int32_t jnum = myrand(10);
            switch (myrand(4)) {
              case 0: {
                std::map<std::string, std::string> recs;
                for (int32_t j = 0; j < jnum; j++) {
                  char jbuf[RECBUFSIZ];
                  size_t jsiz = std::sprintf(jbuf, "%lld", (long long)(myrand(range) + 1));
                  recs[std::string(jbuf, jsiz)] = std::string(kbuf, ksiz);
                }
                if (db_->set_bulk(recs, myrand(4)) != (int64_t)recs.size()) {
                  dberrprint(db_, __LINE__, "DB::set_bulk");
                  err_ = true;
                }
                break;
              }
              case 1: {
                std::vector<std::string> keys;
                for (int32_t j = 0; j < jnum; j++) {
                  char jbuf[RECBUFSIZ];
                  size_t jsiz = std::sprintf(jbuf, "%lld", (long long)(myrand(range) + 1));
                  keys.push_back(std::string(jbuf, jsiz));
                }
                if (db_->remove_bulk(keys, myrand(4)) < 0) {
                  dberrprint(db_, __LINE__, "DB::remove_bulk");
                  err_ = true;
                }
                break;
              }
              default: {
                std::vector<std::string> keys;
                for (int32_t j = 0; j < jnum; j++) {
                  char jbuf[RECBUFSIZ];
                  size_t jsiz = std::sprintf(jbuf, "%lld", (long long)(myrand(range) + 1));
                  keys.push_back(std::string(jbuf, jsiz));
                }
                std::map<std::string, std::string> recs;
                if (db_->get_bulk(keys, &recs, myrand(4)) < 0) {
                  dberrprint(db_, __LINE__, "DB::get_bulk");
                  err_ = true;
                }
                break;
              }
            }
          }
          if (i == rnum_ / 2) {
            if (myrand(thnum_ * 4) == 0) {
              if (!db_->clear()) {
                dberrprint(db_, __LINE__, "DB::clear");
                err_ = true;
              }
            } else {
              class SyncProcessor : public kc::BasicDB::FileProcessor {
               private:
                bool process(const std::string& path, int64_t count, int64_t size) {
                  yield();
                  return true;
                }
              } syncprocessor;
              if (!db_->synchronize(false, &syncprocessor)) {
                dberrprint(db_, __LINE__, "DB::synchronize");
                err_ = true;
              }
            }
          }
          if (tran) {
            yield();
            if (!db_->end_transaction(myrand(10) > 0)) {
              dberrprint(db_, __LINE__, "DB::end_transactin");
              err_ = true;
            }
          }
          if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
            oputchar('.');
            if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
          }
        }
        delete cur;
      }
     private:
      int32_t id_;
      PROTODB* db_;
      int64_t rnum_;
      int32_t thnum_;
      const char* lbuf_;
      bool err_;
    };
    char lbuf[RECBUFSIZL];
    std::memset(lbuf, '*', sizeof(lbuf));
    ThreadWicked threads[THREADMAX];
    if (thnum < 2) {
      threads[0].setparams(0, &db, rnum, thnum, lbuf);
      threads[0].run();
      if (threads[0].error()) err = true;
    } else {
      for (int32_t i = 0; i < thnum; i++) {
        threads[i].setparams(i, &db, rnum, thnum, lbuf);
        threads[i].start();
      }
      for (int32_t i = 0; i < thnum; i++) {
        threads[i].join();
        if (threads[i].error()) err = true;
      }
    }
    dbmetaprint(&db, itcnt == itnum);
    if (!db.close()) {
      dberrprint(&db, __LINE__, "DB::close");
      err = true;
    }
    oprintf("time: %.3f\n", kc::time() - stime);
  }
  oprintf("%s\n\n", err ? "error" : "ok");
  return err ? 1 : 0;
}


// perform order command
template <class PROTODB>
static int32_t proctran(const char* tname, int64_t rnum, int32_t thnum, int32_t itnum) {
  oprintf("<%s Transaction Test>\n  seed=%u  rnum=%lld  thnum=%d  itnum=%d\n\n",
          tname, g_randseed, (long long)rnum, thnum, itnum);
  bool err = false;
  PROTODB db;
  PROTODB paradb;
  for (int32_t itcnt = 1; itcnt <= itnum; itcnt++) {
    oprintf("iteration %d updating:\n", itcnt);
    double stime = kc::time();
    uint32_t omode = kc::BasicDB::OWRITER | kc::BasicDB::OCREATE;
    if (itcnt == 1) omode |= kc::BasicDB::OTRUNCATE;
    if (!db.open("-", omode)) {
      dberrprint(&db, __LINE__, "DB::open");
      err = true;
    }
    if (!paradb.open("para", omode)) {
      dberrprint(&paradb, __LINE__, "DB::open");
      err = true;
    }
    class ThreadTran : public kc::Thread {
     public:
      void setparams(int32_t id, PROTODB* db, PROTODB* paradb, int64_t rnum,
                     int32_t thnum, const char* lbuf) {
        id_ = id;
        db_ = db;
        paradb_ = paradb;
        rnum_ = rnum;
        thnum_ = thnum;
        lbuf_ = lbuf;
        err_ = false;
      }
      bool error() {
        return err_;
      }
      void run() {
        kc::DB::Cursor* cur = db_->cursor();
        int64_t range = rnum_ * thnum_;
        char kbuf[RECBUFSIZ];
        size_t ksiz = std::sprintf(kbuf, "%lld", (long long)(myrand(range) + 1));
        if (!cur->jump(kbuf, ksiz) && db_->error() != kc::BasicDB::Error::NOREC) {
          dberrprint(db_, __LINE__, "Cursor::jump");
          err_ = true;
        }
        bool tran = true;
        if (!db_->begin_transaction(false)) {
          dberrprint(db_, __LINE__, "DB::begin_transaction");
          tran = false;
          err_ = true;
        }
        bool commit = myrand(10) > 0;
        for (int64_t i = 1; !err_ && i <= rnum_; i++) {
          ksiz = std::sprintf(kbuf, "%lld", (long long)(myrand(range) + 1));
          const char* vbuf = kbuf;
          size_t vsiz = ksiz;
          if (myrand(10) == 0) {
            vbuf = lbuf_;
            vsiz = myrand(RECBUFSIZL) / (myrand(5) + 1);
          }
          class VisitorImpl : public kc::DB::Visitor {
           public:
            explicit VisitorImpl(const char* vbuf, size_t vsiz, kc::BasicDB* paradb) :
                vbuf_(vbuf), vsiz_(vsiz), paradb_(paradb) {}
           private:
            const char* visit_full(const char* kbuf, size_t ksiz,
                                   const char* vbuf, size_t vsiz, size_t* sp) {
              return visit_empty(kbuf, ksiz, sp);
            }
            const char* visit_empty(const char* kbuf, size_t ksiz, size_t* sp) {
              const char* rv = NOP;
              switch (myrand(3)) {
                case 0: {
                  rv = vbuf_;
                  *sp = vsiz_;
                  if (paradb_) paradb_->set(kbuf, ksiz, vbuf_, vsiz_);
                  break;
                }
                case 1: {
                  rv = REMOVE;
                  if (paradb_) paradb_->remove(kbuf, ksiz);
                  break;
                }
              }
              return rv;
            }
            const char* vbuf_;
            size_t vsiz_;
            kc::BasicDB* paradb_;
          } visitor(vbuf, vsiz, !tran || commit ? paradb_ : NULL);
          if (myrand(4) == 0) {
            if (!cur->accept(&visitor, true, myrand(2) == 0) &&
                db_->error() != kc::BasicDB::Error::NOREC) {
              dberrprint(db_, __LINE__, "Cursor::accept");
              err_ = true;
            }
          } else {
            if (!db_->accept(kbuf, ksiz, &visitor, true)) {
              dberrprint(db_, __LINE__, "DB::accept");
              err_ = true;
            }
          }
          if (myrand(1000) == 0) {
            ksiz = std::sprintf(kbuf, "%lld", (long long)(myrand(range) + 1));
            if (!cur->jump(kbuf, ksiz)) {
              if (db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              } else if (!cur->jump() && db_->error() != kc::BasicDB::Error::NOREC) {
                dberrprint(db_, __LINE__, "Cursor::jump");
                err_ = true;
              }
            }
            std::vector<std::string> keys;
            keys.reserve(100);
            while (myrand(50) != 0) {
              std::string key;
              if (cur->get_key(&key)) {
                keys.push_back(key);
                if (!cur->get_value(&key) && kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "Cursor::get_value");
                  err_ = true;
                }
              } else {
                if (db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "Cursor::get_key");
                  err_ = true;
                }
                break;
              }
              if (!cur->step()) {
                if (db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "Cursor::jump");
                  err_ = true;
                }
                break;
              }
            }
            class Remover : public kc::DB::Visitor {
             public:
              explicit Remover(kc::BasicDB* paradb) : paradb_(paradb) {}
             private:
              const char* visit_full(const char* kbuf, size_t ksiz,
                                     const char* vbuf, size_t vsiz, size_t* sp) {
                if (myrand(200) == 0) return NOP;
                if (paradb_) paradb_->remove(kbuf, ksiz);
                return REMOVE;
              }
              kc::BasicDB* paradb_;
            } remover(!tran || commit ? paradb_ : NULL);
            std::vector<std::string>::iterator it = keys.begin();
            std::vector<std::string>::iterator end = keys.end();
            while (it != end) {
              if (myrand(50) == 0) {
                if (!cur->accept(&remover, true, false) &&
                    db_->error() != kc::BasicDB::Error::NOREC) {
                  dberrprint(db_, __LINE__, "Cursor::accept");
                  err_ = true;
                }
              } else {
                if (!db_->accept(it->c_str(), it->size(), &remover, true)) {
                  dberrprint(db_, __LINE__, "DB::accept");
                  err_ = true;
                }
              }
              ++it;
            }
          }
          if (tran && myrand(100) == 0) {
            if (db_->end_transaction(commit)) {
              yield();
              if (!db_->begin_transaction(false)) {
                dberrprint(db_, __LINE__, "DB::begin_transaction");
                tran = false;
                err_ = true;
              }
            } else {
              dberrprint(db_, __LINE__, "DB::end_transaction");
              err_ = true;
            }
          }
          if (id_ < 1 && rnum_ > 250 && i % (rnum_ / 250) == 0) {
            oputchar('.');
            if (i == rnum_ || i % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)i);
          }
        }
        if (tran && !db_->end_transaction(commit)) {
          dberrprint(db_, __LINE__, "DB::end_transaction");
          err_ = true;
        }
        delete cur;
      }
     private:
      int32_t id_;
      PROTODB* db_;
      PROTODB* paradb_;
      int64_t rnum_;
      int32_t thnum_;
      const char* lbuf_;
      bool err_;
    };
    char lbuf[RECBUFSIZL];
    std::memset(lbuf, '*', sizeof(lbuf));
    ThreadTran threads[THREADMAX];
    if (thnum < 2) {
      threads[0].setparams(0, &db, &paradb, rnum, thnum, lbuf);
      threads[0].run();
      if (threads[0].error()) err = true;
    } else {
      for (int32_t i = 0; i < thnum; i++) {
        threads[i].setparams(i, &db, &paradb, rnum, thnum, lbuf);
        threads[i].start();
      }
      for (int32_t i = 0; i < thnum; i++) {
        threads[i].join();
        if (threads[i].error()) err = true;
      }
    }
    oprintf("iteration %d checking:\n", itcnt);
    if (db.count() != paradb.count()) {
      dberrprint(&db, __LINE__, "DB::count");
      err = true;
    }
    class VisitorImpl : public kc::DB::Visitor {
     public:
      explicit VisitorImpl(int64_t rnum, kc::BasicDB* paradb) :
          rnum_(rnum), paradb_(paradb), err_(false), cnt_(0) {}
      bool error() {
        return err_;
      }
     private:
      const char* visit_full(const char* kbuf, size_t ksiz,
                             const char* vbuf, size_t vsiz, size_t* sp) {
        cnt_++;
        size_t rsiz;
        char* rbuf = paradb_->get(kbuf, ksiz, &rsiz);
        if (rbuf) {
          delete[] rbuf;
        } else {
          dberrprint(paradb_, __LINE__, "DB::get");
          err_ = true;
        }
        if (rnum_ > 250 && cnt_ % (rnum_ / 250) == 0) {
          oputchar('.');
          if (cnt_ == rnum_ || cnt_ % (rnum_ / 10) == 0) oprintf(" (%08lld)\n", (long long)cnt_);
        }
        return NOP;
      }
      int64_t rnum_;
      kc::BasicDB* paradb_;
      bool err_;
      int64_t cnt_;
    } visitor(rnum, &paradb), paravisitor(rnum, &db);
    if (!db.iterate(&visitor, false)) {
      dberrprint(&db, __LINE__, "DB::iterate");
      err = true;
    }
    oprintf(" (end)\n");
    if (visitor.error()) err = true;
    if (!paradb.iterate(&paravisitor, false)) {
      dberrprint(&db, __LINE__, "DB::iterate");
      err = true;
    }
    oprintf(" (end)\n");
    if (paravisitor.error()) err = true;
    if (!paradb.close()) {
      dberrprint(&paradb, __LINE__, "DB::close");
      err = true;
    }
    dbmetaprint(&db, itcnt == itnum);
    if (!db.close()) {
      dberrprint(&db, __LINE__, "DB::close");
      err = true;
    }
    oprintf("time: %.3f\n", kc::time() - stime);
  }
  oprintf("%s\n\n", err ? "error" : "ok");
  return err ? 1 : 0;
}



// END OF FILE

enum Token {
  EOF = -1,

  ID = 0,
  INT = 1,
  FLT = 2,
  KWD = 3,
};

typedef struct token {
  int type;
  char* line;
  void* value;
  unsigned long long line_num;
  unsigned long long colm_num;
};

static 


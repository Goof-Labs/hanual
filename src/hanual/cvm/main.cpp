#include "parse.cpp"

int main(void)
{
    Hanual::HanualFile *file = new Hanual::HanualFile("test.txt");
    file->print();
}

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct HanualFileSpec HanualFileSpec;

struct HanualFileSpec
{
    char magicNumber[4];
    char checkSum[44];
    uint8_t vMajor;
    uint8_t vMinor;
    uint8_t vMicro;
};

static void parseHeader(HanualFileSpec *spc, FILE *fh)
{

    fread((void *)(spc->magicNumber), sizeof(char), 4, fh);
    fread((void *)(spc->checkSum), sizeof(char), 44, fh);

    // version
    char b;
    fread(&b, sizeof(uint8_t), 1, fh);
    spc->vMajor = (uint8_t)b;

    fread(&b, sizeof(uint8_t), 1, fh);
    spc->vMinor = (uint8_t)b;

    fread(&b, sizeof(uint8_t), 1, fh);
    spc->vMicro = (uint8_t)b;
}

void parseFile(const char *fp)
{
    FILE *fh;
    fh = fopen(fp, "rb");

    HanualFileSpec *hfs = malloc(sizeof(HanualFileSpec));

    parseHeader(hfs, fh);

    fclose(fh);
}

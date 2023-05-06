#ifndef __INC_parse__

#define __INC_parse__

#include "constants.cpp"
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>

namespace Hanual
{
    class HanualFile
    {
    private:
        std::vector<Hanual::HanualConstant> consts;
        char magicNumber[4];
        char checkSum[44];
        uint8_t vMajor;
        uint8_t vMinor;
        uint8_t vMicro;

        void parseHeader(FILE *fh)
        {
            // read magic num
            char buffer1[4];
            fread(buffer1, 1, 4, fh);
            for (uint8_t i = 0; i < 4; i++)
                magicNumber[i] = (char)buffer1[i];

            // check sum
            char buffer2[44];
            fread(buffer2, 1, 44, fh);

            for (uint8_t i = 0; i < 44; i++)
                checkSum[i] = (char)buffer2[i];

            // version
            char versionBuffer[1];

            fread(versionBuffer, 1, 1, fh);
            vMajor = (char)versionBuffer[0];

            fread(versionBuffer, 1, 1, fh);
            vMinor = (char)versionBuffer[0];

            fread(versionBuffer, 1, 1, fh);
            vMicro = (char)versionBuffer[0];
        }

    public:
        HanualFile(const char *fp)
        {
            FILE *fh;
            fh = fopen(fp, "rb");

            parseHeader(fh);

            fclose(fh);
        }
    };
}
#endif

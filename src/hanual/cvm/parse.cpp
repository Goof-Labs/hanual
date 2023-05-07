#ifndef __INC_parse__

#define __INC_parse__

#include "constants.cpp"
#include <stdint.h>
#include <stdlib.h>
#include <iostream>
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
            vMajor = (uint8_t)versionBuffer[0];

            fread(versionBuffer, 1, 1, fh);
            vMinor = (uint8_t)versionBuffer[0];

            fread(versionBuffer, 1, 1, fh);
            vMicro = (uint8_t)versionBuffer[0];
        }

    public:
        HanualFile(const char *fp)
        {
            FILE *fh;
            fh = fopen(fp, "rb");

            parseHeader(fh);

            fclose(fh);
        }

        void print()
        {
            std::cout << "MAGIC-NUM:";

            for (uint8_t i = 0; i < 4; i++)
                std::cout << this->magicNumber[i];

            std::cout << std::endl;

            std::cout << "CHECK-SUM:";

            for (uint8_t i = 0; i < 44; i++)
                std::cout << this->checkSum[i];

            std::cout << std::endl;

            std::cout << "vMajor:" << this->vMajor + 0 << std::endl;
            std::cout << "vMinor:" << this->vMinor + 0 << std::endl;
            std::cout << "vMicro:" << this->vMicro + 0 << std::endl;
        }
    };
}

#endif

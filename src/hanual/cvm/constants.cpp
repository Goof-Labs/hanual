#include <stdint.h>
#include <iostream>
#include <sstream>

namespace Hanual
{
    class HanualConstant
    {
    private:
        void *value; // read only
        uint8_t type;

        // all these functions discard the first byte this is because
        // the type is still passed to the function
        void intFromBytes(uint8_t bytes[])
        {
            /* Intagers in the constant pool can be a maximum of 255 for some reason so this makes our life easier */
            this->value = (void *)(&bytes[1]);
        }

        void strFromBytes(uint8_t bytes[])
        {
            std::stringstream bffr;

            for (unsigned int idx = 1; true; idx++)
            {
                if (bytes[idx] == 0)
                    break;

                bffr << bytes[idx];
            }

            this->value = (void *)bffr.str().c_str();
        }

        void fltFromBytes(uint8_t bytes[])
        {
            uint8_t denom = bytes[1];
            uint8_t numer = bytes[2];
            this->value = (void *)(denom / numer);
        }

    public:
        HanualConstant(char bytes[1024])
        {
            switch (bytes[0])
            {
            case (0x00):
                intFromBytes((unsigned char *)&bytes);
                type = 0;
                break;

            case (0x01):
                strFromBytes((unsigned char *)&bytes);
                type = 1;
                break;

            case (0x02):
                fltFromBytes((unsigned char *)&bytes);
                type = 2;
                break;

            default:
                break;
            };
        }

        void print()
        {
            std::cout << "TYPE:" << type + 0 << "\n";
        }
    };
} // namespace Hanual

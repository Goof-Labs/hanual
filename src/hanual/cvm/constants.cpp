#include <stdint.h>
#include <sstream>
#include <memory>
#include <vector>

namespace Hanual
{
    class HanualConstant
    {
    private:
        void *value; // read only

        // all these functions discard the first byte this is because
        // the type is still passed to the function
        void intFromBytes(uint8_t bytes[], uint16_t length)
        {
            /* Intagers in the constant pool can be a maximum of 255 for some reason so this makes our life easier */
            this->value = (void *)(&bytes[1]);
        }

        void strFromBytes(uint8_t bytes[], uint16_t length)
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

        void fltFromBytes(uint8_t bytes[], uint16_t length)
        {
            uint8_t denom = bytes[1];
            uint8_t numer = bytes[2];
            this->value = (void *)(denom / numer);
        }

    public:
        HanualConstant(uint8_t bytes[], uint16_t length)
        {
            switch (bytes[0])
            {
            case (0x00):
                intFromBytes(bytes, length);
                break;

            case (0x01):
                strFromBytes(bytes, length);
                break;

            case (0x02):
                fltFromBytes(bytes, length);
                break;

            default:
                break;
            };
        }
    };

    std::vector<HanualConstant> constantsFromBytes(uint8_t bytes[], uint8_t num)
    {
        std::vector<HanualConstant>
            vec;
    }
} // namespace Hanual

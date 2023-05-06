#include <stdint.h>

namespace Hanual
{
    class HanualConstant
    {
    private:
        void *value; // read only

        // all these functions discard the first byte this is because
        // the type is still passed to the function
        void intFromBytes(uint8_t bytes[], uint16_t length) {}
        void strFromBytes(uint8_t bytes[], uint16_t length) {}
        void fltFromBytes(uint8_t bytes[], uint16_t length) {}

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
} // namespace Hanual

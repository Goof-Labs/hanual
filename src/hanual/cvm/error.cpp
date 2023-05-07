#ifndef __INC_error__

#define __INC_error__

#include "include/colorPrint.hpp"
#include "string"

namespace Hanual
{
    class Error
    {
    private:
        char *msg;

    public:
        Error(std::string msg)
        {
            this->msg = (char *)msg.c_str();
        }

        void beRaised()
        {
            print_color(color_red);
            std::cout << "RUNTIME-ERROR: " << this->msg << std::endl;
            print_color_reset();
        }
    };
} // namespace Hanual

#endif

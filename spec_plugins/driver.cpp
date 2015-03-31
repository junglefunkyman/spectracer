#include <iostream>

class Driver {
    public:
        void connect(){
            std::cout << "Connected" << std::endl;
        }

        double* read(){
        	double* spectrum = NULL;
            std::cout << "Read" << std::endl;
            return spectrum;
        }
};

extern "C" {
    Driver* Driver_new(){ return new Driver(); }
    void Driver_connect(Driver* driver){ driver->connect(); }
    double* Driver_read(Driver* driver){ return driver->read(); }
}
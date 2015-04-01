#include <iostream>
#include <stdlib.h>

using namespace std;

class Driver {
    public:
        void connect(){
            std::cout << "Connected" << std::endl;
        }

        void read(int* array, int size) {
            int min = 100;
            int range = 50;
        	for (int i = 0; i < size; i++) {
                array[i] = min + rand() % range;
            }
            cout << "Read" << endl;
        }
};

extern "C" {
    Driver* Driver_new(){ return new Driver(); }
    void Driver_connect(Driver* driver){ driver->connect(); }
    void Driver_read(Driver* driver, int* array, int size){ driver->read(array, size); }
}
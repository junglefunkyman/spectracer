g++ -c -fPIC driver.cpp -o driver.o
g++ -shared -Wl -o libdriver.so  driver.o
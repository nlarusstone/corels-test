
P2 := python2
P3 := python3

BUILD := ./build

CLEAN := ./build

python2: setup.py
	$(P2) setup.py $(BUILD)

python3: setup.py
	$(P3) setup.py $(BUILD)

install2: setup.py ../src/libcorels.so
	sudo cp ../src/libcorels.so /usr/local/lib
	$(P2) setup.py install

install3: setup.py ../src/libcorels.so
	sudo cp ../src/libcorels.so /usr/local/lib
	$(P3) setup.py install

clean:
	rm -rf $(CLEAN)

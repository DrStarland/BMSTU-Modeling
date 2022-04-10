%.o : %.c *.h %.cpp *.hpp
	g++ -c $< -Wall -Werror -pedantic 

app.exe: main.o picar.o eyler.o
	g++ -o app.exe main.o picar.o eyler.o

test.exe: main.o picar.o eyler.o
	g++ -o app.exe main.o picar.o eyler.o

clean: 
	rm *.o *.exe
# Pico-Dirty-Blaster Workshop
# Module 1:  Assembly
![MAX10 10M08 Evaluation Kit connected to Pico-Dirty-Blaster](./img/pico-dirty-blaster-connected.jpg)

## Detailed Assembly Instructions

An adapter PCB is provided that connects to pins 21 - 26 of the Raspberry Pi Pico board.  
![Front and back of adapter PCB](./img/th-pcb-front-back.jpg)
These are the JTAG pins used by the Pico DirtyJTAG project as shown here:
![Pico DirtyJTAG Pinout Diagram](./img/detailed_pinout.png)
These boards should be soldered together with a single row header installed in the bottom of the Pico board with the adapter PCB on the top side as shown in these pictures:
![Top view of assembly](./img/th-top.jpg)
![Bottom view of assembly](./img/th-bottom.jpg)
It is recommended to solder pins 40 and 28 of the header to hold it in place first, then start soldering the adapter to the short header pins extending through the top side of the Pico board.  The adapter should line up with the end of the Pico board.  The silkscreen outline of the 10 pin header should face up, away from the Pico board.  The rectangluar GND pad on the adapter should match up with the rectangluar GND pad on the Pico board.
After the six pins are soldered to the adapter, you can finish soldering the rest of the header and the other 20 pin header to the other edge of the Pico board.
Next solder the pads on the back side of the adapter PCB to the castlelated edge pads of the Pico board.
Finally, solder the 10 pin shrouded header to the adapter PCB.  The shrouded header should cover up the silkscreen outline on the top side of the board.  Ensure that the cutout in the side of the shroud and the pin 1 indicator line up with the square pin one pad of the adapter.


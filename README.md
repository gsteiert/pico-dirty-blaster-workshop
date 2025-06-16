# Pico-Dirty-Blaster Workshop
Files and documentation for Pico-Dirty-Blaster Workshop
![MAX10 10M08 Evaluation Kit connected to Pico-Dirty-Blaster](./img/pico-dirty-blaster-connected.jpg)

## Overview

In this workshop you will turn a Raspberry Pi Pico board into an FPGA programmer and practice multiple methods of loading an FPGA with open source tools.

This workshop was originally run at Crowd Supply Teardown 2024 demonstrating drag-n-drop programming using JBC files.  For Teardown 2025, we will demonstrate how to use openFPGALoader to configure the FPGA and write data to user flash memory (UFM) with the same hardware.

## Modules

This workshop is split into three modules:

1. [Assemble Pico-Dirty-Blaster](modules/1-assembly.md)
2. [Drag-n-Drop Programming with JBC and UF2 (2024)](modules/2-drag-n-drop-jbc.md)
3. [Programming MAX10 with openFPGALoader (new for 2025)](modules/3-openFPGALoader-UFM.md)

The first module is required for the second and third, but the second and third can be run independently in any order.

### Assembling Pico Dirty Blaster

A kit of parts is provided to build an FPGA programmer out of a Raspberry Pi Pico board.  This will be used in both of other modules.

### Drag-n-Drop Programming with JBC and UF2 (2024)

This module demonstrates how to use the drag-n-drop bootloader in the Raspberry Pi Pico board to transfer a configuration image and load it into the MAX10.  The Drag-n-Drop interface does not require any software installation and is the most cross-platform method.

### Programming MAX10 with openFPGALoader (new for 2025)

This module demonstrates MAX10 support built into openFPGALoader, including the ability to load arbitrary data files into user flash memory.  openFPGALoader is a command line utility designed to run in a UNIX environment like Linux.

## Example Files
Example images are provided by target board in the "examples" folder.  Current example images are built from FuseSoC blinky with different output LED settings, and a SERV Servant RISC-V hello world example, also built with FuseSoC.
 * [LED to Bleive (FuseSoC Blinky)](https://github.com/fusesoc/blinky)
 * [Servant: FPGA Reference Platform](https://serv.readthedocs.io/en/latest/servant.html)
 * [PicoRV32 on MAX10 with UFM](https://github.com/gsteiert/picomaxdev)

## Generating JBC UF2 Files
 * [Generating uncompressed JBC files](https://github.com/gsteiert/pico-dirty-blaster-workshop/blob/main/generate-jbc.md)
 * [Converting JBC to UF2](https://github.com/steieio/jbcuf2)



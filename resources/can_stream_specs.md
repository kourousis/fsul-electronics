# CAN Stream Specifications

## General
| CAN bus Baud Rate | 1 MBd           |
| Identifiers       | All 29Bit       |
| 8 Data Packets    | All 8 Bytes Ea. |
| Send Frequency    | 10 Hz           |

All Data Values Signed 16  bit sent LSB first (little endian)

## Data Packets

| Identifier    | Data 1            | Data 1 Units  | Data 2            | Data 2 Units | Data 3         | Data 3 Units  | Data 4           | Data 4 Units                |
|---------------|-------------------|---------------|-------------------|--------------|----------------|---------------|------------------|-----------------------------|
| 0x2000        | RPM               | RPM           | TPS               | %            | Water Temp     | Degrees C     | Air Temp         | Degrees C                   |
| 0x2001        | Manifold Pressure | kPa           | Lambda x1000      | Lambda x1000 | Speed          | kph x10       | Oil Pressure     | kPa                         |
| 0x2002        | Fuel Pressure     | kPa           | Oil Temperature   | Degrees C    | Battery        | Volts x10     | Fuel Consumption | L/Hr x10                    |
| 0x2003        | Current Gear      | Gear Position | Advance           | Degrees x10  | Injection Time | ms x100       | Fuel Consumption | L/100k m x10                |
| 0x2004        | Ana1              | mV            | Ana2              | mV           | Ana3           | mV            | Cam Advance      | Degrees x10                 |
| 0x2005        | Cam Targ          | Degrees x10   | Cam PWM x10       | % x10        | Crank Errors   | no. of errors | Cam Errors       | no. of errors               |
| 0x2006        | Cam2 Adv          | Degrees x10   | Cam2 Targ         | Degrees x10  | Cam2 PWM       | % x10         | External 5v      | mV                          |
| 0x2007        | Inj Duty Cycle    | %             | Lambda PID Target | % x10        | Lambda PID Adj | % x10         | ECU Switches     | Below in ECU Switches Table |
| 0x2008        | RD Speed          | kph x10       | R UD Speed        | kph x10      | LD Speed       | kph x10       | L UD Speed       | kph x10                     |
| 0x2009        | Right Lambda      | lambda x1000  |                   |              |                |               |                  |                             |

## ECU Switches Table

| Bit | Value                 |
|-----|-----------------------|
| 0   | LAUNCH BUTTON PRESSED |
| 1   | LAUNCH ACTIVE         |
| 2   | TRACTION ON           |
| 3   | TRACTION WET          |
| 4   | FUEL PUMP ON          |
| 5   | FAN OUTPUT ON         |
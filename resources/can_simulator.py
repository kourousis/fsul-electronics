import time
import random
import struct
from datetime import datetime

class DTASwinS40Simulator:
    def __init__(self, bitrate=1000000, frequency=10):
        self.bitrate = bitrate  # 1 Mbps
        self.frequency = frequency  # 10 Hz
        self.interval = 1.0 / frequency
        self.running = False
        self.message_count = 0
        self.start_time = None
        
        # 29-bit identifiers for DTASwin S40 ECU
        self.can_ids = [
            0x2000, 0x2001, 0x2002, 0x2003, 0x2004,
            0x2005, 0x2006, 0x2007, 0x2008, 0x2009
        ]
        
        # Initialize state variables for realistic data simulation
        self.engine_running = True
        self.current_gear = 1
        self.vehicle_speed = 0
        self.rpm = 800
        self.manifold_pressure = 30
        self.water_temp = 85
        self.air_temp = 25
        self.oil_temp = 90
        self.battery_voltage = 138  # 13.8V
        self.fuel_consumption = 120  # 12.0 L/100km
        
    def pack_signed_16bit_le(self, value):
        """Pack signed 16-bit value as little endian"""
        return struct.pack('<h', int(value))
    
    def generate_message_0x2000(self):
        """RPM, TPS, Water Temp, Air Temp"""
        # Simulate realistic engine behavior
        if self.engine_running:
            self.rpm = 800 + random.randint(0, 200) + (abs((time.time() % 10) - 5) * 100)
            self.rpm = min(8000, max(800, self.rpm))
        
        tps = random.randint(10, 90)  # Throttle position 10-90%
        water_temp = 80 + random.randint(-5, 20)  # 75-100°C
        air_temp = 20 + random.randint(-5, 15)  # 15-35°C
        
        data = (self.pack_signed_16bit_le(self.rpm) +      # RPM
                self.pack_signed_16bit_le(tps) +           # TPS %
                self.pack_signed_16bit_le(water_temp) +    # Water Temp °C
                self.pack_signed_16bit_le(air_temp))       # Air Temp °C
        
        return data.hex().upper()
    
    def generate_message_0x2001(self):
        """Manifold Pressure, Lambda, Speed, Oil Pressure"""
        # Manifold pressure correlates with RPM and throttle
        self.manifold_pressure = min(100, max(20, self.rpm / 100 + random.randint(-5, 5)))
        
        lambda_val = 1000 + random.randint(-50, 50)  # Lambda around 1.0
        self.vehicle_speed = max(0, min(200, (self.rpm / 40) + random.randint(-5, 5)))
        speed_scaled = int(self.vehicle_speed * 10)  # kph x10
        
        oil_pressure = 200 + (self.rpm / 20) + random.randint(-10, 10)
        oil_pressure = min(500, max(100, oil_pressure))
        
        data = (self.pack_signed_16bit_le(self.manifold_pressure) +  # Manifold Pressure kPa
                self.pack_signed_16bit_le(lambda_val) +              # Lambda x1000
                self.pack_signed_16bit_le(speed_scaled) +            # Speed kph x10
                self.pack_signed_16bit_le(oil_pressure))             # Oil Pressure kPa
        
        return data.hex().upper()
    
    def generate_message_0x2002(self):
        """Fuel Pressure, Oil Temperature, Battery, Fuel Consumption L/Hr"""
        fuel_pressure = 300 + random.randint(-20, 20)
        self.oil_temp = 80 + (self.rpm / 100) + random.randint(-5, 5)
        battery_voltage_scaled = int(self.battery_voltage)  # Already x10
        fuel_consumption_hr = 50 + (self.rpm / 100) + random.randint(-10, 10)
        
        data = (self.pack_signed_16bit_le(fuel_pressure) +        # Fuel Pressure kPa
                self.pack_signed_16bit_le(self.oil_temp) +        # Oil Temperature °C
                self.pack_signed_16bit_le(battery_voltage_scaled) + # Battery Volts x10
                self.pack_signed_16bit_le(fuel_consumption_hr))   # Fuel Consumption L/Hr x10
        
        return data.hex().upper()
    
    def generate_message_0x2003(self):
        """Current Gear, Advance, Injection Time, Fuel Consumption L/100km"""
        # Auto-shift simulation based on speed
        if self.vehicle_speed > 80 and self.current_gear < 6:
            self.current_gear = 6
        elif self.vehicle_speed > 60 and self.current_gear < 5:
            self.current_gear = 5
        elif self.vehicle_speed > 40 and self.current_gear < 4:
            self.current_gear = 4
        elif self.vehicle_speed > 25 and self.current_gear < 3:
            self.current_gear = 3
        elif self.vehicle_speed > 10 and self.current_gear < 2:
            self.current_gear = 2
        elif self.vehicle_speed < 5:
            self.current_gear = 1
        
        advance = 150 + random.randint(-10, 10)  # Degrees x10 (15.0 degrees)
        injection_time = 1000 + (self.rpm / 10) + random.randint(-50, 50)  # ms x100
        self.fuel_consumption = max(50, 200 - (self.vehicle_speed / 2) + random.randint(-20, 20))
        
        data = (self.pack_signed_16bit_le(self.current_gear) +    # Current Gear
                self.pack_signed_16bit_le(advance) +              # Advance Degrees x10
                self.pack_signed_16bit_le(injection_time) +       # Injection Time ms x100
                self.pack_signed_16bit_le(self.fuel_consumption)) # Fuel Consumption L/100km x10
        
        return data.hex().upper()
    
    def generate_message_0x2004(self):
        """Ana1, Ana2, Ana3, Cam Advance"""
        ana1 = 2500 + random.randint(-100, 100)  # mV
        ana2 = 1500 + random.randint(-100, 100)  # mV
        ana3 = 800 + random.randint(-50, 50)     # mV
        cam_advance = 100 + random.randint(-10, 10)  # Degrees x10
        
        data = (self.pack_signed_16bit_le(ana1) +        # Ana1 mV
                self.pack_signed_16bit_le(ana2) +        # Ana2 mV
                self.pack_signed_16bit_le(ana3) +        # Ana3 mV
                self.pack_signed_16bit_le(cam_advance))  # Cam Advance Degrees x10
        
        return data.hex().upper()
    
    def generate_message_0x2005(self):
        """Cam Targ, Cam PWM, Crank Errors, Cam Errors"""
        cam_target = 120 + random.randint(-5, 5)     # Degrees x10
        cam_pwm = 500 + random.randint(-20, 20)      # % x10
        crank_errors = random.randint(0, 2)          # Number of errors
        cam_errors = random.randint(0, 1)            # Number of errors
        
        data = (self.pack_signed_16bit_le(cam_target) +   # Cam Target Degrees x10
                self.pack_signed_16bit_le(cam_pwm) +      # Cam PWM % x10
                self.pack_signed_16bit_le(crank_errors) + # Crank Errors
                self.pack_signed_16bit_le(cam_errors))    # Cam Errors
        
        return data.hex().upper()
    
    def generate_message_0x2006(self):
        """Cam2 Adv, Cam2 Targ, Cam2 PWM, External 5v"""
        cam2_adv = 110 + random.randint(-5, 5)       # Degrees x10
        cam2_target = 115 + random.randint(-5, 5)    # Degrees x10
        cam2_pwm = 480 + random.randint(-20, 20)     # % x10
        external_5v = 5000 + random.randint(-100, 100)  # mV
        
        data = (self.pack_signed_16bit_le(cam2_adv) +     # Cam2 Advance Degrees x10
                self.pack_signed_16bit_le(cam2_target) +  # Cam2 Target Degrees x10
                self.pack_signed_16bit_le(cam2_pwm) +     # Cam2 PWM % x10
                self.pack_signed_16bit_le(external_5v))   # External 5v mV
        
        return data.hex().upper()
    
    def generate_message_0x2007(self):
        """Inj Duty Cycle, Lambda PID Target, Lambda PID Adj, ECU Switches"""
        inj_duty_cycle = min(95, max(5, (self.rpm / 100) + random.randint(0, 10)))
        lambda_pid_target = 1000 + random.randint(-20, 20)  # % x10
        lambda_pid_adj = 0 + random.randint(-50, 50)        # % x10
        
        # ECU Switches (bitfield)
        ecu_switches = 0
        if self.vehicle_speed > 0:
            ecu_switches |= 0x01  # Bit 0: LAUNCH BUTTON PRESSED (simulated)
        if self.vehicle_speed > 80:
            ecu_switches |= 0x02  # Bit 1: LAUNCH ACTIVE
        ecu_switches |= 0x04      # Bit 2: TRACTION ON
        if random.random() > 0.8:
            ecu_switches |= 0x08  # Bit 3: TRACTION WET (occasionally)
        ecu_switches |= 0x10      # Bit 4: FUEL PUMP ON
        if self.water_temp > 95:
            ecu_switches |= 0x20  # Bit 5: FAN OUTPUT ON
        
        data = (self.pack_signed_16bit_le(inj_duty_cycle) +    # Injection Duty Cycle %
                self.pack_signed_16bit_le(lambda_pid_target) + # Lambda PID Target % x10
                self.pack_signed_16bit_le(lambda_pid_adj) +    # Lambda PID Adjustment % x10
                self.pack_signed_16bit_le(ecu_switches))       # ECU Switches bitfield
        
        return data.hex().upper()
    
    def generate_message_0x2008(self):
        """RD Speed, R UD Speed, LD Speed, L UD Speed"""
        # Simulate wheel speeds with slight variations
        rd_speed = int(self.vehicle_speed * 10) + random.randint(-2, 2)
        r_ud_speed = int(self.vehicle_speed * 10) + random.randint(-3, 1)
        ld_speed = int(self.vehicle_speed * 10) + random.randint(-1, 3)
        l_ud_speed = int(self.vehicle_speed * 10) + random.randint(-2, 2)
        
        data = (self.pack_signed_16bit_le(rd_speed) +     # RD Speed kph x10
                self.pack_signed_16bit_le(r_ud_speed) +   # R UD Speed kph x10
                self.pack_signed_16bit_le(ld_speed) +     # LD Speed kph x10
                self.pack_signed_16bit_le(l_ud_speed))    # L UD Speed kph x10
        
        return data.hex().upper()
    
    def generate_message_0x2009(self):
        """Right Lambda only (other bytes zero)"""
        right_lambda = 980 + random.randint(-30, 30)  # Lambda x1000
        
        data = (self.pack_signed_16bit_le(right_lambda) +  # Right Lambda x1000
                b'\x00\x00\x00\x00\x00\x00')              # Remaining 6 bytes zero
        
        return data.hex().upper()
    
    def generate_can_message(self, can_id):
        """Generate CAN data based on CAN ID"""
        if can_id == 0x2000:
            return self.generate_message_0x2000()
        elif can_id == 0x2001:
            return self.generate_message_0x2001()
        elif can_id == 0x2002:
            return self.generate_message_0x2002()
        elif can_id == 0x2003:
            return self.generate_message_0x2003()
        elif can_id == 0x2004:
            return self.generate_message_0x2004()
        elif can_id == 0x2005:
            return self.generate_message_0x2005()
        elif can_id == 0x2006:
            return self.generate_message_0x2006()
        elif can_id == 0x2007:
            return self.generate_message_0x2007()
        elif can_id == 0x2008:
            return self.generate_message_0x2008()
        elif can_id == 0x2009:
            return self.generate_message_0x2009()
        else:
            # Fallback - should not happen
            return '0000000000000000'
    
    def format_log_entry(self, timestamp, can_id, data):
        """Format a CAN message as a log entry with 29-bit identifier"""
        dt = datetime.now()
        return f"{dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} " \
               f"CAN {can_id:08X} [8] {data}\n"
    
    def simulate_stream(self, duration=60, log_file="dtaswin_s40_log.txt"):
        """Simulate CAN stream for specified duration"""
        self.running = True
        self.start_time = time.time()
        self.message_count = 0
        
        print(f"Starting DTASwin S40 CAN stream simulation")
        print(f"Baud Rate: {self.bitrate}bps, Frequency: {self.frequency}Hz")
        print(f"All identifiers: 29-bit, All data: 8 bytes, Signed 16-bit LSB first")
        print(f"Logging to: {log_file}")
        print(f"Duration: {duration} seconds")
        print("-" * 60)
        
        with open(log_file, 'w') as f:
            # Write log header
            f.write(f"# DTASwin S40 ECU CAN Bus Log\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Baud Rate: {self.bitrate} bps\n")
            f.write(f"# Frequency: {self.frequency} Hz\n")
            f.write(f"# Identifiers: All 29-bit, Data: All 8 bytes\n")
            f.write(f"# Data Format: Signed 16-bit LSB first (little endian)\n")
            f.write("#" + "-" * 60 + "\n")
            
            end_time = time.time() + duration
            
            while time.time() < end_time and self.running:
                cycle_start = time.time()
                
                # Generate all 10 messages in each cycle (10Hz)
                for can_id in self.can_ids:
                    data = self.generate_can_message(can_id)
                    log_entry = self.format_log_entry(time.time(), can_id, data)
                    f.write(log_entry)
                    f.flush()  # Ensure data is written immediately
                    
                    self.message_count += 1
                
                # Calculate sleep time to maintain 10Hz frequency
                cycle_time = time.time() - cycle_start
                sleep_time = max(0, self.interval - cycle_time)
                time.sleep(sleep_time)
        
        print(f"Simulation completed.")
        print(f"Total messages: {self.message_count}")
        print(f"Total frames: {self.message_count} (all 8-byte frames)")
        print(f"Average frequency: {self.message_count/duration:.2f} Hz")
        print(f"Data rate: {(self.message_count * (8 + 8 + 8)) / duration / 1000:.2f} kB/s")  # Rough estimate
    
    def stop(self):
        """Stop the simulation"""
        self.running = False

# Usage example
if __name__ == "__main__":
    # Create DTASwin S40 simulator
    simulator = DTASwinS40Simulator(bitrate=1000000, frequency=10)
    
    # Simulate for 30 seconds (adjust as needed)
    try:
        simulator.simulate_stream(duration=30, log_file="dtaswin_s40_ecu_log.txt")
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
        simulator.stop()
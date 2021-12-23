EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "ili9341-driver"
Date "2021-12-20"
Rev "0.1"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L RPi_Pico:Pico U1
U 1 1 61C06024
P 6400 3750
F 0 "U1" H 6400 4965 50  0001 C CNN
F 1 "Pico" H 6400 4850 50  0000 C CNN
F 2 "RPi_Pico:RPi_Pico_SMD_TH" V 6400 3750 50  0001 C CNN
F 3 "" H 6400 3750 50  0001 C CNN
	1    6400 3750
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0101
U 1 1 61C21E38
P 7300 3150
F 0 "#PWR0101" H 7300 3000 50  0001 C CNN
F 1 "+3.3V" H 7450 3150 50  0000 C CNN
F 2 "" H 7300 3150 50  0001 C CNN
F 3 "" H 7300 3150 50  0001 C CNN
	1    7300 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7100 3200 7300 3200
Wire Wire Line
	7300 3200 7300 3150
$Comp
L power:+3.3V #PWR0104
U 1 1 61C2E84A
P 3600 4050
F 0 "#PWR0104" H 3600 3900 50  0001 C CNN
F 1 "+3.3V" H 3750 4050 50  0000 C CNN
F 2 "" H 3600 4050 50  0001 C CNN
F 3 "" H 3600 4050 50  0001 C CNN
	1    3600 4050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 61C32205
P 3600 5750
F 0 "#PWR0105" H 3600 5500 50  0001 C CNN
F 1 "GND" H 3605 5577 50  0000 C CNN
F 2 "" H 3600 5750 50  0001 C CNN
F 3 "" H 3600 5750 50  0001 C CNN
	1    3600 5750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 61C25408
P 7200 5750
F 0 "#PWR0106" H 7200 5500 50  0001 C CNN
F 1 "GND" H 7205 5577 50  0000 C CNN
F 2 "" H 7200 5750 50  0001 C CNN
F 3 "" H 7200 5750 50  0001 C CNN
	1    7200 5750
	1    0    0    -1  
$EndComp
$Comp
L IL9341-240x320-TFT-LCD:IL9341-240x320-TFT-LCD U2
U 1 1 61C087BC
P 3000 4800
F 0 "U2" H 2800 5500 50  0001 C CNN
F 1 "ILI9341 Breakout" H 3000 5550 50  0000 C CNN
F 2 "Display:CR2013-MI2120" H 3000 4100 50  0001 C CNN
F 3 "http://pan.baidu.com/s/11Y990" H 2350 5300 50  0001 C CNN
	1    3000 4800
	-1   0    0    -1  
$EndComp
NoConn ~ 5700 4500
NoConn ~ 5700 4000
NoConn ~ 5700 3500
NoConn ~ 5700 2800
NoConn ~ 5700 2900
NoConn ~ 7100 4000
NoConn ~ 7100 3700
NoConn ~ 7100 3600
NoConn ~ 7100 3500
NoConn ~ 7100 3400
NoConn ~ 7100 3300
NoConn ~ 7100 3000
NoConn ~ 7100 2900
NoConn ~ 7100 2800
NoConn ~ 7100 3100
NoConn ~ 6300 4900
NoConn ~ 6400 4900
NoConn ~ 6500 4900
Wire Wire Line
	3550 4450 3700 4450
Wire Wire Line
	3550 4250 3600 4250
NoConn ~ 5700 3700
NoConn ~ 5700 3600
NoConn ~ 7100 4200
NoConn ~ 7100 4100
NoConn ~ 7100 3900
NoConn ~ 7100 4700
Wire Wire Line
	7100 4500 7200 4500
Wire Wire Line
	7200 4500 7200 5750
NoConn ~ 5700 3000
Text Label 5300 3100 0    50   ~ 0
spi0_sck
Text Label 5300 3200 0    50   ~ 0
spi0_mosi
Text Label 5300 3300 0    50   ~ 0
spi0_miso
Text Label 5300 3400 0    50   ~ 0
sd_cs
Text Label 3750 5150 0    50   ~ 0
touch_cs
Text Label 3750 5250 0    50   ~ 0
spi0_mosi
Text Label 3750 5350 0    50   ~ 0
spi0_miso
Text Label 3750 5450 0    50   ~ 0
touch_irq
Text Label 5300 4100 0    50   ~ 0
spi1_sck
Text Label 5300 4200 0    50   ~ 0
spi1_mosi
Text Label 5300 4300 0    50   ~ 0
spi1_miso
Text Label 5300 4400 0    50   ~ 0
tft_cs
Text Label 3750 4350 0    50   ~ 0
tft_cs
Text Label 3750 4850 0    50   ~ 0
tft_led
Text Label 2100 4850 0    50   ~ 0
spi0_miso
Text Label 2100 4750 0    50   ~ 0
spi0_mosi
Text Label 2100 4650 0    50   ~ 0
sd_cs
Wire Wire Line
	3550 4350 4000 4350
Text Label 3750 4550 0    50   ~ 0
tft_dc
Wire Wire Line
	3550 4150 3600 4150
Wire Wire Line
	3600 4150 3600 4050
Text Label 3750 4650 0    50   ~ 0
spi1_mosi
Text Label 3750 4950 0    50   ~ 0
spi1_miso
Wire Wire Line
	5250 4700 5700 4700
Entry Wire Line
	1850 4850 1950 4950
Entry Wire Line
	1850 4750 1950 4850
Entry Wire Line
	1850 4650 1950 4750
Wire Wire Line
	1950 4950 2500 4950
Wire Wire Line
	1950 4850 2500 4850
Wire Wire Line
	1950 4750 2500 4750
Entry Wire Line
	4450 5350 4550 5450
Entry Wire Line
	4450 5250 4550 5350
Entry Wire Line
	4450 5050 4550 5150
Entry Wire Line
	4550 3000 4650 3100
Entry Wire Line
	4550 3100 4650 3200
Entry Wire Line
	4550 3200 4650 3300
Wire Wire Line
	3550 5350 4450 5350
Wire Wire Line
	3550 5250 4450 5250
Wire Wire Line
	3550 5050 4450 5050
Text Label 5300 4700 0    50   ~ 0
tft_led
Text Label 5300 4600 0    50   ~ 0
tft_dc
Text Label 5300 3900 0    50   ~ 0
touch_cs
Text Label 5300 3800 0    50   ~ 0
touch_irq
Wire Wire Line
	4650 3100 5700 3100
Wire Wire Line
	4650 3200 5700 3200
Wire Wire Line
	4650 3300 5700 3300
Wire Wire Line
	4700 4850 4700 5450
Wire Wire Line
	4700 5450 5250 5450
Wire Wire Line
	5250 5450 5250 4700
Wire Wire Line
	3550 4850 4700 4850
Wire Wire Line
	3700 4450 3700 5650
Entry Wire Line
	4950 4950 5050 4850
Entry Wire Line
	4950 4750 5050 4650
Entry Wire Line
	4950 4650 5050 4550
Entry Wire Line
	5050 4300 5150 4200
Entry Wire Line
	5050 4200 5150 4100
Entry Wire Line
	5050 4400 5150 4300
Wire Wire Line
	3550 4650 4950 4650
Wire Wire Line
	3550 4750 4950 4750
Wire Wire Line
	3550 4950 4950 4950
Wire Wire Line
	5150 4100 5700 4100
Wire Wire Line
	5150 4200 5700 4200
Wire Wire Line
	5150 4300 5700 4300
Wire Wire Line
	4800 4550 4800 5350
Wire Wire Line
	4800 5350 5150 5350
Wire Wire Line
	5150 5350 5150 4600
Wire Wire Line
	5150 4600 5700 4600
Wire Wire Line
	3550 4550 4800 4550
Wire Wire Line
	4200 5150 4200 3900
Wire Wire Line
	3550 5150 4200 5150
Wire Wire Line
	4200 3900 5700 3900
Wire Wire Line
	4300 5450 4300 3800
Wire Wire Line
	4300 3800 5700 3800
Wire Wire Line
	3550 5450 4300 5450
Wire Wire Line
	5200 4400 5200 4000
Wire Wire Line
	5200 4000 4000 4000
Wire Wire Line
	4000 4000 4000 4350
Wire Wire Line
	5200 4400 5700 4400
Wire Wire Line
	2000 3400 2000 4650
Wire Wire Line
	2000 3400 5700 3400
Wire Wire Line
	2000 4650 2500 4650
Wire Wire Line
	3600 5750 3600 4250
Wire Wire Line
	3700 5650 7700 5650
Wire Wire Line
	7700 3800 7700 5650
Wire Wire Line
	7100 3800 7700 3800
Text Label 3750 4750 0    50   ~ 0
spi1_sck
Text Label 3750 5050 0    50   ~ 0
spi0_sck
Text Label 2100 4950 0    50   ~ 0
spi0_sck
Wire Bus Line
	1850 1500 4550 1500
NoConn ~ 7100 4600
NoConn ~ 7100 4400
NoConn ~ 7100 4300
Wire Bus Line
	1850 1500 1850 4850
Wire Bus Line
	4550 1500 4550 5450
Wire Bus Line
	5050 4200 5050 4850
$EndSCHEMATC

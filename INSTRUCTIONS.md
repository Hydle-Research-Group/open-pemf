# Building OpenPEMF

## Introduction

## Requirements

| Quantity | Item | Description |
| - | - | - |
| 1 | [Raspberry Pi Pico "H" (1st Generation)](https://www.sparkfun.com/raspberry-pi-pico-h.html?src=raspberrypi) | Primary Microcontroller |
| 1 | [1.3" OLED Display & Rotary Encoder Module (Control Knob)](https://www.amazon.com/Display-Combined-Encoder-Interface-arduino/dp/B0DMYQHM9J?crid=X9ZTLYSS4LK8&dib=eyJ2IjoiMSJ9.KcC-ClV00-zsSt1xJ0-bqAhpk9VThuxsrS8C90N4lJEgmkXD96VsBLlqPAMwnEb5AI1jnljVacIQYEly0Vi_GQY6Ab__PiWSc9fRohIsGv4im4tQsJNSSJyM17oflBpFC2fsG-AUnArXDZGwAUoChHAmCp9VfAt4XXEu-wsokLN-XfOn15xk4OqmSgWPz2iZhZChw42OgTy_oEYRk4zaAuGgNZibQoN3ISJN621y3ts.bZ5iC5Ax2QZ7Op3S6kixV8lMCer8_9lCB_hF7rMYYAQ&dib_tag=se&keywords=0.96%2F1.3+inch+white+OLED+display+combined+with+EC11+rotary+encoder+module%2CIIC+interface+for+Arduinos+-+1.3+inch&nsdOptOutParam=true&qid=1793292329&sprefix=%2Caps%2C180&sr=8-1) | Control Display |
| 1 | [SparkFun MOSFET Power Switch & Buck Regulator](https://www.sparkfun.com/sparkfun-mosfet-power-switch-and-buck-regulator-low-side.html) | Power Source (Logic + System) | 
| 1 | [BIGTREETECH TMC2209 Stepper Motor Driver (V1.3)](https://biqu.equipment/products/btt-tmc2209-stepper-driver) | Pulse Generator |
| 1 | [12V 5A DC Power Supply (5.5x2.1mm Barrel-Jack Compatible)](https://www.amazon.com/5-5x2-1mm-Converter-Transformer-Surveillance-External/dp/B07GFFG1BQ?crid=383J1GHX4L3T4&dib=eyJ2IjoiMSJ9.QaSKR99Xv48J2M8_VqVTmNw-GovV7Q_rzaDTXpEsZLjnwtpYRxgd6X85g0F4HClrxFNCwCTD7GVSJRv-ho23I1UTd6LjmZWs1MzoV9Vzp0dTGy65vmfAG11vBtXtVMNVH4p1aJfu9Y2BeJjlZ4wdOeGqcdAigoYVkbYCz0VNtm_IE9X1ycAhicL_i9ttdgRFeJN9sx6qLaTrtvzoM5m74fVOHWxLl8eXU1kTQ9xMFfg.riypyNZJVVE6_v0DloRqQiPqmmW3wMhyQEXZgTEsoG8&dib_tag=se&keywords=12v%2B5a%2Bpower%2Bsupply%2Bdc%2Bbarrel%2Bjack%2B5.5x2.1&nsdOptOutParam=true&qid=1791384006&sprefix=12v%2B5a%2Bpower%2Bsupply%2Bdc%2Bbarrel%2Bjack%2B5.5x2.%2Caps%2C226&sr=8-3&th=1) | Power supply |
| 1 | ["Pogo Pin" Style Connector (Wired, 1x6)](https://www.amazon.com/Connector-Pogopin-Female-Spacing-Spring/dp/B0HM7Q1DHC?dib=eyJ2IjoiMSJ9.mB-CeHh1JSu4zfDg0NTThVDBbAgDiyVrMy4O_5pEyhWwlOfBl8BOP_hp1Iod5uJ1lHOj6XnfWjuAmFSr_VwOJkiAeY-mji932305OYP7XXK6EEipPWKDjeEAtQflsY6ZomJN88uG6lwRaQflnLebvPLIsdRfw_Xh3C29QQJFE_1FNOO3K1A-lTudpMyigS-l1qDR_nCtgGJFfdvdkg-gb6KOBLJkc-5bsi4nd0RijKc.rDwpQpHoUlc4jaNjFkaGylnoaGotZ91iIn0J-o5WQlc&dib_tag=se&keywords=pogo%2Bpin%2Bconnector&qid=1792413616&sr=8-9&th=1) | Treatment Coil Connection |
| 1 | [18AWG Stranded Wire (~3m or More)](https://www.amazon.com/0-35mm%C2%B2-Electrical-Colors-Tinned-breadboard/dp/B08F7F6PH4?dib=eyJ2IjoiMSJ9.Z8M0SEpBswaKS4KRcWtSQ3-KrayAyyyaZFTfcQd5zKoBSGTtibB6F2Q1hFfES-Uj35PtVmgDC9-jABzgFApMiYmxq8Nh3Fmt7ictd2kOCAXf-HKX6qQPfhTP18rZzqqYLHNeHYVWBbitxBUVNvpbLHbO8csqlw6VAmZb9x3a5iQfNU-lpGjV3q72BIqBqrTNgRme7vzRoItOTjHzOGxe4PzCtqNnSmMX_Wm7VutST4xMxkbNYvNJlwsyR8MZhs0-bxmjqXYHm6c9mfE6dyfL2MCkhf3yE0bvEQX-f2eCjDU.lHGs6Zvfs06A03BpnkuJ66OnGcKHxdArNw-kxZ8Owf8&dib_tag=se&keywords=solid%2Bcore%2Bwire&qid=1793290824&sr=8-6&th=1) | Treatment Coil Cable | 
| 1 | [18AWG Solid Core Copper Wire](https://www.amazon.com/0-35mm%C2%B2-Electrical-Colors-Tinned-breadboard/dp/B09WHMHTCG?dib=eyJ2IjoiMSJ9.Z8M0SEpBswaKS4KRcWtSQ3-KrayAyyyaZFTfcQd5zKoBSGTtibB6F2Q1hFfES-Uj35PtVmgDC9-jABzgFApMiYmxq8Nh3Fmt7ictd2kOCAXf-HKX6qQPfhTP18rZzqqYLHNeHYVWBbitxBUVNvpbLHbO8csqlw6VAmZb9x3a5iQfNU-lpGjV3q72BIqBqrTNgRme7vzRoItOTjHzOGxe4PzCtqNnSmMX_Wm7VutST4xMxkbNYvNJlwsyR8MZhs0-bxmjqXYHm6c9mfE6dyfL2MCkhf3yE0bvEQX-f2eCjDU.lHGs6Zvfs06A03BpnkuJ66OnGcKHxdArNw-kxZ8Owf8&dib_tag=se&keywords=solid%2Bcore%2Bwire&qid=1793290824&sr=8-6&th=1) or **Your Choice** | Wiring |
| 1 | [22AWG Solid Core Copper Wire](https://www.amazon.com/0-35mm%C2%B2-Electrical-Colors-Tinned-breadboard/dp/B09WHQ18KL?dib=eyJ2IjoiMSJ9.Z8M0SEpBswaKS4KRcWtSQ3-KrayAyyyaZFTfcQd5zKoBSGTtibB6F2Q1hFfES-Uj35PtVmgDC9-jABzgFApMiYmxq8Nh3Fmt7ictd2kOCAXf-HKX6qQPfhTP18rZzqqYLHNeHYVWBbitxBUVNvpbLHbO8csqlw6VAmZb9x3a5iQfNU-lpGjV3q72BIqBqrTNgRme7vzRoItOTjHzOGxe4PzCtqNnSmMX_Wm7VutST4xMxkbNYvNJlwsyR8MZhs0-bxmjqXYHm6c9mfE6dyfL2MCkhf3yE0bvEQX-f2eCjDU.lHGs6Zvfs06A03BpnkuJ66OnGcKHxdArNw-kxZ8Owf8&dib_tag=se&keywords=solid+core+wire&qid=1793290824&sr=8-6) or **Your Choice** | Wiring |
| 1 | 2.54mm Pin Headers (Male, 1x10) **Your Choice** | Display Connection |
| 2 | 2.54mm Pin Headers (Female, 1x20) **Your Choice** | Microcontroller Mount |
| 2 | 2.54mm Screw Terminal (>2A Continuous, 22-18AWG, 1x6) **Your Choice** | PCB Input |
| 1 | Dupont ribbon cable (1x10) **Your Choice** | Display Connection |

*Items marked "Your Choice" are left up to you on where to purchase from.*

Additionally, a capable 3D printer and PETG filament are recommended. We encourage the usage of PETG, as the OpenPEMF enclosure contains electronics that can potentially heat up.

# OpenPEMF

An open-source medical device to stimulate blood-flow and potentially relieve pain in targeted areas.

> [!WARNING]
> OpenPEMF creates rapidly changing electromagnetic fields and can cause **serious death or injury** if used incorrectly. OpenPEMF is an **untested**, **non-clinically evaluated**, **Pulsed Electromagnetic Field (PEMF) device**, and should **NOT** be used by you or others with in-body electronics such as pacemakers, hearing aids, or any other **magnetic-sensitive implants**.

## About

The OpenPEMF project was created as an open-source design inspired by the [BEMER device](https://bemergroup.com/en_US/human-line/products/overview). The BEMER device uses Pulsed Electromagnetic Fields (PEMF) to, what the BEMER Group has claimed, stimulate blood flow in parts of the body.  

Whilst the effects of [PEMF therapy](https://my.clevelandclinic.org/health/treatments/pulsed-electromagnetic-field-pemf-therapy) are unstudied and controversial, there is a chance that PEMF devices **do** stimulate blood movement to some degree. OpenPEMF is designed to make access to this treatment affordable and open, for anyone.

## How It Works

At its core, OpenPEMF uses a coil of wire and a pulse generator. This setup creates a changing electromagnetic field, simply by running current through the coil via the pulse generator. The device runs on 12V DC with a peak current of ~2A.

The pulse generator we chose is a repurposed [TMC2209 stepper motor driver](https://global.bttwiki.com/TMC2209.html). The TMC2209 outputs two sinusoidal-like waves (two phases), with one phase offset by 60° depending on the configuration. The actual "treatment applicator" is a handheld plastic assembly. Inside are the two phases of wire, wound in a coil with a diameter of 10cm.

The BEMER Group [describes using a special waveform](https://patents.google.com/patent/US8808159B2/en) for stimulating "autoregulatory mechanisms in the organism". This requires modifying the strength of the magnetic field, which is dependent on current and the number of turns per unit length:

$$
B = \mu_0 n I
$$

One concern is that researchers don't know if a special waveform is *required* to stimulate tissue, muscles, or blood flow. [A study that used both fake and real PEMF therapy](https://pmc.ncbi.nlm.nih.gov/articles/PMC2670735/#ack1) showed that using low-frequency magnetic fields on patients with musculoskeletal chronic pain yielded results indicating a slight healing effect.

The BEMER group specifies on their website that the device runs at ~30Hz with variable intensities. From what we've determined, the frequency and intensity of the magnetic field both matter, **but not significantly enough** to determine a special "biometric" waveform. For that reason, we designed a 30Hz exponentially-growing waveform for OpenPEMF:

$$
f(t) =
\begin{cases}
32 \cdot \sin(30t), & t < 4 \\
\dfrac{32}{t - 3} \cdot \sin(30t), & t \leq 20
\end{cases}
$$

*Where `t` is time in minutes (counted down by the device) and `f(t)` is the current value for the TMC2209.*

Since the TMC2209 already generates the sine wave, a micro controller (Raspberry Pi Pico) can send 30Hz pulses to the STEP pin, and configure the driver's current with time with UART communication. 

The OpenPEMF firmware is designed to have 3 levels a user can "session" with. All levels use the same waveform, meaning the only thing that changes is the time.

- Level 1 lasts 5 minutes and is low intensity.
- Level 2 lasts 15 minutes and reaches medium intensity.
- Level 3 lasts 20 minutes and reaches the highest intensity.

With all of this in mind, it should be known that the OpenPEMF unit and other PEMF devices do **NOT** generate ionizing radiation. The device frequency is well below that of radio waves.  

## Usage

Power on the device by plugging the 12V DC (2A) power supply into the jack near the back of the device.

Once the device is on, you will likely need to configure the level. Pick a level depending on the pain you are feeling:

- Level 1 lasts 5 minutes and is low intensity. *For little to no pain*
- Level 2 lasts 15 minutes and reaches medium intensity. *For medium pain, i.e. a bruise*
- Level 3 lasts 20 minutes and reaches the highest intensity. *For hard pain, such as aches, soreness, or torn muscles.*

Once you are ready, hold the applicator on a targeted area (preferably where pain is occurring) and click "Start Session" to start the device. 

## Building Your Own

*[See the instructions](INSTRUCTIONS.md).* We have written documentation to help you build an OpenPEMF device yourself. Expect an initial cost of roughly $100 (USD) to construct an OpenPEMF unit.

## Free & Open-Source

OpenPEMF is 100% free with no drawbacks or limitations. There is no "premium" version; you get the latest and greatest, all licensed under the GPL-3.0.

The entire project is public, to anyone. This includes the source code and design files. There are no "hidden mechanisms" included in this repository; every reference and used factor exists completely and fully.

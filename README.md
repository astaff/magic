# Fitness Equipment Liberator

Transform any exercise machine that has any kind of display into a fully hackable, open platform.

## Liberate Any Machine

- Treadmills
- Exercise Bikes
- Ellipticals
- Rowing Machines
- Stair Climbers
- And more!

If it's got a digital readout, we can hack it!

## Core Features

1. Raw speed data (currently reed switch, but could be hall effect, encoder, etc.)
2. Resistance/incline/effort control with position feedback (servo, stepper, etc.)
3. Heart rate monitoring (chest strap, Polar strap, etc.) (coming soon)

## Why?

- Break free from Peloton, iFit, and other locked-down ecosystems
- Breathe new life into old or "bricked" smart equipment
- Create custom interfaces and experiences without limitations
- Build your own fitness apps using real exercise data

## Quick Start

1. Flash `board.py` to your microcontroller (works on Raspberry Pi Pico H, others TBD)
2. Connect to your exercise machine's existing sensors and controls (works with reed switch for speed, DC motor for effort, potentiometer for position)
3. Run `api.py` or `ui.py` on any computer connected to the microcontroller via serial interface (via USB)
4. Start hacking your workouts!

## API Endpoints

- `GET /speed`: Stream speed data
- `GET /position`: Stream effort position
- `GET /left`: Decrease effort
- `GET /right`: Increase effort
- `GET /stop`: Stop effort adjustment
- `GET /heartrate`: Stream heart rate data (coming soon)

## Hack Ideas

1. Replace sad crappy screens with tablets or smartphones
2. Turn workouts into simple games or challenges
2. Create multi-machine workout programs
3. Develop VR/AR fitness experiences using real exercise data
4. Build a community-driven workout-sharing platform
5. Implement advanced fitness tracking and analytics

## Contributing

Whether you're reverse-engineering a high-end machine or breathing new life into vintage equipment, we want to see it! Fork the repo, hack away, and submit a pull request.

Let's turn every piece of fitness equipment into an open playground for innovation!

## License

Copyright 2024 Artyom Astafurov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

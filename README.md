# UPS Monitor

A Home Assistant custom integration for monitoring UPS (Uninterruptible Power Supply) devices connected to your Home Assistant server via I2C.

## Features

This integration provides the following sensor entities:

- **UPS Battery** - Battery level in percentage (%)
- **UPS Voltage** - Battery voltage in millivolts (mV)
- **UPS Charging** - Charging state (charging/discharging)

## Supported UPS Devices
One of the following UPS devices can be selected during configuration:
- **X1205 UPS for Raspberry Pi** - Hardware UPS HAT using X1205 chip with I2C communication
- **Dummy** - Debug mode for testing without physical hardware

## Prerequisites

### Enable I2C on Your Home Assistant Server

Before using this integration, you need to enable I2C on your Home Assistant server.

#### For Raspberry Pi / Home Assistant OS:

1. Access the Home Assistant host system (SSH with debug enabled or direct access)
2. Enable I2C by adding to `/boot/config.txt`:
   ```
   dtparam=i2c_arm=on
   ```
3. Reboot your system
4. Verify I2C is enabled:
   ```bash
   ls /dev/i2c*
   ```
   You should see `/dev/i2c-1` or similar

#### For Other Linux Systems:

1. Load the I2C kernel modules:
   ```bash
   sudo modprobe i2c-dev
   ```
2. Make it persistent by adding to `/etc/modules`:
   ```
   i2c-dev
   ```
3. Ensure your user has permissions to access I2C devices

## Installation

### Via HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/ups_monitor` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "UPS Monitor"
4. Select your UPS type:
   - **X1205** for physical X1205 UPS hardware
   - **Dummy** for testing without hardware
5. Configure the I2C bus and address if using X1205
6. The integration will create three sensor entities

## Troubleshooting

- Ensure I2C is properly enabled on your system
- Check that the UPS hardware is properly connected
- Verify I2C address matches your hardware (default is usually 0x50 or 0x51)
- Check Home Assistant logs for any error messages

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

See [LICENSE](LICENSE) file for details.


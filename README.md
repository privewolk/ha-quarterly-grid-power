# ha-quarterly-grid-power
A Home Assistant custom integration that calculates average grid power per quarter-hour from a selected power sensor. Usefull for flemish residences to see the peak value of the current quarter
# Quarterly Grid Power

A Home Assistant custom integration that calculates the average power imported from the electricity grid during the current quarter-hour.

It is particularly useful for residents of Flanders who want to monitor their electricity use in relation to the Flemish **capaciteitstarief**. The calculated quarter-hour average can help users understand the power peaks that may contribute to their capacity-tariff profile. It is an indicative monitoring tool, not an official tariff calculation.

The integration lets you select an existing power sensor during setup and creates a sensor showing the average grid-import power for the current quarter-hour.

> **Important:** This is a community-maintained custom integration. The maker is not responsible for incorrect sensor values, missing values, inaccurate calculations, data loss, equipment damage, financial loss, or any other consequences resulting from the use of this integration. Do not use this integration as the sole basis for safety-critical, regulatory, billing, or other important decisions.

## Features

- Select an existing Home Assistant power sensor during setup.
- Calculates the average imported grid power for the current quarter-hour.
- Updates every **10 seconds**.
- Starts a new averaging period at:
  - `00` minutes past the hour
  - `15` minutes past the hour
  - `30` minutes past the hour
  - `45` minutes past the hour
- Uses the final reading from the previous quarter as the first value of the new quarter.
- Treats negative source values as `0 W`, which is useful when negative values represent power export to the grid.
- Uses Home Assistant’s normal integration setup flow; no YAML automation or `input_number` helpers are required.

## Requirements

- Home Assistant
- HACS
- An existing Home Assistant sensor that reports power in watts (`W`)

The selected source sensor should have a numeric state, for example:

```text
408
```

The source sensor should not normally have a state of `unknown` or `unavailable`.

## Installation through HACS

This integration is currently installed as a custom HACS repository.

1. Open **HACS** in Home Assistant.
2. Open the **Integrations** section.
3. Open the three-dot menu in the top-right corner.
4. Select **Custom repositories**.
5. Enter the URL of this GitHub repository.
6. Select **Integration** as the repository type.
7. Click **Add**.
8. Search for **Quarterly Grid Power**.
9. Install the integration.
10. Restart Home Assistant when HACS asks you to do so.

After the restart, continue with the configuration steps below.

## Configuration

1. Open **Settings → Devices & services**.
2. Click **Add integration**.
3. Search for **Quarterly Grid Power**.
4. Select the integration.
5. In the setup window, select the sensor that reports power imported from the grid.

The setup window looks like this:

![Quarterly Grid Power setup window](images/configuration.png)

6. Click **Submit**.
7. Finish the setup.
8. Wait up to 10 seconds for the first value to appear.

The integration creates a sensor named:

```text
Current quarter average
```

The entity ID is assigned by Home Assistant and may differ depending on your installation. A typical entity ID is:

```text
sensor.current_quarter_average
```

## How the calculation works

The selected source sensor is read every 10 seconds. Each numeric reading is added to the current quarter-hour calculation.

The average is calculated as:

```text
average power = sum of readings / number of readings
```

At the start of every quarter-hour, the integration begins a new calculation. The last valid reading from the previous quarter is used as the first value of the new quarter instead of starting with zero.

Negative readings are treated as zero:

```text
negative reading -> 0 W
```

This behaviour assumes that negative values indicate power being exported to the grid. If your source sensor uses a different sign convention, verify the result before relying on the calculated value.

## Update interval

The calculated sensor is updated every **10 seconds**.

The accuracy of the average depends on the source sensor. If the source sensor updates less frequently than every 10 seconds, the integration may read the same value more than once. The integration cannot create accuracy that is not present in the source data.

## Troubleshooting

### The sensor shows `Unknown`

Check the following:

1. Confirm that the selected source sensor still exists.
2. Go to **Developer Tools → States**.
3. Find the selected source sensor.
4. Confirm that its state is numeric, such as `408`.
5. Confirm that it is not `unknown` or `unavailable`.
6. Restart Home Assistant after changing or restoring the source sensor.

### The sensor shows `0 W`

The source sensor may currently report a negative value. Negative values are deliberately converted to zero because they are assumed to represent grid export.

### The integration cannot be added twice for the same source sensor

Each source sensor can only be configured once. Remove the existing Quarterly Grid Power configuration before adding the same source sensor again.

### HACS shows a commit hash instead of a version number

HACS may show a commit hash when the repository does not have a GitHub release. Create a release using a version tag such as:

```text
v1.0.3
```

Then refresh HACS and update the integration.

## Removing the integration

1. Go to **Settings → Devices & services**.
2. Find **Quarterly Grid Power**.
3. Open its configuration entry.
4. Open the three-dot menu.
5. Select **Delete**.

If the configuration entry is not visible, remove the created sensor from **Settings → Devices & services → Entities**, then restart Home Assistant and check the integrations page again.

## Privacy

This integration does not require an external account or cloud service. It reads the selected Home Assistant entity locally.

## Limitations

- The integration depends on the selected source sensor being available and accurate.
- The average is based on readings taken every 10 seconds, not on a certified energy-metering calculation.
- Restarting Home Assistant can interrupt the current quarter’s calculation.
- Historical values may be unavailable or incomplete after an installation, upgrade, restart, or source-entity interruption.
- Negative values are converted to zero.
- The integration should not be used for official billing, legal reporting, safety systems, or financial decisions.

## Disclaimer

The maker provides this integration without guarantees regarding accuracy, availability, reliability, compatibility, or fitness for a particular purpose. The maker is not responsible for errors in the source sensor value or in the calculated value, nor for any direct or indirect loss or damage arising from installation or use of the integration. Use it at your own risk and independently verify important measurements.

## Support

Before opening an issue, include:

- Home Assistant version
- Integration version
- Source sensor entity ID
- Source sensor state and unit
- The calculated sensor state
- Relevant Home Assistant log messages
- Steps needed to reproduce the problem

Never include passwords, tokens, private URLs, or other confidential information in an issue.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

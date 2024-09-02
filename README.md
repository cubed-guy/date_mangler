# Date Mangler

An interactive command-line utility for manipulating date and time objects.

## Setup

- Clone or [download](https://github.com/cubed-guy/date_mangler/archive/refs/heads/master.zip) the repository.
- Make sure you have [python](https://www.python.org/downloads/) installed.
- Start the program by running `date_mangler.py` from your file browser or terminal.

```bash
cd date_mangler  # the directory of the repository
python3 date_mangler.py
```

Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to exit.

## Example

```
int 0
Operions.add
multiplier = 1
> 14H15M

timedelta 14:15:00
Operions.add
multiplier = 1
> /5M

float 171.0
Operions.div
multiplier = 1
> 1700000000u

datetime 2023-11-14 22:13:20
Operions.div
multiplier = 1
> -0u/1S

float 1700000000.0
Operions.div
multiplier = 1
>
```

In the above example:
- By adding hours and minutes, we created a simple `timedelta` object of `14:15:00`.
- We divided this by 5 minutes to see how many chunks of 5 minutes can fit in that time.
- We converted 1,700,000,000 from a Unix timestamp to a `datetime` object. If the operation is invalid, Date mangler sets `value` to the submitted object.
- We subtracted the Unix timestamp and divided it by 1 second to convert back from `datetime` to the Unix timestamp.

## How it works

Date mangler keeps track of a `value`, an `operation` and a `multiplier`. Manipulations are performed by submitting objects.
Date mangler performs the `operation` on the `value` and the submitted object to calculate the new `value`.

The following commands submit different kinds of objects:

|Command|Description|
|--|--|
| . | Submits the `multiplier` as an `int` |
| S | Submits a `timedelta` object of `multiplier` seconds |
| M | Submits a `timedelta` object of `multiplier` minutes |
| H | Submits a `timedelta` object of `multiplier` hours |
| d | Submits a `timedelta` object with `multiplier` days |
| m | Submits a `monthdelta` object with year = `multiplier` |
| y | Submits a `monthdelta` object with year = `multiplier` |
| n | Submits the current time |
| u | Submits the time after `multiplier` seconds from the Unix epoch |

`monthdelta` is a variation on `timedelta` that specifies the number of months rather than days.
This distinction is useful because adding 1 month can mean adding anything from 28 to 31 days.

A few more points to note:
- Submitting an object resets `multiplier` to 1.
- If the operation between `value` and the submitted object is invalid, `value` is set to the submitted object.

Some commands perform manipulations without submitting an object. Instead, they directly affect `value`, `operation` or `multiplier`.

|Command|Description|
|--|--|
| 0-9 | Sets `multiplier` to the specified number |
| _ | Multiplies `multiplier` by -1 |
| Y | Sets the `year` field of `value` to `multiplier` (Resets `multiplier` to 1) |
| ^ | Sets `value` to the `multiplier` (This is different from ".", because it bypasses the `operation`) |
| + | Sets `operation` to `add` |
| - | Sets `operation` to `sub` |
| * | Sets `operation` to `mul` |
| / | Sets `operation` to `div` |

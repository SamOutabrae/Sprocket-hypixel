# sprocket-hypixel

A Sprocket module for viewing Hypixel stats.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following:

- A working installation of [Sprocket](https://github.com/SamOutabrae/Sprocket)
- A valid Hypixel API key
- The `requests` and `pandas` Python libraries installed

### Installation

1. **Clone the Repository**  
   Clone this repository into the `modules/` directory of your Sprocket installation.

2. **Set Up Your API Key**  
   Inside the `sprocket-hypixel` directory, duplicate the file `config.toml.default`, renaming it to `config.toml`.
   Change the `api_key` to your Hypixel API key.

3. **Update `modules.toml`**  
   Add the following section to your `modules.toml` file:

   ```toml
   [sprocket-hypixel]
   mainfile = "hypixel.py"
   ```


Your project structure should look something like this:

```
sprocket-root/
├── sprocket.py
├── modules.toml
├── token.txt
└── modules/
    └── sprocket-hypixel/
        ├── hypixel.py
        ├── config.toml
        └── (other sprocket-hypixel files)
```

### Running the Bot

To start the bot, simply run `sprocket.py` from the root directory. If everything is set up correctly, you should see:

```
Loaded cogs for sprocket-hypixel
```

in the terminal without any errors. You're ready to use the Hypixel module!

## Tracking

`sprocket-hypixel` supports stat tracking over time, allowing you to view your daily progress and compare performance between dates.

To enable tracking:

1. Schedule `gamemodes/tracking/updater.py` to run once per day using a task scheduler like `cron` (Linux) or Task Scheduler (Windows).
2. Open `config.toml` and set the `tracking` option to `true`.

Tracking is disabled by default, so make sure you configure both steps to begin collecting historical data.

## Commands

`sprocket-hypixel` provides several commands for viewing your Hypixel stats directly in Discord. Below is a breakdown of each command and what it does:

---

### `/map_username <username>`

Links your Minecraft username to your Discord account, allowing you to use other commands without typing your username every time.  
Once mapped, future commands will automatically use your saved username if none is provided.

---

### `/bw [username]`

Displays Bedwars stats for the specified username.  
If you've mapped your username with `/map_username`, you can omit the `username` parameter.

---

### `/today_bw [username]`
*Requires tracking*

Shows your Bedwars stats for any tracked player *so far today*.
If your username is mapped and you want to see your own stats, you don't need to supply it.

---

### `/yesterday_bw [username]`
*Requires tracking*

Displays Bedwars stats for any tracked player*from yesterday*. This also requires tracking to be enabled.  
Again, the `username` argument is optional if you've used `/map_username`.

---

### `/duels [username] [start_date] [end_date]`

Returns your UHC Duels stats. This command supports optional arguments:

- `username`: Minecraft username to look up (required if not mapped)
- `start_date`: If provided alone, shows stats from that day
- `start_date` + `end_date`: Shows your stat progression between those two dates

> Note: Date-based options only work if tracking is enabled.
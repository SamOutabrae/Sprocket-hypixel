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
   Inside the `sprocket-hypixel` directory, create a file named `hypixel_token.txt` and paste your Hypixel API key into it. The file should contain only the key, with no extra spaces or newlines.

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
        ├── hypixel_token.txt
        └── (other sprocket-hypixel files)
```

### Running the Bot

To start the bot, simply run `sprocket.py` from the root directory. If everything is set up correctly, you should see:

```
Loaded cogs for sprocket-hypixel
```

in the terminal without any errors. You're ready to use the Hypixel module!
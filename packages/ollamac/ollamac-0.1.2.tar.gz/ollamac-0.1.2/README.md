# ollama Command Line Interface

## Installation

### Windows
1. Install Ubuntu on WSL via  `wsl ---install`
2. Start Ubuntu
3. Install CUDA (https://docs.nvidia.com/cuda/wsl-user-guide/index.html)
4. Install Ollama (https://ollama.ai/download/linux)

## Start Ollama

After the installation start Ollama by `ollama serve`

If you get an error like
```
Error: listen tcp 127.0.0.1:11434: bind: address already in use
```

You can define the address to use for Ollama by setting the environment variable `OLLAMA_HOST`
```
export OLLAMA_HOST=localhost:8888
```

Run the LLM serving should give you the following output
```
wsl:~$ ollama serve
2023/10/25 19:38:15 images.go:822: total blobs: 0
2023/10/25 19:38:15 images.go:829: total unused blobs removed: 0
2023/10/25 19:38:15 routes.go:662: Listening on 127.0.0.1:8888 (version 0.1.5)
```

## Pull a model
This step is optional. On the first usage, the model will get pulled anyway.
Execute the following command to pull the llama2 model.
```
ollama pull llama2
```
Make sure you are using the same OLLAMA_HOST where your server is started.

On the server you should see output like:
```
[GIN] 2023/10/25 - 19:45:38 | 200 |        35.1µs |       127.0.0.1 | HEAD     "/"
[GIN] 2023/10/25 - 19:45:38 | 200 |     385.599µs |       127.0.0.1 | GET      "/api/tags"
2023/10/25 19:45:41 download.go:126: downloading 22f7f8ef5f4c in 64 59 MB part(s)
...
```

## Install ollamac
* Execute `pip install ollamac`

## Usage

```bash
usage: ollamac.py [-h] [--model MODEL] [--host HOST] [--port PORT] [--sync]
                  prompt

ollama command line utility.

positional arguments:
  prompt         Required prompt to be send to the ollama model.

options:
  -h, --help     show this help message and exit
  --model MODEL  The name of the ollama model to use. Default is "llama2".
  --host HOST    The hostname where ollama serve is running. Default is
                 "localhost".
  --port PORT    The port where ollama serve is running. Default is "8888".
  --sync         This switch executes the query synchronous.
```

## Examples

### Blogpost
```bash
(.venv) PS F:\git\playground> python -m ollamac "Write a blogpost about the new iphone 15 in 400 words."                  

Title: The New iPhone 15: A Game-Changer in Smartphone Technology

Apple has just released its latest and greatest iPhone, the iPhone 15, and it's a real showstopper. Packed with cutting-edge technology and design innovations, this phone is sure to revolutionize the way we use our smartphones. Here are some of the most exciting features of the new iPhone 15:

Super Retina XDR Display: The iPhone 15 boasts a stunning Super Retina XDR display, which offers an unparalleled viewing experience. With a 120Hz refresh rate and a peak brightness of 1000 nits, this display is perfect for watching videos, playing games, and browsing the web.

A15 Bionic Chip: The iPhone 15 is powered by Apple's latest A15 Bionic chip, which provides lightning-fast performance and efficiency. This chip offers a 20% boost in processing speed and a 40% improvement in energy efficiency compared to the previous generation.       

Triple-Lens Camera: The iPhone 15 features a triple-lens camera system, including a wide-angle lens, a telephoto lens, and a macro lens. This allows users to capture stunning photos and videos with unparalleled detail and depth. The camera also supports advanced features like night mode, portrait mode, and more.

Longer Battery Life: With up to 12 hours of internet use on a single charge, the iPhone 15 offers significantly longer battery life than its predecessors. This means users can enjoy their phone all day without needing to worry about running out of juice.

Wireless Charging: The iPhone 15 supports wireless charging, allowing users to simply place their phone on a charging pad to recharge. This feature is especially convenient for those who are always on the go and don't want to be tethered to a cord.

Enhanced Security: With advanced biometric authentication features like Face ID and Touch ID, the iPhone 15 offers an unparalleled level of security. Users can securely unlock their phone with just a glance or a fingerprint, keeping their personal information safe from prying eyes.

Overall, the new iPhone 15 is a game-changer in smartphone technology. With its stunning display, powerful processor, advanced camera system, longer battery life, wireless charging capabilities, and enhanced security features, this phone is sure to revolutionize the way we use our smartphones. Whether you're a tech enthusiast or just looking for an upgrade, the iPhone 15 is definitely worth checking out.
```